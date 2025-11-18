from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import time
from dotenv import load_dotenv
import requests

import pandas as pd
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
import redis

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from db_classes import *
from models.ModelRegistry import ModelRegistry

load_dotenv()

# SQL Alchemy Setup
engine = create_engine(os.environ.get("DATABASE_URL"), pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Redis Consumer Setup
REDIS_URL = os.environ.get("REDIS_URL").split(":") #TODO: Might need to switch to RabbitMQ for one-time consume & guaranteed delivery
REDIS_TOPIC = os.environ.get("REDIS_TOPIC")
r = redis.Redis(host=REDIS_URL[0], port=REDIS_URL[1])
consumer = r.pubsub()

# Notification Constants
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# Forecasting Models Constants
TREND_TO_MODEL_MAP = {
    'gentle_drift_noise': 'sarimax',
    'gradual_steady_increase': 'autoets',
    'profit_linked': 'nbeats',
    'proportional_to_sales': 'lstm',
    'rate_cycle_rise_ease': 'autoets',
    'sales_seasonal_cycle': 'nbeats',
    'seasonal_with_short_hump': 'sarimax',
    'static': 'static'
}
TREND_SET = set(TREND_TO_MODEL_MAP.keys())
MODEL_TO_WEIGHT_EXTENSION_TYPE_MAP = {
    'sarimax': 'pkl',
    'autoets': 'json',
    'lstm': 'pt',
    'nbeats': 'ckpt',
    'static': 'json'
}
TRAINING_DATA_MONTHS = 36
FORECAST_DATA_MONTHS = 3

# App Functionality
def runConsumer():
    try: 
        dbSession = SessionLocal() # Try to set up DB session
        consumer.subscribe(REDIS_TOPIC) # Try to subscribe
        while True:
            message = consumer.get_message(timeout=1.0) # Polls for new messages at interval of 1 second
            if message == None:
                continue
            if message['type'] == 'subscribe': # Indicates successful subscription
                print(f" * Subscribed to Redis topic successfully:", message['channel'].decode(), 
                        "\n * Listening for messages...")
                continue
            print(" * Received message:", message)
            if message['type'] == 'message':
                processMessage(message['data'].decode(),dbSession)
                print(f" * Message processed successfully, listening for more messages...")
            time.sleep(0.1) # Apparently avoids some error
    except KeyboardInterrupt:
        print(" * Service interrupted manually by user")
    finally:
        consumer.unsubscribe()
        dbSession.close()
        
# Business Logic (Generate forecasts)
def processMessage(message, dbSession):
    print(" * Processing message: " + message + "...")
    latest_date = getLatestPNLEntryDate(dbSession)

    # Model Training Phase
    training_data = retrieveTrainingData(dbSession, latest_date)
    for trend_name in TREND_SET:
        # if trend_name != "gentle_drift_noise": #TEST 
        #     continue #TEST
        train_status = trainForTrend(trend_name.lower(), training_data[trend_name])
        if train_status:
            pass # Send a redis message if needed

    # Forecasting Phase
    output_data = {
        "pnl_forecasts": [],
        "kpi_forecasts": [],
        "notifications": []
    }
    all_forecasts = {} # Format for KPI calculation function >> looks like {"BB1":[{"A001-0001":3},{},{}]}
    
    forecasted_months = [(latest_date+relativedelta(months=i)).strftime("%m-%Y") for i in range(1,4)]
    forecasting_data = retrieveForecastingData(dbSession, latest_date)
    print(" * Generating forecasts for months: ", ", ".join(forecasted_months))
    for trend_name in TREND_SET:
        # if trend_name != "gentle_drift_noise": #TEST
        #     continue #TEST
        model_forecasts = forecastForTrend(trend_name.lower(), forecasting_data[trend_name]) # outputs data like {"A001-0001::BB1":[val1,val2,val3],...}
        print(f" * Updating forecasts in DB for {trend_name}...")
        output_data["pnl_forecasts"].append(updateDBForecasts(dbSession, forecasted_months, model_forecasts))
        
        for cat_bu, fcs in model_forecasts.items():
            pnl_category, business_unit = cat_bu.split("::")
            if business_unit not in all_forecasts:
                all_forecasts[business_unit] = [{},{},{}]
            for i in range(len(fcs)):
                all_forecasts[business_unit][i][pnl_category] = fcs[i]

    # KPI Calculation Phase
    bu_kpis = {}
    print(" * Calculating and updating KPI forecasts in DB...")
    for bu, monthly_fcs in all_forecasts.items():
        monthly_fkpis = {}
        for i in range(len(monthly_fcs)):
            added_kpis = insertKPIForecastsPerBUAndMonth(dbSession, 
                    monthly_fcs[i], bu, forecasted_months[i]) # Insert once and get change log
            output_data["kpi_forecasts"].extend(added_kpis) # Add to output data
            monthly_fkpis[forecasted_months[i]] = { entry["kpi_alias"]:entry["value"] for entry in added_kpis } # Store KPI - value mappings for each BU for notifications
        bu_kpis[bu] = monthly_fkpis
    # bu_kpis structure: { "BB1": { "10-2025":{"PROF":val, "GPM":val,...}, "11-2025":{...}, "12-2025":{...} }, "BB2": {...} }

    # Notification Phase
    bu_employee_dict = retrieveBUsAndEmployees(dbSession)
    employee_param_dict = retrieveEmployeesAndParams(dbSession, forecasted_months)
    param_guide = retrieveParametersByCategory(dbSession)

    print(" * Creating notification alerts for employees...")
    for bu, employees in bu_employee_dict.items():
        monthly_kpis = bu_kpis[bu]
        for emp in employees:
            if emp["id"] not in employee_param_dict:
                continue
            parameters = employee_param_dict[emp["id"]]
            if parameters:
                flags = flagParameters(monthly_kpis, parameters, param_guide)
                output_data["notifications"].append(sendNotification(dbSession, emp, flags, forecasted_months))
                print(" * Forecast alert sent to employee:", emp["name"], "for BU:", bu)
    return output_data
        
# Notification Functions
def retrieveBUsAndEmployees(dbSession):
    employees = dbSession.scalars(select(Employee)
            .where(Employee.business_unit != None)).all()

    output_data = {}
    for emp in employees:
        if emp.business_unit not in output_data:
            output_data[emp.business_unit] = []
        output_data[emp.business_unit].append(emp.json())
    # output_data structure: { "BB1": [ <employee_data>, <employee_data>, ... ], "BBS2":[],... }
    return output_data

def retrieveEmployeesAndParams(dbSession, forecasted_months):
    parameters = dbSession.scalars(
            select(Parameter)
            .where(Parameter.month >= datetime.strptime(forecasted_months[0], "%m-%Y").date())
            .where(Parameter.month <= datetime.strptime(forecasted_months[-1], "%m-%Y").date())
            .order_by()
        ).all()

    output_data = {}
    for param in parameters:
        mth = param.month.strftime("%m-%Y")
        if param.employee_id not in output_data:
            output_data[param.employee_id] = {}
        if mth not in output_data[param.employee_id]:
            output_data[param.employee_id][mth] = {}
        output_data[param.employee_id][mth][param.kpi_alias] = param.value
    # output_data structure: { employee_id: {"10-2025":{ param_name: param_value, ... },{},{}], employee_id2: []}
    return output_data

def retrieveParametersByCategory(dbSession):
    kpi_categories = dbSession.scalars(select(KPICategory)).all()
    
    output_data = {}
    for cat in kpi_categories:
        output_data[cat.alias] = cat.category
    # output_data structure: { "GPM:"PROF", "RT":"SALES",...}
    return output_data

def flagParameters(monthly_kpis, parameters, param_guide):
    output_data = {}
    for mth, mth_kpis in monthly_kpis.items():
        output_data[mth] = {}
        if mth in parameters:
            mth_params = parameters[mth]
        for kpi_alias in mth_kpis.keys():
            value = mth_kpis[kpi_alias]
            target = mth_params[kpi_alias]
            if value is None or target is None:
                continue
            if param_guide[kpi_alias] in ["PROFIT", "SALES"]:
                if value < target:
                    output_data[mth][kpi_alias] = (value, target)
            elif param_guide[kpi_alias] in ["COST"]:
                if value > target:
                    output_data[mth][kpi_alias] = (value, target)

    # output_data structure: [{"GPM":(val,targ)},{"GPM":(val,targ)},{}]
    return output_data

def sendNotification(dbSession, employee, flags, forecasted_months):
    empty = True
    for mth_flags in flags.values():
        if mth_flags:
            empty = False
    if empty:
        return {} # No flags >> no notification

    subject, body = craftNotificationContent(employee,flags, forecasted_months)

    output_data = insertDBNotification(dbSession, employee, subject, body)
    if employee["phone_number"]:
        sendWhatsappNotification(employee["phone_number"], subject, body)
    if employee["email"]:
        sendEmailNotification(employee["email"], subject, body)
    
    return output_data

def craftNotificationContent(employee, flags, forecasted_months):
    subject = "[FORECAST ALERT] Business Unit: " + employee["business_unit"]
    body = []

    for i in range(len(forecasted_months)):
        mth = forecasted_months[i]
        message = mth + ":\nKPI\t| Forecasted Value\t| Target"
        kpis = flags[mth]
        if kpis:
            for kpi_alias, (value, target) in kpis.items():
                message += f"\n{kpi_alias}\t| {value}\t\t| {target}"
            body.append(message)
            
    body = "\n\n".join(body)

    return subject, body

def insertDBNotification(dbSession, employee, subject, body):
    notification = Notification(
        employee_id=employee["id"],
        type="FORECAST_ALERT",
        subject=subject,
        body=body,
        is_read=False
        )
    dbSession.add(notification)

    try:
        dbSession.commit()
        return notification.json()
    except Exception as e:
        print(f" * Error inserting notification into DB:", str(e))
        return {}

def sendWhatsappNotification(phone_number, subject, body):
    url = f"https://graph.facebook.com/v22.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,      # single number
        "type": "text",
        "text": {"body": f"{subject}\n\n{body}"}
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f" * WhatsApp message sent to {phone_number} successfully!")
        return response.json()
    except requests.exceptions.RequestException as e:
        return {f" * Error sending WhatsApp message to {phone_number}: {e}"}


def sendEmailNotification(email, subject, body):
    message = MIMEMultipart()
    message["From"] = f"Traffic-light Simulation Hub <{SENDER_EMAIL}>"
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls() # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD) # Log in to Gmail account
            server.send_message(message) # Send the email
        print(f" * Email sent to {email} successfully")
    except Exception as e:
        print(f" * Failed to send email to {email}: {e}")

# Utility Functions
def getLatestPNLEntryDate(dbSession):
    latest_entry = dbSession.scalars(select(PNLEntry)
        .order_by(PNLEntry.month.desc())
    ).first()
    latest_date = datetime.strptime(latest_entry.json()['month'], "%m-%Y").date() if latest_entry else datetime.now().date()
    return latest_date

# Training Functions
def retrieveTrainingData(dbSession, latest_date):
    stmt = (
        select(PNLEntry)
        .join(PNLCategory, PNLCategory.code == PNLEntry.pnl_code)
        .where(PNLEntry.month > latest_date - relativedelta(months=TRAINING_DATA_MONTHS))
        .order_by(PNLEntry.month)
    )
    entries = dbSession.scalars(stmt).all()

    months = []
    output_data = {}
    output_data.update({trend_name:{} for trend_name in TREND_SET})
    for entry in entries:
        trend_name = entry.pnl_category.trend.lower()
        key = entry.pnl_code + "::" + entry.business_unit
        mth = entry.month.strftime("%m-%Y")
        if mth not in months:
            months.append(mth)
        if key not in output_data[trend_name]:
            output_data[trend_name][key] = []
        output_data[trend_name][key].append(float(entry.value) if entry.value is not None else None)
    
    for trend in output_data:
        output_data[trend]["months"] = months
    
    return output_data

def trainForTrend(trend_name,training_data):
    model_name = TREND_TO_MODEL_MAP[trend_name]
    print(f" * Training model {model_name} for {trend_name}...")
    try: 
        # INSTANTIATE UNFITTED MODEL OBJECT
        train_model = ModelRegistry.create(model_name)

        # TRAIN MODEL
        train_model.train(data=training_data, input_size=24,
                        output_size=3, epochs=50)

        # SAVE WEIGHTS
        weight_extension_type = MODEL_TO_WEIGHT_EXTENSION_TYPE_MAP[model_name]
        train_model.save(f"weights/{trend_name}/weight.{weight_extension_type}")
        print(" * Model trained successfully!")
        return True
    except Exception as e:
        print(f" * Error training model:", str(e))
        return False
    
# Forecasting Functions
def retrieveForecastingData(dbSession, latest_date):
    stmt = (
        select(PNLEntry)
        .join(PNLCategory, PNLCategory.code == PNLEntry.pnl_code)
        .where(PNLEntry.month > latest_date - relativedelta(months=FORECAST_DATA_MONTHS))
        .order_by(PNLEntry.month)
    )
    entries = dbSession.scalars(stmt).all()

    months = []
    output_data = {}
    output_data.update({trend_name:{} for trend_name in TREND_SET})
    for entry in entries:
        trend_name = entry.pnl_category.trend.lower()
        key = entry.pnl_code + "::" + entry.business_unit
        mth = entry.month.strftime("%m-%Y")
        if mth not in months:
            months.append(mth)
        if key not in output_data[trend_name]:
            output_data[trend_name][key] = []
        output_data[trend_name][key].append(float(entry.value) if entry.value is not None else None)
    
    for trend in output_data:
        output_data[trend]["months"] = months

    return output_data
    
def forecastForTrend(trend_name, forecasting_data):
    model_name = TREND_TO_MODEL_MAP[trend_name]
    print(f" * Forecasting with model {model_name} for {trend_name}...")
    try:
        # LOAD WEIGHTS
        weight_extension_type = MODEL_TO_WEIGHT_EXTENSION_TYPE_MAP[model_name]
        pred_model = ModelRegistry.load_model(
            model_name, f'weights/{trend_name}/weight.{weight_extension_type}')
        
        # GENERATE FORECASTS PER CATEGORY::BUSINESS_UNIT
        output_data = {}
        for cat_bu in forecasting_data:
            if cat_bu == "months":
                continue

            context_data = forecasting_data[cat_bu]

            output_data[cat_bu] = pred_model.predict(
                series_name=cat_bu,
                steps=3,
                last_values=context_data
            )
        print(" * Forecasts generated successfully!")
        return output_data
    except Exception as e:
        print(f" * Error forecasting with {model_name}:", str(e))
        return {}

def updateDBForecasts(dbSession, forecasted_months, forecasts):

    # GET EXISTING FORECASTS
    existing_forecasts = dbSession.scalars(select(PNLForecast)).all()
    existing_forecasts = {(efc.pnl_code, efc.business_unit, efc.month.strftime("%m-%Y")):efc for efc in existing_forecasts}
    
    output_data = []
    for cat_bu, fcs in forecasts.items():
        pnl_category, business_unit = cat_bu.split("::")

        for i in range(len(forecasted_months)):
            key = (pnl_category, business_unit, forecasted_months[i])
            change_status = "unchanged"

            # UPDATE EXISTING FORECAST
            if key in existing_forecasts.keys():
                fc_entry = existing_forecasts[key]
                fc_entry.value = float(fcs[i])
                change_status = "updated"

            # INSERT NEW FORECAST
            else:
                fc_entry = PNLForecast(
                    pnl_code=pnl_category,
                    business_unit=business_unit,
                    month=datetime.strptime(forecasted_months[i], "%m-%Y").date(),
                    value=float(fcs[i])
                )
                dbSession.add(fc_entry)
                change_status = "created"

            output_fc = fc_entry.json()
            output_fc.update({"change_status": change_status})
            output_data.append(output_fc)

    try:
        dbSession.commit()
        print(" * Forecasts updated successfully")
        return output_data
    except Exception as e:
        dbSession.rollback()
        print(f" * Error updating forecasts:", str(e))
        return []

# KPI Functions
def insertKPIForecastsPerBUAndMonth(dbSession, entry_dict, bu, month_str): # TODO: Accept dictionary instead of df
    output_data = []
    month = datetime.strptime(month_str, "%m-%Y").date()

    kpi_dict = { # calculate KPIs and consolidate
        **calculateProfitKPIs(entry_dict),
        **calculateSalesKPIs(entry_dict),
        **calculateCostKPIs(entry_dict)
    }

    for kpi_alias, kpi_value in kpi_dict.items():
        change_status = "unchanged"

        # print(f"Checking database if KPI Entry exists: {kpi_alias} - {bu} - {month_str}")
        kpi_entry = dbSession.scalars(
            select(KPIForecast)
            .filter_by(kpi_alias=kpi_alias, business_unit=bu, month=month)
        ).first()

        if kpi_entry:
            # print(f"\tExisting KPI Entry found: {kpi_entry.kpi_alias} - {kpi_entry.business_unit} - {kpi_entry.month}")
            if isFloatEqualSafe(kpi_entry.value, kpi_value, dp=4):
                # print(f"\t\tValue matches, no action required.")
                pass
            else:
                # print(f"\t\tValue mismatch, updating value: {kpi_entry.value} -> {kpi_value}")
                kpi_entry.value = kpi_value
                change_status = "updated"

        else:
            # print(f"\tNo existing KPI Entry found, proceeding to create: {kpi_alias} - {bu} - {month_str} - {kpi_value}")
            kpi_entry = KPIForecast(
                kpi_alias=kpi_alias,
                business_unit=bu,
                month=month,
                value=kpi_value
            )
            dbSession.add(kpi_entry)
            change_status = "created"

        output_entry = kpi_entry.json()
        output_entry.update({"change_status": change_status})
        output_data.append(output_entry)
    try:
        dbSession.commit()
        print(f" * KPI forecasts for {bu}: {month_str} calculated & updated successfully")
        return output_data
    except Exception as e:
        dbSession.rollback()
        print(f" * Error updating KPI forecasts:", str(e))
        return []

def isFloatEqualSafe(a,b,dp):
    if a is None and b is None:
        return True
    if a is not None and b is not None:
        return f"{a:.{dp}f}" == f"{b:.{dp}f}"
    return False

def calculateProfitKPIs(entries):
    output_data = {
        "PROF": None,
        "GPM": None,
        "OPM": None,
        "NPM": None,
        "QR": None
    }
    
    # summing data
    sales_revenue = 0
    sales_adjustments = 0
    other_incomes = 0
    cogs = 0
    op_expenses = 0
    fin_expenses = 0
    for code, val in entries.items():
        if pd.isna(val): # skip if value is pd.NA (does not trigger ValueError because NaN is a special float value) or None
            continue
        try:
            val = float(str(val).strip())
        except ValueError:
            continue  # skip if value cannot be converted to float (non-numeric)

        if code.startswith("5000-") and code not in ["5000-A015", "5000-M004"]:
            sales_revenue += val
        if code.startswith("5500"):
            sales_adjustments += val
        if code.startswith("8") or code in ["5000-A015", "5000-M004"]:
            other_incomes += val
        if code.startswith("6"):
            cogs += val
        if code.startswith("901") or code.startswith("902"):
            op_expenses += val
        if code.startswith("900"):
            fin_expenses += val

    # intermediate calculations
    net_sales = sales_revenue - sales_adjustments
    all_expenses = op_expenses + fin_expenses
    all_incomes = sales_revenue + other_incomes - sales_adjustments

    # KPI calculations
    output_data["PROF"] = round(all_incomes - cogs - all_expenses, 2)
    output_data["GPM"] = round((sales_revenue - cogs) / sales_revenue * 100, 4) if sales_revenue != 0 else None
    output_data["OPM"] = round((net_sales - cogs - op_expenses) / net_sales * 100, 4) if net_sales != 0 else None
    output_data["NPM"] = round((all_incomes - cogs - all_expenses) / all_incomes * 100, 4) if all_incomes != 0 else None
    output_data["QR"] = None

    return output_data

def calculateSalesKPIs(entries):
    output_data = {
        "SALES": None, 
        "ROS": None,
        "DSO": None,
        "RT": None
    }

    # summing data
    sales_revenue = 0
    sales_adjustments = 0
    cogs = 0
    op_expenses = 0
    for code, val in entries.items():
        if pd.isna(val): # skip if value is pd.NA (does not trigger ValueError because NaN is a special float value) or None
            continue
        try:
            val = float(str(val).strip())
        except ValueError:
            continue  # skip if value cannot be converted to float (non-numeric)

        if code.startswith("5000-") and code not in ["5000-A015", "5000-M004"]:
            sales_revenue += val
        if code.startswith("5500"):
            sales_adjustments += val
        if code.startswith("6"):
            cogs += val
        if code.startswith("901") or code.startswith("902"):
            op_expenses += val

    # intermediate calculations
    net_sales = sales_revenue - sales_adjustments
    operating_profit = sales_revenue - sales_adjustments - cogs - op_expenses

    # KPI calculations
    output_data["SALES"] = round(net_sales, 2)
    output_data["ROS"] = round(operating_profit / net_sales * 100, 4) if net_sales != 0 else None
    output_data["DSO"] = None
    output_data["RT"] = None

    return output_data

def calculateCostKPIs(entries):
    output_data = {
        "COST": None, 
        "COGSR": None,
        "DPO": None,
        "OHR": None
    }

    # summing data
    sales_revenue = 0
    sales_adjustments = 0
    cogs = 0
    all_expenses = 0
    overhead_costs = 0
    for code, val in entries.items():
        if pd.isna(val): # skip if value is pd.NA (does not trigger ValueError because NaN is a special float value) or None
            continue
        try:
            val = float(str(val).strip())
        except ValueError:
            continue  # skip if value cannot be converted to float (non-numeric)

        if code.startswith("5000-") and code not in ["5000-A015", "5000-M004"]:
            sales_revenue += val
        if code.startswith("5500"):
            sales_adjustments += val
        if code.startswith("6"):
            cogs += val
        if code.startswith("9"):
            all_expenses += val
        if code.startswith("902") or code.startswith("9000-D"):
            overhead_costs += val

    # intermediate calculations
    net_sales = sales_revenue - sales_adjustments

    # KPI calculations
    output_data["COST"] = round(cogs + all_expenses, 2)
    output_data["COGSR"] = round(cogs / net_sales * 100, 4) if net_sales != 0 else None
    output_data["DPO"] = None
    output_data["OHR"] = round(overhead_costs / net_sales * 100, 4) if net_sales != 0 else None

    return output_data

if __name__ == '__main__':
    print(" * Forecast service running:" + os.path.basename(__file__) + "...")
    runConsumer()
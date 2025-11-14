from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import time
from dotenv import load_dotenv
import json

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
import redis

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
MODEL_SET = set(TREND_TO_MODEL_MAP.values())
MODEL_TO_WEIGHT_EXTENSION_TYPE_MAP = {
    'sarimax': 'pkl',
    'autoets': 'json',
    'lstm': 'pt',
    'nbeats': 'ckpt'
}

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
    for model_name in MODEL_SET:
        train_status = trainModel(model_name.lower(), training_data[model_name])
        if train_status:
            pass # Send a redis message if needed

    # Forecasting Phase
    forecasting_data = retrieveForecastingData(dbSession, latest_date)
    output_data = {
        "forecasts": [],
        "kpis": [],
        "notifications": []
    }

    all_forecasts = {} # TODO: Format for KPI calculation function
    for model_name in MODEL_SET:
        model_forecasts = forecastModel(model_name.lower(), forecasting_data[model_name])
        print(f" * Updating forecasts in DB for {model_name}...")
        output_data["forecasts"].append(updateDBForecasts(dbSession, forecasting_data["months"], model_forecasts))
    #     all_forecasts[]=

    # bu_kpis = {}
    # forecast_months = [latest_date+relativedelta(months=i) for i in range(1,4)]
    # for bu in bu_list:
    #     for month in forecast_months:
    #         added_kpis = insertKPIEntriesPerBU(df, bu, month) # Insert once and get change log
    #         output_data["kpi_entries"].extend(added_kpis) # Add to output data
    #         bu_kpis[bu] = { entry["kpi_alias"]:entry["value"] for entry in added_kpis } # Store KPI - value mappings for each BU for notifications
    # pass


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
        .where(PNLEntry.month > latest_date - relativedelta(months=12))
        .order_by(PNLEntry.month)
    )
    entries = dbSession.scalars(stmt).all()

    output_data = {"months": []}
    output_data.update({model:{} for model in MODEL_SET})
    for entry in entries:
        model = TREND_TO_MODEL_MAP[entry.pnl_category.trend.lower()]
        key = entry.pnl_code + "::" + entry.business_unit
        month = entry.month.strftime("%m-%Y")
        if month not in output_data["months"]:
            output_data["months"].append(month)
        if key not in output_data[model]:
            output_data[model][key] = []
        output_data[model][key].append(float(entry.value) if entry.value is not None else None)
    return output_data

def trainModel(model_name,training_data):
    print(" * Training model: " + model_name + "...")
    try: 
        # INSTANTIATE UNFITTED MODEL OBJECT
        train_model = ModelRegistry.create(model_name)

        # TRAIN MODEL
        train_model.train(data=training_data, input_size=12,
                        output_size=3, epochs=50)

        # SAVE WEIGHTS
        weight_extension_type = MODEL_TO_WEIGHT_EXTENSION_TYPE_MAP[model_name]
        train_model.save(f'weight.{weight_extension_type}')
        print(" * Model trained successfully!")
        return True
    except Exception as e:
        print(f" * Error training {model_name}:", str(e))
        return False
    
# Forecasting Functions
def retrieveForecastingData(dbSession, latest_date):
    stmt = (
        select(PNLEntry)
        .join(PNLCategory, PNLCategory.code == PNLEntry.pnl_code)
        .where(PNLEntry.month > latest_date - relativedelta(months=12))
        .order_by(PNLEntry.month)
    )
    entries = dbSession.scalars(stmt).all()

    output_data = {"months": []}
    output_data.update({model:{} for model in MODEL_SET})
    for entry in entries:
        model = TREND_TO_MODEL_MAP[entry.pnl_category.trend.lower()]
        key = entry.pnl_code + "::" + entry.business_unit
        month = entry.month.strftime("%m-%Y")
        if month not in output_data["months"]:
            output_data["months"].append(month)
        if key not in output_data[model]:
            output_data[model][key] = []
        output_data[model][key].append(float(entry.value) if entry.value is not None else None)
    return output_data
    
def forecastModel(model_name, forecasting_data):
    print(" * Forecasting with model: " + model_name + "...")
    try:
        # LOAD WEIGHTS
        weight_extension_type = MODEL_TO_WEIGHT_EXTENSION_TYPE_MAP[model_name]
        pred_model = ModelRegistry.load_model(
            model_name, f'weight.{weight_extension_type}')
        
        # GENERATE FORECASTS PER CATEGORY::BUSINESS_UNIT
        output_data = {"months": forecasting_data["months"]}
        for cat_bu in forecasting_data:
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

def updateDBForecasts(dbSession, months, forecasts):
    # GET EXISTING FORECASTS
    existing_forecasts = dbSession.scalars(select(PNLForecast)).all()
    existing_forecasts = {(efc.pnl_code, efc.business_unit, efc.month.strftime("%m-%Y")):efc for efc in existing_forecasts}
    
    output_data = []
    for cat_bu, fcs in forecasts.items():
        pnl_category, business_unit = cat_bu.split("::")

        for i in range(len(months)):
            key = (pnl_category, business_unit, months[i])
            change_status = "unchanged"

            # UPDATE EXISTING FORECAST
            if key in existing_forecasts.keys():
                fc_entry = existing_forecasts[key]
                fc_entry.value = fcs[i]
                change_status = "updated"

            # INSERT NEW FORECAST
            else:
                fc_entry = PNLForecast(
                    pnl_code=pnl_category,
                    business_unit=business_unit,
                    month=datetime.strptime(months[i], "%m-%Y").date(),
                    value=fcs[i]
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

# # KPI Functions
# def insertKPIForecastsPerBU(dbSession, df, bu, month_str): # TODO: Accept dictionary instead of df
#     output_data = []
#     month = datetime.strptime(month_str, "%m-%Y").date()
#     entry_dict = df.set_index("Code")[bu].to_dict() # convert to Code-Value dict for PNL entries

#     kpi_dict = { # calculate KPIs and consolidate
#         **calculateProfitKPIs(entry_dict),
#         **calculateSalesKPIs(entry_dict),
#         **calculateCostKPIs(entry_dict)
#     }

#     for kpi_alias, kpi_value in kpi_dict.items():
#         change_status = "unchanged"

#         print(f"Checking database if KPI Entry exists: {kpi_alias} - {bu} - {month_str}")
#         kpi_entry = dbSession.scalars(
#             select(KPIForecast)
#             .filter_by(kpi_alias=kpi_alias, business_unit=bu, month=month)
#         ).first()

#         if kpi_entry:
#             print(f"\tExisting KPI Entry found: {kpi_entry.kpi_alias} - {kpi_entry.business_unit} - {kpi_entry.month}")
#             if isFloatEqualSafe(kpi_entry.value, kpi_value, dp=4):
#                 print(f"\t\tValue matches, no action required.")
#             else:
#                 print(f"\t\tValue mismatch, updating value: {kpi_entry.value} -> {kpi_value}")
#                 kpi_entry.value = kpi_value
#                 change_status = "updated"
#         else:
#             print(f"\tNo existing KPI Entry found, proceeding to create: {kpi_alias} - {bu} - {month_str} - {kpi_value}")
#             kpi_entry = KPIForecast(
#                 kpi_alias=kpi_alias,
#                 business_unit=bu,
#                 month=month,
#                 value=kpi_value
#             )
#             dbSession.add(kpi_entry)
#             change_status = "created"

#         output_entry = kpi_entry.json()
#         output_entry.update({"change_status": change_status})
#         output_data.append(output_entry)

#     return output_data

# def isFloatEqualSafe(a,b,dp):
#     if a is None and b is None:
#         return True
#     if a is not None and b is not None:
#         return f"{a:.{dp}f}" == f"{b:.{dp}f}"
#     return False

# def calculateProfitKPIs(entries):
#     output_data = {
#         "PROF": None,
#         "GPM": None,
#         "OPM": None,
#         "NPM": None,
#         "QR": None
#     }
    
#     # summing data
#     sales_revenue = 0
#     sales_adjustments = 0
#     other_incomes = 0
#     cogs = 0
#     op_expenses = 0
#     fin_expenses = 0
#     for code, val in entries.items():
#         if pd.isna(val): # skip if value is pd.NA (does not trigger ValueError because NaN is a special float value) or None
#             continue
#         try:
#             val = float(str(val).strip())
#         except ValueError:
#             continue  # skip if value cannot be converted to float (non-numeric)

#         if code.startswith("5000-") and code not in ["5000-A015", "5000-M004"]:
#             sales_revenue += val
#         if code.startswith("5500"):
#             sales_adjustments += val
#         if code.startswith("8") or code in ["5000-A015", "5000-M004"]:
#             other_incomes += val
#         if code.startswith("6"):
#             cogs += val
#         if code.startswith("901") or code.startswith("902"):
#             op_expenses += val
#         if code.startswith("900"):
#             fin_expenses += val

#     # intermediate calculations
#     net_sales = sales_revenue - sales_adjustments
#     all_expenses = op_expenses + fin_expenses
#     all_incomes = sales_revenue + other_incomes - sales_adjustments

#     # KPI calculations
#     output_data["PROF"] = round(all_incomes - cogs - all_expenses, 2)
#     output_data["GPM"] = round((sales_revenue - cogs) / sales_revenue * 100, 4) if sales_revenue != 0 else None
#     output_data["OPM"] = round((net_sales - cogs - op_expenses) / net_sales * 100, 4) if net_sales != 0 else None
#     output_data["NPM"] = round((all_incomes - cogs - all_expenses) / all_incomes * 100, 4) if all_incomes != 0 else None
#     output_data["QR"] = None

#     return output_data

# def calculateSalesKPIs(entries):
#     output_data = {
#         "SALES": None, 
#         "ROS": None,
#         "DSO": None,
#         "RT": None
#     }

#     # summing data
#     sales_revenue = 0
#     sales_adjustments = 0
#     cogs = 0
#     op_expenses = 0
#     for code, val in entries.items():
#         if pd.isna(val): # skip if value is pd.NA (does not trigger ValueError because NaN is a special float value) or None
#             continue
#         try:
#             val = float(str(val).strip())
#         except ValueError:
#             continue  # skip if value cannot be converted to float (non-numeric)

#         if code.startswith("5000-") and code not in ["5000-A015", "5000-M004"]:
#             sales_revenue += val
#         if code.startswith("5500"):
#             sales_adjustments += val
#         if code.startswith("6"):
#             cogs += val
#         if code.startswith("901") or code.startswith("902"):
#             op_expenses += val

#     # intermediate calculations
#     net_sales = sales_revenue - sales_adjustments
#     operating_profit = sales_revenue - sales_adjustments - cogs - op_expenses

#     # KPI calculations
#     output_data["SALES"] = round(net_sales, 2)
#     output_data["ROS"] = round(operating_profit / net_sales * 100, 4) if net_sales != 0 else None
#     output_data["DSO"] = None
#     output_data["RT"] = None

#     return output_data

# def calculateCostKPIs(entries):
#     output_data = {
#         "COST": None, 
#         "COGSR": None,
#         "DPO": None,
#         "OHR": None
#     }

#     # summing data
#     sales_revenue = 0
#     sales_adjustments = 0
#     cogs = 0
#     all_expenses = 0
#     overhead_costs = 0
#     for code, val in entries.items():
#         if pd.isna(val): # skip if value is pd.NA (does not trigger ValueError because NaN is a special float value) or None
#             continue
#         try:
#             val = float(str(val).strip())
#         except ValueError:
#             continue  # skip if value cannot be converted to float (non-numeric)

#         if code.startswith("5000-") and code not in ["5000-A015", "5000-M004"]:
#             sales_revenue += val
#         if code.startswith("5500"):
#             sales_adjustments += val
#         if code.startswith("6"):
#             cogs += val
#         if code.startswith("9"):
#             all_expenses += val
#         if code.startswith("902") or code.startswith("9000-D"):
#             overhead_costs += val

#     # intermediate calculations
#     net_sales = sales_revenue - sales_adjustments

#     # KPI calculations
#     output_data["COST"] = round(cogs + all_expenses, 2)
#     output_data["COGSR"] = round(cogs / net_sales * 100, 4) if net_sales != 0 else None
#     output_data["DPO"] = None
#     output_data["OHR"] = round(overhead_costs / net_sales * 100, 4) if net_sales != 0 else None

#     return output_data

if __name__ == '__main__':
    print("Forecast service running:" + os.path.basename(__file__) + "...")
    runConsumer()
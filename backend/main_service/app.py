from datetime import datetime
import json
import re
from dateutil.relativedelta import relativedelta
from zoneinfo import ZoneInfo
import os
from dotenv import load_dotenv

from flask import Flask, jsonify, request
import pandas as pd
from sqlalchemy import or_, and_, func, select
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import redis

from db_classes import *

pd.set_option('display.max_columns', None)
load_dotenv() # only for local development with .env file >> loads variables into system environment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(
    app,
    resources={r"/*": {
            "origins": ["http://localhost:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "allow_headers": ["Content-Type"]
        }},
    supports_credentials=True
)

# Redis Producer
REDIS_URL = os.environ.get("REDIS_URL").split(":")
producer = redis.Redis(host=REDIS_URL[0], port=REDIS_URL[1])
REDIS_TOPIC = os.environ.get("REDIS_TOPIC")

# Constants
timezone = ZoneInfo(os.environ.get("TIMEZONE"))

######################## EMPLOYEE ########################
@app.route("/employee/all/", methods=['GET'])
def getAllEmployees():
    employees = db.session.scalars(db.select(Employee)).all()
    if employees:
        return jsonify(
            {
                "code": 200,
                "data": [item.json() for item in employees]
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No employees found :("
        }
    ), 404

@app.route("/employee/id/<employee_id>/", methods=['GET'])
def getEmployeeById(employee_id):
    employee = db.session.scalars(db.select(Employee).filter_by(id=employee_id)).first()
    if employee:
        return jsonify(
            {
                "code": 200,
                "data": employee.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Employee not found :("
        }
    ), 404

@app.route("/employee/email/<email>/", methods=['GET'])
def getEmployeeByEmail(email):
    employee = db.session.scalars(db.select(Employee).filter_by(email=email)).first()
    if employee:
        return jsonify(
            {
                "code": 200,
                "data": employee.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Employee not found :("
        }
    ), 404

@app.route("/employee/authenticate/", methods=['POST'])
def authenticateEmployee():
    data = request.get_json()

    if not data or not all(
        key in data for key in ['email', 'password']
    ):
        return jsonify(
            {
                "code": 400,
                "message": "Invalid/missing input data :("
            }
        ), 400
    
    employee = db.session.scalars(db.select(Employee).filter_by(email=data['email'])).first()

    if not employee:
        return jsonify(
            {
                "code": 404,
                "message": "Authentication failed - Employee not found :("
            }
        ), 404

    if employee.authenticate(data['password']):
        return jsonify(
            {
                "code": 200,
                "data": employee.json()
            }
        ), 200
    return jsonify(
        {
            "code": 401,
            "message": "Authentication failed - Invalid password :("
        }
    ), 401

######################## PARAMETER ########################
@app.route("/parameter/all/<employee_id>/", methods=['GET'])
def getParametersByEmployeeId(employee_id):
    parameters = db.session.scalars(db.select(Parameter)
        .filter_by(employee_id=employee_id)
        .order_by(Parameter.month)
        ).all()

    output_data = {'keys': [], 'parameters': {}} # convert to appropriate output format
    for param in parameters:
        param = param.json()
        if param['month'] not in output_data['keys']:
            output_data['keys'].append(param['month'])
            output_data['parameters'][param['month']] = {}
        output_data['parameters'][param['month']][param['kpi_alias']] = param['value']

    if output_data:
        return jsonify(
            {
                "code": 200,
                "data": output_data
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No parameters found :("
        }
    ), 404

@app.route("/parameter/latest/<employee_id>/", methods=['GET'])
def getLatestParametersByEmployeeId(employee_id):
    parameters = db.session.scalars(db.select(Parameter)
        .filter_by(employee_id=employee_id)
        .order_by(Parameter.month.desc())
        ).all()

    output_data = {} # convert to appropriate output format
    latest_date = None
    for param in parameters:
        param = param.json()
        if latest_date is None: # use first date as latest date
            latest_date = param['month']
        if param['month'] != latest_date: # stop when date changes
            break
        output_data[param['kpi_alias']] = param['value']

    if output_data:
        return jsonify(
            {
                "code": 200,
                "data": output_data
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No parameters found :("
        }
    ), 404

@app.route("/parameter/15mths/<employee_id>/", methods=['GET'])
def get15MonthsParametersByEmployeeId(employee_id):
    latest_date = getLatestPNLEntryDate(employee_id)

    parameters = db.session.scalars(db.select(Parameter)
        .filter_by(employee_id=employee_id)
        .filter(
            and_(
                Parameter.month > latest_date - relativedelta(months=12),
                Parameter.month <= latest_date + relativedelta(months=3)
            )
        )
        .order_by(Parameter.month)
    ).all()

    output_data = {'keys': [], 'parameters': {}}
    for param in parameters:
        param = param.json()
        print(param)
        if param['month'] not in output_data['keys']:
            output_data['keys'].append(param['month'])
            output_data['parameters'][param['month']] = {}
        output_data['parameters'][param['month']][param['kpi_alias']] = param['value']

    if output_data:
        return jsonify(
            {
                "code": 200,
                "data": output_data
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No parameters found :("
        }
    ), 404

@app.route("/parameter/batch/", methods=['POST'])
def setNewParameters():
    data = request.get_json()
    output_data = []
    input_month = datetime.strptime(data.get('month'), '%m-%Y').date()

    if not data or not all(
        key in data for key in ['employee_id', 'month', 'parameters']
    ):
        return jsonify(
            {
                "code": 400,
                "message": "Invalid/missing input data :("
            }
        ), 400
    
    for param, val in data['parameters'].items():
        # Retrieve parameter: If exists, update. If not, create new.
        parameter = db.session.scalars(
            db.select(Parameter)
            .filter_by(employee_id=data['employee_id'])
            .filter_by(kpi_alias=param)
            .filter_by(month=input_month)
        ).first()

        if parameter:
            print(f"Existing parameter found, proceeding to update \"{param}: {val}\"...")
            parameter.value = val
            output_param = parameter.json()
            output_param.update({"change_status":"updated"})
            output_data.append(output_param)
        else:
            print(f"No existing parameter found, proceeding to create \"{param}: {val}\"...")
            parameter = Parameter(
                employee_id=data['employee_id'],
                kpi_alias=param,
                month=input_month,
                value=val
            )
            db.session.add(parameter)
            output_param = parameter.json()
            output_param.update({"change_status":"created"})
            output_data.append(output_param)
        
    try:
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": output_data,
                "message": "Parameters set successfully :)"
            }
        ), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "code": 500,
                "message": f"An error occurred while setting parameters: {str(e)}"
            }
        ), 500

######################## PNL ENTRY ########################
@app.route("/category/all/")
def getAllPNLCategories():
    categories = db.session.scalars(db.select(PNLCategory)).all()
    if categories:
        return jsonify(
            {
                "code": 200,
                "data": {
                    item.json()["code"]:{
                        "name": item.json()["name"], 
                        "description": item.json()["description"],
                        "parent_code": item.json()["parent_code"],
                        "trend": item.json()["trend"]
                    } for item in categories
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No PNL categories found :("
        }
    ), 404

@app.route("/entry/individual/<pnl_code>/<bu_alias>/")
def getPNLEntriesByCodeAndBU(pnl_code, bu_alias):
    entries = db.session.scalars(db.select(PNLEntry)
        .filter_by(pnl_code=pnl_code)
        .filter_by(business_unit=bu_alias.upper())    
    ).all()

    if entries:
        return jsonify(
            {
                "code": 200,
                "data": [item.json() for item in entries]
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "data": [],
            "message": "No PNL entries found :("
        }
    ), 404

@app.route("/entry/sales/<bu_alias>/")
def getLast12MonthsSalesPNLEntriesByBU(bu_alias):
    latest_date = getLatestPNLEntryDate(bu_alias)
    print(f"Fetching based on latest month: {latest_date.strftime('%m-%Y')}")

    entries = db.session.scalars(db.select(PNLEntry)
        .filter_by(business_unit=bu_alias.upper())
        .filter(or_(
            PNLEntry.pnl_code.like('5%'),
            PNLEntry.pnl_code.like('8%')
        ))
        .filter(PNLEntry.month > latest_date - relativedelta(months=12))
        .order_by(PNLEntry.month)
    ).all()

    output_data = {'keys': [], 'entries': {}} # convert to appropriate output format
    for entry in entries:
        entry = entry.json()
        if entry['month'] not in output_data['keys']:
            output_data['keys'].append(entry['month'])
            output_data['entries'][entry['month']] = {}
        output_data['entries'][entry['month']][entry['pnl_code']] = entry['value']

    if entries:
        return jsonify(
            {
                "code": 200,
                "data": output_data
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No PNL entries found :("
        }
    ), 404

@app.route("/entry/cost/<bu_alias>/")
def getLast12MonthsCostPNLEntriesByBU(bu_alias):
    latest_date = getLatestPNLEntryDate(bu_alias)
    print(f"Fetching based on latest month: {latest_date.strftime('%m-%Y')}")

    entries = db.session.scalars(db.select(PNLEntry)
        .filter_by(business_unit=bu_alias.upper())
        .filter(or_(
            PNLEntry.pnl_code.like('6%'),
            PNLEntry.pnl_code.like('9%')
        ))
        .filter(PNLEntry.month > latest_date - relativedelta(months=12))
        .order_by(PNLEntry.month)
    ).all()

    output_data = {'keys': [], 'entries': {}} # convert to appropriate output format
    for entry in entries:
        entry = entry.json()
        if entry['month'] not in output_data['keys']:
            output_data['keys'].append(entry['month'])
            output_data['entries'][entry['month']] = {}
        output_data['entries'][entry['month']][entry['pnl_code']] = entry['value']

    if entries:
        return jsonify(
            {
                "code": 200,
                "data": output_data
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No PNL entries found :("
        }
    ), 404

######################## PNL FORECAST ########################
@app.route("/forecast/individual/<pnl_code>/<bu_alias>/")
def getPNLForecastsByCodeAndBU(pnl_code, bu_alias):
    forecasts = db.session.scalars(db.select(PNLForecast)
        .filter_by(pnl_code=pnl_code)
        .filter_by(business_unit=bu_alias.upper())
    ).all()

    if forecasts:
        return jsonify(
            {
                "code": 200,
                "data": [item.json() for item in forecasts]
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "data": [],
            "message": "No PNL forecasts found :("
        }
    ), 404

@app.route("/forecast/sales/<bu_alias>/")
def getNext3MonthsSalesPNLForecastsByBU(bu_alias):
    latest_date = getLatestPNLEntryDate(bu_alias)
    print(f"Fetching based on latest month: {latest_date.strftime('%m-%Y')}")

    forecasts = db.session.scalars(db.select(PNLForecast)
        .filter_by(business_unit=bu_alias.upper())
        .filter(or_(
            PNLForecast.pnl_code.like('5%'),
            PNLForecast.pnl_code.like('8%')
        ))
        .filter(
            and_(
                PNLForecast.month > latest_date,
                PNLForecast.month <= latest_date + relativedelta(months=3)
            )
        )
        .order_by(PNLForecast.month)
    ).all()

    output_data = {'keys': [], 'forecasts': {}} # convert to appropriate output format
    for fc in forecasts:
        fc = fc.json()
        if fc['month'] not in output_data['keys']:
            output_data['keys'].append(fc['month'])
            output_data['forecasts'][fc['month']] = {}
        output_data['forecasts'][fc['month']][fc['pnl_code']] = fc['value']

    if forecasts:
        return jsonify(
            {
                "code": 200,
                "data": output_data
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No PNL entries found :("
        }
    ), 404

@app.route("/forecast/cost/<bu_alias>/")
def getNext3MonthsCostPNLForecastsByBU(bu_alias):
    latest_date = getLatestPNLEntryDate(bu_alias)
    print(f"Fetching based on latest month: {latest_date.strftime('%m-%Y')}")

    forecasts = db.session.scalars(db.select(PNLForecast)
        .filter_by(business_unit=bu_alias.upper())
        .filter(or_(
            PNLForecast.pnl_code.like('6%'),
            PNLForecast.pnl_code.like('9%')
        ))
        .filter(
            and_(
                PNLForecast.month > latest_date,
                PNLForecast.month <= latest_date + relativedelta(months=3)
            )
        )
        .order_by(PNLForecast.month)
    ).all()

    output_data = {'keys': [], 'forecasts': {}} # convert to appropriate output format
    for entry in forecasts:
        entry = entry.json()
        if entry['month'] not in output_data['keys']:
            output_data['keys'].append(entry['month'])
            output_data['forecasts'][entry['month']] = {}
        output_data['forecasts'][entry['month']][entry['pnl_code']] = entry['value']

    if forecasts:
        return jsonify(
            {
                "code": 200,
                "data": output_data
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No PNL entries found :("
        }
    ), 404

######################## KPI ########################
@app.route("/kpi/category/")
def getAllKPICategories():
    kpi_categories = db.session.scalars(db.select(KPICategory)).all()
    if kpi_categories:
        return jsonify(
            {
                "code": 200,
                "data": {
                    item.json()["alias"]:{
                        "name": item.json()["name"], 
                        "description": item.json()["description"],
                        "category": item.json()["category"]
                    } for item in kpi_categories
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No KPI categories found :("
        }
    ), 404

@app.route("/kpi/profit/<bu_alias>/")
def getLast12MonthsProfitKPIsByBU(bu_alias):
    latest_date = getLatestPNLEntryDate(bu_alias)
    print(f"Fetching based on latest month: {latest_date.strftime('%m-%Y')}")

    entries = db.session.scalars(db.select(KPIEntry)
        .filter_by(business_unit=bu_alias.upper())
        .join(KPICategory, KPIEntry.kpi_alias == KPICategory.alias)
        .where(KPICategory.category == "PROFIT")
        .filter(KPIEntry.month > latest_date - relativedelta(months=12))
        .filter(KPIEntry.month <= latest_date)
        .order_by(KPIEntry.month)
    ).all()

    output_data = {'keys': [], 'kpis': {}} # convert to appropriate output format
    for entry in entries:
        entry = entry.json()
        if entry['month'] not in output_data['keys']:
            output_data['keys'].append(entry['month'])
            output_data['kpis'][entry['month']] = {}
        output_data['kpis'][entry['month']][entry['kpi_alias']] = entry['value']

    if entries:
        return jsonify(
            {
                "code": 200,
                "data": output_data
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No KPI entries found :("
        }
    ), 404

@app.route("/kpi/sales/<bu_alias>/")
def getLast12MonthsSalesKPIsByBU(bu_alias):
    latest_date = getLatestPNLEntryDate(bu_alias)
    print(f"Fetching based on latest month: {latest_date.strftime('%m-%Y')}")

    entries = db.session.scalars(db.select(KPIEntry)
        .filter_by(business_unit=bu_alias.upper())
        .join(KPICategory, KPIEntry.kpi_alias == KPICategory.alias)
        .where(KPICategory.category == "SALES")
        .filter(KPIEntry.month > latest_date - relativedelta(months=12))
        .filter(KPIEntry.month <= latest_date)
        .order_by(KPIEntry.month)
    ).all()

    output_data = {'keys': [], 'kpis': {}} # convert to appropriate output format
    for entry in entries:
        entry = entry.json()
        if entry['month'] not in output_data['keys']:
            output_data['keys'].append(entry['month'])
            output_data['kpis'][entry['month']] = {}
        output_data['kpis'][entry['month']][entry['kpi_alias']] = entry['value']

    if entries:
        return jsonify(
            {
                "code": 200,
                "data": output_data
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No KPI entries found :("
        }
    ), 404

@app.route("/kpi/cost/<bu_alias>/")
def getLast12MonthsCostKPIsByBU(bu_alias):
    latest_date = getLatestPNLEntryDate(bu_alias)
    print(f"Fetching based on latest month: {latest_date.strftime('%m-%Y')}")

    entries = db.session.scalars(db.select(KPIEntry)
        .filter_by(business_unit=bu_alias.upper())
        .join(KPICategory, KPIEntry.kpi_alias == KPICategory.alias)
        .where(KPICategory.category == "COST")
        .filter(
            and_(
                KPIEntry.month > latest_date - relativedelta(months=12),
                KPIEntry.month <= latest_date
            )
        )
        .order_by(KPIEntry.month)
    ).all()

    output_data = {'keys': [], 'kpis': {}} # convert to appropriate output format
    for entry in entries:
        entry = entry.json()
        if entry['month'] not in output_data['keys']:
            output_data['keys'].append(entry['month'])
            output_data['kpis'][entry['month']] = {}
        output_data['kpis'][entry['month']][entry['kpi_alias']] = entry['value']

    if entries:
        return jsonify(
            {
                "code": 200,
                "data": output_data
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No KPI entries found :("
        }
    ), 404

@app.route("/kpi/f_profit/<bu_alias>/")
def getForecasted3MonthsProfitKPIsByBU(bu_alias):
    latest_date = getLatestPNLEntryDate(bu_alias)
    print(f"Fetching based on latest month: {latest_date.strftime('%m-%Y')}")

    entries = db.session.scalars(db.select(KPIForecast)
        .filter_by(business_unit=bu_alias.upper())
        .join(KPICategory, KPIForecast.kpi_alias == KPICategory.alias)
        .where(KPICategory.category == "PROFIT")
        .filter(
            and_(
                KPIForecast.month > latest_date,
                KPIForecast.month <= latest_date + relativedelta(months=3)
            )
        )
        .order_by(KPIForecast.month)
    ).all()

    output_data = {'keys': [], 'kpis': {}} # convert to appropriate output format
    for entry in entries:
        entry = entry.json()
        if entry['month'] not in output_data['keys']:
            output_data['keys'].append(entry['month'])
            output_data['kpis'][entry['month']] = {}
        output_data['kpis'][entry['month']][entry['kpi_alias']] = entry['value']

    if entries:
        return jsonify(
            {
                "code": 200,
                "data": output_data
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No KPI forecasts found :("
        }
    ), 404

@app.route("/kpi/f_sales/<bu_alias>/")
def getForecasted3MonthsSalesKPIsByBU(bu_alias):
    latest_date = getLatestPNLEntryDate(bu_alias)
    print(f"Fetching based on latest month: {latest_date.strftime('%m-%Y')}")

    entries = db.session.scalars(db.select(KPIForecast)
        .filter_by(business_unit=bu_alias.upper())
        .join(KPICategory, KPIForecast.kpi_alias == KPICategory.alias)
        .where(KPICategory.category == "SALES")
        .filter(
            and_(
                KPIForecast.month > latest_date,
                KPIForecast.month <= latest_date + relativedelta(months=3)
            )
        )
        .order_by(KPIForecast.month)
    ).all()

    output_data = {'keys': [], 'kpis': {}} # convert to appropriate output format
    for entry in entries:
        entry = entry.json()
        if entry['month'] not in output_data['keys']:
            output_data['keys'].append(entry['month'])
            output_data['kpis'][entry['month']] = {}
        output_data['kpis'][entry['month']][entry['kpi_alias']] = entry['value']

    if entries:
        return jsonify(
            {
                "code": 200,
                "data": output_data
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No KPI forecasts found :("
        }
    ), 404

@app.route("/kpi/f_cost/<bu_alias>/")
def getForecasted3MonthsCostKPIsByBU(bu_alias):
    latest_date = getLatestPNLEntryDate(bu_alias)
    print(f"Fetching based on latest month: {latest_date.strftime('%m-%Y')}")

    entries = db.session.scalars(db.select(KPIForecast)
        .filter_by(business_unit=bu_alias.upper())
        .join(KPICategory, KPIForecast.kpi_alias == KPICategory.alias)
        .where(KPICategory.category == "COST")
        .filter(
            and_(
                KPIForecast.month > latest_date,
                KPIForecast.month <= latest_date + relativedelta(months=3)
            )
        )
        .order_by(KPIForecast.month)
    ).all()

    output_data = {'keys': [], 'kpis': {}} # convert to appropriate output format
    for entry in entries:
        entry = entry.json()
        if entry['month'] not in output_data['keys']:
            output_data['keys'].append(entry['month'])
            output_data['kpis'][entry['month']] = {}
        output_data['kpis'][entry['month']][entry['kpi_alias']] = entry['value']

    if entries:
        return jsonify(
            {
                "code": 200,
                "data": output_data
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "No KPI forecasts found :("
        }
    ), 404

######################## LOAD DATA ########################
@app.route("/load_data/<month>/", methods=['POST'])
def loadData(month):
    input_file = request.files.get('pnl_report')

    df = reportToDataFrame(input_file)
    output_data = {
        "business_units": [],
        "pnl_categories": [],
        "pnl_entries": [],
        "kpi_entries": [],
        "parameters": []
    }

    # Populate 3 months ahead Parameters in DB
    output_data["parameters"] = insertNext3MonthsDefaultParameters(month)

    # Insert BUs from header into DB
    output_data["business_units"] = insertBusinessUnits(list(df.columns)[2:])

    # Insert PNL Categories and Entries into DB
    indent_standard = len(df["Code"].iloc[0]) - len(df["Code"].iloc[0].lstrip(' '))
    prev_codes = [None]
    prev_names = [""]
    for i, row in df.iterrows():
        # Determining parent-child relationship of categories using indentation
        tier = round( (len(row["Code"]) - len(row["Code"].lstrip(' '))) / indent_standard )
        if tier >= len(prev_codes):
            prev_codes.append(row["Code"].strip())
            prev_names.append(row["Name"].strip())
        else:
            prev_codes[tier] = row["Code"].strip()
            prev_codes = prev_codes[:tier+1]
            prev_names[tier] = row["Name"].strip()
            prev_names = prev_names[:tier+1]
        parent = prev_codes[tier-1]
        description = (">".join(prev_names[1:tier]) + ">") if len(prev_names)>1 else None

        row["Code"] = row["Code"].strip()
        output_data["pnl_categories"].append(insertPNLCatPerRow(row, parent, description))
        output_data["pnl_entries"].extend(insertPNLEntriesPerRow(row, month))

    # Calculate and insert KPIs into DB
    df["Code"] = df["Code"].str.strip() # Strip all whitespaces for Code column
    bu_kpis = {}
    for bu in list(df.columns)[2:]:
        added_kpis = insertKPIEntriesPerBU(df, bu, month) # Insert once and get change log
        output_data["kpi_entries"].extend(added_kpis) # Add to output data
        bu_kpis[bu] = { entry["kpi_alias"]:entry["value"] for entry in added_kpis } # Store KPI - value mappings for each BU for notifications

    try:
        db.session.commit()
        # db.session.rollback() # For testing
        
        # Trigger Forecast Service
        triggerForecastService()

        return jsonify(
            {
                "code": 200,
                "data": output_data,
                "message": "Data has been loaded successfully. :) Triggering Machine Learning retraining and forecast generation..."
            }
        ), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "code": 500,
                "message": f"An error occurred while setting parameters: {str(e)}"
            }
        ), 500
    
# Helper Methods
def reportToDataFrame(file):
    if not file:
        raise ValueError("No file provided")

    # Handle both Excel (.xls,.xlsx,.xlsm) and .csv files
    ext = os.path.splitext(file.filename)[1].lower()

    if ext == ".csv":
        df = pd.read_csv(file, header=None, dtype=str)
    elif ext in [".xls", ".xlsx", ".xlsm"]:
        df = pd.read_excel(file, sheet_name=0, header=None, dtype=str)
    else:
        raise ValueError("Unsupported file format: " + ext)

    # Clean dataframe
    df.replace(r"^\s*$", pd.NA, regex=True, inplace=True) # replaces empty strings with NaN
    df = df.dropna(how="all", axis=0) # drop all NaN rows
    df = df.dropna(how="all", axis=1) # drop all NaN columns

    # Business Units
    bu_df = df[(df.iloc[:, 0].isna()) & (df.iloc[:, 1].isna())].iloc[0] # retrieve BU header row
    bu_df[[0,1]] = ["Code","Name"] # adjust BU row to use as header
    bu_df[findSumColumn(bu_df)] = "TOTAL"
    df.columns = bu_df # use BU row as header

    # Further clean dataframe for PNLCategory and PNLEntry
    df = df.loc[:, df.columns.notna()] # drop NaN header columns
    df = df.dropna(subset=["Code", "Name"]) # drop rows without Code or Name filled

    return df

def findSumColumn(series):
    possible_values = ["ytd","yeartodate","total","totals"]
    for i, value in series.items():
        if type(value) is not str:
            continue
        value = re.sub(r"[^A-Za-z]+", "", value).lower()
        if value in possible_values:
            return i
    return None

def insertNext3MonthsDefaultParameters(month_str):
    output_data = []
    current_month = datetime.strptime(month_str, "%m-%Y").date()
    
    # Get latest values for each parameter for each employee
    subquery = select(
        Parameter.employee_id,
        Parameter.kpi_alias,
        func.max(Parameter.month).label('max_month')
    ).group_by(Parameter.employee_id, Parameter.kpi_alias).subquery()
    stmt = select(Parameter).join(
        subquery,
        (Parameter.employee_id == subquery.c.employee_id) &
        (Parameter.kpi_alias == subquery.c.kpi_alias) &
        (Parameter.month == subquery.c.max_month)
    )
    latest_params = db.session.scalars(stmt).all()
    latest_params = { (param.employee_id, param.kpi_alias): param.value for param in latest_params }

    # Get existing parameters for next 3 months (to avoid modification/error from creating row that exists)
    existing_params = db.session.scalars(db.select(Parameter)
        .filter(
            and_(
                Parameter.month > current_month,
                Parameter.month <= current_month + relativedelta(months=3)
            )
        )
        .order_by(Parameter.month)
    ).all()
    existing_params = [ (param.employee_id, param.kpi_alias, param.month.strftime("%m-%Y")) for param in existing_params ]
    print(existing_params)

    # Parameters have to be updated for every KPI and every manager Employee
    employee_ids = db.session.scalars(db.select(Employee.id).where(Employee.role.in_(["BU Manager", "Senior Manager"]))).all()
    kpi_aliases = db.session.scalars(db.select(KPICategory.alias)).all()

    for eid in employee_ids:
        for kpi in kpi_aliases:
            mth = current_month + relativedelta(months=1)
            while mth <= current_month + relativedelta(months=3):
                if (eid, kpi, mth.strftime("%m-%Y")) in existing_params:
                    print(f"Parameter already exists, skipping: {eid} - {kpi} - {mth.strftime('%m-%Y')}")
                    mth += relativedelta(months=1)
                    continue
                val = latest_params.get((eid, kpi), 0) # default to 0 if no previous value
                print(f"Inserting parameter: {eid} - {kpi} - {mth.strftime('%m-%Y')} - {val}")
                param = Parameter(
                    employee_id = eid,
                    kpi_alias = kpi,
                    month = mth,
                    value = latest_params.get((eid, kpi), 0) # set to latest value or 0 if non-existent
                )
                db.session.add(param)

                out_param = param.json()
                out_param.update({"change_status":"created"})
                output_data.append(out_param)

                mth += relativedelta(months=1)

    return output_data

def insertBusinessUnits(series):
    output_bus = []
    for val in series:
        val = val.strip().upper()
        change_status = "unchanged"
        
        # Retrieve business unit
        print(f"Checking database if BU exists: {val}")
        bu = db.session.scalars(
            db.select(BusinessUnit)
            .filter_by(alias=val)
        ).first()

        if bu:
            print(f"\tExisting BU found, no action required: {bu.alias} - {bu.name}")
        else:
            print(f"\tNo existing BU found, proceeding to create: {val} - {val}")
            bu = BusinessUnit(
                alias=val,
                name=val
            )
            db.session.add(bu)
            change_status = "created"
        out_bu = bu.json()
        out_bu.update({"change_status": change_status})
        output_bus.append(out_bu)
    return output_bus

def insertPNLCatPerRow(series, parent_code = None, description = None):
    code = series["Code"].strip()
    name = series["Name"].strip().upper()
    change_status = "unchanged"

    print(f"Checking database if PNL Category exists: {code}")
    pnl_cat = db.session.scalars(
        db.select(PNLCategory)
        .filter_by(code=code)
    ).first()

    if pnl_cat:
        print(f"\tExisting PNL Category found: {pnl_cat.code} - {pnl_cat.name}")
        if pnl_cat.name == name:
            print(f"\t\tName matches, no action required.")
        else:
            print(f"\t\tName mismatch, updating name: -> {name}")
            pnl_cat.name = name
            change_status = "updated"
        if pnl_cat.parent_code == parent_code and pnl_cat.description == description:
            print(f"\t\tParent code and description matches, no action required.")
        else:
            print(f"\t\tParent code or description mismatch, updating: -> ({parent_code}, {description})")
            pnl_cat.parent_code = parent_code
            pnl_cat.description = description
            change_status = "updated"
    else:
        print(f"\tNo existing PNL Category found, proceeding to create: {code} - {name}")
        pnl_cat = PNLCategory(
            code=code,
            name=name,
            description = None,
            parent_code = parent_code
        )
        db.session.add(pnl_cat)
        change_status = "created"

    output_cat = pnl_cat.json()
    output_cat.update({"change_status": change_status})
    return output_cat

def isFloatEqualSafe(a,b,dp):
    if a is None and b is None:
        return True
    if a is not None and b is not None:
        return f"{a:.{dp}f}" == f"{b:.{dp}f}"
    return False

def insertPNLEntriesPerRow(series, month_str):
    code = series["Code"].strip()
    month = datetime.strptime(month_str, "%m-%Y").date()
    output_entries = []

    for bu, val in series.iloc[2:].items(): # skip Code and Name
        bu = bu.strip().upper()
        if pd.isna(val): # skip if value is pd.NA (does not trigger ValueError because NaN is a special float value) or None
            continue
        try:
            val = float(str(val).strip())
        except ValueError:
            continue  # skip if value cannot be converted to float (non-numeric)
        change_status = "unchanged"

        print(f"Checking database if PNL Entry exists: {code} - {bu} - {month}")
        pnl_entry = db.session.scalars(
            db.select(PNLEntry)
            .filter_by(pnl_code=code, business_unit=bu, month=month)
        ).first()

        if pnl_entry:
            print(f"\tExisting PNL Entry found: {pnl_entry.pnl_code} - {pnl_entry.business_unit} - {pnl_entry.month}")
            if isFloatEqualSafe(pnl_entry.value, val, dp=2):
                print(f"\t\tValue matches, no action required.")
            else:
                print(f"\t\tValue mismatch, updating value: {pnl_entry.value} -> {val}")
                pnl_entry.value = val
                change_status = "updated"
        else:
            print(f"\tNo existing PNL Entry found, proceeding to create: {code} - {bu} - {month} - {val}")
            pnl_entry = PNLEntry(
                pnl_code=code,
                business_unit=bu,
                month=month,
                value=val
            )
            db.session.add(pnl_entry)
            change_status = "created"

        output_entry = pnl_entry.json()
        output_entry.update({"change_status": change_status})
        output_entries.append(output_entry)

    return output_entries

def insertKPIEntriesPerBU(df, bu, month_str):
    output_data = []
    month = datetime.strptime(month_str, "%m-%Y").date()
    entry_dict = df.set_index("Code")[bu].to_dict() # convert to Code-Value dict for PNL entries

    kpi_dict = { # calculate KPIs and consolidate
        **calculateProfitKPIs(entry_dict),
        **calculateSalesKPIs(entry_dict),
        **calculateCostKPIs(entry_dict)
    }

    for kpi_alias, kpi_value in kpi_dict.items():
        change_status = "unchanged"

        print(f"Checking database if KPI Entry exists: {kpi_alias} - {bu} - {month_str}")
        kpi_entry = db.session.scalars(
            db.select(KPIEntry)
            .filter_by(kpi_alias=kpi_alias, business_unit=bu, month=month)
        ).first()

        if kpi_entry:
            print(f"\tExisting KPI Entry found: {kpi_entry.kpi_alias} - {kpi_entry.business_unit} - {kpi_entry.month}")
            if isFloatEqualSafe(kpi_entry.value, kpi_value, dp=4):
                print(f"\t\tValue matches, no action required.")
            else:
                print(f"\t\tValue mismatch, updating value: {kpi_entry.value} -> {kpi_value}")
                kpi_entry.value = kpi_value
                change_status = "updated"
        else:
            print(f"\tNo existing KPI Entry found, proceeding to create: {kpi_alias} - {bu} - {month_str} - {kpi_value}")
            kpi_entry = KPIEntry(
                kpi_alias=kpi_alias,
                business_unit=bu,
                month=month,
                value=kpi_value
            )
            db.session.add(kpi_entry)
            change_status = "created"

        output_entry = kpi_entry.json()
        output_entry.update({"change_status": change_status})
        output_data.append(output_entry)

    return output_data

def calculateProfitKPIs(entries):
    output_data = {
        "PROF": None, #TODO: Very arbitrary, currently just takes all the income minus all the costs
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
        "SALES": None, #TODO: Very arbitrary, currently just sums all income except "Other Incomes"
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
        "COST": None, #TODO: Very arbitrary, currently just sums all cogs and expenses
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

@app.route("/test/trigger/", methods=['POST'])
def triggerForecastService(): #TODO test
    message = json.dumps("initiate") # replace "initiate" with data in future if needed
    producer.publish(REDIS_TOPIC, message)
    return jsonify({"status": "success", "message": "Forecast service triggered"}), 200


######################### Notifications ##########################
# 1) Get all notifications for an employee
@app.route("/notifications/<employee_id>", methods=['GET'])
def get_notifications_by_employee(employee_id):
    notifications = db.session.scalars(
        db.select(Notification).where(Notification.employee_id == employee_id)
    ).all()

    if notifications:
        return jsonify({
            "code": 200,
            "data": [n.json() for n in notifications]
        }), 200

    return jsonify({
        "code": 404,
        "message": f"No notifications found for employee_id {employee_id}"
    }), 404


# 2) Mark a notification as read
@app.route("/notifications/<int:notification_id>/read", methods=['PATCH'])
def mark_notification_read(notification_id):
    notification = db.session.get(Notification, notification_id)

    if not notification:
        return jsonify({
            "code": 404,
            "message": f"Notification {notification_id} not found"
        }), 404

    notification.is_read = True
    db.session.commit()

    return jsonify({
        "code": 200,
        "data": notification.json(),
        "message": "Notification marked as read"
    }), 200


# (Optional) Mark all notifications for an employee as read
@app.route("/notifications/<employee_id>/read_all", methods=['PATCH'])
def mark_all_notifications_read(employee_id):
    notifications = db.session.scalars(
        db.select(Notification).where(Notification.employee_id == employee_id,
                                      Notification.is_read == False)
    ).all()

    if not notifications:
        return jsonify({
            "code": 404,
            "message": f"No unread notifications for employee_id {employee_id}"
        }), 404

    for n in notifications:
        n.is_read = True

    db.session.commit()

    return jsonify({
        "code": 200,
        "message": f"Marked {len(notifications)} notifications as read"
    }), 200


# 3) Delete a notification
@app.route("/notifications/<int:notification_id>", methods=['DELETE'])
def delete_notification(notification_id):
    notification = db.session.get(Notification, notification_id)

    if not notification:
        return jsonify({
            "code": 404,
            "message": f"Notification {notification_id} not found"
        }), 404

    db.session.delete(notification)
    db.session.commit()

    return jsonify({
        "code": 200,
        "message": f"Notification {notification_id} deleted"
    }), 200

######################## Helper Functions ########################
# General
def getLatestPNLEntryDate(bu_alias):
    latest_entry = db.session.scalars(db.select(PNLEntry)
        .filter_by(business_unit=bu_alias.upper())
        .order_by(PNLEntry.month.desc())
    ).first()
    latest_date = datetime.strptime(latest_entry.json()['month'], "%m-%Y").date() if latest_entry else datetime.now().date()
    return latest_date

# No Longer Used
def getLast12MonthsPNLEntries(bu_alias):
    latest_date = getLatestPNLEntryDate(bu_alias)
    print(f"Fetching based on latest month: {latest_date.strftime('%m-%Y')}")

    entries = db.session.scalars(db.select(PNLEntry)
        .filter_by(business_unit=bu_alias.upper())
        .filter(PNLEntry.month > latest_date - relativedelta(months=12))
        .order_by(PNLEntry.month)
    ).all()

    lookup_dict = {'keys': [], 'entries': {}} # convert to appropriate output format
    for entry in entries:
        entry = entry.json()
        if entry['month'] not in lookup_dict['keys']:
            lookup_dict['keys'].append(entry['month'])
            lookup_dict['entries'][entry['month']] = {}
        lookup_dict['entries'][entry['month']][entry['pnl_code']] = entry['value']

    return lookup_dict

def getNext3MonthsPNLForecasts(bu_alias):
    latest_date = getLatestPNLEntryDate(bu_alias)
    print(f"Fetching based on latest month: {latest_date.strftime('%m-%Y')}")

    entries = db.session.scalars(db.select(PNLForecast)
        .filter_by(business_unit=bu_alias.upper())
        .filter(
            and_(
                PNLForecast.month > latest_date,
                PNLForecast.month <= latest_date + relativedelta(months=3)
            )
        )
        .order_by(PNLForecast.month)
    ).all()

    lookup_dict = {'keys': [], 'entries': {}} # convert to appropriate output format
    for entry in entries:
        entry = entry.json()
        if entry['month'] not in lookup_dict['keys']:
            lookup_dict['keys'].append(entry['month'])
            lookup_dict['entries'][entry['month']] = {}
        lookup_dict['entries'][entry['month']][entry['pnl_code']] = entry['value']

    return lookup_dict

if __name__ == '__main__':
    print("Monolithic flask application running:" + os.path.basename(__file__) + "...")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
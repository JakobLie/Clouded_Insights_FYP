from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from zoneinfo import ZoneInfo
import os
from dotenv import load_dotenv

from flask import Flask, jsonify, request
from sqlalchemy import or_, and_
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import db_classes

load_dotenv() # only for local development with .env file >> loads variables into system environment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

# Constants
timezone = ZoneInfo(os.environ.get("TIMEZONE"))

######################## EMPLOYEE ########################
@app.route("/employee/all/", methods=['GET'])
def getAllEmployees():
    employees = db.session.scalars(db.select(db_classes.Employee)).all()
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
    employee = db.session.scalars(db.select(db_classes.Employee).filter_by(id=employee_id)).first()
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
    employee = db.session.scalars(db.select(db_classes.Employee).filter_by(email=email)).first()
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
    
    employee = db.session.scalars(db.select(db_classes.Employee).filter_by(email=data['email'])).first()

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
    parameters = db.session.scalars(db.select(db_classes.Parameter)
        .filter_by(employee_id=employee_id)
        .order_by(db_classes.Parameter.created_date)
        ).all()

    output_data = {'keys': [], 'parameters': {}} # convert to appropriate output format
    for param in parameters:
        param = param.json()
        if param['created_date'] not in output_data['keys']:
            output_data['keys'].append(param['created_date'])
            output_data['parameters'][param['created_date']] = {}
        output_data['parameters'][param['created_date']][param['name']] = param['value']

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
    parameters = db.session.scalars(db.select(db_classes.Parameter)
        .filter_by(employee_id=employee_id)
        .order_by(db_classes.Parameter.created_date.desc())
        ).all()

    output_data = {} # convert to appropriate output format
    latest_date = None
    for param in parameters:
        param = param.json()
        if latest_date is None: # use first date as latest date
            latest_date = param['created_date']
        if param['created_date'] != latest_date: # stop when date changes
            break
        output_data[param['name']] = param['value']

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
    current_date = datetime.now(timezone).date()

    if not data or not all(
        key in data for key in ['employee_id', 'parameters']
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
            db.select(db_classes.Parameter)
            .filter_by(employee_id=data['employee_id'])
            .filter_by(name=param)
            .filter_by(created_date=current_date)
        ).first()

        if parameter:
            print(f"Existing parameter found, proceeding to update \"{param}: {val}\"...")
            parameter.value = val
            output_param = parameter.json()
            output_param.update({"change_status":"updated"})
            output_data.append(output_param)
        else:
            print(f"No existing parameter found, proceeding to create \"{param}: {val}\"...")
            parameter = db_classes.Parameter(
                employee_id=data['employee_id'],
                name=param,
                created_date=current_date,
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
    categories = db.session.scalars(db.select(db_classes.PNLCategory)).all()
    if categories:
        return jsonify(
            {
                "code": 200,
                "data": {
                    item.json()["code"]:{
                        "name": item.json()["name"], 
                        "description": item.json()["description"]
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
    entries = db.session.scalars(db.select(db_classes.PNLEntry)
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

    entries = db.session.scalars(db.select(db_classes.PNLEntry)
        .filter_by(business_unit=bu_alias.upper())
        .filter(or_(
            db_classes.PNLEntry.pnl_code.like('5%'),
            db_classes.PNLEntry.pnl_code.like('8%')
        ))
        .filter(db_classes.PNLEntry.month > latest_date - relativedelta(months=12))
        .order_by(db_classes.PNLEntry.month)
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

    entries = db.session.scalars(db.select(db_classes.PNLEntry)
        .filter_by(business_unit=bu_alias.upper())
        .filter(or_(
            db_classes.PNLEntry.pnl_code.like('6%'),
            db_classes.PNLEntry.pnl_code.like('9%')
        ))
        .filter(db_classes.PNLEntry.month > latest_date - relativedelta(months=12))
        .order_by(db_classes.PNLEntry.month)
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
    forecasts = db.session.scalars(db.select(db_classes.PNLForecast)
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

    forecasts = db.session.scalars(db.select(db_classes.PNLForecast)
        .filter_by(business_unit=bu_alias.upper())
        .filter(or_(
            db_classes.PNLForecast.pnl_code.like('5%'),
            db_classes.PNLForecast.pnl_code.like('8%')
        ))
        .filter(
            and_(
                db_classes.PNLForecast.month > latest_date,
                db_classes.PNLForecast.month <= latest_date + relativedelta(months=3)
            )
        )
        .order_by(db_classes.PNLForecast.month)
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

    forecasts = db.session.scalars(db.select(db_classes.PNLForecast)
        .filter_by(business_unit=bu_alias.upper())
        .filter(or_(
            db_classes.PNLForecast.pnl_code.like('6%'),
            db_classes.PNLForecast.pnl_code.like('9%')
        ))
        .filter(
            and_(
                db_classes.PNLForecast.month > latest_date,
                db_classes.PNLForecast.month <= latest_date + relativedelta(months=3)
            )
        )
        .order_by(db_classes.PNLForecast.month)
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
@app.route("/kpi/profit/<bu_alias>/")
def getLast12MonthsProfitKPIsByBU(bu_alias):
    lookup_dict = getLast12MonthsPNLEntries(bu_alias)

    output_data = {'keys': [], 'kpis': {}}
    for month in lookup_dict['keys']:
        month_entries = lookup_dict['entries'].get(month, {})
        month_kpis = calculateProfitKPIs(month_entries)
        output_data['keys'].append(month)
        output_data['kpis'][month] = month_kpis

    return jsonify(
        {
            "code": 200,
            "data": output_data
        }
    ), 200

@app.route("/kpi/sales/<bu_alias>/")
def getLast12MonthsSalesKPIsByBU(bu_alias):
    lookup_dict = getLast12MonthsPNLEntries(bu_alias)

    output_data = {'keys': [], 'kpis': {}}
    for month in lookup_dict['keys']:
        month_entries = lookup_dict['entries'].get(month, {})
        month_kpis = calculateSalesKPIs(month_entries)
        output_data['keys'].append(month)
        output_data['kpis'][month] = month_kpis

    return jsonify(
        {
            "code": 200,
            "data": output_data
        }
    ), 200

@app.route("/kpi/cost/<bu_alias>/")
def getLast12MonthsCostKPIsByBU(bu_alias):
    lookup_dict = getLast12MonthsPNLEntries(bu_alias)

    output_data = {'keys': [], 'kpis': {}}
    for month in lookup_dict['keys']:
        month_entries = lookup_dict['entries'].get(month, {})
        month_kpis = calculateCostKPIs(month_entries)
        output_data['keys'].append(month)
        output_data['kpis'][month] = month_kpis

    return jsonify(
        {
            "code": 200,
            "data": output_data
        }
    ), 200\

@app.route("/kpi/f_profit/<bu_alias>/")
def getForecasted3MonthsProfitKPIsByBU(bu_alias):
    lookup_dict = getNext3MonthsPNLForecasts(bu_alias)

    output_data = {'keys': [], 'kpis': {}}
    for month in lookup_dict['keys']:
        month_entries = lookup_dict['entries'].get(month, {})
        month_kpis = calculateProfitKPIs(month_entries)
        output_data['keys'].append(month)
        output_data['kpis'][month] = month_kpis

    return jsonify(
        {
            "code": 200,
            "data": output_data
        }
    ), 200

@app.route("/kpi/f_sales/<bu_alias>/")
def getForecasted3MonthsSalesKPIsByBU(bu_alias):
    lookup_dict = getNext3MonthsPNLForecasts(bu_alias)

    output_data = {'keys': [], 'kpis': {}}
    for month in lookup_dict['keys']:
        month_entries = lookup_dict['entries'].get(month, {})
        month_kpis = calculateSalesKPIs(month_entries)
        output_data['keys'].append(month)
        output_data['kpis'][month] = month_kpis

    return jsonify(
        {
            "code": 200,
            "data": output_data
        }
    ), 200

@app.route("/kpi/f_cost/<bu_alias>/")
def getForecasted3MonthsCostKPIsByBU(bu_alias):
    lookup_dict = getNext3MonthsPNLForecasts(bu_alias)

    output_data = {'keys': [], 'kpis': {}}
    for month in lookup_dict['keys']:
        month_entries = lookup_dict['entries'].get(month, {})
        month_kpis = calculateCostKPIs(month_entries)
        output_data['keys'].append(month)
        output_data['kpis'][month] = month_kpis

    return jsonify(
        {
            "code": 200,
            "data": output_data
        }
    ), 200

######################## Helper Functions ########################
# General
def getLatestPNLEntryDate(bu_alias):
    latest_entry = db.session.scalars(db.select(db_classes.PNLEntry)
        .filter_by(business_unit=bu_alias.upper())
        .order_by(db_classes.PNLEntry.month.desc())
    ).first()
    latest_date = datetime.strptime(latest_entry.json()['month'], "%m-%Y").date() if latest_entry else datetime.now().date()
    return latest_date

# KPI Calculation
def getLast12MonthsPNLEntries(bu_alias):
    latest_date = getLatestPNLEntryDate(bu_alias)
    print(f"Fetching based on latest month: {latest_date.strftime('%m-%Y')}")

    entries = db.session.scalars(db.select(db_classes.PNLEntry)
        .filter_by(business_unit=bu_alias.upper())
        .filter(db_classes.PNLEntry.month > latest_date - relativedelta(months=12))
        .order_by(db_classes.PNLEntry.month)
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

    entries = db.session.scalars(db.select(db_classes.PNLForecast)
        .filter_by(business_unit=bu_alias.upper())
        .filter(
            and_(
                db_classes.PNLForecast.month > latest_date,
                db_classes.PNLForecast.month <= latest_date + relativedelta(months=3)
            )
        )
        .order_by(db_classes.PNLForecast.month)
    ).all()

    lookup_dict = {'keys': [], 'entries': {}} # convert to appropriate output format
    for entry in entries:
        entry = entry.json()
        if entry['month'] not in lookup_dict['keys']:
            lookup_dict['keys'].append(entry['month'])
            lookup_dict['entries'][entry['month']] = {}
        lookup_dict['entries'][entry['month']][entry['pnl_code']] = entry['value']

    return lookup_dict

def calculateProfitKPIs(entries):
    output_data = {
        "Profit": None, #TODO: Very arbitrary, currently just takes all the income minus all the costs
        "Gross Profit Margin": None,
        "Operating Profit Margin": None,
        "Net Profit Margin": None,
        "Quick Ratio": None
    }
    
    # summing data
    sales_revenue = sum(value for code, value in entries.items() if code.startswith("5000-") and code not in ["5000-A015", "5000-M004"])
    sales_adjustments = sum(value for code, value in entries.items() if code == '5500')
    other_incomes =  sum(value for code, value in entries.items() if code.startswith("8") or code in ["5000-A015", "5000-M004"])
    cogs = sum(value for code, value in entries.items() if code.startswith('6'))
    op_expenses = sum(value for code, value in entries.items() if code.startswith('901') or code.startswith('902'))
    fin_expenses = sum(value for code, value in entries.items() if code.startswith('900'))
    print(sales_revenue, sales_adjustments, other_incomes, cogs, op_expenses, fin_expenses)

    # intermediate calculations
    net_sales = sales_revenue - sales_adjustments
    all_expenses = op_expenses + fin_expenses
    all_incomes = sales_revenue + other_incomes - sales_adjustments

    # KPI calculations
    output_data["Profit"] = all_incomes - cogs - all_expenses
    output_data["Gross Profit Margin"] = round((sales_revenue - cogs) / sales_revenue * 100, 4) if sales_revenue != 0 else None
    output_data["Operating Profit Margin"] = round((net_sales - cogs - op_expenses) / net_sales * 100, 4) if net_sales != 0 else None
    output_data["Net Profit Margin"] = round((all_incomes - cogs - all_expenses) / all_incomes * 100, 4) if all_incomes != 0 else None
    output_data["Quick Ratio"] = None

    return output_data

def calculateSalesKPIs(entries):
    output_data = {
        "Sales": None, #TODO: Very arbitrary, currently just sums all income except "Other Incomes"
        "Return on Sales": None,
        "Days Sales Outstanding (DSO)": None,
        "Receivables Turnover": None
    }

    # summing data
    sales_revenue = sum(value for code, value in entries.items() if code.startswith("5000-") and code not in ["5000-A015", "5000-M004"])
    sales_adjustments = sum(value for code, value in entries.items() if code == '5500')
    cogs = sum(value for code, value in entries.items() if code.startswith('6'))
    op_expenses = sum(value for code, value in entries.items() if code.startswith('901') or code.startswith('902'))
    print(sales_revenue, sales_adjustments, cogs, op_expenses)

    # intermediate calculations
    net_sales = sales_revenue - sales_adjustments
    operating_profit = sales_revenue - sales_adjustments - cogs - op_expenses

    # KPI calculations
    output_data["Sales"] = net_sales
    output_data["Return on Sales"] = round(operating_profit / net_sales * 100, 4) if net_sales != 0 else None
    output_data["Days Sales Outstanding (DSO)"] = None
    output_data["Receivables Turnover"] = None

    return output_data

def calculateCostKPIs(entries):
    output_data = {
        "Cost": None, #TODO: Very arbitrary, currently just sums all cogs and expenses
        "COGS Ratio": None,
        "Days Payable Outstanding (DPO)": None,
        "Overhead Ratio": None
    }

    # summing data
    sales_revenue = sum(value for code, value in entries.items() if code.startswith("5000-") and code not in ["5000-A015", "5000-M004"])
    sales_adjustments = sum(value for code, value in entries.items() if code == '5500')
    cogs = sum(value for code, value in entries.items() if code.startswith('6'))
    all_expenses = sum(value for code, value in entries.items() if code.startswith('9'))
    overhead_costs = sum(value for code, value in entries.items() if code.startswith('902') or code.startswith('9000-D'))
    
    # intermediate calculations
    net_sales = sales_revenue - sales_adjustments

    # KPI calculations
    output_data["Cost"] = cogs + all_expenses
    output_data["COGS Ratio"] = round(cogs / net_sales * 100, 4) if net_sales != 0 else None
    output_data["Days Payable Outstanding (DPO)"] = None
    output_data["Overhead Ratio"] = round(overhead_costs / net_sales * 100, 4) if net_sales != 0 else None

    return output_data

if __name__ == '__main__':
    print("Monolithic flask application running:" + os.path.basename(__file__) + "...")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
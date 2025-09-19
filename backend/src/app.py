from datetime import datetime
from zoneinfo import ZoneInfo
import os
from dotenv import load_dotenv

from flask import Flask, jsonify, request
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
@app.route("/employee/", methods=['GET'])
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
        key in data for key in ['employee_id', 'password']
    ):
        return jsonify(
            {
                "code": 400,
                "message": "Invalid/missing input data :("
            }
        ), 400
    
    employee = db.session.scalars(db.select(db_classes.Employee).filter_by(id=data['employee_id'])).first()

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
@app.route("/parameter/all/<employee_id>", methods=['GET'])
def getParametersByEmployeeId(employee_id):
    parameters = db.session.scalars(db.select(db_classes.Parameter).filter_by(employee_id=employee_id)).all()

    output_data = {} # convert to appropriate output format
    for param in parameters:
        param = param.json()
        if param['created_date'] not in output_data:
            output_data[param['created_date']] = {}
        output_data[param['created_date']][param['name']] = param['value']

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

@app.route("/parameter/latest/<employee_id>", methods=['GET'])
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
@app.route("/entry/<pnl_code>/<bu_alias>")
def getPNLEntriesByCodeAndBU(pnl_code, bu_alias):
    pnl_entries = db.session.scalars(db.select(db_classes.PNLEntry)
        .filter_by(code=pnl_code)
        .filter_by(business_unit=bu_alias)    
    ).all()

    if pnl_entries:
        return jsonify(
            {
                "code": 200,
                "data": [item.json() for item in pnl_entries]
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "data": [],
            "message": "No PNL entries found :("
        }
    ), 404

######################## PNL FORECAST ########################
@app.route("/forecast/<pnl_code>/<bu_alias>")
def getPNLForecastasByCodeAndBU(pnl_code, bu_alias):
    pnl_entries = db.session.scalars(db.select(db_classes.PNLForecast)
        .filter_by(code=pnl_code)
        .filter_by(business_unit=bu_alias)
    ).all()

    if pnl_entries:
        return jsonify(
            {
                "code": 200,
                "data": [item.json() for item in pnl_entries]
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "data": [],
            "message": "No PNL forecasts found :("
        }
    ), 404


if __name__ == '__main__':
    print("Monolithic flask application running:" + os.path.basename(__file__) + "...")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
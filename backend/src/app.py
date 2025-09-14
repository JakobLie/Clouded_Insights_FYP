import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import db_classes

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

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
            "data": [],
            "message": "No employees found :("
        }
    ), 404

@app.route("/employee/<str:id>", methods=['GET'])
def getEmployeeById(id):
    employee = db.session.scalars(db.select(db_classes.Employee).filter_by(id=id)).first()
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
            "data": {
                "id": id
            },
            "message": "Employee not found :("
        }
    ), 404


######################## PARAMETER ########################
@app.route("/parameter/<str:employee_id>", methods=['GET'])
def getAllParametersByEmployeeId(employee_id):
    parameters = db.session.scalars(db.select(db_classes.Parameter).filter_by(employee_id=employee_id)).all()
    if parameters:
        return jsonify(
            {
                "code": 200,
                "data": [item.json() for item in parameters]
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "data": [],
            "message": "No parameters found :("
        }
    ), 404

@app.route("/parameter/", methods=['POST'])
def setNewParameter():
    data = request.get_json()
    
    if not data:
        return jsonify(
            {
                "code": 400,
                "message": "No input data provided :("
            }
        ), 400
    try:
        new_parameter = db_classes.Parameter(
            employee_id=data['employee_id'],
            parameter_name=data['parameter_name'],
            parameter_value=data['parameter_value']
        )
        db.session.add(new_parameter)
        db.session.commit()
        return jsonify(
            {
                "code": 201,
                "data": new_parameter.json(),
                "message": "New parameter created successfully!"
            }
        ), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "code": 500,
                "message": f"An error occurred: {str(e)}"
            }
        ), 500



if __name__ == '__main__':
    print("Monolithic flask application running:" + os.path.basename(__file__) + "...")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
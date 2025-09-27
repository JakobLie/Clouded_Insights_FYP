import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Staff(db.Model):
    __tablename__ = 'staff'
    staff_id = db.Column(db.Integer, primary_key=True)
    staff_fname = db.Column(db.String(50), nullable=False)
    staff_lname = db.Column(db.String(50), nullable=False)
    dept = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    reporting_manager = db.Column(db.Integer, nullable=False)
    role = db.Column(db.Integer, nullable=False)

    def json(self):
        return {
            'staff_id': self.staff_id,
            'staff_fname': self.staff_fname,
            'staff_lname': self.staff_lname,
            'dept': self.dept,
            'position': self.position,
            'country': self.country,
            'email': self.email,
            'reporting_manager': self.reporting_manager,
            'role': self.role
        }


@app.route("/employees", methods=['GET'])
def getAllStaff():
    employees = db.session.scalars(db.select(Staff)).all()
    if employees:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "employees": [item.json() for item in employees]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "data": [],
            "message": "No employees found :("
        }
    ), 404


@app.route("/staff/<int:id>", methods=['GET'])
def getStaffById(id):
    staff = db.session.scalars(db.select(Staff).filter_by(staff_id=id)).first()
    if staff:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "staff": staff.json()
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "data": {
                "staff_id": id
            },
            "message": "Staff not found :("
        }
    ), 404


@app.route("/dept/<int:id>", methods=['GET'])
def getDeptById(id):
    staff = db.session.scalars(db.select(Staff).filter_by(staff_id=id)).first()
    if not staff:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "staff_id": id
                },
                "message": "Staff not found :("
            }
        ), 404
    
    dept = staff.dept

    department = db.session.scalars(db.select(Staff).filter_by(dept=dept)).all()
    if len(department):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "team": [item.json() for item in department]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "data": {
                "staff_id": id
            },
            "message": "Department not found :("
        }
    ), 404


@app.route("/team/<int:id>", methods=['GET'])
def getTeamById(id):
    staff = db.session.scalars(db.select(Staff).filter_by(staff_id=id)).first()
    if not staff:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "staff_id": id
                },
                "message": "Staff not found :("
            }
        ), 404
    
    manager_id = staff.reporting_manager

    team = db.session.scalars(db.select(Staff).filter_by(reporting_manager=manager_id)).all()
    if len(team):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "team": [item.json() for item in team]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "data": {
                "staff_id": id
            },
            "message": "Team not found :("
        }
    ), 404

@app.route("/employees/<int:id>", methods=['GET'])
def getEmployeesById(id):
    employees = db.session.scalars(db.select(Staff).filter_by(reporting_manager=id)).all()
    if len(employees):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "employees": [item.json() for item in employees]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "data": {
                "staff_id": id
            },
            "message": "Employees not found :("
        }
    ), 404

@app.route("/request/staff/<int:staff_id>", methods=['POST'])
def createRequest(staff_id):
    data = request.get_json(silent=True)
    if data and "comment" in data:
        comment = data["comment"]
    else:
        comment = None

    latest_request = db.session.scalars(db.select(Request).order_by(Request.request_id.desc())).first()
    request_id = latest_request.json()['request_id']+1
    request_entry = Request(request_id, staff_id, comment)
    try:
        db.session.add(request_entry)
        return_data = {'request_id':request_id ,'staff_id':staff_id, 'status':None, 'comment':comment}
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "staff_id": staff_id
                },
                "message": "An error occurred creating the request :("+str(e)
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": {
                "request": return_data
            }
        }
    ), 201

@app.route("/request/<int:request_id>", methods=["PUT"])
def updateRequest(request_id):
    # retrieve json data and preprocess it for database update
    data = request.get_json()
    status = data["status"]
    if isinstance(status,str):
        status = RequestStatus[status.upper()].asInteger()
    if "comment" not in data or data["comment"]==None:
        comment = " | "
    else:
        comment = ": " + data["comment"] + " | "

    # retrieve request to be updated: if it doesn't exist >> return with error 404 not found
    request_entry = db.session.scalars(db.select(Request).filter_by(request_id=request_id)).first()
    if not request_entry:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "request_id": request_id
                },
                "message": "Request not found :("
            }
        ), 404
    
    # attempt to update
    try:
        request_entry.status = status
        if request_entry.comment==None:
            request_entry.comment = ""
        request_entry.comment += RequestStatus(status).asString() + comment
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "request_id": request_id,
                    "status": data["status"],
                    "comment": comment
                },
                "message": "An error occurred updating the request :("+str(e)
            }
        ), 500
    return jsonify(
        {
            "code": 200,
            "data": {
                "request": request_entry.json()
            }
        }
    ), 200

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage staff ...")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5002)), debug=True)

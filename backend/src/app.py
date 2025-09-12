import os
from flask import Flask, jsonify
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

@app.route("/employee", methods=['GET'])
def getAllEmployees():
    employees = db.session.scalars(db.select(db_classes.Employee)).all()
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

if __name__ == '__main__':
    print("Monolithic flask application running:" + os.path.basename(__file__) + "...")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
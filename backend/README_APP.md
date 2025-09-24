# Flask App Docker Compose Setup

A Flask-based RESTful API app using Flask-SQLAlchemy for managing employees and their parameters.

---

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Running Flask App with Docker Compose](#running-flask-app-with-docker-compose)
- [API Endpoints](#api-endpoints)
  - [Employee APIs](#employee-apis)
  - [Parameter APIs](#parameter-apis)
- [Input and Output Formats](#input-and-output-formats)
- [Technologies](#technologies)

---

## Getting Started

### Prerequisites
- Docker Desktop, Docker & Docker Compose (usually bundled together) installed on your machine
[https://www.docker.com/get-started/]

### Running Flask App with Docker Compose
1. Open Docker Desktop to start the Docker Daemon
2. Navigate to the the project's `~/Backend/` folder containing the `compose.yaml` file in your command line
3. Run the command `docker compose -p cloudedinsights up --build`

Default server runs at `http://127.0.0.1:5000`

---

## API Endpoints

### Summary
#### Employee APIs

| Method | Endpoint                           | Description                        |
|--------|----------------------------------|----------------------------------|
| GET    | /employee/                       | Get all employees                 |
| GET    | /employee/id/&lt;employee_id&gt;/        | Get employee by ID                |
| GET    | /employee/email/&lt;email&gt;/          | Get employee by email             |
| POST   | /employee/authenticate/          | Authenticate employee for login   |

#### Parameter APIs

| Method | Endpoint                           | Description                              |
|--------|----------------------------------|----------------------------------------|
| GET    | /parameter/all/&lt;employee_id&gt;         | Get all parameters for an employee     |
| GET    | /parameter/latest/&lt;employee_id&gt;      | Get latest parameters for an employee  |
| POST   | /parameter/batch/                 | Create or update multiple parameters   |

---

## Details, Input and Output

### GET /employee/
Simply gets all employee records in the database.

- **Output (JSON):**
```json
{
    "code": 200,
    "data": [
        {
            "business_unit": "BB1",
            "created_at": "18-09-2025 12:16:34",
            "email": "jakob@tsh.com.sg",
            "id": "abcd-abcd-abcd",
            "name": "Jakob Lie",
            "role": "BU Manager"
        },
        ...
    ]
}
```

### GET /employee/id/<employee_id>/
Gets the specific employee entry based on employee ID.

- **Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "business_unit": "BB1",
        "created_at": "18-09-2025 12:16:34",
        "email": "jakob@tsh.com.sg",
        "id": "abcd-abcd-abcd",
        "name": "Jakob Lie",
        "role": "BU Manager"
    }
}
```

### GET /employee/email/<email>/
Gets the specific employee entry based on email.

- **Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "business_unit": "BB1",
        "created_at": "18-09-2025 12:16:34",
        "email": "jakob@tsh.com.sg",
        "id": "abcd-abcd-abcd",
        "name": "Jakob Lie",
        "role": "BU Manager"
    }
}
```

### POST /employee/authenticate/
Currently only uses simple password matching (password=password). Used for dummy login simulation for the prototype. Takes in email and password.

- **Input (JSON):**
```json
{
    "email":"jakob@tsh.com.sg",
    "password":"hashed_password_1"
}
```

- **Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "business_unit": "BB1",
        "created_at": "18-09-2025 12:16:34",
        "email": "jakob@tsh.com.sg",
        "id": "abcd-abcd-abcd",
        "name": "Jakob Lie",
        "role": "BU Manager"
    }
}
```

---

### GET /parameter/all/<employee_id>/
Gets all parameters, including historical and active parameters for the employee using employee ID.

- **Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "01-07-2025": {
            "Cost Budget": 20000.0,
            "Sales Target": 40000.0
        },
        "15-09-2025": {
            "Cost Budget": 102.0,
            "Cost Of Goods Sold Ratio": 0.31
        },
        ...
    }
}
```

### GET /parameter/latest/<employee_id>/
Gets only the active (latest) parameters for a given employee based on ID.

- **Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "Cost Budget": 23000.0,
        "Net Profit Margin": 0.15
    }
}
```

### POST /parameter/batch/
Processes the setting of multiple parameters. If the parameter has already been created within the same day, it will update the value associated. If not, it will create a new parameter entry in the database for the current day. The current date is determined using timezone data provided in the environment variables.

- **Input (JSON):**
```json
{
    "employee_id": "abcd-abcd-abcd",
    "parameters":{
        "Net Profit Margin": 0.15,
        "Receivables Turnover": 0.30,
        "Cost Budget": 23000
    }
}
```

- **Output (JSON):**
```json
{
    "code": 200,
    "data": [
        {
            "change_status": "updated",
            "created_date": "19-09-2025",
            "employee_id": "abcd-abcd-abcd",
            "is_notified": false,
            "name": "Net Profit Margin",
            "value": 0.15
        },
        {
            "change_status": "created",
            "created_date": "19-09-2025",
            "employee_id": "abcd-abcd-abcd",
            "is_notified": false,
            "name": "Receivables Turnover",
            "value": 0.3
        },
        ...
    ]
}
```

---

## Technologies

- Python 3.12
- Flask
- Flask-SQLAlchemy
- Flask-Cors
- PostgreSQL
- Docker Compose
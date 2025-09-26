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

| Method | Endpoint                             | Description                      |
|--------|--------------------------------------|----------------------------------|
| GET    | /employee/all/                       | Get all employees                |
| GET    | /employee/id/&lt;employee_id&gt;/    | Get employee by ID               |
| GET    | /employee/email/&lt;email&gt;/       | Get employee by email            |
| POST   | /employee/authenticate/              | Authenticate employee for login  |

#### Parameter APIs

| Method | Endpoint                                 | Description                                           |
|--------|------------------------------------------|-------------------------------------------------------|
| GET    | /parameter/all/&lt;employee_id&gt;/      | Get all parameters for an employee                    |
| GET    | /parameter/latest/&lt;employee_id&gt;/   | Get latest parameters for an employee                 |
| POST   | /parameter/batch/                        | Create or update multiple parameters for an employee  |

#### PNL Entry APIs
| Method | Endpoint                                 | Description                                           |
|--------|------------------------------------------|-------------------------------------------------------|
| GET    | /category/all/                           | Get all PNL category codes, names and descriptions    |
| GET    | /entry/individual/&lt;pnl_code&gt;/&lt;business_unit&gt;/    | Get all entries for a BU and month    |
| GET    | /entry/sales/&lt;business_unit&gt;/      | Get last 12 months sales PNL entries for a BU         |
| GET    | /entry/cost/&lt;business_unit&gt;/       | Get last 12 months cost PNL entries for a BU          |

#### PNL Forecast APIs
| Method | Endpoint                                 | Description                                           |
|--------|------------------------------------------|-------------------------------------------------------|
| GET    | /forecast/individual/&lt;pnl_code&gt;/&lt;business_unit&gt;/     | Get all forecasts for a BU in a month  |
| GET    | /forecast/sales/&lt;business_unit&gt;/   | Get next 3 months sales PNL forecasts for a BU         |
| GET    | /forecast/cost/&lt;business_unit&gt;/    | Get next 3 months cost PNL forecasts for a BU          |

#### PNL KPI APIs
| Method | Endpoint                                 | Description                                           |
|--------|------------------------------------------|-------------------------------------------------------|
| GET    | /kpi/profit/&lt;business_unit&gt;/       | Get last 12 months profit PNL KPIs for a BU           |
| GET    | /kpi/sales/&lt;business_unit&gt;/        | Get last 12 months sales PNL KPIs for a BU            |
| GET    | /kpi/cost/&lt;business_unit&gt;/         | Get last 12 months cost PNL KPIs for a BU             |
| GET    | /kpi/f_profit/&lt;business_unit&gt;/     | Get next 3 months forecasted profit PNL KPIs for a BU |
| GET    | /kpi/f_sales/&lt;business_unit&gt;/      | Get next 3 months forecasted sales PNL KPIs for a BU  |
| GET    | /kpi/f_cost/&lt;business_unit&gt;/       | Get next 3 months forecasted cost PNL KPIs for a BU   |

---
## Context

### KPIs

**Profit KPIs**
1. Gross Profit Margin: 
```math
GPM = \frac{Sale\space Revenue-COGS}{Sale\space Revenue}\times 100\%
```
2. Operating Profit Margin: 
```math
Net\space Sales=Sale\space Revenue-Sale\space Adjustments
```
```math
OPM=\frac{Net\space Sales-COGS-Operating\space Expenses}{Net\space Sales}\times 100\%
```
3. Net Profit Margin:
```math
Income=Sale\space Revenue-Sale\space Adjustments+Other\space Incomes
```
```math
Expenses=Operating\space Expenses + Financial\space Expenses
```
```math
NPM=\frac{Income-Expenses-COGS}{Income}\times 100\%
```
4. Quick Ratio: _Currently incalculable without Accounts Receivable_

**Sales KPIs**
1. Days Sales Outstanding (DSO): _Currently incalculable without Accounts Receivable_
2. Receivables Turnover: _Currently incalculable without Accounts Receivable_
3. Return on Sales: 
```math
Net\space Sales=Sale\space Revenue-Sale\space Adjustments
```
```math
Operating\space Profit=Sale\space Revenue-Sale\space Adjustments-COGS-Operating\space Expenses
```
```math
NPM=\frac{Operating\space Profit}{Net\space Sales}\times 100\%
```
**Cost KPIs**
1. COGS Ratio: 
```math
Net\space Sales=Sale\space Revenue-Sale\space Adjustments
```
```math
NPM=\frac{COGS}{Net\space Sales}\times 100\%
```
2. Days Payable Outstanding (DPO): _Currently incalculable without Accounts Payable_
3. Overhead Ratio: 
```math
Net\space Sales=Sale\space Revenue-Sale\space Adjustments
```
```math
NPM=\frac{Overhead\space Costs}{Net\space Sales}\times 100\%
```

---

## Details, Input and Output

### GET /employee/all/
Simply gets all employee records in the database.

**Output (JSON):**
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

### GET /employee/id/%lt;employee_id&gt;/
Gets the specific employee entry based on employee ID.

**Output (JSON):**
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

### GET /employee/email/&lt;email&gt;/
Gets the specific employee entry based on email. Take note that '@' values must be replaced with '%40' in the route. (_e.g. jakob%40tsh.com.sg_)

**Output (JSON):**
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

**Input (JSON):**
```json
{
    "email":"jakob@tsh.com.sg",
    "password":"hashed_password_1"
}
```

**Output (JSON):**
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
Gets all parameters, including historical and active parameters for the employee using employee ID. Also gets keys (months) in ascending order (earliest to latest).

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "keys": [
            "01-07-2025",
            "15-09-2025",
            ...
        ],
        "parameters": {
            "01-07-2025": {
                "Cost Budget": 20000.0,
                "Sales Target": 40000.0
            },
            "15-09-2025": {
                "Cost Budget": 102.0,
                "Cost Of Goods Sold Ratio": 0.31,
                ...
            },
            ...
        }
    }
}
```

### GET /parameter/latest/<employee_id>/
Gets only the active (latest) parameters for a given employee based on ID.

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "Cost Budget": 102.0,
        "Cost Of Goods Sold Ratio": 0.31,
        ...
    }
}
```

### POST /parameter/batch/
Processes the setting of multiple parameters. If the parameter has already been created within the same day, it will update the value associated (`"change_status":"updated"`). If not, it will create a new parameter entry in the database for the current day(`"change_status":"created"`). The current date is determined using timezone data provided in the system environment variables (provided in `compose.yaml`).

**Input (JSON):**
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

**Output (JSON):**
```json
{
    "code": 200,
    "data": [
        {
            "change_status": "created",
            "created_date": "25-09-2025",
            "employee_id": "abcd-abcd-abcd",
            "is_notified": null,
            "name": "Net Profit Margin",
            "value": 0.15
        },
        {
            "change_status": "updated",
            "created_date": "25-09-2025",
            "employee_id": "abcd-abcd-abcd",
            "is_notified": null,
            "name": "Receivables Turnover",
            "value": 0.3
        },
        ...
    ]
}
```

---

### GET /category/all/
Gets all PNL categories, mapping their codes to their names and descriptions.

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "5000-0000": {
            "description": "",
            "name": "SALES REVENUE"
        },
        "5000-A000": {
            "description": "SALES REVENUE",
            "name": "ASSEMBLY"
        },
        "5000-A001": {
            "description": "SALES REVENUE/ASSEMBLY",
            "name": "ASB SALES MODULE BB"
        },
        ...
    }
}
```

### GET /entry/individual/&lt;pnl_code&gt;/&lt;business_unit&gt;/
Gets all the PNL entries of a business unit for a specific PNL category code.

**Output (JSON):**
```json
{
    "code": 200,
    "data": [
        {
            "business_unit": "BB1",
            "month": "07-2024",
            "pnl_code": "5000-A001",
            "value": 37000.0
        },
        ...
    ]
}
```

### GET /entry/sales/&lt;business_unit&gt;/
Gets all sales PNL entries for the last 12 months for a business unit, under `"entries"`. The months will also be retrieved in ascending order (earliest to latest), under `"keys"`.
- The last 12 months are relative to the latest PNL entry and if non-existent, today's date.
- Sales PNL entries include those with category codes starting with '5' [ SALES ] or '8' [ OTHER INCOMES ].

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "entries": {
            "08-2025": {
                "5000-A001": 50000.0,
                "5000-M001": 20000.0,
                "5000-M002": 10000.0
            },
            ...
        },
        "keys": [
            "10-2024",
            ...
            "08-2025",
            "09-2025"
        ]
    }
}
```

### GET /entry/cost/&lt;business_unit&gt;/
Gets all cost PNL entries for the last 12 months for a business unit, under `"entries"`. The months will also be retrieved in ascending order (earliest to latest), under `"keys"`.
- The last 12 months are relative to the latest PNL entry and if non-existent, today's date.
- Cost PNL entries include those with category codes starting with '6' [ COST OF GOODS SOLD ] or '9' [ EXPENSES ].

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "entries": {
            "08-2025": {
                "6004-0002": 5000.0,
                "6005-1001": 3000.0
            },
            ...
        },
        "keys": [
            "10-2024",
            ...
            "08-2025",
            "09-2025"
        ]
    }
}
```

---

### GET /forecast/individual/&lt;pnl_code&gt;/&lt;business_unit&gt;/
Gets all the PNL forecasts of a business unit for a specific PNL category code.

**Output (JSON):**
```json
{
    "code": 200,
    "data": [
        {
            "business_unit": "BB1",
            "month": "10-2025",
            "pnl_code": "5000-A001",
            "value": 55000.0
        },
        ...
    ]
}
```

### GET /forecast/sales/&lt;business_unit&gt;/
Gets all sales PNL forecasts for the next 3 months for a business unit, under `"forecasts"`. The months will also be retrieved in ascending order (earliest to latest), under `"keys"`.
- The next 3 months are relative to the latest PNL entry and if non-existent, today's date.
- Sales PNL entries include those with category codes starting with '5' [ SALES ] or '8' [ OTHER INCOMES ].

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "forecasts": {
            "10-2025": {
                "5000-A001": 55000.0,
                "5000-M001": 22000.0,
                "5000-M002": 11000.0
            },
            ...
        },
        "keys": [
            "10-2025",
            "11-2025",
            "12-2025"
        ]
    }
}
```

### GET /forecast/cost/&lt;business_unit&gt;/
Gets all cost PNL forecasts for the next 3 months for a business unit, under `"forecasts"`. The months will also be retrieved in ascending order (earliest to latest), under `"keys"`.
- The next 3 months are relative to the latest PNL entry and if non-existent, today's date.
- Cost PNL entries include those with category codes starting with '6' [ COST OF GOODS SOLD ] or '9' [ EXPENSES ].

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "forecasts": {
            "10-2025": {
                "6004-0002": 6000.0,
                "6005-1001": 3500.0
            },
            ...
        },
        "keys": [
            "10-2025",
            "11-2025",
            "12-2025"
        ]
    }
}
```

---

### GET /kpi/profit/&lt;business_unit&gt;/
Calculates all Profit KPIs for the last 12 months for a business unit, under `"kpis"`. The months will also be retrieved in ascending order (earliest to latest), under `"keys"`.
- The last 12 months are relative to the latest PNL entry and if non-existent, today's date.

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "keys": [
            "10-2024",
            ...
            "08-2025",
            "09-2025"
        ],
        "kpis": {
            "01-2025": {
                "Gross Profit Margin": 100.0,
                "Net Profit Margin": 100.0,
                "Operating Profit Margin": 100.0,
                "Quick Ratio": null
            },
            ...
        }
    }
}
```

### GET /kpi/sales/&lt;business_unit&gt;/
Calculates all Sales KPIs for the last 12 months for a business unit, under `"kpis"`. The months will also be retrieved in ascending order (earliest to latest), under `"keys"`.
- The last 12 months are relative to the latest PNL entry and if non-existent, today's date.

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "keys": [
            "10-2024",
            ...
            "08-2025",
            "09-2025"
        ],
        "kpis": {
            "01-2025": {
                "Days Sales Outstanding (DSO)": null,
                "Receivables Turnover": null,
                "Return on Sales": 100.0
            },
            ...
        }
    }
}
```

### GET /kpi/cost/&lt;business_unit&gt;/
Calculates all Cost KPIs for the last 12 months for a business unit, under `"kpis"`. The months will also be retrieved in ascending order (earliest to latest), under `"keys"`.
- The last 12 months are relative to the latest PNL entry and if non-existent, today's date.

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "keys": [
            "10-2024",
            ...
            "08-2025",
            "09-2025"
        ],
        "kpis": {
            "01-2025": {
                "COGS Ratio": 0.0,
                "Days Payable Outstanding (DPO)": null,
                "Overhead Ratio": 0.0
            },
            ...
        }
    }
}
```

### GET /kpi/f_profit/&lt;business_unit&gt;/
Calculates all forecasted Profit KPIs for the next 3 months for a business unit, under `"kpis"`. The months will also be retrieved in ascending order (earliest to latest), under `"keys"`.
- The next 3 months are relative to the latest PNL entry and if non-existent, today's date.

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "keys": [
            "10-2025",
            "11-2025",
            "12-2025"
        ],
        "kpis": {
            "10-2025": {
                "Gross Profit Margin": 89.2045,
                "Net Profit Margin": 89.2045,
                "Operating Profit Margin": 89.2045,
                "Quick Ratio": null
            },
            ...
        }
    }
}
```

### GET /kpi/f_sales/&lt;business_unit&gt;/
Calculates all forecasted Sales KPIs for the next 3 months for a business unit, under `"kpis"`. The months will also be retrieved in ascending order (earliest to latest), under `"keys"`.
- The next 3 months are relative to the latest PNL entry and if non-existent, today's date.

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "keys": [
            "10-2025",
            "11-2025",
            "12-2025"
        ],
        "kpis": {
            "10-2025": {
                "Days Sales Outstanding (DSO)": null,
                "Receivables Turnover": null,
                "Return on Sales": 89.2045
            },
            ...
        }
    }
}
```

### GET /kpi/f_cost/&lt;business_unit&gt;/
Calculates all forecasted Cost KPIs for the next 3 months for a business unit, under `"kpis"`. The months will also be retrieved in ascending order (earliest to latest), under `"keys"`.
- The next 3 months are relative to the latest PNL entry and if non-existent, today's date.

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "keys": [
            "10-2025",
            "11-2025",
            "12-2025"
        ],
        "kpis": {
            "10-2025": {
                "COGS Ratio": 10.7955,
                "Days Payable Outstanding (DPO)": null,
                "Overhead Ratio": 0.0
            },
            ...
        }
    }
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
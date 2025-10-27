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
  - [PNL Entry APIs](#pnl-entry-apis)
  - [PNL Forecast APIs](#pnl-forecast-apis)
  - [KPI APIs](#kpi-apis)
  - [Load Data APIs](#load-data-api)
- [Context](#context)
  - [KPIs](#kpis)
- [API Details](#api-details)
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
| GET    | /parameter/15mths/&lt;employee_id&gt;/   | Get 12 months back and 3 months forward parameters    |
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

#### KPI APIs
| Method | Endpoint                                 | Description                                           |
|--------|------------------------------------------|-------------------------------------------------------|
| GET    | /kpi/category/                           | Gets all KPI categories                               |
| GET    | /kpi/profit/&lt;business_unit&gt;/       | Get last 12 months profit PNL KPIs for a BU           |
| GET    | /kpi/sales/&lt;business_unit&gt;/        | Get last 12 months sales PNL KPIs for a BU            |
| GET    | /kpi/cost/&lt;business_unit&gt;/         | Get last 12 months cost PNL KPIs for a BU             |
| GET    | /kpi/f_profit/&lt;business_unit&gt;/     | Get next 3 months forecasted profit PNL KPIs for a BU |
| GET    | /kpi/f_sales/&lt;business_unit&gt;/      | Get next 3 months forecasted sales PNL KPIs for a BU  |
| GET    | /kpi/f_cost/&lt;business_unit&gt;/       | Get next 3 months forecasted cost PNL KPIs for a BU   |

#### LOAD DATA API
| Method | Endpoint                                 | Description                                           |
|--------|------------------------------------------|-------------------------------------------------------|
| POST   | /load_data/&lt;month&gt;/                | Loads data from "pnl_report" Excel/CSV file into DB, also orchestrates multiple processes   |

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

## API Details

### GET /employee/all/
Simply gets all employee records in the database.

**Output (JSON):**
```json
{
    "code": 200,
    "data": [
        {
            "business_unit": "BB1",
            "created_at": "27-10-2025 05:23:27",
            "email": "jakob@tsh.com.sg",
            "id": "abcd-abcd-abcd",
            "name": "Jakob Lie",
            "phone_number": "+6588888888",
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
        "created_at": "27-10-2025 05:23:27",
        "email": "jakob@tsh.com.sg",
        "id": "abcd-abcd-abcd",
        "name": "Jakob Lie",
        "phone_number": "+6588888888",
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
        "created_at": "27-10-2025 05:23:27",
        "email": "jakob@tsh.com.sg",
        "id": "abcd-abcd-abcd",
        "name": "Jakob Lie",
        "phone_number": "+6588888888",
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
    "data": "data": {
        "business_unit": "BB1",
        "created_at": "27-10-2025 05:23:27",
        "email": "jakob@tsh.com.sg",
        "id": "abcd-abcd-abcd",
        "name": "Jakob Lie",
        "phone_number": "+6588888888",
        "role": "BU Manager"
    }
}
```

---

### GET /parameter/all/&lt;employee_id&gt;/
Gets all parameters, including historical and active parameters for the employee using employee ID. Also gets keys (months) in ascending order (earliest to latest). Use in tandem with **GET /kpi/category/** to get the names of the parameters.

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
            "07-2025": {
                "COST": 20000.0,
                "SALES": 40000.0,
                ...
            },
            "09-2025": {
                "COGSR": 0.31,
                "COST": 102.0,
                ...
            },
            ...
        }
    }
}
```

### GET /parameter/latest/&lt;employee_id&gt;/
Gets only the active (latest) parameters for a given employee based on ID. Use in tandem with **GET /kpi/category/** to get the names of the parameters.

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "COGSR": 0.31,
        "COST": 102.0,
        ...
    }
}
```

### GET /parameter/15mths/&lt;employee_id&gt;/
Gets all the parameters for an employee 12 months back and 3 months forward, 15 months in total. Also gets keys (months) in ascending order (earliest to latest). Use in tandem with **GET /kpi/category/** to get the names of the parameters.

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "keys": [
            "10-2024",
            "11-2024",
            ...
            "01-2026",
        ],
        "parameters": {
            "07-2025": {
                "COST": 20000.0,
                "SALES": 40000.0,
                ...
            },
            "09-2025": {
                "COGSR": 0.31,
                "COST": 102.0,
                ...
            }
        }
    }
}
```

### POST /parameter/batch/
Processes the setting of multiple parameters. If the parameter has already been created for the specified month, it will update the value associated (`"change_status":"updated"`). If not, it will create a new parameter entry in the database for the specified month (`"change_status":"created"`).

**Input (JSON):**
```json
{
    "employee_id": "abcd-abcd-abcd",
    "month":"11-2025",
    "parameters":{
        "COGSR": 0.31,
        "COST": 102.0,
        "DPO": 0.32,
        ...
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
            "employee_id": "abcd-abcd-abcd",
            "is_notified": false,
            "kpi_alias": "COGSR",
            "month": "10-2025",
            "value": 0.31
        },
        {
            "change_status": "updated",
            "employee_id": "abcd-abcd-abcd",
            "is_notified": false,
            "kpi_alias": "COST",
            "month": "11-2025",
            "value": 102.0
        },
        ...
    ],
    "message": "Parameters set successfully :)"
}
```

---

### GET /category/all/
Gets all PNL categories, mapping their codes to their names, descriptions, parent codes and trends.

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "5000-0000": {
            "description": null,
            "name": "SALES REVENUE",
            "parent_code": null,
            "trend": "STATIC"
        },
        "5000-A000": {
            "description": null,
            "name": "ASSEMBLY",
            "parent_code": "5000-0000",
            "trend": "STATIC"
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
                "5000-M002": 10000.0,
                ...
            },
            ...
        },
        "keys": [
            "11-2024",
            ...
            "09-2025",
            "10-2025"
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
                "6005-1001": 3000.0,
                ...
            },
            ...
        },
        "keys": [
            "11-2024",
            ...
            "08-2025",
            "10-2025"
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
            "11-2025": {
                "5000-A001": 55000.0,
                "5000-M001": 22000.0,
                "5000-M002": 11000.0,
                ...
            },
            ...
        },
        "keys": [
            "11-2025",
            "12-2025",
            "01-2026"
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
            "11-2025": {
                "6004-0002": 6000.0,
                "6005-1001": 3500.0,
                ...
            },
            ...
        },
        "keys": [
            "11-2025",
            "12-2025",
            "01-2026"
        ]
    }
}
```

---

### GET /kpi/category/
Retrieves all KPI categories, mapping their alias to their category, description and full name. Used in tandem with Parameter APIs and other KPI APIs.

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "COGSR": {
            "category": "COST",
            "description": "Cost of goods sold as a percentage of sales, showing production cost efficiency.",
            "name": "COGS Ratio"
        },
        "COST": {
            "category": "COST",
            "description": "Total cost, summing cost of goods sold and operating expenses.",
            "name": "Cost"
        },
        ...
    }
}
```

### GET /kpi/profit/&lt;business_unit&gt;/
Retrieves all Profit KPIs for the last 12 months for a business unit, under `"kpis"`. The months will also be retrieved in ascending order (earliest to latest), under `"keys"`.
- The last 12 months are relative to the latest PNL entry and if non-existent, today's date.

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "keys": [
            "11-2024",
            ...
            "08-2025",
            "10-2025"
        ],
        "kpis": {
            "01-2025": {
                "GPM": 1.1665,
                "NPM": -7.377,
                "OPM": -7.6969,
                "PROF": -357432.66,
                "QR": null
            },
            ...
        }
    }
}
```

### GET /kpi/sales/&lt;business_unit&gt;/
Retrieves all Sales KPIs for the last 12 months for a business unit, under `"kpis"`. The months will also be retrieved in ascending order (earliest to latest), under `"keys"`.
- The last 12 months are relative to the latest PNL entry and if non-existent, today's date.

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "keys": [
            "11-2024",
            ...
            "08-2025",
            "10-2025"
        ],
        "kpis": {
            "01-2025": {
                "DSO": null,
                "ROS": -7.6969,
                "RT": null,
                "SALES": 4810000.0
            },
            ...
        }
    }
}
```

### GET /kpi/cost/&lt;business_unit&gt;/
Retrieves all Cost KPIs for the last 12 months for a business unit, under `"kpis"`. The months will also be retrieved in ascending order (earliest to latest), under `"keys"`.
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
                "COGSR": 98.8335,
                "COST": 5202677.22,
                "DPO": null,
                "OHR": 8.5038
            },
            ...
        }
    }
}
```

### GET /kpi/f_profit/&lt;business_unit&gt;/
Retrieves all forecasted Profit KPIs for the next 3 months for a business unit, under `"kpis"`. The months will also be retrieved in ascending order (earliest to latest), under `"keys"`.
- The next 3 months are relative to the latest PNL entry and if non-existent, today's date.

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "keys": [
            "11-2025",
            "12-2025",
            "01-2026"
        ],
        "kpis": {
            "11-2025": {
                "GPM": 1.1665,
                "NPM": -7.377,
                "OPM": -7.6969,
                "PROF": -357432.66,
                "QR": null
            },
            ...
        }
    }
}
```

### GET /kpi/f_sales/&lt;business_unit&gt;/
Retrieves all forecasted Sales KPIs for the next 3 months for a business unit, under `"kpis"`. The months will also be retrieved in ascending order (earliest to latest), under `"keys"`.
- The next 3 months are relative to the latest PNL entry and if non-existent, today's date.

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "keys": [
            "11-2025",
            "12-2025",
            "01-2026"
        ],
        "kpis": {
            "11-2025": {
                "DSO": null,
                "ROS": -7.6969,
                "RT": null,
                "SALES": 4810000.0
            },
            ...
        }
    }
}
```

### GET /kpi/f_cost/&lt;business_unit&gt;/
Retrieves all forecasted Cost KPIs for the next 3 months for a business unit, under `"kpis"`. The months will also be retrieved in ascending order (earliest to latest), under `"keys"`.
- The next 3 months are relative to the latest PNL entry and if non-existent, today's date.

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "keys": [
            "11-2025",
            "12-2025",
            "01-2026"
        ],
        "kpis": {
            "11-2025": {
                "COGSR": 98.8335,
                "COST": 5202677.22,
                "DPO": null,
                "OHR": 8.5038
            },
            ...
        }
    }
}
```

---

### POST /load_data/&lt;month&gt;/
Loads all data in the monthly report to the database, including:
1. Business Units (from BU header row)
2. PNL Categories (from header columns)
3. PNL Entries (from data rows per BU)
4. KPI Entries (calculated on data to be uploaded)
5. Parameters (simply autopopulates next 3 months with last set value for each employee)

For each data entry, the API will check the database for existing entries for the specified month. If the value differs, it will update the value associated (`"change_status":"updated"`). If the value does not differ, no action will be made (`"change_status":"unchanged"`). If there is no existing entry, it will create a new entry in the database for the specified month (`"change_status":"created"`).

On top of this, this API also orchestrates the following processes:
1. Triggers forecasting services to retrain models and generate forecasts

**Input (Form Data):**
| Key        | Value                                |
|------------|--------------------------------------|
| pnl_report | PNL Monthly Report File (Excel/CSV)  |

**Output (JSON):**
```json
{
    "code": 200,
    "data": {
        "business_units": [
            {
                "alias": "TOTAL",
                "bu_name": "Total",
                "change_status": "unchanged"
            },
            {
                "alias": "BB1",
                "bu_name": "Box Build 1",
                "change_status": "unchanged"
            },
	        ...
        ],
        "kpi_entries": [
            {
                "business_unit": "TOTAL",
                "change_status": "created",
                "kpi_alias": "PROF",
                "month": "11-2025",
                "value": -84984742.12
            },
            {
                "business_unit": "TOTAL",
                "change_status": "created",
                "kpi_alias": "GPM",
                "month": "11-2025",
                "value": -177.8542
            },
            ...
        ],
        "parameters": [

        ],
        "pnl_categories": [
            {
                "change_status": "unchanged",
                "code": "5000-0000",
                "description": null,
                "name": "SALES REVENUE",
                "parent_code": null,
                "trend": "STATIC"
            },
            {
                "change_status": "unchanged",
                "code": "5000-A000",
                "description": null,
                "name": "ASSEMBLY",
                "parent_code": "5000-0000",
                "trend": "STATIC"
            },
	        ...
        ],
        "pnl_entries": [
            {
                "business_unit": "TOTAL",
                "change_status": "created",
                "month": "11-2025",
                "pnl_code": "5000-A001",
                "value": 6000000.0
            },
            {
                "business_unit": "BB1",
                "change_status": "created",
                "month": "11-2025",
                "pnl_code": "5000-A001",
                "value": 4000000.0
            },
	        ...
        ]
    },
    "message": "Data has been loaded successfully. :) Triggering Machine Learning retraining and forecast generation..."
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
- Kafka
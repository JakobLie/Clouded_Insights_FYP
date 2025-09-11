CREATE TABLE business_unit (
    alias VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE employee (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL,
    business_unit VARCHAR(10) REFERENCES business_unit(alias),
    password_hash VARCHAR(128) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE parameter (
    employee_id VARCHAR(20) REFERENCES employee(id),
    name VARCHAR(100) NOT NULL,
    value NUMERIC(15, 2) NOT NULL,
    is_notified BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (employee_id, name)
);

CREATE TABLE notification (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR(20) REFERENCES employee(id),
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP    
);

CREATE TABLE pnl_category (
    code VARCHAR(15) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL
);

CREATE TABLE pnl_entry (
    pnl_code VARCHAR(15) REFERENCES pnl_category(code),
    business_unit VARCHAR(10) REFERENCES business_unit(alias),
    month DATE,
    value NUMERIC(15, 2) NOT NULL,
    PRIMARY KEY (pnl_code, business_unit, month)
);

CREATE TABLE pnl_forecast (
    pnl_code VARCHAR(15) REFERENCES pnl_category(code),
    business_unit VARCHAR(10) REFERENCES business_unit(alias),
    month DATE,
    value NUMERIC(15, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (pnl_code, business_unit, month)
);
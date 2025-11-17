CREATE TABLE business_unit (
    alias VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE employee (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone_number VARCHAR(20) UNIQUE,
    role VARCHAR(50) NOT NULL,
    business_unit VARCHAR(10) REFERENCES business_unit(alias),
    password_hash VARCHAR(128) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notification (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR(20) REFERENCES employee(id),
    type VARCHAR(50) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP    
);

CREATE TABLE pnl_category (
    code VARCHAR(15) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_code VARCHAR(15) REFERENCES pnl_category(code),
    description TEXT,
    trend VARCHAR(50) NOT NULL DEFAULT 'static'
);

CREATE TABLE pnl_entry (
    pnl_code VARCHAR(15) REFERENCES pnl_category(code),
    business_unit VARCHAR(10) REFERENCES business_unit(alias),
    month DATE,
    value NUMERIC(15,2),
    PRIMARY KEY (pnl_code, business_unit, month)
);

CREATE TABLE pnl_forecast (
    pnl_code VARCHAR(15) REFERENCES pnl_category(code),
    business_unit VARCHAR(10) REFERENCES business_unit(alias),
    month DATE,
    value NUMERIC(15,2),
    PRIMARY KEY (pnl_code, business_unit, month)
);

CREATE TABLE kpi_category (
    alias VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT
);

CREATE TABLE parameter (
    employee_id VARCHAR(20) REFERENCES employee(id),
    kpi_alias VARCHAR(10) REFERENCES kpi_category(alias),
    month DATE,
    value NUMERIC(15,4),
    is_notified BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (employee_id, kpi_alias, month)
);

CREATE TABLE kpi_entry (
    kpi_alias VARCHAR(10) REFERENCES kpi_category(alias),
    business_unit VARCHAR(10) REFERENCES business_unit(alias),
    month DATE,
    value NUMERIC(15,4),
    PRIMARY KEY (kpi_alias, business_unit, month)
);

CREATE TABLE kpi_forecast (
    kpi_alias VARCHAR(10) REFERENCES kpi_category(alias),
    business_unit VARCHAR(10) REFERENCES business_unit(alias),
    month DATE,
    value NUMERIC(15,4),
    PRIMARY KEY (kpi_alias, business_unit, month)
);
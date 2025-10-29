-- Insert business units
INSERT INTO business_unit (alias, name) VALUES
    ('BB1', 'Box Build 1'),
    ('BBS2', 'Box Build 2'),
    ('HQ', 'Headquarters'),
    ('LOG', 'Logistics'),
    ('MCE', 'Mechanical Engineering'),
    ('TOTAL', 'Total');

-- Insert employees
INSERT INTO employee (id, name, email, phone_number, role, business_unit, password_hash) VALUES
    ('abcd-abcd-abcd', 'Jakob Lie', 'jakob@tsh.com.sg', '+6588888888', 'BU Manager', 'BB1', 'hashed_password_1'),
    ('abcd-abcd-abce', 'Jeremy Lin Kairui son of Lin Chee', '+6588888889', 'jeremy@tsh.com.sg', 'BU Manager', 'MCE', 'hashed_password_1'),
    ('abcd-abcd-abcf', 'Sarah Thauheed', 'sarah@tsh.com.sg', '+6588888890', 'BU Manager', 'HQ', 'hashed_password_1'),
    ('abcd-abcd-abcg', 'Benedict Ting', 'bennett@tsh.com.sg', '+6588888891', 'Senior Manager', 'TOTAL', 'hashed_password_1'),
    ('abcd-abcd-abch', 'Zachary Tay', 'zachary@tsh.com.sg', '+6588888892', 'Accountant', NULL, 'hashed_password_1');

-- Insert notifications
INSERT INTO notification (employee_id, type, subject, body, is_read,created_at) VALUES 
    ('abcd-abcd-abcd', 'ALERT', 'Prediction for January Profit is more than 5% below Target', 'Predicted Profit: SGD1,000,000\\nTarget Profit: SGD2,000,000', FALSE, '2025-09-01 00:00:00'),
    ('abcd-abcd-abcd', 'ALERT', 'Budget for August 2025 has been exceeded.', 'Budget exceeded by 10%.', FALSE, '2025-09-01 00:00:00'),
    ('abcd-abcd-abcd', 'ALERT', 'Budget for October 2025 is in the red.', 'Budget deficit of 5%.', FALSE,'2025-09-30 00:00:00'),
    ('abcd-abcd-abcd', 'ALERT', 'Budget for September 2025 has been exceeded.', 'Budget exceeded by 15%.', FALSE, '2025-09-30 00:00:00'),
    ('abcd-abcd-abcd', 'ALERT', 'Target for September 2025 is in the yellow.', 'Target at risk of not being met.', FALSE, '2025-08-31 00:00:00');

-- Insert P&L categories
-- INSERT INTO pnl_category (code, name, description, parent_code) VALUES
--     ('5000-0000', 'SALES REVENUE', '', NULL),
--     ('5000-A000', 'ASSEMBLY','SALES REVENUE', '5000-0000'),
--     ('5000-A001', 'ASB SALES MODULE BB','SALES REVENUE/ASSEMBLY', '5000-A000'),
--     ('5000-M000', 'MACHINERY', 'SALES REVENUE', '5000-0000'),
--     ('5000-M001', 'MC SALES IN HOUSE  ( MIDA )', 'SALES REVENUE/MACHINERY', '5000-M000'),
--     ('5000-M002', 'MC SALES OUTSOURCE  ( MIDA )', 'SALES REVENUE/MACHINERY', '5000-M000'),
--     ('5500-0000', 'SALES RETURN/RETURN INWARD', '', NULL),
--     ('6000-0000', 'COST OF GOODS SOLD 1', '', NULL),
--     ('6001-0000', 'OPENING  STOCK', 'COST OF GOODS SOLD 1', '6000-0000'),
--     ('6002-A000', 'ASSEMBLY PURCHASES', 'COST OF GOODS SOLD 1', '6000-0000'),
--     ('6002-A001', 'ASB PUR WIREHANESS', 'COST OF GOODS SOLD 1/ASSEMBLY PURCHASES', '6002-A000'),
--     ('6002-A002', 'ASB PUR MODULE BB', 'COST OF GOODS SOLD 1/ASSEMBLY PURCHASES', '6002-A000'),
--     ('6003-0000', 'CLOSING STOCK', '', NULL),
--     ('6004-0000', 'COST OF GOODS SOLD 2', '', NULL),
--     ('6004-0001', 'PROD-LABOUR COSTS', 'COST OF GOODS SOLD 2', '6004-0000'),
--     ('6004-0002', 'PROD-WAGES & ALLOW', 'COST OF GOODS SOLD 2/PROD-LABOUR COSTS', '6004-0001'),
--     ('6004-0004', 'PROD-EPF', 'COST OF GOODS SOLD 2/PROD-LABOUR COSTS', '6004-0001'),
--     ('6004-0005', 'PROD-SOCSO', 'COST OF GOODS SOLD 2/PROD-LABOUR COSTS', '6004-0001'),
--     ('6005-0000', 'PROD-OVERHEADS', '', NULL),
--     ('6005-1000', 'PROD OVERHEAD 1', 'PROD-OVERHEADS', '6005-0000'),
--     ('6005-1001', 'MC PROD -SUB CONTRATOR', 'PROD-OVERHEADS/PROD OVERHEAD 1', '6005-1000'),
--     ('6005-1002', 'PROD-DEPRECIATION', 'PROD-OVERHEADS/PROD OVERHEAD 1', '6005-1000');

-- Insert P&L entries
-- INSERT INTO pnl_entry (pnl_code, business_unit, month, value) VALUES
--     ('5000-A001', 'BB1', '2025-08-01', 50000),
--     ('5000-M001', 'BB1', '2025-08-01', 20000),
--     ('5000-M002', 'BB1', '2025-08-01', 10000),
--     ('6004-0002', 'BB1', '2025-08-01', 5000),
--     ('6005-1001', 'BB1', '2025-08-01', 3000),
--     ('5000-A001', 'HQ', '2025-08-01', 80000),
--     ('5000-M001', 'HQ', '2025-08-01', 30000),
--     ('5000-M002', 'HQ', '2025-08-01', 20000),
--     ('6004-0002', 'HQ', '2025-08-01', 7000),
--     ('6005-1001', 'HQ', '2025-08-01', 4000),
--     ('5000-A001', 'BB1', '2025-09-01', 50000),
--     ('5000-M001', 'BB1', '2025-09-01', 20000),
--     ('5000-M002', 'BB1', '2025-09-01', 10000),
--     ('6004-0002', 'BB1', '2025-09-01', 5000),
--     ('6005-1001', 'BB1', '2025-09-01', 3000),
--     ('5000-A001', 'HQ', '2025-09-01', 80000),
--     ('5000-M001', 'HQ', '2025-09-01', 30000),
--     ('5000-M002', 'HQ', '2025-09-01', 20000),
--     ('6004-0002', 'HQ', '2025-09-01', 7000),
--     ('6005-1001', 'HQ', '2025-09-01', 4000),
--     ('5000-A001', 'BB1', '2025-07-01', 45000),
--     ('5000-A001', 'BB1', '2025-06-01', 40000),
--     ('5000-A001', 'BB1', '2025-05-01', 40000),
--     ('5000-A001', 'BB1', '2025-04-01', 48000),
--     ('5000-A001', 'BB1', '2025-03-01', 41000),
--     ('5000-A001', 'BB1', '2025-02-01', 39000),
--     ('5000-A001', 'BB1', '2025-01-01', 38000),
--     ('5000-A001', 'BB1', '2024-12-01', 43000),
--     ('5000-A001', 'BB1', '2024-11-01', 40000),
--     ('5000-A001', 'BB1', '2024-10-01', 41000),
--     ('5000-A001', 'BB1', '2024-09-01', 39000),
--     ('5000-A001', 'BB1', '2024-08-01', 38000),
--     ('5000-A001', 'BB1', '2024-07-01', 37000);

-- Insert P&L forecasts
-- INSERT INTO pnl_forecast (pnl_code, business_unit, month, value) VALUES
--     ('5000-A001', 'BB1', '2025-10-01', 55000),
--     ('5000-M001', 'BB1', '2025-10-01', 22000),
--     ('5000-M002', 'BB1', '2025-10-01', 11000),
--     ('6004-0002', 'BB1', '2025-10-01', 6000),
--     ('6005-1001', 'BB1', '2025-10-01', 3500),
--     ('5000-A001', 'HQ', '2025-10-01', 85000),
--     ('5000-M001', 'HQ', '2025-10-01', 32000),
--     ('5000-M002', 'HQ', '2025-10-01', 21000),
--     ('6004-0002', 'HQ', '2025-10-01', 7500),
--     ('6005-1001', 'HQ', '2025-10-01', 4500),
--     ('5000-A001', 'BB1', '2025-11-01', 55000),
--     ('5000-A001', 'BB1', '2025-12-01', 55000),
--     ('5000-A001', 'BB1', '2026-01-01', 55000),
--     ('5000-A001', 'BB1', '2026-02-01', 55000);

-- Insert KPI categories
INSERT INTO kpi_category (alias, name, category, description) VALUES
    ('PROF', 'Profit', 'PROFIT', 'Gross profit, summing sales income and subtracting cost of goods sold.'),
    ('GPM', 'Gross Profit Margin', 'PROFIT', 'Measures gross profit as a percentage of sales, showing how efficiently a company produces goods.'),
    ('OPM', 'Operating Profit Margin', 'PROFIT', 'Operating income as a percentage of sales, showing profitability after operating expenses.'),
    ('NPM', 'Net Profit Margin', 'PROFIT', 'Net income as a percentage of sales, showing overall profitability after all expenses, taxes, and interest.'),
    ('QR', 'Quick Ratio', 'PROFIT', 'Measures ability to meet short-term liabilities with liquid assets, excluding inventory.'),
    ('SALES', 'Sales', 'SALES', 'Total revenue from goods sold or services provided, including sales revenue and adjustments.'),
    ('ROS', 'Return On Sales', 'SALES', 'Another term for operating profit margin, evaluates operational efficiency relative to sales.'),
    ('DSO', 'Days Sales Outstanding', 'SALES', 'Currently incalculable'),
    ('RT', 'Receivables Turnover', 'SALES','Currently incalculable'),
    ('COST', 'Cost', 'COST','Total cost, summing cost of goods sold and operating expenses.'),
    ('COGSR', 'COGS Ratio', 'COST','Cost of goods sold as a percentage of sales, showing production cost efficiency.'),
    ('DPO', 'Days Payable Outstanding', 'COST','Currently incalculable'),
    ('OHR', 'Overhead Ratio', 'COST','Measures overhead (indirect costs) as a percentage of sales.');

-- Insert parameters
INSERT INTO parameter (employee_id, kpi_alias, month, value, is_notified) VALUES
    ('abcd-abcd-abcd', 'SALES', '2025-07-01', 40000, FALSE),
    ('abcd-abcd-abcd', 'COST', '2025-07-01', 20000, FALSE),
    ('abcd-abcd-abcd', 'SALES', '2025-09-15', 101, FALSE),
    ('abcd-abcd-abcd', 'COST', '2025-09-15', 102, FALSE),
    ('abcd-abcd-abcd', 'GPM', '2025-09-15', 0.11, FALSE),
    ('abcd-abcd-abcd', 'OPM', '2025-09-15', 0.12, FALSE),
    ('abcd-abcd-abcd', 'NPM', '2025-09-15', 0.13, FALSE),
    ('abcd-abcd-abcd', 'QR', '2025-09-15', 0.14, FALSE),
    ('abcd-abcd-abcd', 'ROS', '2025-09-15', 0.21, FALSE),
    ('abcd-abcd-abcd', 'DSO', '2025-09-15', 0.22, FALSE),
    ('abcd-abcd-abcd', 'RT', '2025-09-15', 0.23, FALSE),
    ('abcd-abcd-abcd', 'COGSR', '2025-09-15', 0.31, FALSE),
    ('abcd-abcd-abcd', 'DPO', '2025-09-15', 0.32, FALSE),
    ('abcd-abcd-abcd', 'OHR', '2025-09-15', 0.33, FALSE);

-- Insert KPIs
-- INSERT INTO kpi_entry (kpi_alias, business_unit, month, value) VALUES
--     ('GPM', 'BB1', '2025-08-01', 90.0),
--     ('OPM', 'BB1', '2025-08-01', 90.0),
--     ('NPM', 'BB1', '2025-08-01', 90.0),
--     ('QR', 'BB1', '2025-08-01', NULL),
--     ('ROS', 'BB1', '2025-08-01', 90.0),
--     ('DSO', 'BB1', '2025-08-01', NULL),
--     ('RT', 'BB1', '2025-08-01', NULL),
--     ('COGSR', 'BB1', '2025-08-01', 10.0),
--     ('DPO', 'BB1', '2025-08-01', NULL),
--     ('OHR', 'BB1', '2025-08-01', 10.0),
--     ('GPM', 'BB1', '2025-09-01', 90.5),
--     ('OPM', 'BB1', '2025-09-01', 91.2),
--     ('NPM', 'BB1', '2025-09-01', 90.3222),
--     ('QR', 'BB1', '2025-09-01', NULL),
--     ('ROS', 'BB1', '2025-09-01', 89.1111),
--     ('DSO', 'BB1', '2025-09-01', NULL),
--     ('RT', 'BB1', '2025-09-01', NULL),
--     ('COGSR', 'BB1', '2025-09-01', 11.2222),
--     ('DPO', 'BB1', '2025-09-01', NULL),
--     ('OHR', 'BB1', '2025-09-01', 9.0);

-- Insert KPI Forecasts
INSERT INTO kpi_entry (kpi_alias, business_unit, month, value) VALUES
    ('GPM', 'BB1', '2025-10-01', 90.0),
    ('OPM', 'BB1', '2025-10-01', 90.0),
    ('NPM', 'BB1', '2025-10-01', 90.0),
    ('QR', 'BB1', '2025-10-01', NULL),
    ('ROS', 'BB1', '2025-10-01', 90.0),
    ('DSO', 'BB1', '2025-10-01', NULL),
    ('RT', 'BB1', '2025-10-01', NULL),
    ('COGSR', 'BB1', '2025-10-01', 10.0),
    ('DPO', 'BB1', '2025-10-01', NULL),
    ('OHR', 'BB1', '2025-10-01', 10.0),
    ('GPM', 'BB1', '2025-11-01', 89.2045),
    ('OPM', 'BB1', '2025-11-01', 89.2045),
    ('NPM', 'BB1', '2025-11-01', 89.2045),
    ('QR', 'BB1', '2025-11-01', NULL),
    ('ROS', 'BB1', '2025-11-01', 89.2045),
    ('DSO', 'BB1', '2025-11-01', NULL),
    ('RT', 'BB1', '2025-11-01', NULL),
    ('COGSR', 'BB1', '2025-11-01', 10.7955),
    ('DPO', 'BB1', '2025-11-01', NULL),
    ('OHR', 'BB1', '2025-11-01', 10.75);
-- Insert business units
INSERT INTO business_unit (alias, name) VALUES
    ('BB1', 'Box Build 1'),
    ('BBS2', 'Box Build 2'),
    ('HQ', 'Headquarters'),
    ('LOG', 'Logistics'),
    ('MCE', 'Mechanical Engineering');

-- Insert employees
INSERT INTO employee (id, name, email, role, business_unit, password_hash) VALUES
    ('abcd-abcd-abcd', 'Jakob Lie', 'jakob@tsh.com.sg', 'BU Manager', 'BB1', 'hashed_password_1'),
    ('abcd-abcd-abce', 'Jeremy Lin Kairui son of Lin Chee', 'jeremy@tsh.com.sg', 'BU Manager', 'MCE', 'hashed_password_1'),
    ('abcd-abcd-abcf', 'Sarah Thauheed', 'sarah@tsh.com.sg', 'BU Manager', 'HQ', 'hashed_password_1'),
    ('abcd-abcd-abcg', 'Benedict Ting', 'bennett@tsh.com.sg', 'Senior Manager', NULL, 'hashed_password_1'),
    ('abcd-abcd-abch', 'Zachary Tay', 'zachary@tsh.com.sg', 'Accountant', NULL, 'hashed_password_1');

-- Insert parameters
INSERT INTO parameter (employee_id, name, created_date, value, is_notified) VALUES
    ('abcd-abcd-abcd', 'Sales Target', '2025-07-01', 40000, FALSE),
    ('abcd-abcd-abcd', 'Cost Budget', '2025-07-01', 20000, FALSE),
    ('abcd-abcd-abcd', 'Sales Target', '2025-09-15', 101, FALSE),
    ('abcd-abcd-abcd', 'Cost Budget', '2025-09-15', 102, FALSE),
    ('abcd-abcd-abcd', 'Gross Profit Margin', '2025-09-15', 0.11, FALSE),
    ('abcd-abcd-abcd', 'Operating Profit Margin', '2025-09-15', 0.12, FALSE),
    ('abcd-abcd-abcd', 'Net Profit Margin', '2025-09-15', 0.13, FALSE),
    ('abcd-abcd-abcd', 'Quick Ratio', '2025-09-15', 0.14, FALSE),
    ('abcd-abcd-abcd', 'Return On Sales', '2025-09-15', 0.21, FALSE),
    ('abcd-abcd-abcd', 'Days Sales Outstanding', '2025-09-15', 0.22, FALSE),
    ('abcd-abcd-abcd', 'Receivables Turnover', '2025-09-15', 0.23, FALSE),
    ('abcd-abcd-abcd', 'Cost Of Goods Sold Ratio', '2025-09-15', 0.31, FALSE),
    ('abcd-abcd-abcd', 'Days Payable Outstanding', '2025-09-15', 0.32, FALSE),
    ('abcd-abcd-abcd', 'Overhead Ratio', '2025-09-15', 0.33, FALSE);

-- Insert notifications
INSERT INTO notification (employee_id, type, subject, body, is_read,created_at) VALUES 
    ('abcd-abcd-abcd', 'ALERT', 'Prediction for January Profit is more than 5% below Target', 'Predicted Profit: SGD1,000,000\\nTarget Profit: SGD2,000,000', FALSE, '2025-09-01 00:00:00'),
    ('abcd-abcd-abcd', 'ALERT', 'Budget for August 2025 has been exceeded.', 'Budget exceeded by 10%.', FALSE, '2025-09-01 00:00:00'),
    ('abcd-abcd-abcd', 'ALERT', 'Budget for October 2025 is in the red.', 'Budget deficit of 5%.', FALSE,'2025-09-30 00:00:00'),
    ('abcd-abcd-abcd', 'ALERT', 'Budget for September 2025 has been exceeded.', 'Budget exceeded by 15%.', FALSE, '2025-09-30 00:00:00'),
    ('abcd-abcd-abcd', 'ALERT', 'Target for September 2025 is in the yellow.', 'Target at risk of not being met.', FALSE, '2025-08-31 00:00:00');

-- Insert P&L categories
INSERT INTO pnl_category (code, name, description) VALUES
    ('5000-0000', 'SALES REVENUE', ''),
    ('5000-A000', 'ASSEMBLY','SALES REVENUE'),
    ('5000-A001', 'ASB SALES MODULE BB','SALES REVENUE/ASSEMBLY'),
    ('5000-M000', 'MACHINERY', 'SALES REVENUE'),
    ('5000-M001', 'MC SALES IN HOUSE  ( MIDA )', 'SALES REVENUE/MACHINERY'),
    ('5000-M002', 'MC SALES OUTSOURCE  ( MIDA )', 'SALES REVENUE/MACHINERY'),
    ('5500-0000', 'SALES RETURN/RETURN INWARD', ''),
    ('6000-0000', 'COST OF GOODS SOLD 1', ''),
    ('6001-0000', 'OPENING  STOCK', 'COST OF GOODS SOLD 1'),
    ('6002-A000', 'ASSEMBLY PURCHASES', 'COST OF GOODS SOLD 1'),
    ('6002-A001', 'ASB PUR WIREHANESS', 'COST OF GOODS SOLD 1/ASSEMBLY PURCHASES'),
    ('6002-A002', 'ASB PUR MODULE BB', 'COST OF GOODS SOLD 1/ASSEMBLY PURCHASES'),
    ('6003-0000', 'CLOSING STOCK', ''),
    ('6004-0000', 'COST OF GOODS SOLD 2', ''),
    ('6004-0001', 'PROD-LABOUR COSTS', 'COST OF GOODS SOLD 2'),
    ('6004-0002', 'PROD-WAGES & ALLOW', 'COST OF GOODS SOLD 2/PROD-LABOUR COSTS'),
    ('6004-0004', 'PROD-EPF', 'COST OF GOODS SOLD 2/PROD-LABOUR COSTS'),
    ('6004-0005', 'PROD-SOCSO', 'COST OF GOODS SOLD 2/PROD-LABOUR COSTS'),
    ('6005-0000', 'PROD-OVERHEADS', ''),
    ('6005-1000', 'PROD OVERHEAD 1', 'PROD-OVERHEADS'),
    ('6005-1001', 'MC PROD -SUB CONTRATOR', 'PROD-OVERHEADS/PROD OVERHEAD 1'),
    ('6005-1002', 'PROD-DEPRECIATION', 'PROD-OVERHEADS/PROD OVERHEAD 1');
    
-- Insert P&L entries
INSERT INTO pnl_entry (pnl_code, business_unit, month, value) VALUES
    ('5000-A001', 'BB1', '2025-08-01', 50000),
    ('5000-M001', 'BB1', '2025-08-01', 20000),
    ('5000-M002', 'BB1', '2025-08-01', 10000),
    ('6004-0002', 'BB1', '2025-08-01', 5000),
    ('6005-1001', 'BB1', '2025-08-01', 3000),
    ('5000-A001', 'HQ', '2025-08-01', 80000),
    ('5000-M001', 'HQ', '2025-08-01', 30000),
    ('5000-M002', 'HQ', '2025-08-01', 20000),
    ('6004-0002', 'HQ', '2025-08-01', 7000),
    ('6005-1001', 'HQ', '2025-08-01', 4000),
    ('5000-A001', 'BB1', '2025-09-01', 50000),
    ('5000-M001', 'BB1', '2025-09-01', 20000),
    ('5000-M002', 'BB1', '2025-09-01', 10000),
    ('6004-0002', 'BB1', '2025-09-01', 5000),
    ('6005-1001', 'BB1', '2025-09-01', 3000),
    ('5000-A001', 'HQ', '2025-09-01', 80000),
    ('5000-M001', 'HQ', '2025-09-01', 30000),
    ('5000-M002', 'HQ', '2025-09-01', 20000),
    ('6004-0002', 'HQ', '2025-09-01', 7000),
    ('6005-1001', 'HQ', '2025-09-01', 4000);

-- Insert P&L forecasts
INSERT INTO pnl_forecast (pnl_code, business_unit, month, value) VALUES
    ('5000-A001', 'BB1', '2025-10-01', 55000),
    ('5000-M001', 'BB1', '2025-10-01', 22000),
    ('5000-M002', 'BB1', '2025-10-01', 11000),
    ('6004-0002', 'BB1', '2025-10-01', 6000),
    ('6005-1001', 'BB1', '2025-10-01', 3500),
    ('5000-A001', 'HQ', '2025-10-01', 85000),
    ('5000-M001', 'HQ', '2025-10-01', 32000),
    ('5000-M002', 'HQ', '2025-10-01', 21000),
    ('6004-0002', 'HQ', '2025-10-01', 7500),
    ('6005-1001', 'HQ', '2025-10-01', 4500);
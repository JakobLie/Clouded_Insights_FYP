-- Insert business units
INSERT INTO business_unit (alias, name) VALUES
    ('BB1', 'Box Build 1'),
    ('BBS2', 'Box Build 2'),
    ('HQ', 'Headquarters'),
    ('LOG', 'Logistics'),
    ('MCE', 'Mechanical Engineering');

-- Insert employees
INSERT INTO employee (id, name, email, role, business_unit, password_hash) VALUES
    ('abcd-abcd-abcd', 'Jakob Lie', 'jakob@tsh.com.sg', 'Senior Manager', NULL, 'hashed_password_1'),
    ('abcd-abcd-abce', 'Jeremy Lin Kairui son of Lin Chee', 'jeremy@tsh.com.sg', 'BU Manager', 'BB1', 'hashed_password_1'),
    ('abcd-abcd-abcf', 'Sarah Thauheed', 'sarah@tsh.com.sg', 'BU Manager', 'HQ', 'hashed_password_1'),
    ('abcd-abcd-abcg', 'Benedict Ting', 'bennett@tsh.com.sg', 'BU Manager', 'MCE', 'hashed_password_1'),
    ('abcd-abcd-abch', 'Zachary Tay', 'zachary@tsh.com.sg', 'Accountant', NULL, 'hashed_password_1');

-- Insert parameters
INSERT INTO parameter (employee_id, name, value, is_notified) VALUES
    ('abcd-abcd-abcd', 'Target', 40000, FALSE),
    ('abcd-abcd-abcd', 'Budget', 20000, FALSE);

-- Insert notifications
INSERT INTO notification (employee_id, message, is_read,created_at) VALUES 
    ('abcd-abcd-abcd', 'Budget for August 2025 has been exceeded.', FALSE, '2025-09-01 00:00:00'),
    ('abcd-abcd-abcd', 'Budget for October 2025 is in the red.', FALSE,'2025-09-30 00:00:00'),
    ('abcd-abcd-abcd', 'Budget for September 2025 has been exceeded.', FALSE, '2025-09-30 00:00:00'),
    ('abcd-abcd-abcd', 'Target for September 2025 is in the yellow.', FALSE, '2025-08-31 00:00:00');

-- Insert P&L categories
INSERT INTO pnl_category (code, name, category) VALUES
    ('5000-A001', 'Revenue', 'Income'),
    ('5000-A002', 'Cost of Goods Sold', 'Expense'),
    ('5000-A003', 'Salaries', 'Expense'),
    ('5000-A004', 'Marketing', 'Expense'),
    ('5000-A005', 'Research and Development', 'Expense');

-- Insert P&L entries
INSERT INTO pnl_entry (pnl_code, business_unit, month, value) VALUES
    ('5000-A001', 'BB1', '2025-08-01', 50000),
    ('5000-A002', 'BB1', '2025-08-01', 20000),
    ('5000-A003', 'BB1', '2025-08-01', 10000),
    ('5000-A004', 'BB1', '2025-08-01', 5000),
    ('5000-A005', 'BB1', '2025-08-01', 3000),
    ('5000-A001', 'HQ', '2025-08-01', 80000),
    ('5000-A002', 'HQ', '2025-08-01', 30000),
    ('5000-A003', 'HQ', '2025-08-01', 20000),
    ('5000-A004', 'HQ', '2025-08-01', 7000),
    ('5000-A005', 'HQ', '2025-08-01', 4000),
    ('5000-A001', 'BB1', '2025-09-01', 50000),
    ('5000-A002', 'BB1', '2025-09-01', 20000),
    ('5000-A003', 'BB1', '2025-09-01', 10000),
    ('5000-A004', 'BB1', '2025-09-01', 5000),
    ('5000-A005', 'BB1', '2025-09-01', 3000),
    ('5000-A001', 'HQ', '2025-09-01', 80000),
    ('5000-A002', 'HQ', '2025-09-01', 30000),
    ('5000-A003', 'HQ', '2025-09-01', 20000),
    ('5000-A004', 'HQ', '2025-09-01', 7000),
    ('5000-A005', 'HQ', '2025-09-01', 4000);

-- Insert P&L forecasts
INSERT INTO pnl_forecast (pnl_code, business_unit, month, value, created_at) VALUES
    ('5000-A001', 'BB1', '2025-10-01', 55000, '2025-09-30 00:00:00'),
    ('5000-A002', 'BB1', '2025-10-01', 22000, '2025-09-30 00:00:00'),
    ('5000-A003', 'BB1', '2025-10-01', 11000, '2025-09-30 00:00:00'),
    ('5000-A004', 'BB1', '2025-10-01', 6000, '2025-09-30 00:00:00'),
    ('5000-A005', 'BB1', '2025-10-01', 3500, '2025-09-30 00:00:00'),
    ('5000-A001', 'HQ', '2025-10-01', 85000, '2025-09-30 00:00:00'),
    ('5000-A002', 'HQ', '2025-10-01', 32000, '2025-09-30 00:00:00'),
    ('5000-A003', 'HQ', '2025-10-01', 21000, '2025-09-30 00:00:00'),
    ('5000-A004', 'HQ', '2025-10-01', 7500, '2025-09-30 00:00:00'),
    ('5000-A005', 'HQ', '2025-10-01', 4500, '2025-09-30 00:00:00');
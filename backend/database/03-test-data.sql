/* TEST INSERT STATEMENTS */

-- Insert employees
INSERT INTO employee (id, name, email, phone_number, role, business_unit, password_hash) VALUES
    ('abcd-abcd-abcd', 'Jakob Lie', 'jakob.lie.2022@scis.smu.edu.sg', '+6583885396', 'BU Manager', 'BB1', 'password'),
    ('abcd-abcd-abce', 'Jeremy Lin Kairui son of Lin Chee', 'jeremylin.2022@scis.smu.edu.sg', '+6596694584', 'BU Manager', 'MCE', 'hashed_password_1'),
    ('abcd-abcd-abcf', 'Sarah Thauheed', 'sthauheed.2022@scis.smu.edu.sg', '+6582689919', 'BU Manager', 'HQ', 'hashed_password_1'),
    ('abcd-abcd-abcg', 'Benedict Ting', NULL, NULL, 'Senior Manager', 'TOTAL', 'hashed_password_1'),
    ('abcd-abcd-abch', 'Zachary Tay', NULL, NULL, 'Accountant', 'TOTAL', 'hashed_password_1');

-- Insert notifications
INSERT INTO notification (employee_id, type, subject, body, is_read,created_at) VALUES 
    ('abcd-abcd-abcd', 'ALERT', 'Prediction for January Profit is more than 5% below Target', 'Predicted Profit: SGD1,000,000\\nTarget Profit: SGD2,000,000', FALSE, '2025-09-01 00:00:00'),
    ('abcd-abcd-abcd', 'ALERT', 'Budget for August 2025 has been exceeded.', 'Budget exceeded by 10%.', FALSE, '2025-09-01 00:00:00'),
    ('abcd-abcd-abcd', 'ALERT', 'Budget for October 2025 is in the red.', 'Budget deficit of 5%.', FALSE,'2025-09-30 00:00:00'),
    ('abcd-abcd-abcd', 'ALERT', 'Budget for September 2025 has been exceeded.', 'Budget exceeded by 15%.', FALSE, '2025-09-30 00:00:00'),
    ('abcd-abcd-abcd', 'ALERT', 'Target for September 2025 is in the yellow.', 'Target at risk of not being met.', FALSE, '2025-08-31 00:00:00');

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
    ('abcd-abcd-abcd', 'OHR', '2025-09-15', 0.33, FALSE),
    ('abcd-abcd-abce', 'SALES', '2025-07-01', 40000, FALSE),
    ('abcd-abcd-abce', 'COST', '2025-07-01', 20000, FALSE),
    ('abcd-abcd-abce', 'SALES', '2025-09-15', 101, FALSE),
    ('abcd-abcd-abce', 'COST', '2025-09-15', 102, FALSE),
    ('abcd-abcd-abce', 'GPM', '2025-09-15', 0.11, FALSE),
    ('abcd-abcd-abce', 'OPM', '2025-09-15', 0.12, FALSE),
    ('abcd-abcd-abce', 'NPM', '2025-09-15', 0.13, FALSE),
    ('abcd-abcd-abce', 'QR', '2025-09-15', 0.14, FALSE),
    ('abcd-abcd-abce', 'ROS', '2025-09-15', 0.21, FALSE),
    ('abcd-abcd-abce', 'DSO', '2025-09-15', 0.22, FALSE),
    ('abcd-abcd-abce', 'RT', '2025-09-15', 0.23, FALSE),
    ('abcd-abcd-abce', 'COGSR', '2025-09-15', 0.31, FALSE),
    ('abcd-abcd-abce', 'DPO', '2025-09-15', 0.32, FALSE),
    ('abcd-abcd-abce', 'OHR', '2025-09-15', 0.33, FALSE);

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
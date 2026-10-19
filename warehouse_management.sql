-- Create the database
CREATE DATABASE IF NOT EXISTS warehouse_management;
USE warehouse_management;

-- Create the database
CREATE DATABASE IF NOT EXISTS warehouse_management;
USE warehouse_management;

-- Categories
CREATE TABLE Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Descriptions
CREATE TABLE Descriptions (
    description_id INT AUTO_INCREMENT PRIMARY KEY,
    details TEXT NOT NULL
);

-- Prices
CREATE TABLE Prices (
    price_id INT AUTO_INCREMENT PRIMARY KEY,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(10) NOT NULL
);

-- Products
CREATE TABLE Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category_id INT,
    description_id INT,
    price_id INT,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id),
    FOREIGN KEY (description_id) REFERENCES Descriptions(description_id),
    FOREIGN KEY (price_id) REFERENCES Prices(price_id)
);

-- Warehouses
CREATE TABLE Warehouses (
    warehouse_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL
);

-- Locations
CREATE TABLE Locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    warehouse_id INT,
    name VARCHAR(100) NOT NULL,
    FOREIGN KEY (warehouse_id) REFERENCES Warehouses(warehouse_id)
);

-- Stock
CREATE TABLE Stock (
    stock_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    warehouse_id INT,
    location_id INT,
    quantity INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (warehouse_id) REFERENCES Warehouses(warehouse_id),
    FOREIGN KEY (location_id) REFERENCES Locations(location_id)
);

-- Suppliers
CREATE TABLE Suppliers (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_info VARCHAR(255)
);

-- Orders
CREATE TABLE Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT,
    order_date DATE NOT NULL,
    status VARCHAR(50),
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
);

-- OrderDetails
CREATE TABLE OrderDetails (
    order_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Deliveries
CREATE TABLE Deliveries (
    delivery_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    delivery_date DATE,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

-- Payments
CREATE TABLE Payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    amount DECIMAL(10, 2),
    method VARCHAR(50),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

-- Invoices
CREATE TABLE Invoices (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    total_amount DECIMAL(10, 2),
    due_date DATE,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

-- Employees
CREATE TABLE Employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50),
    warehouse_id INT,
    FOREIGN KEY (warehouse_id) REFERENCES Warehouses(warehouse_id)
);

-- Transfers
CREATE TABLE Transfers (
    transfer_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    from_location INT,
    to_location INT,
    quantity INT,
    transfer_date DATE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (from_location) REFERENCES Locations(location_id),
    FOREIGN KEY (to_location) REFERENCES Locations(location_id)
);

-- Logs
CREATE TABLE Logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    action TEXT,
    log_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

-- Alerts
CREATE TABLE Alerts (
    alert_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    warehouse_id INT,
    message TEXT,
    alert_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (warehouse_id) REFERENCES Warehouses(warehouse_id)
);

-- Notifications
CREATE TABLE Notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    alert_id INT,
    employee_id INT,
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (alert_id) REFERENCES Alerts(alert_id),
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

-- Reports
CREATE TABLE Reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    report_type VARCHAR(100),
    created_by INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES Employees(employee_id)
);

-- History
CREATE TABLE History (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    action TEXT,
    action_date DATE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Users table for login


-- Sample login user
INSERT INTO tbuser (username, password) VALUES ('admin', 'admin123');
INSERT INTO tbuser (username, password) VALUES ('admin', 'admin123');


-- Categories
INSERT INTO Categories (name) VALUES 
('Electronics'), 
('Furniture'), 
('Pharmaceuticals');

-- Descriptions
INSERT INTO Descriptions (details) VALUES 
('Smartphone device'), 
('Office chair'), 
('COVID-19 vaccine');

-- Prices
INSERT INTO Prices (amount, currency) VALUES 
(699.99, 'USD'), 
(120.00, 'USD'), 
(15.00, 'USD');

-- Products
INSERT INTO Products (name, category_id, description_id, price_id) VALUES 
('iPhone 13', 1, 1, 1),
('Ergonomic Chair', 2, 2, 2),
('Pfizer Vaccine', 3, 3, 3);

-- Warehouses
INSERT INTO Warehouses (name, address) VALUES 
('Central Warehouse', '123 Main St'),
('North Depot', '456 North Ave');

-- Locations
INSERT INTO Locations (warehouse_id, name) VALUES 
(1, 'Aisle 1'),
(1, 'Aisle 2'),
(2, 'Cold Storage');

-- Stock
INSERT INTO Stock (product_id, warehouse_id, location_id, quantity) VALUES 
(1, 1, 1, 15),
(2, 1, 2, 5),
(3, 2, 3, 50);

-- Suppliers
INSERT INTO Suppliers (name, contact_info) VALUES 
('TechWorld Inc.', 'tech@world.com'),
('Office Supplies Co.', 'contact@officeco.com'),
('HealthPlus Pharma', 'support@healthplus.com');

-- Orders
INSERT INTO Orders (supplier_id, order_date, status) VALUES 
(1, '2024-05-01', 'Pending'),
(2, '2024-05-03', 'Completed'),
(3, '2024-05-04', 'Shipped');

-- OrderDetails
INSERT INTO OrderDetails (order_id, product_id, quantity) VALUES 
(1, 1, 10),
(2, 2, 3),
(3, 3, 20);

-- Deliveries
INSERT INTO Deliveries (order_id, delivery_date) VALUES 
(2, '2024-05-05'),
(3, '2024-05-06');

-- Payments
INSERT INTO Payments (order_id, amount, method) VALUES 
(2, 360.00, 'Credit Card'),
(3, 300.00, 'Bank Transfer');

-- Invoices
INSERT INTO Invoices (order_id, total_amount, due_date) VALUES 
(1, 6999.90, '2024-06-01'),
(3, 300.00, '2024-06-10');

-- Employees
INSERT INTO Employees (name, role, warehouse_id) VALUES 
('Alice Johnson', 'Manager', 1),
('Bob Smith', 'Worker', 2);

-- Transfers
INSERT INTO Transfers (product_id, from_location, to_location, quantity, transfer_date) VALUES 
(1, 1, 2, 5, '2024-05-07'),
(3, 3, 1, 10, '2024-05-08');

-- Logs
INSERT INTO Logs (employee_id, action, log_time) VALUES 
(1, 'Updated stock records', NOW()),
(2, 'Transferred items', NOW());

-- Alerts
INSERT INTO Alerts (product_id, warehouse_id, message, alert_date) VALUES 
(2, 1, 'Low stock alert: Ergonomic Chair', NOW());

-- Notifications
INSERT INTO Notifications (alert_id, employee_id, sent_at) VALUES 
(1, 1, NOW());

-- Reports
INSERT INTO Reports (report_type, created_by, created_at) VALUES 
('Inventory Summary', 1, NOW()),
('Order Analysis', 2, NOW());

-- History
INSERT INTO History (product_id, action, action_date) VALUES 
(1, 'Created product', '2024-04-01'),
(2, 'Stock updated', '2024-05-02');

-- tbuser (login)
INSERT INTO tbuser (username, password) VALUES 
('admin', 'admin123');




DELIMITER //

CREATE PROCEDURE GetLowStockItems(IN threshold INT)
BEGIN
    SELECT 
        p.name AS product_name,
        w.name AS warehouse,
        l.name AS location,
        s.quantity
    FROM Stock s
    JOIN Products p ON s.product_id = p.product_id
    JOIN Warehouses w ON s.warehouse_id = w.warehouse_id
    JOIN Locations l ON s.location_id = l.location_id
    WHERE s.quantity < threshold;
END //

DELIMITER ;



DELIMITER //

CREATE PROCEDURE GetSupplierOrders(IN supplierName VARCHAR(100))
BEGIN
    SELECT 
        o.order_id,
        o.order_date,
        o.status,
        p.name AS product_name,
        od.quantity
    FROM Orders o
    JOIN Suppliers s ON o.supplier_id = s.supplier_id
    JOIN OrderDetails od ON o.order_id = od.order_id
    JOIN Products p ON od.product_id = p.product_id
    WHERE s.name = supplierName
    ORDER BY o.order_date DESC;
END //

DELIMITER ;



DELIMITER //

CREATE PROCEDURE AddProduct(
    IN productName VARCHAR(100),
    IN categoryId INT,
    IN descriptionId INT,
    IN priceId INT
)
BEGIN
    INSERT INTO Products (name, category_id, description_id, price_id)
    VALUES (productName, categoryId, descriptionId, priceId);
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE UpdateStock(
    IN p_ProductID INT,
    IN p_WarehouseID INT,
    IN p_LocationID INT,
    IN p_Quantity INT
)
BEGIN
    DECLARE currentQty INT;

    SELECT quantity INTO currentQty
    FROM Stock
    WHERE product_id = p_ProductID AND warehouse_id = p_WarehouseID AND location_id = p_LocationID;

    IF currentQty IS NULL THEN
        INSERT INTO Stock (product_id, warehouse_id, location_id, quantity)
        VALUES (p_ProductID, p_WarehouseID, p_LocationID, p_Quantity);
    ELSE
        UPDATE Stock
        SET quantity = p_Quantity
        WHERE product_id = p_ProductID AND warehouse_id = p_WarehouseID AND location_id = p_LocationID;
    END IF;
END //

DELIMITER ;



DELIMITER //

CREATE PROCEDURE TransferStock(
    IN p_ProductID INT,
    IN p_FromLocationID INT,
    IN p_ToLocationID INT,
    IN p_Quantity INT
)
BEGIN
    DECLARE currentQty INT;

    -- Get current quantity at source
    SELECT quantity INTO currentQty
    FROM Stock
    WHERE product_id = p_ProductID AND location_id = p_FromLocationID;

    -- Ensure enough stock exists
    IF currentQty IS NULL OR currentQty < p_Quantity THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Not enough stock in source location.';
    ELSE
        -- Decrease from source
        UPDATE Stock
        SET quantity = quantity - p_Quantity
        WHERE product_id = p_ProductID AND location_id = p_FromLocationID;

        -- Add to destination (or insert if missing)
        INSERT INTO Stock (product_id, warehouse_id, location_id, quantity)
        SELECT p_ProductID, warehouse_id, p_ToLocationID, p_Quantity
        FROM Locations
        WHERE location_id = p_ToLocationID
        ON DUPLICATE KEY UPDATE quantity = quantity + p_Quantity;
    END IF;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE TransferStock(
    IN p_ProductID INT,
    IN p_FromLocationID INT,
    IN p_ToLocationID INT,
    IN p_Quantity INT
)
BEGIN
    DECLARE currentQty INT;

    -- Get current quantity at source
    SELECT quantity INTO currentQty
    FROM Stock
    WHERE product_id = p_ProductID AND location_id = p_FromLocationID;

    -- Ensure enough stock exists
    IF currentQty IS NULL OR currentQty < p_Quantity THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Not enough stock in source location.';
    ELSE
        -- Decrease from source
        UPDATE Stock
        SET quantity = quantity - p_Quantity
        WHERE product_id = p_ProductID AND location_id = p_FromLocationID;

        -- Add to destination (or insert if missing)
        INSERT INTO Stock (product_id, warehouse_id, location_id, quantity)
        SELECT p_ProductID, warehouse_id, p_ToLocationID, p_Quantity
        FROM Locations
        WHERE location_id = p_ToLocationID
        ON DUPLICATE KEY UPDATE quantity = quantity + p_Quantity;
    END IF;
END //

DELIMITER ;


SHOW TABLES;
SELECT * FROM tbuser;


-- View login users
SELECT * FROM tbuser;

-- View all categories
SELECT * FROM Categories;

-- View all descriptions
SELECT * FROM Descriptions;

-- View all prices
SELECT * FROM Prices;

-- View all products
SELECT * FROM Products;

-- View all warehouses
SELECT * FROM Warehouses;

-- View all locations
SELECT * FROM Locations;

-- View stock levels
SELECT * FROM Stock;

-- View suppliers
SELECT * FROM Suppliers;

-- View orders
SELECT * FROM Orders;

-- View order details
SELECT * FROM OrderDetails;

-- View deliveries
SELECT * FROM Deliveries;

-- View payments
SELECT * FROM Payments;

-- View invoices
SELECT * FROM Invoices;

-- View employees
SELECT * FROM Employees;

-- View transfers
SELECT * FROM Transfers;

-- View logs
SELECT * FROM Logs;

-- View alerts
SELECT * FROM Alerts;

-- View notifications
SELECT * FROM Notifications;

-- View reports
SELECT * FROM Reports;

-- View history
SELECT * FROM History;



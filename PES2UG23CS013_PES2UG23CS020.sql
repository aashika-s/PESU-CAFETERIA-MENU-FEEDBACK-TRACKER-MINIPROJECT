-- CREATE DATABASE IF NOT EXISTS cafeteria_db;
-- USE cafeteria_db;

-- -- Drop in dependency order
-- SET FOREIGN_KEY_CHECKS = 0;
-- SET FOREIGN_KEY_CHECKS = 1;

-- -- 1. Student
-- CREATE TABLE Student (
--   SRN VARCHAR(15) PRIMARY KEY,
--   Name VARCHAR(100) NOT NULL,
--   Email VARCHAR(150) NOT NULL UNIQUE,
--   Phone VARCHAR(20),
--   CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
-- ) ;


-- -- 2. Staff
-- CREATE TABLE Staff (
--   StaffID INT AUTO_INCREMENT PRIMARY KEY,
--   Name VARCHAR(100) NOT NULL,
--   Email VARCHAR(150) NOT NULL UNIQUE,
--   Role VARCHAR(50) NOT NULL DEFAULT 'Staff',
--   CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
-- ) ;

-- -- 3. FoodItem
-- CREATE TABLE FoodItem (
--   ItemID INT AUTO_INCREMENT PRIMARY KEY,
--   ItemName VARCHAR(100) NOT NULL,
--   Category VARCHAR(50) DEFAULT 'Snack',
--   Price DECIMAL(7,2) NOT NULL CHECK (Price >= 0),
--   IsActive TINYINT(1) NOT NULL DEFAULT 1
-- );

-- -- 4. Menu
-- CREATE TABLE Menu (
--   MenuID INT AUTO_INCREMENT PRIMARY KEY,
--   MenuDate DATE NOT NULL,
--   StaffID INT NULL,
--   Notes VARCHAR(255),
--   CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
--   CONSTRAINT fk_menu_staff FOREIGN KEY (StaffID)
--     REFERENCES Staff(StaffID)
--     ON DELETE SET NULL
--     ON UPDATE CASCADE
-- ) ;

-- -- 5. MenuFood (Menu ↔ FoodItem M:N)
-- CREATE TABLE MenuFood (
--   MenuID INT NOT NULL,
--   ItemID INT NOT NULL,
--   PRIMARY KEY (MenuID, ItemID),
--   CONSTRAINT fk_mf_menu FOREIGN KEY (MenuID)
--     REFERENCES Menu(MenuID)
--     ON DELETE CASCADE
--     ON UPDATE CASCADE,
--   CONSTRAINT fk_mf_item FOREIGN KEY (ItemID)
--     REFERENCES FoodItem(ItemID)
--     ON DELETE CASCADE
--     ON UPDATE CASCADE
-- ) ;

-- -- 6. Orders (safe FK name)
-- CREATE TABLE Orders (
--   OrderID INT AUTO_INCREMENT PRIMARY KEY,
--   SRN VARCHAR(15),
--   OrderDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   Status VARCHAR(30) NOT NULL DEFAULT 'Placed',
--   CONSTRAINT fk_orders_student FOREIGN KEY (SRN)
--     REFERENCES Student(SRN)
--     ON DELETE SET NULL
--     ON UPDATE CASCADE
-- ) ;

-- -- 7. Order_Items (safe FK names)
-- CREATE TABLE Order_Items (
--   OrderID INT NOT NULL,
--   ItemID INT NOT NULL,
--   Quantity INT NOT NULL DEFAULT 1 CHECK (Quantity > 0),
--   PRIMARY KEY (OrderID, ItemID),
--   CONSTRAINT fk_orderitems_orders FOREIGN KEY (OrderID)
--     REFERENCES Orders(OrderID)
--     ON DELETE CASCADE
--     ON UPDATE CASCADE,
--   CONSTRAINT fk_orderitems_fooditem FOREIGN KEY (ItemID)
--     REFERENCES FoodItem(ItemID)
--     ON DELETE CASCADE
--     ON UPDATE CASCADE
-- ) ;

-- -- 8. Review
-- CREATE TABLE Review (
--   ReviewID INT AUTO_INCREMENT PRIMARY KEY,
--   SRN VARCHAR(15),
--   ItemID INT NOT NULL,
--   Rating TINYINT NOT NULL CHECK (Rating BETWEEN 1 AND 5),
--   Feedback VARCHAR(500),
--   ReviewDate DATETIME DEFAULT CURRENT_TIMESTAMP,
--   CONSTRAINT fk_review_student FOREIGN KEY (SRN)
--     REFERENCES Student(SRN)
--     ON DELETE SET NULL
--     ON UPDATE CASCADE,
--   CONSTRAINT fk_review_item FOREIGN KEY (ItemID)
--     REFERENCES FoodItem(ItemID)
--     ON DELETE CASCADE
--     ON UPDATE CASCADE
-- );

-- -- ==============================
-- -- DML: Insert sample data
-- -- ==============================

-- INSERT INTO Student (SRN, Name, Email, Phone) VALUES
-- ('PESU2021001','Asha Kumar','asha.kumar@pes.edu','+91-9876543210'),
-- ('PESU2021002','Rohit Sharma','rohit.sharma@pes.edu','+91-9123456780'),
-- ('PESU2021003','Meera Nair','meera.nair@pes.edu','+91-9988776655'),
-- ('PESU2021004','Karan Gupta','karan.gupta@pes.edu','+91-9012345678'),
-- ('PESU2021005','Sara Iyer','sara.iyer@pes.edu','+91-9034567890');

-- INSERT INTO Staff (Name, Email, Role) VALUES
-- ('Suresh Rao','suresh.rao@pes.edu','Manager'),
-- ('Rekha Devi','rekha.devi@pes.edu','Chef'),
-- ('Manoj Kumar','manoj.kumar@pes.edu','Cashier'),
-- ('Anita Fernandes','anita.fernandes@pes.edu','Supervisor'),
-- ('Vikram Singh','vikram.singh@pes.edu','Chef');

-- INSERT INTO FoodItem (ItemName, Category, Price) VALUES
-- ('Masala Dosa','Breakfast',45.00),
-- ('Veg Sandwich','Snack',35.00),
-- ('Chicken Biryani','Lunch',95.00),
-- ('Paneer Butter Masala','Lunch',120.00),
-- ('Cold Coffee','Beverage',40.00),
-- ('Idli','Breakfast',30.00);

-- INSERT INTO Menu (MenuDate, StaffID, Notes) VALUES
-- ('2025-08-01', 1, 'Standard weekday menu'),
-- ('2025-08-02', 2, 'Special: Sandwich day'),
-- ('2025-08-03', 1, 'Weekend menu'),
-- ('2025-08-04', 4, 'Low-oil special'),
-- ('2025-08-05', 2, 'Chef specials');

-- INSERT INTO MenuFood (MenuID, ItemID) VALUES
-- (1, 1), (1, 6), (1, 5),
-- (2, 2), (2, 5),
-- (3, 3), (3, 4),
-- (4, 1), (4, 2), (4, 5),
-- (5, 3), (5, 4);

-- INSERT INTO Orders (SRN, OrderDate, Status) VALUES
-- ('PESU2021001', '2025-08-01 08:30:00', 'Completed'),
-- ('PESU2021002', '2025-08-01 09:10:00', 'Completed'),
-- ('PESU2021003', '2025-08-02 13:00:00', 'Completed'),
-- ('PESU2021004', '2025-08-03 12:45:00', 'Placed'),
-- ('PESU2021005', '2025-08-03 13:10:00', 'Completed');

-- INSERT INTO Order_Items (OrderID, ItemID, Quantity) VALUES
-- (1, 1, 1), (1, 5, 1),
-- (2, 6, 2),
-- (3, 2, 1), (3, 5, 1),
-- (4, 3, 1),
-- (5, 4, 1), (5, 5, 1);

-- INSERT INTO Review (SRN, ItemID, Rating, Feedback) VALUES
-- ('PESU2021001', 1, 5, 'Dosa was crisp and tasty.'),
-- ('PESU2021002', 6, 4, 'Idli soft, chutney ok.'),
-- ('PESU2021003', 2, 3, 'Sandwich a bit dry, add more chutney.'),
-- ('PESU2021004', 3, 4, 'Biryani well cooked but slightly oily.'),
-- ('PESU2021005', 4, 2, 'Paneer lacked seasoning, needs improvement.');


-- CREATE OR REPLACE VIEW ItemRatings AS
-- SELECT f.ItemID, f.ItemName,
--        COUNT(r.ReviewID) AS NumReviews,
--        ROUND(AVG(r.Rating),2) AS AvgRating
-- FROM FoodItem f
-- LEFT JOIN Review r ON f.ItemID = r.ItemID
-- GROUP BY f.ItemID, f.ItemName;

-- -- ==============================
-- -- SHOW CREATE TABLE 
-- -- ==============================


-- SELECT * FROM Student;
-- SELECT * FROM Staff;
-- SELECT * FROM FoodItem;
-- SELECT * FROM Menu;
-- SELECT * FROM MenuFood;
-- SELECT * FROM Orders;
-- SELECT * FROM Order_Items;
-- SELECT * FROM Review;
-- SELECT * FROM ItemRatings;





CREATE DATABASE IF NOT EXISTS cafeteria_db;
USE cafeteria_db;

-- ==============================
-- DDL: Create Tables
-- ==============================

-- Drop tables in reverse dependency order if they exist
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS Student, Staff, FoodItem, Menu, MenuFood, Orders, Order_Items, Review;
DROP VIEW IF EXISTS ItemRatings;
DROP PROCEDURE IF EXISTS GetStudentReviews;
DROP FUNCTION IF EXISTS GetTotalSpentByStudent;
DROP TRIGGER IF EXISTS before_review_update;
SET FOREIGN_KEY_CHECKS = 1;

-- 1. Student
CREATE TABLE Student (
  SRN VARCHAR(15) PRIMARY KEY,
  Name VARCHAR(100) NOT NULL,
  Email VARCHAR(150) NOT NULL UNIQUE,
  Phone VARCHAR(20),
  CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
) ;

-- 2. Staff
CREATE TABLE Staff (
  StaffID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(100) NOT NULL,
  Email VARCHAR(150) NOT NULL UNIQUE,
  Role VARCHAR(50) NOT NULL DEFAULT 'Staff',
  CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
) ;

-- 3. FoodItem
CREATE TABLE FoodItem (
  ItemID INT AUTO_INCREMENT PRIMARY KEY,
  ItemName VARCHAR(100) NOT NULL,
  Category VARCHAR(50) DEFAULT 'Snack',
  Price DECIMAL(7,2) NOT NULL CHECK (Price >= 0),
  IsActive TINYINT(1) NOT NULL DEFAULT 1
);

-- 4. Menu
CREATE TABLE Menu (
  MenuID INT AUTO_INCREMENT PRIMARY KEY,
  MenuDate DATE NOT NULL,
  StaffID INT NULL,
  Notes VARCHAR(255),
  CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_menu_staff FOREIGN KEY (StaffID)
    REFERENCES Staff(StaffID)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ;

-- 5. MenuFood (Menu ↔ FoodItem M:N)
CREATE TABLE MenuFood (
  MenuID INT NOT NULL,
  ItemID INT NOT NULL,
  PRIMARY KEY (MenuID, ItemID),
  CONSTRAINT fk_mf_menu FOREIGN KEY (MenuID)
    REFERENCES Menu(MenuID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_mf_item FOREIGN KEY (ItemID)
    REFERENCES FoodItem(ItemID)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ;

-- 6. Orders
CREATE TABLE Orders (
  OrderID INT AUTO_INCREMENT PRIMARY KEY,
  SRN VARCHAR(15),
  OrderDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  Status VARCHAR(30) NOT NULL DEFAULT 'Placed',
  CONSTRAINT fk_orders_student FOREIGN KEY (SRN)
    REFERENCES Student(SRN)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ;

-- 7. Order_Items
CREATE TABLE Order_Items (
  OrderID INT NOT NULL,
  ItemID INT NOT NULL,
  Quantity INT NOT NULL DEFAULT 1 CHECK (Quantity > 0),
  PRIMARY KEY (OrderID, ItemID),
  CONSTRAINT fk_orderitems_orders FOREIGN KEY (OrderID)
    REFERENCES Orders(OrderID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_orderitems_fooditem FOREIGN KEY (ItemID)
    REFERENCES FoodItem(ItemID)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ;

-- 8. Review
CREATE TABLE Review (
  ReviewID INT AUTO_INCREMENT PRIMARY KEY,
  SRN VARCHAR(15),
  ItemID INT NOT NULL,
  Rating TINYINT NOT NULL CHECK (Rating BETWEEN 1 AND 5),
  Feedback VARCHAR(500),
  ReviewDate DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_review_student FOREIGN KEY (SRN)
    REFERENCES Student(SRN)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT fk_review_item FOREIGN KEY (ItemID)
    REFERENCES FoodItem(ItemID)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- ==============================
-- DDL: Create View
-- ==============================

CREATE OR REPLACE VIEW ItemRatings AS
SELECT f.ItemID, f.ItemName,
       COUNT(r.ReviewID) AS NumReviews,
       ROUND(AVG(r.Rating),2) AS AvgRating
FROM FoodItem f
LEFT JOIN Review r ON f.ItemID = r.ItemID
GROUP BY f.ItemID, f.ItemName;

-- ==============================
-- DDL: Create Advanced DB Objects (Trigger, Procedure, Function)
-- ==============================

-- 1. Trigger
CREATE TRIGGER before_review_update 
BEFORE UPDATE ON Review 
FOR EACH ROW 
SET NEW.ReviewDate = NOW();

-- 2. Procedure
DELIMITER //
CREATE PROCEDURE GetStudentReviews(IN s_srn VARCHAR(15))
BEGIN
    SELECT * FROM Review WHERE SRN = s_srn;
END //
DELIMITER ;

-- 3. Function
DELIMITER //
CREATE FUNCTION GetTotalSpentByStudent(s_srn VARCHAR(15))
RETURNS DECIMAL(10, 2)
READS SQL DATA
BEGIN
    DECLARE total_spent DECIMAL(10, 2);

    SELECT SUM(oi.Quantity * fi.Price)
    INTO total_spent
    FROM Orders o
    JOIN Order_Items oi ON o.OrderID = oi.OrderID
    JOIN FoodItem fi ON oi.ItemID = fi.ItemID
    WHERE o.SRN = s_srn;

    RETURN IFNULL(total_spent, 0.00);
END //
DELIMITER ;


-- ==============================
-- DML: Insert sample data
-- ==============================

INSERT INTO Student (SRN, Name, Email, Phone) VALUES
('PESU2021001','Asha Kumar','asha.kumar@pes.edu','+91-9876543210'),
('PESU2021002','Rohit Sharma','rohit.sharma@pes.edu','+91-9123456780'),
('PESU2021003','Meera Nair','meera.nair@pes.edu','+91-9988776655'),
('PESU2021004','Karan Gupta','karan.gupta@pes.edu','+91-9012345678'),
('PESU2021005','Sara Iyer','sara.iyer@pes.edu','+91-9034567890');

INSERT INTO Staff (Name, Email, Role) VALUES
('Suresh Rao','suresh.rao@pes.edu','Manager'),
('Rekha Devi','rekha.devi@pes.edu','Chef'),
('Manoj Kumar','manoj.kumar@pes.edu','Cashier'),
('Anita Fernandes','anita.fernandes@pes.edu','Supervisor'),
('Vikram Singh','vikram.singh@pes.edu','Chef');

INSERT INTO FoodItem (ItemName, Category, Price) VALUES
('Masala Dosa','Breakfast',45.00),
('Veg Sandwich','Snack',35.00),
('Chicken Biryani','Lunch',95.00),
('Paneer Butter Masala','Lunch',120.00),
('Cold Coffee','Beverage',40.00),
('Idli','Breakfast',30.00);

INSERT INTO Menu (MenuDate, StaffID, Notes) VALUES
('2025-08-01', 1, 'Standard weekday menu'),
('2025-08-02', 2, 'Special: Sandwich day'),
('2025-08-03', 1, 'Weekend menu'),
('2025-08-04', 4, 'Low-oil special'),
('2025-08-05', 2, 'Chef specials');

INSERT INTO MenuFood (MenuID, ItemID) VALUES
(1, 1), (1, 6), (1, 5),
(2, 2), (2, 5),
(3, 3), (3, 4),
(4, 1), (4, 2), (4, 5),
(5, 3), (5, 4);

INSERT INTO Orders (SRN, OrderDate, Status) VALUES
('PESU2021001', '2025-08-01 08:30:00', 'Completed'),
('PESU2021002', '2025-08-01 09:10:00', 'Completed'),
('PESU2021003', '2025-08-02 13:00:00', 'Completed'),
('PESU2021004', '2025-08-03 12:45:00', 'Placed'),
('PESU2021005', '2025-08-03 13:10:00', 'Completed');

INSERT INTO Order_Items (OrderID, ItemID, Quantity) VALUES
(1, 1, 1), (1, 5, 1),
(2, 6, 2),
(3, 2, 1), (3, 5, 1),
(4, 3, 1),
(5, 4, 1), (5, 5, 1);

INSERT INTO Review (SRN, ItemID, Rating, Feedback) VALUES
('PESU2021001', 1, 5, 'Dosa was crisp and tasty.'),
('PESU2021002', 6, 4, 'Idli soft, chutney ok.'),
('PESU2021003', 2, 3, 'Sandwich a bit dry, add more chutney.'),
('PESU2021004', 3, 4, 'Biryani well cooked but slightly oily.'),
('PESU2021005', 4, 2, 'Paneer lacked seasoning, needs improvement.');


-- ==============================
-- Final Test Queries
-- ==============================
SELECT '-- Basic Data Verification --' AS 'TEST';
SELECT * FROM Student;
SELECT * FROM Staff;
SELECT * FROM FoodItem;
SELECT * FROM Menu;
SELECT * FROM MenuFood;
SELECT * FROM Orders;
SELECT * FROM Order_Items;
SELECT * FROM Review;

-- =A. View (Implicit Aggregation/Join)
SELECT '-- Testing View (ItemRatings) --' AS 'TEST';
SELECT * FROM ItemRatings;

-- B. Procedure and Function
SELECT '-- Testing Procedure and Function --' AS 'TEST';
CALL GetStudentReviews('PESU2021001');
SELECT GetTotalSpentByStudent('PESU2021001') AS 'TotalSpentByAsha';


-- ==============================
-- Advanced Queries (Join, Nested, Aggregate)
-- ==============================

-- 1. JOIN QUERY
SELECT
    s.Name,
    fi.ItemName,
    o.OrderDate
FROM
    Student s
JOIN
    Orders o ON s.SRN = o.SRN
JOIN
    Order_Items oi ON o.OrderID = oi.OrderID
JOIN
    FoodItem fi ON oi.ItemID = fi.ItemID
WHERE
    fi.ItemName LIKE '%Dosa%';


-- 2. NESTED QUERY (Subquery)
SELECT ItemName, Price 
FROM FoodItem 
WHERE ItemID NOT IN (SELECT DISTINCT ItemID FROM Review);

-- 3. AGGREGATE QUERY
SELECT 
    s.SRN,
    s.Name,
    COUNT(r.ReviewID) AS NumReviews,
    IFNULL(ROUND(AVG(r.Rating), 2), 0.00) AS AvgRating
FROM 
    Student s
LEFT JOIN 
    Review r ON s.SRN = r.SRN
GROUP BY 
    s.SRN, s.Name
ORDER BY 
    NumReviews DESC;
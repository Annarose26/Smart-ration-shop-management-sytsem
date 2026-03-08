-- CREATE DATABASE ration_shop;
-- USE ration_shop;

-- login table

-- CREATE TABLE user (id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(50),password VARCHAR(50),role VARCHAR(20) NOT NULL);
-- INSERT INTO user ( id, username, password, role)VALUES ( null,'admin', 'admin123', 'admin');
-- INSERT INTO user ( id, username, password, role)VALUES ( null,'anna', '1234', 'user');
-- SELECT * FROM user;
-- USE ration_shop;
-- DESCRIBE user;
--  SELECT * FROM user;

-- book now table

-- CREATE TABLE card_holder (id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(100),card_number VARCHAR(20) UNIQUE,card_type VARCHAR(10),members INT,mobile VARCHAR(15),username VARCHAR(50));
-- INSERT INTO card_holder(name, card_number, card_type, members, mobile, username)VALUES('Anna Rose','1234','APL',5,'9876543210','anna'),('Paul M L','123','BPL',4,'9876543278','paul'),('Asha','12345','BPL',3,'9876543211','asha');
-- SELECT * FROM card_holder; 
-- ALTER TABLE card_holder ADD profile_image VARCHAR(255); 
-- UPDATE card_holder SET profile_image='images/gir.jpg' WHERE id = 1;
-- UPDATE card_holder SET profile_image='images/boy.jpg'WHERE id = 2;
-- UPDATE card_holder SET profile_image='images/girl1.jpg'WHERE id = 3;
-- UPDATE card_holder SET profile_image='images/girl2.jpg'WHERE id = 4;
-- UPDATE card_holder SET profile_image='images/girl.jpg' WHERE id = 8;
-- UPDATE card_holder SET profile_image='images/girl.jpg' WHERE id = 1;
-- SELECT id, name FROM card_holder;
-- ALTER TABLE card_holder ADD gender VARCHAR(10);


-- stock table 

-- CREATE TABLE stock (id INT AUTO_INCREMENT PRIMARY KEY,item_name VARCHAR(100) NOT NULL,card_type VARCHAR(20) NOT NULL,fixed_qty INT NOT NULL,price DECIMAL(10,2) NOT NULL,available_qty INT NOT NULL,image VARCHAR(255)); 
-- INSERT INTO stock (item_name, card_type, fixed_qty, price, available_qty, image) VALUES('Rice', 'APL', 10, 30, 100, 'static/images/rice.jpg'),('Rice', 'BPL', 15, 10, 200, 'static/images/rice.jpg'),('Rice', 'AAY', 20, 5, 150, 'static/images/rice.jpg'),('Sugar', 'APL', 2, 40, 50, 'static/images/sugar.jpg'),('Wheat', 'BPL', 5, 20, 80, 'static/images/wheat.jpg'); 
-- INSERT INTO stock (item_name, card_type, fixed_qty, price, available_qty, image) VALUES('Kerosene', 'APL', 10, 30, 100, 'static/images/kerosene.jpg'),('Kerosene', 'BPL', 11, 40, 110, 'static/images/kerosene.jpg');
-- SELECT * FROM stock; 
-- UPDATE stock SET image='images/rice.jpg' WHERE id=1;
-- UPDATE stock SET image='images/rice.jpg' WHERE id=2;
-- UPDATE stock SET image='images/rice.jpg' WHERE id=3;
-- UPDATE stock SET image='images/sugar.jpg' WHERE id=4;
-- UPDATE stock SET image='images/wheat.jpg' WHERE id=5;
-- UPDATE stock SET image='images/kerosene.jpg' WHERE id=6;
-- UPDATE stock SET image='images/kerosene.jpg' WHERE id=7;
-- UPDATE stock SET image='images/rice.jpg' WHERE item_name='Rice';
-- UPDATE stock SET image='images/sugar.jpg' WHERE item_name='Sugar';
-- UPDATE stock SET image='images/wheat.jpg' WHERE item_name='Wheat';
-- UPDATE stock SET image='images/kerosene.jpg' WHERE item_name='Kerosene';

-- notice table 

-- CREATE TABLE notices (id INT AUTO_INCREMENT PRIMARY KEY,title VARCHAR(150) NOT NULL,message TEXT NOT NULL,type ENUM('shop','government') NOT NULL,status ENUM('active','inactive') DEFAULT 'active',created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP); 
-- INSERT INTO notices (title, message, type, status) VALUES('Shop Closed Due to Biometric Issue','Due to biometric machine technical damage, the ration shop will remain closed today. Service will resume once the issue is resolved.','shop','active'),('Wheat Stock Temporarily Unavailable','Wheat stock is currently unavailable due to supply delay. New stock is expected within 3 days.','shop','active'),('Maintenance Work Notice','Electric maintenance work will be carried out tomorrow from 10 AM to 1 PM. During this time, distribution services will be paused.','shop','active'),('Rice Price Revised','As per government order, the price of rice has been revised to ₹2 per kg for eligible card holders.','government','active'),('Onam Special Ration Kit Distribution','Special Onam ration kits will be distributed from 10th March to 20th March for all eligible families.','government','active'),('New Ration Card Registration Drive','Government has announced a special registration drive for new ration card applicants from 1st April to 15th April.','government','active'),('Sugar Quantity Increased','Monthly sugar allocation has been increased by 1 kg for BPL and AAY card holders as per new government directive.','government','active'); 
-- SELECT * FROM notices;



-- report table 

-- CREATE TABLE reports (id INT AUTO_INCREMENT PRIMARY KEY,title VARCHAR(200) NOT NULL,description TEXT NOT NULL,name VARCHAR(100) NOT NULL,card_number VARCHAR(50) NOT NULL,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP); 
-- INSERT INTO reports (title, description, name, card_number) VALUES('Biometric Machine Not Working','Fingerprint scanner is not detecting properly during distribution.','Rajesh Kumar','APL12345'),('Kerosene Not Supplied','Kerosene not available for last 5 days.','Anitha P','BPL56789'),('Poor Quality Rice','Rice contains stones and dust particles.','Suresh Nair','AAY88990');


-- bookings table

-- CREATE TABLE bookings (id INT AUTO_INCREMENT PRIMARY KEY,card_holder_id INT NOT NULL,booking_date DATE NOT NULL,booking_time TIME NOT NULL,total_amount INT NOT NULL,status ENUM('Pending','Approved','Rejected','Completed') DEFAULT 'Pending',created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY (card_holder_id) REFERENCES card_holder(id));
-- INSERT INTO bookings (card_holder_id, booking_date, booking_time, total_amount, status)VALUES(1, '2026-02-20', '10:30:00', 350.00, 'Pending'),(2, '2026-02-21', '11:15:00', 220.00, 'Approved'),(3, '2026-02-22', '09:45:00', 180.00, 'Completed'),(1, '2026-02-23', '02:00:00', 400.00, 'Rejected'),(2, '2026-02-24', '03:30:00', 275.00, 'Pending');
-- ALTER TABLE bookings ADD card_type VARCHAR(10);
--  SELECT * FROM bookings;

-- book items table

-- CREATE TABLE booking_items (id INT AUTO_INCREMENT PRIMARY KEY,booking_id INT NOT NULL,stock_id INT NOT NULL,quantity INT NOT NULL,total_price INT NOT NULL,FOREIGN KEY (booking_id) REFERENCES bookings(id),FOREIGN KEY (stock_id) REFERENCES stock(id));
-- INSERT INTO booking_items (booking_id, stock_id, quantity, total_price)VALUES-- Booking 1 (Anna - id 1)(1, 1, 10, 300.00),(1, 4, 2, 50.00),-- Booking 2 (Paul - id 2)(2, 2, 15, 150.00),(2, 5, 5, 70.00),-- Booking 3 (Asha - id 3)(3, 2, 10, 100.00),(3, 5, 4, 80.00),-- Booking 4 (Anna again)(4, 1, 10, 300.00),(4, 4, 2, 100.00),-- Booking 5 (Paul again)(5, 2, 15, 150.00),(5, 5, 5, 125.00);
-- SELECT * FROM booking_items;


-- activites table 

-- CREATE TABLE activities (id INT AUTO_INCREMENT PRIMARY KEY,message TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);








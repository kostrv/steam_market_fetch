-- Создайте новую базу данных с помощью powershell: Get-Content .\create_database.sql | mysql -u root -p

CREATE DATABASE mydatabase;

USE mydatabase;

CREATE TABLE parsed_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    total_month_sales VARCHAR(50) NOT NULL,
    avg_week_sales VARCHAR(50) NOT NULL,
    avg_day_sales VARCHAR(50) NOT NULL,
    median_price VARCHAR(50) NOT NULL
);

CREATE USER 'username'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON mydatabase.* TO 'username'@'%';
FLUSH PRIVILEGES;
DROP DATABASE IF EXISTS property_db;
CREATE DATABASE property_db;
USE property_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'viewer') NOT NULL
);

CREATE TABLE properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    location VARCHAR(255),
    price INT,
    type VARCHAR(50),
    description TEXT,
    image_url VARCHAR(255),
    submitted_by VARCHAR(50),
    approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample users with hashed passwords:
-- Use Python to generate passwords:
-- from werkzeug.security import generate_password_hash
-- print(generate_password_hash("admin123"))

 
INSERT INTO users (username, password, role) VALUES
('admin', 'scrypt:32768:8:1$ZZoB38ZUJ0Rm4c7s$440f17f36ea2341d83ac8dbcd2b293d3ebd0c964287d185f0be17e5a6d4c36fcbded579c36122cb8d5df0ac287fbbbc92f6a91a60484885f3b3f4b880b75a6c5', 'admin'),
('viewer', 'scrypt:32768:8:1$UNkVEKBUiT8RtG68$7aa7e535c3760e02f2be9e8cfeb7f9b15a358f99dcfe3c8c601d01a08e48e1459b8f23bb4f2be15efae91ae7f38c9a78e9b6e476edc0dfd71947746c1ff61fc6', 'viewer');


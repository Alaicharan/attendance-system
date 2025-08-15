-- Attendance System Database Setup
-- Run this in MySQL to create the required database and tables

-- Create database
CREATE DATABASE IF NOT EXISTS attendance_db;
USE attendance_db;

-- Create students table
CREATE TABLE IF NOT EXISTS students (
    idstudents INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    section VARCHAR(20) NOT NULL,
    batch VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create attendance table
CREATE TABLE IF NOT EXISTS attendance (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    in_time DATETIME NOT NULL,
    out_time DATETIME NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(idstudents) ON DELETE CASCADE
);

-- Insert sample data
INSERT INTO students (name, department, section, batch) VALUES
('Jayasri S', 'IT', 'A', '2024-2028'),
('John Doe', 'CS', 'B', '2024-2028'),
('Jane Smith', 'IT', 'A', '2024-2028'),
('Mike Johnson', 'CS', 'B', '2024-2028'),
('Sarah Wilson', 'IT', 'A', '2024-2028');

-- Insert sample attendance records
INSERT INTO attendance (student_id, in_time) VALUES
(1, '2025-08-15 14:38:00'),
(2, '2025-08-15 14:40:00'),
(3, '2025-08-15 14:42:00');

-- Create indexes for better performance
CREATE INDEX idx_student_id ON attendance(student_id);
CREATE INDEX idx_in_time ON attendance(in_time);
CREATE INDEX idx_department ON students(department);

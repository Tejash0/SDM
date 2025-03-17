-- SQLite
CREATE DATABASE UniversityDB;
USE UniversityDB;

-- Table for Instructor
CREATE TABLE Instructor (
    Ins_ID INT PRIMARY KEY,
    F_Name VARCHAR(50),
    L_Name VARCHAR(50),
    Email VARCHAR(100),
    Phone_No VARCHAR(20),
    Dep_ID INT,
    FOREIGN KEY (Dep_ID) REFERENCES Department(Dep_ID)
);

-- Table for Student
CREATE TABLE Student (
    Stud_ID INT PRIMARY KEY,
    F_Name VARCHAR(50),
    L_Name VARCHAR(50),
    DOB DATE,
    Gender VARCHAR(10),
    Email VARCHAR(100),
    Phone_No VARCHAR(20),
    Address TEXT,
    Dep_ID INT,
    FOREIGN KEY (Dep_ID) REFERENCES Department(Dep_ID)
);

-- Table for Department
CREATE TABLE Department (
    Dep_ID INT PRIMARY KEY,
    Name VARCHAR(100),
    HOD INT,
    N_Student INT,
    N_Instructor INT,
    FOREIGN KEY (HOD) REFERENCES Instructor(Ins_ID)
);

-- Table for Course
CREATE TABLE Course (
    Course_ID INT PRIMARY KEY,
    Name VARCHAR(100),
    Code VARCHAR(20),
    Credits INT,
    Dept_ID INT,
    FOREIGN KEY (Dept_ID) REFERENCES Department(Dep_ID)
);

-- Table for Enrollment
CREATE TABLE Enrollment (
    En_ID INT PRIMARY KEY,
    Stud_ID INT,
    Course_ID INT,
    Grade VARCHAR(5),
    Date DATE,
    FOREIGN KEY (Stud_ID) REFERENCES Student(Stud_ID),
    FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID)
);

-- Run this first (if not done already):
DROP TABLE Student;

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

INSERT INTO Department (Dep_ID, Name, HOD, N_Student, N_Instructor)
VALUES
(1, 'Computer Science', NULL, 0, 0),
(2, 'Mathematics', NULL, 0, 0),
(3, 'Physics', NULL, 0, 0),
(4, 'English', NULL, 0, 0);


INSERT INTO Instructor (Ins_ID, F_Name, L_Name, Email, Phone_No, Dep_ID)
VALUES
(101, 'Alice', 'Smith', 'alice.smith@example.com', '111-111-1111', 1),
(102, 'Bob', 'Johnson', 'bob.johnson@example.com', '222-222-2222', 2),
(103, 'Carol', 'Davis', 'carol.davis@example.com', '333-333-3333', 3),
(104, 'David', 'Brown', 'david.brown@example.com', '444-444-4444', 4);

UPDATE Department SET HOD = 101 WHERE Dep_ID = 1;
UPDATE Department SET HOD = 102 WHERE Dep_ID = 2;
UPDATE Department SET HOD = 103 WHERE Dep_ID = 3;
UPDATE Department SET HOD = 104 WHERE Dep_ID = 4;

-- Run this first (if not done already):
DROP TABLE Student;

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

INSERT INTO Student (Stud_ID, F_Name, L_Name, DOB, Gender, Email, Phone_No, Address, Dep_ID)
VALUES
(201, 'John', 'Doe', '2000-05-15', 'Male', 'john.doe@example.com', '999-999-0001', '123 Main St', 1),
(202, 'Emma', 'Watson', '1999-10-30', 'Female', 'emma.w@example.com', '999-999-0002', '456 Oak St', 1),
(203, 'Mike', 'Lee', '2001-07-21', 'Male', 'mike.lee@example.com', '999-999-0003', '789 Pine St', 2),
(204, 'Sophia', 'Green', '2002-03-18', 'Female', 'sophia.g@example.com', '999-999-0004', '321 Elm St', 3);


INSERT INTO Course (Course_ID, Name, Code, Credits, Dept_ID)
VALUES
(301, 'Database Systems', 'CS305', 4, 1),
(302, 'Linear Algebra', 'MATH201', 3, 2),
(303, 'Quantum Mechanics', 'PHY301', 4, 3),
(304, 'British Literature', 'ENG210', 3, 4);


INSERT INTO Enrollment (En_ID, Stud_ID, Course_ID, Grade, Date)
VALUES
(401, 201, 301, 'A', '2025-01-15'),
(402, 202, 301, 'B+', '2025-01-20'),
(403, 203, 302, 'A-', '2025-02-01'),
(404, 204, 303, 'B', '2025-02-10');


.schema
-- SQLite

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

CREATE TABLE Student (
    Stud_ID INT PRIMARY KEY,
    F_Name VARCHAR(50),
    L_Name VARCHAR(50),
    DOB DATE,
    Gender VARCHAR(10),
    Email VARCHAR(100),
    Phone_No VARCHAR(20),
    Address TEXT,
    Dep_ID INT UNIQUE,
    FOREIGN KEY (Dep_ID) REFERENCES Department(Dep_ID)
);

CREATE TABLE Department (
    Dep_ID INT PRIMARY KEY,
    Name VARCHAR(100),
    HOD INT,
    N_Student INT,
    N_Instructor INT,
    FOREIGN KEY (HOD) REFERENCES Instructor(Ins_ID)
);

CREATE TABLE Course (
    Course_ID INT PRIMARY KEY,
    Name VARCHAR(100),
    Code VARCHAR(20),
    Credits INT,
    Dept_ID INT,
    FOREIGN KEY (Dept_ID) REFERENCES Department(Dep_ID)
);

CREATE TABLE Enrollment (
    En_ID INT PRIMARY KEY,
    Stud_ID INT,
    Course_ID INT,
    Grade VARCHAR(5),
    Date DATE,
    FOREIGN KEY (Stud_ID) REFERENCES Student(Stud_ID),
    FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID)
);




<form action="/add" method="post">
        <label for="Stud_ID">Student ID:</label>
        <input type="number" id="Stud_ID" name="Stud_ID" required>

        <label for="F_Name">First Name:</label>
        <input type="text" id="F_Name" name="F_Name" required>

        <label for="L_Name">Last Name:</label>
        <input type="text" id="L_Name" name="L_Name" required>

        <label for="DOB">Date of Birth:</label>
        <input type="date" id="DOB" name="DOB" required>

        <label for="Gender">Gender:</label>
        <select id="Gender" name="Gender" required>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
        </select>
        <h1></h1>
        <label for="Email">Email:</label>
        <input type="email" id="Email" name="Email" required>

        <label for="Phone_No">Phone Number:</label>
        <input type="tel" id="Phone_No" name="Phone_No" required>

        <label for="Address">Address:</label>
        <textarea id="Address" name="Address" required></textarea>

        <h1></h1>
        <label for="Dep_ID">Department ID:</label>
        <input type="number" id="Dep_ID" name="Dep_ID" required>

        <button type="submit">Add Student</button>
    </form>





SELECT * FROM Users;




    .schema
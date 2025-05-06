--Views

CREATE VIEW StudentCourseGrades AS
SELECT 
    S.Stud_ID,
    S.F_Name || ' ' || S.L_Name AS Student_Name,
    C.Name AS Course_Name,
    E.Grade
FROM Enrollment E
JOIN Student S ON E.Stud_ID = S.Stud_ID
JOIN Course C ON E.Course_ID = C.Course_ID;


SELECT * FROM StudentCourseGrades WHERE Grade = 'A';



CREATE VIEW DepartmentOverview AS
SELECT 
    D.Dep_ID,
    D.Name AS Department_Name,
    I.F_Name || ' ' || I.L_Name AS HOD_Name,
    D.N_Student,
    D.N_Instructor
FROM Department D
LEFT JOIN Instructor I ON D.HOD = I.Ins_ID;


SELECT * FROM DepartmentOverview;



CREATE VIEW InstructorDepartment AS
SELECT 
    I.Ins_ID,
    I.F_Name || ' ' || I.L_Name AS Instructor_Name,
    D.Name AS Department_Name
FROM Instructor I
JOIN Department D ON I.Dep_ID = D.Dep_ID;


SELECT * FROM InstructorDepartment WHERE Department_Name = 'Physics';
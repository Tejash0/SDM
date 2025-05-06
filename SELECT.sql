SELECT 
    S.F_Name || ' ' || S.L_Name AS Student_Name,
    D.Name AS Department_Name
FROM Student S
JOIN Department D ON S.Dep_ID = D.Dep_ID;


SELECT 
    S.F_Name || ' ' || S.L_Name AS Student_Name,
    C.Name AS Course_Name,
    E.Grade
FROM Enrollment E
JOIN Student S ON E.Stud_ID = S.Stud_ID
JOIN Course C ON E.Course_ID = C.Course_ID;



--Sub query

SELECT F_Name, L_Name
FROM Student
WHERE Stud_ID IN (
    SELECT Stud_ID
    FROM Enrollment
    WHERE Course_ID = (
        SELECT Course_ID FROM Course WHERE Name = 'Database Systems'
    )
);

SELECT Name
FROM Department
WHERE Dep_ID IN (
    SELECT Dep_ID
    FROM Instructor
    GROUP BY Dep_ID
    HAVING COUNT(*) > 2
);

SELECT F_Name, L_Name
FROM Instructor
WHERE Ins_ID NOT IN (
    SELECT HOD FROM Department
    WHERE HOD IS NOT NULL
);

SELECT F_Name, L_Name
FROM Student
WHERE Stud_ID IN (
    SELECT Stud_ID
    FROM Enrollment
    GROUP BY Stud_ID
    HAVING COUNT(*) = (
        SELECT MAX(CourseCount)
        FROM (
            SELECT COUNT(*) AS CourseCount
            FROM Enrollment
            GROUP BY Stud_ID
        )
    )
);

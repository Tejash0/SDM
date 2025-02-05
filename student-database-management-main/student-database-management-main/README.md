how to create database

 install SQlite
 
 sqlite3 mydatabase.db
 CREATE TABLE tablename (
    column1 datatype,
    column2 datatype,
    column3 datatype,
    ...
);
INSERT INTO tablename (column1, column2, column3, ...) VALUES (value1, value2, value3, ...);

SELECT * FROM tablename;


import sqlite3

# Create/connect to a database
conn = sqlite3.connect('student.db')
cursor = conn.cursor()

# Create a table for students if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        grade TEXT,
        reg INTEGER
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

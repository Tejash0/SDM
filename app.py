from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Ensure database schema is correct
def initialize_db():
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    
    # Ensure uniqueness for Dep_ID if needed
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Student (
            Stud_ID INTEGER PRIMARY KEY, 
            F_Name TEXT, 
            L_Name TEXT, 
            DOB DATE, 
            Gender TEXT, 
            Email TEXT UNIQUE, 
            Phone_No TEXT, 
            Address TEXT, 
            Dep_ID INTEGER UNIQUE,  -- Enforcing uniqueness
            FOREIGN KEY (Dep_ID) REFERENCES Department(Dep_ID)
        )
    ''')
    
    conn.commit()
    conn.close()

# Home route - display students
@app.route('/')
def index():
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Student')
    students = cursor.fetchall()
    conn.close()
    return render_template('index.html', students=students)

# Add a new student
@app.route('/add', methods=['POST'])
def add_student():
    Stud_ID = request.form['Stud_ID']
    F_Name = request.form['F_Name']
    L_Name = request.form['L_Name']
    DOB = request.form['DOB']
    Gender = request.form['Gender']
    Email = request.form['Email']
    Phone_No = request.form['Phone_No']
    Address = request.form['Address']
    Dep_ID = request.form['Dep_ID']

    try:
        conn = sqlite3.connect('student.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Student (Stud_ID, F_Name, L_Name, DOB, Gender, Email, Phone_No, Address, Dep_ID) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (Stud_ID, F_Name, L_Name, DOB, Gender, Email, Phone_No, Address, Dep_ID))
        
        conn.commit()
        conn.close()
        return redirect('/')
    
    except sqlite3.IntegrityError as e:
        conn.close()
        if "UNIQUE constraint failed: Student.Email" in str(e):
            flash("Error: Email already exists.", 'error')
        elif "UNIQUE constraint failed: Student.Dep_ID" in str(e):
            flash("Error: Department ID must be unique.", 'error')
        else:
            flash("Error: Student ID already exists.", 'error')
        return redirect('/')

# Delete a student
@app.route('/delete/<int:Stud_ID>')
def delete_student(Stud_ID):
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Student WHERE Stud_ID = ?', (Stud_ID,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    initialize_db()  # Ensure the database structure is correct on startup
    app.run(debug=True)

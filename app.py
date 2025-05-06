from flask import Flask, render_template, request, redirect, session, flash, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Session timeout (Optional)
app.permanent_session_lifetime = timedelta(minutes=30)  # Session expires after 30 minutes

# Database Initialization
# 1. Fix the initialize_db() function to create all needed tables:
def initialize_db():
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    
    # Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            User_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT UNIQUE NOT NULL,
            Password TEXT NOT NULL
        )
    ''')

    # Create Department Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Department (
            Dep_ID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL
        )
    ''')

    # Create Student Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Student (
            Stud_ID INTEGER PRIMARY KEY,
            F_Name TEXT NOT NULL,
            L_Name TEXT NOT NULL,
            DOB DATE,
            Gender TEXT,
            Email TEXT UNIQUE,
            Phone_No TEXT,
            Address TEXT,
            Dep_ID INTEGER,
            FOREIGN KEY (Dep_ID) REFERENCES Department(Dep_ID)
        )
    ''')
    
    # Create Course Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Course (
            Course_ID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Code TEXT,
            Credits INTEGER,
            Dep_ID INTEGER,
            FOREIGN KEY (Dep_ID) REFERENCES Department(Dep_ID)
        )
    ''')
    
    # Create Enrollment Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Enrollment (
            En_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Stud_ID INTEGER,
            Course_ID INTEGER,
            Grade TEXT,
            Date DATE DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (Stud_ID) REFERENCES Student(Stud_ID),
            FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID)
        )
    ''')

    # Insert sample departments if none exist
    cursor.execute('SELECT COUNT(*) FROM Department')
    if cursor.fetchone()[0] == 0:
        departments = [
            (1, 'Computer Science'),
            (2, 'Business Administration'),
            (3, 'Engineering')
        ]
        cursor.executemany('INSERT INTO Department (Dep_ID, Name) VALUES (?, ?)', departments)
    
    # Insert sample courses if none exist
    cursor.execute('SELECT COUNT(*) FROM Course')
    if cursor.fetchone()[0] == 0:
        courses = [
            (1, 'Introduction to Programming', 'CS101', 3, 1),
            (2, 'Database Systems', 'CS301', 4, 1),
            (3, 'Marketing Fundamentals', 'BA101', 3, 2),
            (4, 'Engineering Mathematics', 'EN201', 4, 3)
        ]
        cursor.executemany('INSERT INTO Course (Course_ID, Name, Code, Credits, Dep_ID) VALUES (?, ?, ?, ?, ?)', courses)

    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('student.db')
    conn.row_factory = sqlite3.Row
    return conn

# User Authentication Functions
def get_user(username):
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE Username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Get All Students
def get_all_students():
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Student')
    students = cursor.fetchall()
    conn.close()
    return students



# Routes
# 2. Remove one of the duplicate route handlers and combine them:
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect('/login')

    # Fetch all students
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM Student').fetchall()

    # Fetch all courses
    courses = conn.execute('SELECT * FROM Course').fetchall()

    conn.close()

    return render_template('index.html', students=students, courses=courses, default_tab='addTab')
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')

    # Fetch all students
    conn = sqlite3.connect('student.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    students = cur.execute('SELECT * FROM Student').fetchall()

    # Fetch all courses
    courses = cur.execute('SELECT * FROM Course').fetchall()

    conn.close()

    return render_template('index.html', students=students, courses=courses, default_tab='addTab')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)

        try:
            conn = sqlite3.connect('student.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Users (Username, Password) VALUES (?, ?)', (username, hashed_pw))
            conn.commit()
            conn.close()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You need to log in first.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add_student():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Basic Validation
    if not request.form['Stud_ID'] or not request.form['F_Name'] or not request.form['L_Name']:
        flash("All fields are required.", "error")
        return redirect(url_for('home'))

    data = {
        'Stud_ID': request.form['Stud_ID'],
        'F_Name': request.form['F_Name'],
        'L_Name': request.form['L_Name'],
        'DOB': request.form['DOB'],
        'Gender': request.form['Gender'],
        'Email': request.form['Email'],
        'Phone_No': request.form['Phone_No'],
        'Address': request.form['Address'],
        'Dep_ID': request.form['Dep_ID']
    }

    try:
        conn = sqlite3.connect('student.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Student (Stud_ID, F_Name, L_Name, DOB, Gender, Email, Phone_No, Address, Dep_ID)
                          VALUES (:Stud_ID, :F_Name, :L_Name, :DOB, :Gender, :Email, :Phone_No, :Address, :Dep_ID)''', data)
        conn.commit()
        conn.close()
        return redirect(request.referrer)  # Redirect to the referrer page
    except sqlite3.IntegrityError as e:
        conn.close()
        if "UNIQUE constraint failed: Student.Email" in str(e):
            flash("Error: Email already exists.", 'error')
        elif "UNIQUE constraint failed: Student.Stud_ID" in str(e):
            flash("Error: Student ID already exists.", 'error')
        else:
            flash("Error: Could not add student.", 'error')
        return redirect(url_for('home'))

@app.route('/delete/<int:Stud_ID>')
def delete_student(Stud_ID):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Student WHERE Stud_ID = ?', (Stud_ID,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

# 4. Fix the search route to properly handle course enrollments:
@app.route('/search', methods=['POST'])
def search():
    search_id = request.form['search_id']
    conn = get_db_connection()

    # Fetch student details
    student = conn.execute('''SELECT S.*, D.Name AS Dept_Name
                              FROM Student S
                              LEFT JOIN Department D ON S.Dep_ID = D.Dep_ID
                              WHERE S.Stud_ID = ?''', (search_id,)).fetchone()
    
    # Fetch enrolled courses for the student
    enrolled_courses = []
    if student:
        enrolled_courses = conn.execute('''
            SELECT C.Course_ID, C.Name
            FROM Course C
            JOIN Enrollment E ON C.Course_ID = E.Course_ID
            WHERE E.Stud_ID = ?
        ''', (search_id,)).fetchall()
    
    # Fetch all students for the list view
    students = conn.execute('SELECT * FROM Student').fetchall()
    
    # Fetch all courses for other tabs
    all_courses = conn.execute('SELECT * FROM Course').fetchall()
    
    conn.close()
    
    return render_template('index.html', students=students, search_result=student, 
                          courses=enrolled_courses, all_courses=all_courses,
                          search_attempted=True, default_tab='searchTab')

@app.route('/assign', methods=['GET', 'POST'])
def assign_course():
    conn = get_db_connection()
    
    # Fetch all students and courses
    students = conn.execute('SELECT Stud_ID, F_Name, L_Name FROM Student').fetchall()
    courses = conn.execute('SELECT Course_ID, Name FROM Course').fetchall()
    
    if request.method == 'POST':
        student_id = request.form['Stud_ID']
        course_id = request.form['Course_ID']
        grade = request.form['Grade']
        
        # Insert course assignment into Enrollment table
        conn.execute('INSERT INTO Enrollment (Stud_ID, Course_ID, Grade) VALUES (?, ?, ?)',
                     (student_id, course_id, grade))
        conn.commit()
        conn.close()
        flash("Course assigned successfully!", "success")
        return redirect(url_for('assign_course'))
    
    conn.close()
    return render_template('index.html', students=students, courses=courses, default_tab='assignTab')


@app.route('/view_courses')
@login_required
def view_courses():
    conn = get_db_connection()
    all_courses = conn.execute('SELECT * FROM Course').fetchall()
    students = conn.execute('SELECT * FROM Student').fetchall()
    conn.close()
    return render_template("index.html", students=students, courses=all_courses, 
                          search_result=None, search_attempted=False, default_tab='coursesTab')

if __name__ == '__main__':
    initialize_db()
    app.run(debug=True)

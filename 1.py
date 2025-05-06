from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('student.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_all_students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM Student').fetchall()
    conn.close()
    return students

@app.route('/')
def index():
    conn = get_db_connection()
    students = get_all_students()
    courses = conn.execute('SELECT * FROM Course').fetchall()  # Fetch all courses here
    conn.close()
    return render_template('index.html', students=students, courses=courses, default_tab='addTab')

@app.route('/add', methods=['POST'])
def add_student():
    conn = get_db_connection()
    conn.execute('''INSERT INTO Student (Stud_ID, F_Name, L_Name, DOB, Gender, Email, Phone_No, Address, Dep_ID)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 (request.form['Stud_ID'], request.form['F_Name'], request.form['L_Name'],
                  request.form['DOB'], request.form['Gender'], request.form['Email'],
                  request.form['Phone_No'], request.form['Address'], request.form['Dep_ID']))
    conn.commit()
    conn.close()
    flash("Student added successfully!", "success")
    return redirect(url_for('index', default_tab='listTab'))

@app.route('/delete/<int:student_id>')
def delete_student(student_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Student WHERE Stud_ID = ?', (student_id,))
    conn.commit()
    conn.close()
    flash("Student deleted successfully!", "success")
    return redirect(url_for('index', default_tab='listTab'))

@app.route('/search', methods=['POST'])
def search():
    search_id = request.form['search_id']
    conn = get_db_connection()

    # Initialize courses as an empty list to avoid unbound variable error
    courses = []

    # Fetch student details
    student = conn.execute('''SELECT S.*, D.Name AS Dept_Name
                              FROM Student S
                              LEFT JOIN Department D ON S.Dep_ID = D.Dep_ID
                              WHERE S.Stud_ID = ?''', (search_id,)).fetchone()
    
    # Fetch courses the student is enrolled in, including courses even if the student is not enrolled in them
    if student:
        courses = conn.execute('''SELECT C.Course_ID, C.Name
                                  FROM Course C
                                  LEFT JOIN Enrollment E ON C.Course_ID = E.Course_ID
                                  AND E.Stud_ID = ?''', (search_id,)).fetchall()
    
    conn.close()
    
    students = get_all_students()  # Get all students for the list view
    
    # If no courses were found for the student, courses will already be an empty list
    return render_template('index.html', students=students, search_result=student, courses=courses, search_attempted=True, default_tab='searchTab')

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
def view_courses():
    conn = get_db_connection()
    courses = conn.execute('SELECT * FROM Course').fetchall()
    conn.close()
    return render_template('index.html', courses=courses, default_tab='coursesTab')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if the passwords match
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for('register'))

        # Check if the username already exists
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user:
            flash("Username already exists.", "error")
            return redirect(url_for('register'))

        # Hash the password and insert the new user into the database
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        # Check if user exists and password matches
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']  # Make sure 'id' exists
            return redirect(url_for('index'))  # Redirect to home page or dashboard
        else:
            flash("Invalid credentials. Please try again.", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        flash("You have been logged out successfully.", "success")
    else:
        flash("You are not logged in.", "error")
    return redirect(url_for('login'))


# Login required decorator to protect routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You need to log in first.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/some_protected_route')
@login_required
def protected_route():
    # Protected logic here
    return render_template('protected.html')

if __name__ == '__main__':
    app.run(debug=True)

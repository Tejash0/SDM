from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    age = request.form['age']
    grade = request.form['grade']
    reg = request.form['reg']

    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (name, age, grade, reg) VALUES (?, ?, ?, ?)', (name, age, grade, reg))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:student_id>')
def delete_student(student_id):
    conn = sqlite3.connect('student.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)



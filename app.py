
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Connect to database
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create student table
def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Display all students
@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('index.html', students=students)

# Add student
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name'].strip()
    department = request.form['department'].strip()
    email = request.form['email'].strip()

    if not name or not department or not email:
        return "All fields are required!"

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO students (name, department, email) VALUES (?, ?, ?)',
        (name, department, email)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Update student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()

    if request.method == 'POST':
        name = request.form['name'].strip()
        department = request.form['department'].strip()
        email = request.form['email'].strip()

        if not name or not department or not email:
            conn.close()
            return "All fields are required!"

        conn.execute(
            'UPDATE students SET name=?, department=?, email=? WHERE id=?',
            (name, department, email, id)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    student = conn.execute(
        'SELECT * FROM students WHERE id=?', (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return "Student not found!", 404

    return render_template('edit.html', student=student)

# Delete student
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id=?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    create_table()
    app.run(debug=True)

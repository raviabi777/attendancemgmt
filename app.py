from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# Database Initialization
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY,
            student_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username and password are correct (in a real app, you'd use a more secure method)
        if username == 'student' and password == 'password':
            # Mark attendance for the student
            mark_attendance(username)
            return redirect(url_for('dashboard'))

    return render_template('index.html')

# Mark attendance for the student
def mark_attendance(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Get student ID
    cursor.execute('SELECT id FROM students WHERE username = ?', (username,))
    student_id = cursor.fetchone()[0]

    # Insert attendance record
    cursor.execute('INSERT INTO attendance (student_id) VALUES (?)', (student_id,))
    
    conn.commit()
    conn.close()

# Route for the student dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

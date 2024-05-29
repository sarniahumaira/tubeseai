from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'feedback_db'
}

# Database setup
def init_db():
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS feedback_db")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback_db.feedback (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                message TEXT NOT NULL
            )
        """)
        connection.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/')
def index():
    return render_template('feedback_form.html')

@app.route('/submit', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    if not name or not email or not message:
        flash('All fields are required!', 'error')
        return redirect(url_for('index'))

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO feedback (name, email, message) VALUES (%s, %s, %s)', (name, email, message))
        connection.commit()
        flash('Thank you for your feedback!', 'success')
    except Error as e:
        print(f"Error: {e}")
        flash('Failed to submit feedback', 'error')
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return redirect(url_for('index'))

@app.route('/feedback')
def admin():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM feedback')
        feedback_list = cursor.fetchall()
    except Error as e:
        print(f"Error: {e}")
        feedback_list = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    
    return render_template('feedbacklist.html', feedback=feedback_list)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

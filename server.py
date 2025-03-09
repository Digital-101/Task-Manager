import connexion
from flask import Flask, jsonify, request, abort, render_template
import sqlite3

# Helper function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn

# API handlers
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return jsonify([dict(task) for task in tasks])

def create_task():
    task_data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, description, completed)
        VALUES (?, ?, ?)
    ''', (task_data['title'], task_data.get('description', ''), task_data.get('completed', False)))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': task_id, **task_data}), 201

def get_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    conn.close()
    if task is None:
        abort(404, description="Task not found")
    return jsonify(dict(task))

def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return '', 204

# HTML route to render the task management UI
def index():
    return render_template('index.html')

# Create the Connexion app
app = connexion.App(__name__, specification_dir='./')
app.add_api('openapi.yaml')

# Add a route for the HTML interface
app.add_url_rule('/', 'index', index)

# Run the server
if __name__ == '__main__':
    app.run(port=5000)
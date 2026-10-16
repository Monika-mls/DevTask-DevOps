import os
import sqlite3
from pathlib import Path
from flask import Flask, redirect, render_template, request, url_for


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(DATABASE=os.environ.get('DATABASE_PATH', str(Path(__file__).parent / 'tasks.db')))
    if test_config:
        app.config.update(test_config)

    def get_connection():
        database = Path(app.config['DATABASE'])
        database.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        return conn

    with get_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )''')

    @app.get('/')
    def index():
        with get_connection() as conn:
            tasks = conn.execute('SELECT * FROM tasks ORDER BY id DESC').fetchall()
        completed = sum(task['completed'] for task in tasks)
        return render_template('index.html', tasks=tasks, completed=completed)

    @app.post('/add')
    def add_task():
        title = request.form.get('title', '').strip()
        if title and len(title) <= 200:
            with get_connection() as conn:
                conn.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
        return redirect(url_for('index'))

    @app.post('/toggle/<int:task_id>')
    def toggle_task(task_id):
        with get_connection() as conn:
            conn.execute('UPDATE tasks SET completed = 1 - completed WHERE id = ?', (task_id,))
        return redirect(url_for('index'))

    @app.post('/delete/<int:task_id>')
    def delete_task(task_id):
        with get_connection() as conn:
            conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        return redirect(url_for('index'))

    @app.get('/health')
    def health():
        return {'status': 'ok'}, 200

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)
DB_NAME = "tasks.db"


def get_db():
    """Open a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn


def init_db():
    """Create the tasks table if it does not exist yet."""
    with get_db() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS tasks (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   done INTEGER NOT NULL DEFAULT 0
               )"""
        )


@app.route("/tasks", methods=["GET"])
def list_tasks():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM tasks").fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400
    with get_db() as conn:
        cur = conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        task_id = cur.lastrowid
    return jsonify({"id": task_id, "title": title, "done": 0}), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json(silent=True) or {}
    done = 1 if data.get("done") else 0
    with get_db() as conn:
        cur = conn.execute("UPDATE tasks SET done = ? WHERE id = ?", (done, task_id))
    if cur.rowcount == 0:
        return jsonify({"error": "task not found"}), 404
    return jsonify({"id": task_id, "done": done})


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    with get_db() as conn:
        cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    if cur.rowcount == 0:
        return jsonify({"error": "task not found"}), 404
    return "", 204


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
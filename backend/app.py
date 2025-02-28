from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# Configure the SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Initialize the database
with app.app_context():
    db.create_all()

# Route to get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": task.id, "title": task.title, "completed": task.completed} for task in tasks])

# Route to add a new task
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    new_task = Task(title=data["title"])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added successfully"}), 201

# Route to update a task
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404

    data = request.json
    task.title = data.get("title", task.title)
    task.completed = data.get("completed", task.completed)
    db.session.commit()
    return jsonify({"message": "Task updated successfully"})

# Route to delete a task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

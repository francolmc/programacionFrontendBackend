from flask import Blueprint, request, jsonify
from application.extensions import db
from application.tasks.models import Task

tasks_blueprint = Blueprint("tasks", __name__, url_prefix="/api")

@tasks_blueprint.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{ "id": task.id, 'title': task.title, 'completed': task.completed } for task in tasks])

@tasks_blueprint.route("/tasks/<int:task_id>", methods=["GET"])
def get_task_by_id(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    })

@tasks_blueprint.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    new_task = Task(
    title=data["title"],
    description=data["description"])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({
        "message": "Task created successfully"
    }), 201

@tasks_blueprint.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.completed = data.get("completed", task.completed)
    db.session.commit()
    return jsonify({
        "message": "Task updated successfully"
    }), 204

@tasks_blueprint.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({
        "message": "Task deleted successfully"
    })
from flask import Blueprint, request, jsonify
from application.extensions import db
from application.tasks.models import Task

tasks_blueprint = Blueprint("tasks", __name__, url_prefix="/api")

@tasks_blueprint.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{ "id": task.id, 'title': task.title } for task in tasks])

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

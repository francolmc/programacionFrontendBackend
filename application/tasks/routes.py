from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from application.extensions import db
from application.tasks.models import Task

tasks_blueprint = Blueprint("tasks", __name__, url_prefix="/api")

@tasks_blueprint.route("/tasks", methods=["GET"])
@cross_origin()
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{ "id": task.id, 'title': task.title, 'completed': task.completed } for task in tasks])

@tasks_blueprint.route("/tasks/<int:task_id>", methods=["GET"])
@cross_origin()
def get_task_by_id(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    })

@tasks_blueprint.route("/tasks/search", methods=["GET"])
@cross_origin()
def search_tasks():
    search_text = request.args.get("q")
    if not search_text:
        return jsonify({"message": "Debes proporcionar un texto de búsqueda"}), 400

    tasks = Task.query.filter(
        (Task.title.ilike(f"%{search_text}%")) | (Task.description.ilike(f"%{search_text}%"))
    ).all()

    if not tasks:
        return jsonify({"message": "No tasks matched the search were found"}), 404

    task_data = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
        }
        for task in tasks
    ]
    return jsonify(task_data)


@tasks_blueprint.route("/tasks", methods=["POST"])
@cross_origin()
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
@cross_origin()
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.completed = data.get("completed", task.completed)
    db.session.commit()
    return jsonify({
        "message": "Task updated successfully"
    })

@tasks_blueprint.route("/tasks/<int:task_id>", methods=["DELETE"])
@cross_origin()
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({
        "message": "Task deleted successfully"
    })
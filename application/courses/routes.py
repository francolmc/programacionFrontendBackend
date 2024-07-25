from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from application.extensions import db
from application.courses.models import Course

courses_blueprint = Blueprint("courses", __name__, url_prefix="/api")

@courses_blueprint.route("/courses", methods=["GET"])
@cross_origin()
def get_courses():
    courses = Course.query.all()
    return jsonify([{ "id": course.id, 'course_name': course.course_name, 'description': course.description } for course in courses])

@courses_blueprint.route("/courses/<int:course_id>", methods=["GET"])
@cross_origin()
def get_course_by_id(course_id):
    course = Course.query.get_or_404(course_id)
    return jsonify({
        "id": course.id,
        "course_name": course.course_name,
        "description": course.description,
    })

@courses_blueprint.route("/courses/search", methods=["GET"])
@cross_origin()
def search_courses():
    search_text = request.args.get("q")
    if not search_text:
        return jsonify({"message": "Debes proporcionar un texto de búsqueda"}), 400

    courses = Course.query.filter(
        (Course.course_name.ilike(f"%{search_text}%"))
    ).all()

    if not courses:
        return jsonify({"message": "No courses matched the search were found"}), 404

    course_data = [
        {
            "id": course.id,
            "course_name": course.course_name,
            "description": course.price,
        }
        for course in courses
    ]
    return jsonify(course_data)


@courses_blueprint.route("/courses", methods=["POST"])
@cross_origin()
def create_course():
    data = request.get_json()
    new_course = Course(
    course_name=data["course_name"],
    description=data["description"])
    db.session.add(new_course)
    db.session.commit()
    return jsonify({
        "message": "Course created successfully"
    }), 201

@courses_blueprint.route("/courses/<int:course_id>", methods=["PUT"])
@cross_origin()
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    data = request.get_json()
    course.course_name = data.get("product_name", course.course_name)
    course.description = data.get("price", course.description)
    db.session.commit()
    return jsonify({
        "message": "Course updated successfully"
    })

@courses_blueprint.route("/courses/<int:course_id>", methods=["DELETE"])
@cross_origin()
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({
        "message": "Course deleted successfully"
    })
from application.extensions import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
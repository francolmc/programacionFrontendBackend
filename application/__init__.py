from flask import Flask
from application.extensions import db, migrate
from application.tasks.routes import tasks_blueprint
from application.contacts.routes import contacts_blueprint
from application.products.routes import products_blueprint
from application.courses.routes import courses_blueprint
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object("application.config.Config")
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(tasks_blueprint)
    app.register_blueprint(contacts_blueprint)
    app.register_blueprint(products_blueprint)
    app.register_blueprint(courses_blueprint)
    return app
from flask import Flask
from application.extensions import db, migrate
from application.tasks.routes import tasks_blueprint
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, ["http://localhost:5173", "http://localhost:3000"])
    app.config.from_object("application.config.Config")
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(tasks_blueprint)
    return app
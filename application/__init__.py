from flask import Flask
from application.extensions import db, migrate
from application.tasks.routes import tasks_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object("application.config.Config")
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(tasks_blueprint)
    return app
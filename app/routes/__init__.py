from flask import Flask
from .auth import auth_bp
from .users import user_pb
from .courses import courses_bp
from .lessons import lesson_bp


def register_blueprints(app: Flask):
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_pb, url_prefix='/api/user')
    app.register_blueprint(courses_bp, url_prefix='/api/course')
    app.register_blueprint(lesson_bp, url_prefix='/api/lesson')
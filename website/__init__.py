from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'PWAUJSDHJ213'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:salve@localhost/teste'
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    from .models import Restaurante, Mesa

    with app.app_context():
        db.create_all()

    return app


def create_database(app):
    db.create_all(app=app)
    print("Database created successfully")

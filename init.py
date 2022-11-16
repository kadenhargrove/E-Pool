#this file initializes the flask app and database

from flask import Flask
from user import user
from models import db
from auth import login_manager

def create_app(db):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'kjhdolfuhqwp947rq9hfpiau23r4098'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///epool.db'

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(user, url_prefix='')

    create_database(app)

    return app

def create_database(app):
    with app.app_context():
        db.create_all()
    print("created database!")
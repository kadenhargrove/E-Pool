#this file contains the database models

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Users(UserMixin, db.Model):
    id = db.Column(
        db.Integer, 
        primary_key=True)

    email = db.Column(
        db.String(100),
        nullable=False,
        unique=True)

    password = db.Column(
        db.String(200),
        primary_key=False,
        nullable=False,
        unique=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256') # create hashed password

    def check_password(self, password):
        return check_password_hash(self.password, password) # check hashed password

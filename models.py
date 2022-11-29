#this file contains the database models

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
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

    username = db.Column(
        db.String(100),
        nullable=False,
        unique=True)

    password = db.Column(
        db.String(200),
        primary_key=False,
        nullable=False,
        unique=False)

    first_name = db.Column(
        db.String(100),
        primary_key=False,
        nullable=True,
        unique=False)

    last_name = db.Column(
        db.String(100),
        primary_key=False,
        nullable=True,
        unique=False)

    bio = db.Column(
        db.String(200),
        primary_key=False,
        nullable=True,
        unique=False)
        
    frequent_locations = db.Column(
        db.String(200),
        primary_key=False,
        nullable=True,
        unique=False)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256') # create hashed password

    def check_password(self, password):
        return check_password_hash(self.password, password) # check hashed password

class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    friender_username = db.Column(db.String(100), nullable=False)
    friend_username = db.Column(db.String(100), nullable=False)

class Driver(Users):
    driver_rating = db.Column(
        db.Integer,
        nullable=True,
        unique=False)

class Rider(Users):
    rider_rating = db.Column(
        db.Integer,
        nullable=True,
        unique=False)
    
class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
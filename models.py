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
    ticketID = db.Column(
        db.Integer, 
        primary_key=True)
        
    ticketDate = db.Column(
        db.String(100),
        primary_key=False,
        nullable=True,
        unique=False)
    
    ticketComment = db.Column(
        db.String(100),
        primary_key=False,
        nullable=True,
        unique=False)
    
    

    
    
    
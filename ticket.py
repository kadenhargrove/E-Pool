from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from models import Users, db
from user import user

app = Flask(__name__)
app.secret_key = "kjhdolfuhqwp947rq9hfpiau23r4098"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///epool.db'


class Ticket():

    def __init__(self, info, ticketID, comment):
        self.info = info
        self.ticketID = ticketID
        self.comment = comment

    @app.route("/CreateTicket", methods=["POST", "GET"])
    def createTicket(self, info, ticketID):
        if request.method == "POST":
            data_form = request.form["Name", "Location", "Time", "vehicleType"]
            

    def deleteTicket(self, ticketID):
        pass


    def modifyTicket(self, ticketID):
        pass


    def commentTicket(self, ticketID):
        pass


    def likePost():
        pass


        

    

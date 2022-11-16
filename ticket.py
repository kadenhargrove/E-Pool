from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from models import Tickets, db
from user import user

ticket = Blueprint("ticket", __name__, static_folder="static", template_folder="templates")

class Ticket():

    def __init__(self, info, ticketID, comment):
        self.info = info
        self.ticketID = ticketID
        self.comment = comment

    @ticket.route("/CreateTicket", methods=["POST", "GET"])
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


        

    

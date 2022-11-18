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
            
    @ticket.route("/deleteTicket", methods=["POST", "GET"])
    def deleteTicket(self, ticketID):
        
        """
        delete the item in the database that matches the specified
        id in the url
        """
        qry = db.query(ticketID).filter(
        ticket.id==id)
        ticket = qry.first()

        if ticket:
            data_form = request.form(formdata=request.form, obj=ticket)
            if request.method == 'POST' and data_form.validate():
                # delete the item from the database
                db.delete(ticket)
                db.commit()

                flash('ticket deleted successfully')
            

    @ticket.route("/modifyTicket", methods=["POST", "GET"])
    def modifyTicket(self, ticketID):
        qry = db.query(ticketID).filter(
        ticket.id==id)
        ticket = qry.first()

        if ticket:
            data_form = request.form(formdata=request.form, obj=ticket)
            if request.method == 'POST' and data_form.validate():
                # modify ticket form database
                data_form = request.form["Name", "Location", "Time", "vehicleType"]
                
        

    @ticket.route("/commentTicket", methods=["POST", "GET"])
    def commentTicket(self, ticketID):
        qry = db.query(ticketID).filter(
        ticket.id==id)
        ticket = qry.first()
        

    @ticket.route("/likePost", methods=["POST", "GET"])
    def likePost():
        pass


        

    

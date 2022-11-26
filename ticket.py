from flask import Flask, redirect, url_for, render_template, request, session, flash, abort,Blueprint
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from models import Tickets, db
from user import user
from flask_login import login_required, current_user, logout_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

ticketClass = Blueprint("ticket", __name__, static_folder="static", template_folder="templates")

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class Ticket():

    @ticketClass.route("/ticket")
    def ticket():
        return render_template("ticket.html")  

    @ticketClass.route("/createticket", methods=["POST", "GET"])
    @login_required
    def create_ticket():
        form = PostForm()
        if form.validate_on_submit():
            post = Tickets(title=form.title.data, content=form.content.data, author=current_user.email)
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(url_for('user.home'))
        return render_template("create_ticket.html", title='New Ticket', form = form, legend = "New Ticket")

    @ticketClass.route("/post/<int:post_id>")
    def post(post_id):
        post = Tickets.query.get_or_404(post_id)
        return render_template('post.html', title=post.title, post=post)

    @ticketClass.route("/post/<int:post_id>/update", methods=["POST", "GET"])
    @login_required
    def update_post(post_id):
        post = Tickets.query.get_or_404(post_id)
        if post.author != current_user.email:
            abort(403)
        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash('Your post has been updated!', 'success')
            return redirect(url_for('ticket.post', post_id=post.id))
        elif request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.content
        return render_template("create_ticket.html", title='Update Ticket', form = form, legend="Update Ticket")

    @ticketClass.route("/post/<int:post_id>/delete", methods=["POST", "GET"])
    @login_required
    def delete_post(post_id):
        post = Tickets.query.get_or_404(post_id)
        if post.author != current_user.email:
            abort(403)
        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted!', 'success')
        return redirect(url_for('user.home'))
                
    # @ticket.route("/commentTicket", methods=["POST", "GET"])
    # def commentTicket(self, ticketID):
    #     qry = db.query(ticketID).filter(
    #     ticket.id==id)
    #     ticket = qry.first()
        

    # @ticket.route("/likePost", methods=["POST", "GET"])
    # def likePost():
    #     pass


        

    

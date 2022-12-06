from flask import Flask, redirect, url_for, render_template, request, session, flash, abort,Blueprint
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
import json
from models import Notification, Tickets, Users, db
from user import User
from flask_login import login_required, current_user, logout_user
from flask_wtf import FlaskForm
# from app.main.forms import MessageForm
from models import Message

mediator = Blueprint("mediator", __name__, static_folder="static", template_folder="templates")

class Mediator(Users):
    
    def __init__(self, username, groupchat, content):
        self._username = username
        self._groupchat = groupchat
        self._content = content
  

    def getUsername(self):
        return self._username

    def getGroup(self):
        return self._groupchat

    def getContent(self):
        return self._content
    
    
    @mediator.route('/send_message/<recipient>', methods=['GET', 'POST'])
    @login_required
    def send_message(recipient):
        user = User.query.filter_by(username=recipient).first_or_404()
        form = MessageForm()
        if form.validate_on_submit():
            msg = Message(author=current_user, recipient=user,
                        body=form.message.data)
            db.session.add(msg)
            db.session.commit()
            flash(_('Your message has been sent.'))
            return redirect(url_for('main.user', username=recipient))
        return render_template('send_message.html', title=_('Send Message'),
                            form=form, recipient=recipient)
            
        
    @mediator.route('/messages')
    @login_required
    def messages():
        current_user.last_message_read_time = datetime.utcnow()
        current_user.add_notification('unread_message_count', 0)
        db.session.commit()
    
    
    @mediator.route('/notifications')
    @login_required
    def notifications():
        since = request.args.get('since', 0.0, type=float)
        notifications = current_user.notifications.filter(
            Notification.timestamp > since).order_by(Notification.timestamp.asc())
        return jsonify([{
            'name': n.name,
            'data': n.get_data(),
            'timestamp': n.timestamp
        } for n in notifications])
#this file contains the parent class for the different epool users (drivers and riders)

from flask import Blueprint, redirect, url_for, render_template, request, flash
from models import Users, Tickets, Friends, Blocks, db
from auth import login_manager
from flask_login import login_required, logout_user, current_user, login_user

user = Blueprint("user", __name__, static_folder="static", template_folder="templates")

class User:
    @user.route("/")
    @user.route("home")
    def home():
        tickets = Tickets.query.order_by(Tickets.id.desc()).all()
        blocks = Blocks.query.all()

        block_list = []

        if current_user.is_authenticated:
            for block in blocks:
                if block.blocker_username == current_user.username and block.blocked_username != current_user.username:
                    block_list.append(block.blocked_username)

        return render_template("index.html", posts=tickets, block_list=block_list)

    @user.route("/register", methods=["POST", "GET"])
    def create_account():
        if request.method == "POST":
            user_email = request.form["email"]
            user_name = request.form["usrnm"]
            user_password = request.form["psw"]
            found_email = Users.query.filter_by(email=user_email).first()
            found_username = Users.query.filter_by(username=user_name).first()

            if found_email or found_username:
                flash("User exists, please login", 'warning')
                return redirect(url_for("user.login"))
            if len(user_password) < 8:
                flash("Password must be at least 8 characters long!", 'warning')
                return render_template("register.html")
            else:
                flash("New account created!", 'success')
                usr = Users(email = user_email, username = user_name)
                usr.set_password(user_password)
                db.session.add(usr)
                db.session.commit()
                return redirect(url_for("user.login"))
        else:
            if current_user.is_authenticated:
                flash("Already Logged In!", 'success')
                return redirect(url_for("profile.profile"))
            return render_template("register.html")

    @user.route("/login", methods=["POST", "GET"])
    def login():
        if request.method == "POST":
            user_email = request.form["email"]
            user_password = request.form["psw"]
            found_user = Users.query.filter_by(email=user_email).first()

            if not found_user:
                flash("No user found, please sign up!", 'warning')
                return redirect(url_for("user.create_account"))

            if found_user and found_user.check_password(user_password):
                login_user(found_user)
                flash("Login Successful!", 'success')
                return redirect(url_for("profile.profile"))
            
            flash("Password incorrect! Try again.", 'warning')
            return render_template("login.html")
        else:
            if current_user.is_authenticated:
                flash("Already Logged In!", 'success')
                return redirect(url_for("profile.profile"))
            return render_template("login.html")

    @user.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("You have been logged out!", 'success')
        return redirect(url_for("user.login"))
    
    @user.route("/friends")
    @login_required
    def friends():
        users = Users.query.all()
        friendships = Friends.query.all()
        blocks = Blocks.query.all()

        the_friends = []
        usernames = []
        block_list = []

        for block in blocks:
            if block.blocker_username == current_user.username and block.blocked_username != current_user.username:
                block_list.append(block.blocked_username)

        for user in users:
            usernames.append(user.username)
            for friends in friendships:
                if friends.friender_username == current_user.username and user.username == friends.friend_username and user.username != current_user.username:
                    the_friends.append(user.username)

        the_others = set(usernames) - set(the_friends) - set(block_list)

        return render_template("friends.html", the_friends=the_friends, the_others=the_others, block_list=block_list)
    
    @login_manager.user_loader
    def load_user(id):
        """Check if user is logged-in on every page load."""
        if id is not None:
            return Users.query.get(id)
        return None

    @login_manager.unauthorized_handler
    def unauthorized():
        """Redirect unauthorized users to Login page."""
        flash('Please login first!', 'error')
        return redirect(url_for('user.login'))
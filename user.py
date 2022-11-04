#this file contains the parent class for the different epool users (drivers and riders)

from flask import Blueprint, redirect, url_for, render_template, request, session, flash
from models import Users, db

user = Blueprint("user", __name__, static_folder="static", template_folder="templates")

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.myTickets = []
        self.friendList = []

    def add_friend(self, friend):
        self.friendList.append(friend)
    
    def delete_friend(self, friend):
        self.friendList.remove(friend)

    @user.route("/")
    def home():
        return render_template("index.html")

    @user.route("/register", methods=["POST", "GET"])
    def create_account():
        if request.method == "POST":
            user_email = request.form["email"]
            found_user = Users.query.filter_by(email=user_email).first()

            if found_user:
                flash("User exists, please login")
                return redirect(url_for("user.login"))
            else:
                flash("New account created!")
                usr = Users(email = user_email)
                db.session.add(usr)
                db.session.commit()
                return redirect(url_for("user.login"))
        else:
            if "user" in session:
                flash("Already Logged In!")
                return redirect(url_for("user.profile"))
            return render_template("register.html")

    @user.route("/login", methods=["POST", "GET"])
    def login():
        if request.method == "POST":
            user_email = request.form["email"]
            found_user = Users.query.filter_by(email=user_email).first()

            if not found_user:
                flash("User does not exist, please create an account!")
                return redirect(url_for("user.create_account"))

            session["user"] = user_email
            flash("Login Successful!")
            return redirect(url_for("user.profile"))
        else:
            if "user" in session:
                flash("Already Logged In!")
                return redirect(url_for("user.profile"))
            return render_template("login.html")

    @user.route("/profile", methods=["POST", "GET"])
    def profile():
        if "user" in session:
            usr_email = session["user"]
            usr = Users.query.filter_by(email=usr_email).first()
            users = Users.query.all()
            for user in users:
                print(user.email)
            return render_template("profile.html", email=usr.email)
        else:
            flash("You are not logged in!")
            return redirect(url_for("user.login"))

    @user.route("/logout")
    def logout():
        if "user" in session:
            flash("You have been logged out!", "info")
            session.pop("user", None)
            return redirect(url_for("user.login"))
        else:
            flash("You must login before logging out!")
            return redirect(url_for("user.login"))
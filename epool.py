#main epool file
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "kjhdolfuhqwp947rq9hfpiau23r4098"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///epool.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))

    def __init__(self, email):
        self.email = email

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST", "GET"])
def create_account():
    if request.method == "POST":
        user_email = request.form["email"]
        found_user = User.query.filter_by(email=user_email).first()

        if found_user:
            flash("User exists, please login")
            return redirect(url_for("login"))
        else:
            flash("New account created!")
            usr = User(email = user_email)
            db.session.add(usr)
            db.session.commit()
            return redirect(url_for("login"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("profile"))
        return render_template("register.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_email = request.form["email"]
        found_user = User.query.filter_by(email=user_email).first()

        if not found_user:
            flash("User does not exist, please create an account!")
            return redirect(url_for("create_account"))

        session["user"] = user_email
        flash("Login Successful!")
        return redirect(url_for("profile"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("profile"))
        return render_template("login.html")

@app.route("/profile", methods=["POST", "GET"])
def profile():
    if "user" in session:
        usr_email = session["user"]
        usr = User.query.filter_by(email=usr_email).first()
        users = User.query.all()
        for user in users:
            print(user.email)
        return render_template("profile.html", email=usr.email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        flash("You have been logged out!", "info")
        session.pop("user", None)
        return redirect(url_for("login"))
    else:
        flash("You must login before logging out!")
        return redirect(url_for("login"))

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()
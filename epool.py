#main epool file
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from user import User

app = Flask(__name__)
app.secret_key = "kjhdolfuhqwp947rq9hfpiau23r4098"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        flash("Login Successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
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
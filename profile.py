# This files contains the profile class that contains user information

from flask import Blueprint, redirect, url_for, render_template, request, session, flash
from models import Users, db
from flask_login import login_required, logout_user, current_user, login_user

prof = Blueprint("profile", __name__, static_folder="static", template_folder="templates")

class Profile:
    def __init__(self, first_name, last_name, bio, frequent_locations):
        self.first_name = first_name
        self.last_name = last_name
        self.bio = bio
        self.frequent_locations = frequent_locations

    @prof.route("/profile", methods=["POST", "GET"])
    @login_required
    def profile():
        user_email = current_user.email
        fname = current_user.first_name
        users = Users.query.all()
        for user in users:
            print("Email: " + user.email + "\nPassword: " + user.password)
            if user.first_name:
                print("First Name: " + user.first_name)
            if user.last_name:
                print("Last Name: " + user.last_name)
        return render_template("profile.html", email=user_email, first_name=fname)

    @prof.route("/editprofile", methods=["POST", "GET"])
    @login_required
    def edit_profile():
        fname = current_user.first_name
        lname = current_user.last_name
        bio = current_user.bio
        user_email = current_user.email
        freqLoc = current_user.frequent_locations

        if request.method == "POST":
            first_name = request.form["fname"]
            current_user.first_name = first_name
            db.session.commit()

            last_name = request.form["lname"]
            current_user.last_name = last_name
            db.session.commit()

            bio = request.form["bio"]
            current_user.bio = bio
            db.session.commit()

            frequent_locations = request.form["freqLoc"]
            current_user.frequent_locations = frequent_locations
            db.session.commit()

            return redirect(url_for("profile.profile"))
        else:
            return render_template("editprofile.html", email=user_email, first_name=fname, last_name=lname, bio=bio, frequent_locations=freqLoc)
# This files contains the profile class that contains user information

from flask import Blueprint, redirect, url_for, render_template, request, session, flash
from models import Users, db
from flask_login import login_required, logout_user, current_user, login_user

prof = Blueprint("profile", __name__, static_folder="static", template_folder="templates")

class Profile:
    def __init__(self, first_name, last_name, bio):
        self.first_name = first_name
        self.last_name = last_name
        self.bio = bio

    @prof.route("/profile", methods=["POST", "GET"])
    @login_required
    def profile():
        user_email = current_user.email
        fname = current_user.first_name
        users = Users.query.all()
        for user in users:
            print("Email: " + user.email + " Password: " + user.password)
        return render_template("profile.html", email=user_email, first_name=fname)

    @prof.route("/editprofile", methods=["POST", "GET"])
    @login_required
    def edit_profile():
        user_email = current_user.email
        if request.method == "POST":
            first_name = request.form["fname"]
            current_user.first_name = first_name
            db.session.commit()
            return redirect(url_for("profile.profile"))
        else:
            return render_template("editprofile.html", email=user_email)
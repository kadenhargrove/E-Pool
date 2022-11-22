# This files contains the profile class that contains user information

from flask import Blueprint, redirect, url_for, render_template, request, flash
from models import Users, db
from flask_login import login_required, current_user

prof = Blueprint("profile", __name__, static_folder="static", template_folder="templates")

class Profile:
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
            if user.bio:
                print("Bio: " + user.bio)
            if user.frequent_locations:
                print("Frequent Locations: " + user.frequent_locations)
            print()
        return render_template("profile.html", email=user_email, first_name=fname)

    # method for edit profile and create profile
    @prof.route("/editprofile", methods=["POST", "GET"])
    @login_required
    def edit_profile():
        fname = current_user.first_name
        lname = current_user.last_name
        bio = current_user.bio
        user_email = current_user.email
        freqLoc = current_user.frequent_locations

        if request.method == "POST":
            changed = False

            first_name = request.form["fname"]
            if first_name != '':
                current_user.first_name = first_name
                changed = True

            last_name = request.form["lname"]
            if last_name != '':
                current_user.last_name = last_name
                changed = True

            bio = request.form["bio"]
            if bio != '':
                current_user.bio = bio
                changed = True

            frequent_locations = request.form["freqLoc"]
            if frequent_locations != '':
                current_user.frequent_locations = frequent_locations
                changed = True
            
            if changed:
                flash("Profile updated successfully!", 'success')
                db.session.commit()
            return redirect(url_for("profile.profile"))
        else:
            return render_template("editprofile.html", email=user_email, first_name=fname, last_name=lname, bio=bio, frequent_locations=freqLoc)

    @prof.route("/deleteaccount", methods=["POST", "GET"])
    @login_required
    def delete_account():
        return render_template("delete_account.html")
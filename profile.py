# This files contains the profile class that contains user information

from flask import Blueprint, redirect, url_for, render_template, request, flash
from models import Users, db
from flask_login import login_required, current_user, logout_user

prof = Blueprint("profile", __name__, static_folder="static", template_folder="templates")

class Profile:
    @prof.route("/profile", methods=["POST", "GET"])
    @login_required
    def profile():
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
        return render_template("profile.html")

    # method for edit profile and create profile
    @prof.route("/editprofile", methods=["POST", "GET"])
    @login_required
    def edit_profile():
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
            return render_template("editprofile.html")

    # method for deleting user account
    @prof.route("/deleteaccount", methods=["POST", "GET"])
    @login_required
    def delete_account():
        if request.method == "POST":
            password1 = request.form["psw1"]
            password2 = request.form["psw2"]
            
            #check if password is valid
            if current_user.check_password(password1):
                if password1 == password2: # check if passwords match
                    #delete account
                    db.session.delete(current_user)
                    db.session.commit()
                    logout_user()
                    flash("Your account has been successfully deleted.", "success")
                    return redirect(url_for("user.login"))
                else:
                    flash("Passwords do not match.", "warning")
                    return redirect(url_for("profile.delete_account"))

            flash("Password incorrect!", "error")
            return redirect(url_for("profile.delete_account"))
        else:
            return render_template("delete_account.html")
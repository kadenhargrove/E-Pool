# This files contains the profile class that contains user information

from flask import Blueprint, redirect, url_for, render_template, request, flash
from models import Users, Friends, Tickets, Blocks, db, Comment, Like
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
                    #delete user posts
                    tickets = Tickets.query.filter_by(author=current_user.username)
                    for ticket in tickets:
                        db.session.delete(ticket)

                    #delete user friendships
                    friender = Friends.query.filter_by(friender_username=current_user.username)
                    for friendship in friender:
                        db.session.delete(friendship)

                    friend = Friends.query.filter_by(friend_username=current_user.username)
                    for friendship in friend:
                        db.session.delete(friendship)

                    #delete user blockships
                    blocker = Blocks.query.filter_by(blocker_username=current_user.username)
                    for blockship in blocker:
                        db.session.delete(blockship)

                    blocked = Blocks.query.filter_by(blocked_username=current_user.username)
                    for blockship in blocked:
                        db.session.delete(blockship)

                    #delete user comments
                    comments = Comment.query.filter_by(author=current_user.username)
                    for comment in comments:
                        db.session.delete(comment)

                    #delete user likes
                    likes = Like.query.filter_by(author=current_user.username)
                    for like in likes:
                        db.session.delete(like)

                    #delete account
                    db.session.delete(current_user)

                    #commit db changes
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

    # for other users' profile
    @prof.route("/profile/<username>", methods=['GET', 'POST'])
    @login_required
    def other(username):
        the_user = Users.query.filter_by(username=username).first()
        found_friendship = Friends.query.filter_by(friender_username=current_user.username, friend_username = username).first()
        blocked = Blocks.query.filter_by(blocker_username=current_user.username, blocked_username = username).first()
        return render_template("other_profile.html", the_user=the_user, found_friendship=found_friendship, blocked=blocked)
    
    @prof.route("/profile/<username>/addfriend", methods=['GET', 'POST'])
    @login_required
    def add_friend(username):
        the_user = Users.query.filter_by(username=username).first()
        if request.method == "POST":
            found_block = Blocks.query.filter_by(blocker_username=current_user.username, blocked_username = username).first()
            if found_block:
                flash("Cannot friend blocked user!", 'warning')
                return redirect(url_for("user.friends"))

            found_friendship = Friends.query.filter_by(friender_username=current_user.username, friend_username = username).first()
            if found_friendship:
                flash("Already friends!", 'success')
                return redirect(url_for("user.friends"))
                
            elif the_user == current_user:
                    flash('Cannot friend self!', 'warning')
                    return redirect(url_for("user.friends"))
            else:
                friendship = Friends(friender_username=current_user.username, friend_username = username)
                forced_friendship = Friends(friender_username=username, friend_username = current_user.username)
                db.session.add(friendship)
                db.session.add(forced_friendship)
                db.session.commit()
                flash('Friend added!', 'success')
                return redirect(url_for("user.friends"))
        else:
            return render_template("other_profile.html", the_user=the_user)

    @prof.route("/profile/<username>/deletefriend", methods=['GET', 'POST'])
    @login_required
    def delete_friend(username):
        the_user = Users.query.filter_by(username=username).first()
        if request.method == "POST":
            friendship = Friends.query.filter_by(friender_username=current_user.username, friend_username = username).first()
            forced_friendship = Friends.query.filter_by(friender_username=username, friend_username = current_user.username).first()
            db.session.delete(friendship)
            db.session.delete(forced_friendship)
            db.session.commit()
            flash('Friend removed!', 'success')
            return redirect(url_for("user.friends"))
        else:
            return render_template("other_profile.html", the_user=the_user)
    
    @prof.route("/profile/<username>/block", methods=['GET', 'POST'])
    @login_required
    def block(username):
        the_user = Users.query.filter_by(username=username).first()
        if request.method == "POST":
            found_block = Blocks.query.filter_by(blocker_username=current_user.username, blocked_username = username).first()
            if found_block:
                flash("Already blocked user!", 'success')
                return redirect(url_for("user.friends"))
                
            elif the_user == current_user:
                    flash('Cannot block self!', 'warning')
                    return redirect(url_for("user.friends"))
            else:
                #make block entry
                blockship = Blocks(blocker_username=current_user.username, blocked_username = username)
                forced_blockship = Blocks(blocker_username = username, blocked_username=current_user.username)
                db.session.add(blockship)
                db.session.add(forced_blockship)

                #end friendship
                friendship = Friends.query.filter_by(friender_username=current_user.username, friend_username = username).first()
                forced_friendship = Friends.query.filter_by(friender_username=username, friend_username = current_user.username).first()
                if friendship:
                    db.session.delete(friendship)
                if forced_friendship:
                    db.session.delete(forced_friendship)

                db.session.commit()
                flash('User blocked!', 'success')
                return redirect(url_for("user.friends"))
        else:
            return render_template("other_profile.html", the_user=the_user)

    @prof.route("/profile/<username>/unblock", methods=['GET', 'POST'])
    @login_required
    def unblock(username):
        the_user = Users.query.filter_by(username=username).first()
        if request.method == "POST":
            blockship = Blocks.query.filter_by(blocker_username=current_user.username, blocked_username = username).first()
            forced_blockship = Blocks.query.filter_by(blocker_username=username, blocked_username = current_user.username).first()
            db.session.delete(blockship)
            db.session.delete(forced_blockship)
            db.session.commit()
            flash('User unblocked!', 'success')
            return redirect(url_for("user.friends"))
        else:
            return render_template("other_profile.html", the_user=the_user)
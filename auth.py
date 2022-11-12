# This file creates the login manager for flask-login
# This allows both init.py and user.py to import login_manager without circular imports

from flask_login import LoginManager

login_manager = LoginManager()
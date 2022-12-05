"""
This file (test_user.py) contains the functional tests for the `user` blueprint.

These tests use GETs and POSTs to different URLs to check for the proper behavior
of the `user` blueprint.
"""

def test_home(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' or /home page is requested (GET) or is posted to (POST)
    THEN check that the response is valid
    """
    # test that get method returns working home page
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Welcome to E-Pool" in response.data

    response = test_client.get('/home')
    assert response.status_code == 200
    assert b"Welcome to E-Pool" in response.data

    # test that post method is not allowed
    response = test_client.post('/')
    assert not response.status_code == 200
    assert response.status_code == 405
    assert not b"Welcome to E-Pool" in response.data

    response = test_client.post('/home')
    assert not response.status_code == 200
    assert response.status_code == 405
    assert not b"Welcome to E-Pool" in response.data

def test_create_account(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is requested (GET) or is posted to (POST)
    THEN check that the response is valid
    """
    # test that get method returns working register page
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data
    assert b"Have an account?" in response.data

    # test that post method creates a new user account properly
    response = test_client.post('/register',
                                data=dict(email='khargr2@ilstu.edu', 
                                usrnm='khargr2', psw='Epoolisgreat123'), 
                                follow_redirects=True)
    
    assert response.status_code == 200
    assert b'New account created!' in response.data
    assert b'Login' in response.data
    assert b'New around here?' in response.data

    # test that post method fails registration with found email
    response = test_client.post('/register',
                                data=dict(email='khargr2@ilstu.edu', 
                                usrnm='kaden123', psw='Epoolisgreat123'), 
                                follow_redirects=True)
    
    assert response.status_code == 200
    assert b'User exists, please login' in response.data
    assert b'Login' in response.data
    assert b'New around here?' in response.data

    # test that post method fails registration with found username
    response = test_client.post('/register',
                                data=dict(email='kaden123@ilstu.edu', 
                                usrnm='khargr2', psw='Epoolisgreat123'), 
                                follow_redirects=True)
    
    assert response.status_code == 200
    assert b'User exists, please login' in response.data
    assert b'Login' in response.data
    assert b'New around here?' in response.data

    # test that post method fails registration with password < 8 characters
    response = test_client.post('/register',
                                data=dict(email='albert123@ilstu.edu', 
                                usrnm='albert123', psw='Epool'), 
                                follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Password must be at least 8 characters long!' in response.data
    assert not b'New account created!' in response.data
    assert b'Register' in response.data
    assert b'Have an account?' in response.data

def test_create_account_already_logged_in(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is requested (GET) with a user that is already logged in
    THEN check that the response is valid
    """
    # test that get method returns profile page for user who is already logged in
    response = test_client.get('/register', follow_redirects=True)
    assert response.status_code == 200
    assert b"Already Logged In!" in response.data
    assert b"My Profile" in response.data
    assert b"User: default" in response.data
    assert b"Email: defaultuser@gmail.com" in response.data

def test_login_no_user_found(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST) and no user exists
    THEN check that the response is valid
    """
    # test that post method fails login with no existing user found
    response = test_client.post('/login', data=dict(email='newuser@gmail.com', 
                                                    psw='Hello123'), follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Register" in response.data
    assert not b'Login Successful!' in response.data
    assert b'No user found, please sign up!' in response.data
    assert b"Have an account?" in response.data

def test_login(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET) or is posted to (POST)
    THEN check that the response is valid
    """
    # test that get method returns working login page
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"New around here?" in response.data

    # test that post method logs user in properly
    response = test_client.post('/login', data=dict(email='defaultuser@gmail.com', psw='Epoolbetterthanuber'), follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Login Successful!' in response.data
    assert b"My Profile" in response.data
    assert b"User: default" in response.data
    assert b"Email: defaultuser@gmail.com" in response.data

    # test that post method fails login with incorrect password (password should be "Golakers34")
    response = test_client.post('/login', data=dict(email='shaq@gmail.com', psw='Golakers344'), follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"New around here?" in response.data
    assert not b'Login Successful!' in response.data
    assert b'Password incorrect! Try again.' in response.data

def test_login_already_logged_in(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET) and user is already logged in
    THEN check that the response is valid
    """
    # test that get method returns profile page for user who is already logged in
    response = test_client.get('/login', follow_redirects=True)
    assert response.status_code == 200
    assert b"Already Logged In!" in response.data
    assert b"My Profile" in response.data
    assert b"User: default" in response.data
    assert b"Email: defaultuser@gmail.com" in response.data

def test_logout(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is requested (GET)
    THEN check that the response is valid
    """
    # test that get method returns login page if no user is logged in
    response = test_client.get('/logout', follow_redirects=True)

    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"New around here?" in response.data
    assert b"Please login first!" in response.data
    assert not b"You have been logged out!" in response.data

    # test that get method logs user out properly (with logged in user)
    test_client.post('/login', data=dict(email='shaq@gmail.com', 
                                        psw='Golakers34'), follow_redirects=True)
    response = test_client.get('/logout', follow_redirects=True)

    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"New around here?" in response.data
    assert not b"Please login first!" in response.data
    assert b"You have been logged out!" in response.data

def test_friends(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/friends' page is requested (GET)
    THEN check that the response is valid
    """
    # test that get method returns login page if no user is logged in
    response = test_client.get('/friends', follow_redirects=True)

    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"New around here?" in response.data
    assert b"Please login first!" in response.data
    assert not b"Friends" in response.data
    assert not b"Blocked" in response.data
    assert not b"Other Users" in response.data

    # test that get method loads friends page properly (with logged in user)
    test_client.post('/login', data=dict(email='shaq@gmail.com', 
                                        psw='Golakers34'), follow_redirects=True)
    response = test_client.get('/friends', follow_redirects=True)

    assert response.status_code == 200
    assert not b"Login" in response.data
    assert not b"New around here?" in response.data
    assert not b"Please login first!" in response.data
    assert b"Friends" in response.data
    assert b"Blocked" in response.data
    assert b"Other Users" in response.data
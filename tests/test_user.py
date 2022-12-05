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

    # # test that get method returns profile page for user who is already logged in
    # response = test_client.post('/register', data=dict(email='defaultuser@gmail.com', usrnm='default', 
    #                                         psw='Epoolbetterthanuber'), follow_redirects=True)
    # assert response.status_code == 200
    # assert b"Already Logged In!" in response.data
    # assert b"My Profile" in response.data
    # assert b"User: default" in response.data
    # assert b"Email: defaultuser@gmail.com" in response.data

    # test that post method creates a user account properly
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
                                data=dict(email='alber123@ilstu.edu', 
                                usrnm='albert123', psw='Epool'), 
                                follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Password must be at least 8 characters long!' in response.data
    assert not b'New account created!' in response.data
    assert b'Register' in response.data
    assert b'Have an account?' in response.data

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
    # response = test_client.post('/login', data=dict(email='defaultuser@gmail.com', psw='Epoolbetterthanuber'), follow_redirects=True)
    
    # assert response.status_code == 200
    # assert b'Login Successful!' in response.data
    # assert b"My Profile" in response.data
    # assert b"User: default" in response.data
    # assert b"Email: defaultuser@gmail.com" in response.data
"""
This file (test_profile.py) contains the functional tests for the `profile` blueprint.

These tests use GETs and POSTs to different URLs to check for the proper behavior
of the `profile` blueprint.
"""

def test_profile(init_database, test_client):
    test_client.post('/login',
                     data=dict(email='defaultuser@gmail.com', psw='Epoolbetterthanuber'), 
                     follow_redirects=True)
    
    response = test_client.post('/profile', follow_redirects=True)
    assert response.status_code == 200
    
    
def test_edit_profile(init_database, test_client):
    # First, we need to log in to the application
    test_client.post('/login',
                     data=dict(email='defaultuser@gmail.com', psw='Epoolbetterthanuber'), 
                     follow_redirects=True)

    # Next, we can test the /editprofile route
    response = test_client.post('/profile', follow_redirects=True)

    # Ensure that the request was successful (response code 200)
    assert response.status_code == 200

    response = test_client.post('/editprofile', data=dict(
    fname='User',
    lname='Name',
    bio='This is my profile',
    freqLoc='Chicago, IL'
    ), follow_redirects=True)

    # Ensure that the request was successful (response code 200)
    assert response.status_code == 200

    # Test that the response contains the expected data
    assert b"User Name" in response.data
    assert b"This is my profile" in response.data
    assert b"Chicago, IL" in response.data
    
def test_delete_account(init_database, test_client):
    # First, we need to log in to the application
    test_client.post('/login',
                     data=dict(email='defaultuser@gmail.com', psw='Epoolbetterthanuber'), 
                     follow_redirects=True)

    # Next, we can test the /deleteaccount route
    response = test_client.post('/deleteaccount', data=dict(psw1='Epoolbetterthanuber', psw2='Epoolbetterthanuber'), follow_redirects=True)

    assert response.status_code == 200

    #next we need to test that the two passwords are the same
    assert b"Your account has been successfully deleted.", "sucess"
    
    #next we need to test what happens when password 2 is incorrect
    response = test_client.post('/deleteaccount', data=dict(psw1='Epoolbetterthanuber', psw2='Epoolbetterthar'), follow_redirects=True)

    assert b"Passwords do not match.", "warning"

    #next we need to test what happens when password 1 is incorrect
    response = test_client.post('/deleteaccount', data=dict(psw1='Epoolbetterthan', psw2='Epoolbetterthanuber'), follow_redirects=True)
    assert b"Password incorrect!", "error"



def test_add_friend(init_database, test_client):
    # First, we need to log in to the application
    test_client.post('/login',
                     data=dict(email='defaultuser@gmail.com', psw='Epoolbetterthanuber'), 
                     follow_redirects=True)
                     
     # add the user as a friend
    response = test_client.post('/profile/shaqoneil/addfriend', data=dict(
        friender_username="default",
        friend_username="shaqoneil"
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b"Friend added!", "success"

    # check if user is already your friend
    response = test_client.post('/profile/shaqoneil/addfriend', data=dict(
        friender_username="default",
        friend_username="shaqoneil"
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b"Already friends!", "success"

    # cannot friend yourself
    response = test_client.post('/profile/default/addfriend', data=dict(
        friender_username="default",
        friend_username="shaqoneil"
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b"Cannot friend self!", "warning"

    # cannot friend a blocked user
    response = test_client.post('/profile/shaqoneil/block', data=dict(
        blocker_username="default",
        blocked_username="shaqoneil"
    ), follow_redirects=True)

    assert response.status_code == 200

    response = test_client.post('/profile/shaqoneil/addfriend', data=dict(
        friender_username="default",
        friend_username="shaqoneil"
    ), follow_redirects=True)

    assert b"Cannot friend blocked user!", "warning"

    
def test_delete_friend(init_database, test_client):
    # add the user as a friend
    response = test_client.post('/profile/shaqoneil/addfriend', data=dict(
        friender_username="default",
        friend_username="shaqoneil"
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b"Friend added!", "sucess"
    # delete the friend
    response = test_client.post('/profile/shaqoneil/deletefriend', data=dict(
        username="shaqoneil"
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b"Friend removed!", "sucess" in response.data


def test_block(init_database, test_client):
     # block the user
    response = test_client.post('/profile/shaqoneil/block', data=dict(
        blocker_username="default",
        blocked_username="shaqoneil"
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b"User blocked!", "success" in response.data
    
    # user is already blocked
    response = test_client.post('/profile/shaqoneil/block', data=dict(
        blocker_username="default",
        blocked_username="shaqoneil"
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b"Already blocked user!", "success" in response.data

    # cannot block yourself
    response = test_client.post('/profile/default/block', data=dict(
        blocker_username="default",
        blocked_username="shaqoneil"
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b"Cannot block self!", "warning" in response.data
    
def test_unblock(init_database, test_client):
    # block the user
    response = test_client.post('/profile/shaqoneil/block', data=dict(
        blocker_username="default",
        blocked_username="shaqoneil"
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b"User blocked!", "success" in response.data
     # unblock the user
    response = test_client.post('/profile/shaqoneil/unblock', data=dict(
        username="shaqoneil"
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b"User unblocked!", "success" in response.data
    
    

    
 
  





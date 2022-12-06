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
    first_name='User',
    last_name='Name',
    bio='This is my profile',
    frequent_locations='Chicago, IL'
), follow_redirects=True)

    # Ensure that the request was successful (response code 200)
    assert response.status_code == 200

    # Test that the response contains the expected data
    assert b"User Name" in response.data
    assert b"This is my profile" in response.data
    assert b"Chicago, IL" in response.data
    
#def test_delete_account(init_database, test_client):
    
    
    

def test_add_friend(init_database, test_client):
     # add the user as a friend
    response = test_client.post('/profile/shaqoneil/addfriend', data=dict(
        friender_username="default",
        friend_username="shaqoneil"
    ), follow_redirects=True)
    assert response.status_code == 200
     # get the friends page
    test_client.post('/login',
                     data=dict(email='defaultuser@gmail.com', psw='Epoolbetterthanuber'), 
                     follow_redirects=True)

    response = test_client.get('/friends', follow_redirects=True)
    assert response.status_code == 200
    # verify that the friend was added
    assert b"shaqoneil" in response.data


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
    
    

    
 
  





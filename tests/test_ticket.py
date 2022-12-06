"""
This file (test_ticket.py) contains the functional tests for the `ticket` blueprint.

These tests use GETs and POSTs to different URLs to check for the proper behavior
of the `user` blueprint.
"""

def test_ticket(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/ticket' page is requested (GET)
    THEN check that the response is valid
    """
    # test that get method returns working home page
    response = test_client.get('/ticket')
    assert response.status_code == 200
    assert b"E-Pool Tickets" in response.data

def test_create_ticket(test_client, login_default_user, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/create_ticket' page is requested (GET) or is posted to (POST)
    THEN check that the response is valid
    """
    # test that get method loads create ticket page properly
    response = test_client.get('/createticket', follow_redirects=True)
    assert response.status_code == 200
    assert b'New Ticket' in response.data

    # test that post method creates ticket properly
    response = test_client.post('/createticket', data=dict(ticketTitle="First post", 
                                                            ticketContent="Testing!"), 
                                                            follow_redirects=True)
    assert response.status_code == 200
    assert b'Your post has been created!' in response.data
    assert b'Newly and Improved Craigslist Uber' in response.data
    assert b'First post' in response.data

def test_post(test_client, login_default_user, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/post/<int:post_id>' page is requested (GET)
    THEN check that the response is valid
    """
    # test that get method loads post page properly (author post)
    response = test_client.get('/post/12', follow_redirects=True)
    assert response.status_code == 200

    # test that get method loads post page properly (other user post)
    response = test_client.get('/post/13', follow_redirects=True)
    assert response.status_code == 200

def test_update_post(test_client, login_default_user, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/post/<int:post_id>/update' page is requested (GET) or is posted to (POST)
    THEN check that the response is valid
    """
    # test that get method loads update post page properly (author post)
    response = test_client.get('/post/12/update', follow_redirects=True)
    assert response.status_code == 200
    assert b'Update Ticket' in response.data

    # test that get method fails to load update post page (other user post)
    response = test_client.get('/post/13/update', follow_redirects=True)
    assert not response.status_code == 200
    assert response.status_code == 403
    assert not b'Update Ticket' in response.data

    # test that post method updates post properly
    response = test_client.post('/post/12/update', data=dict(ticketTitle="My Test Post", 
                                                            ticketContent="This is a test post."), 
                                                            follow_redirects=True)
    assert response.status_code == 200
    assert not response.status_code == 403
    assert not b'Update Ticket' in response.data
    assert b'My Test Post' in response.data
    assert b'Your post has been updated!' in response.data

def test_delete_post(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/delete_post' page is posted to (POST)
    THEN check that the response is valid
    """
    # test that post method deletes post properly
    response = test_client.post('/post/12/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Your post has been deleted!' in response.data
    assert b'Newly and Improved Craigslist Uber' in response.data # reaches home page

    # test that post method fails to delete other users' post
    response = test_client.post('/post/13/delete', follow_redirects=True)
    assert not response.status_code == 200
    assert response.status_code == 403
    assert not b'Your post has been deleted!' in response.data
    assert not b'Newly and Improved Craigslist Uber' in response.data # does not reach home page

def test_create_comment(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/create_comment/<int:post_id>' page is posted to (POST)
    THEN check that the response is valid
    """
    # test that post method creates comments properly
    response = test_client.post('/create-comment/12', 
                                data=dict(text="This is a comment"), 
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Newly and Improved Craigslist Uber' in response.data # reaches home page

    # test that post fails to create comment with empty comment
    response = test_client.post('/create-comment/12', 
                                data=dict(text=""), 
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Newly and Improved Craigslist Uber' in response.data # reaches home page
    assert b'Comment cannot be empty.' in response.data

    # test that post fails to create comment with nonexistent post
    response = test_client.post('/create-comment/199', 
                                data=dict(text="Hello"), 
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Newly and Improved Craigslist Uber' in response.data # reaches home page
    
def test_delete_comment(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/delete-comment/<comment_id>' page is requested (GET)
    THEN check that the response is valid
    """
    test_client.post('/create-comment/12', 
                    data=dict(id=4, text="This is a comment"), 
                    follow_redirects=True)

    # test that get method deletes comment properly
    response = test_client.get('/delete-comment/4', follow_redirects=True)
    assert response.status_code == 200
    assert b'Newly and Improved Craigslist Uber' in response.data # reaches home page

    # test that get method fails to delete nonexistent comment
    response = test_client.get('/delete-comment/4', follow_redirects=True)
    assert response.status_code == 200
    assert b'Newly and Improved Craigslist Uber' in response.data # reaches home page
    assert b'Comment does not exist.' in response.data

def test_like(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/like-post/<tickets_id>' page is requested (GET)
    THEN check that the response is valid
    """
    # test that get method likes post properly
    response = test_client.get('/like-post/13', follow_redirects=True)
    assert response.status_code == 200
    assert b'Newly and Improved Craigslist Uber' in response.data # reaches home page
    assert b'1' in response.data

    # test that get method unlikes post properly
    response = test_client.get('/like-post/13', follow_redirects=True)
    assert response.status_code == 200
    assert b'Newly and Improved Craigslist Uber' in response.data # reaches home page
    assert b'0' in response.data

    # test that get method fails to like nonexistent post
    response = test_client.get('/like-post/19', follow_redirects=True)
    assert response.status_code == 200
    assert b'Newly and Improved Craigslist Uber' in response.data # reaches home page
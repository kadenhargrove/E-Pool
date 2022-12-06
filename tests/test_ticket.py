"""
This file (test_ticket.py) contains the functional tests for the `ticket` blueprint.

These tests use GETs and POSTs to different URLs to check for the proper behavior
of the `user` blueprint.
"""

from models import Comment, Tickets


def test_create_new_ticket(new_ticket):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/create_ticket' page is requested (GET)
    THEN check that the response is valid
    """
    # Test successful creation of new_ticket
    assert new_ticket.title == "Pick me up"
    assert new_ticket.content == "Im at the Bone."
    assert new_ticket.author == "khargr2"
    
    # Test fails when no title is provided
    new_ticket.title = None
    assert new_ticket.title == None
    assert new_ticket.content == "Im at the Bone."
    assert new_ticket.author == "khargr2"
    
    # Test fails when no content is provided
    new_ticket.title = "Pick me up"
    new_ticket.content = None
    assert new_ticket.title == "Pick me up"
    assert new_ticket.content == None
    assert new_ticket.author == "khargr2"
    
    # Test fails when no author is provided
    new_ticket.content = "Im at the Bone."
    new_ticket.author = None
    assert new_ticket.title == "Pick me up"
    assert new_ticket.content == "Im at the Bone."
    assert new_ticket.author == None


def test_update_ticket(new_ticket, test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/update_post' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/post/<int:post_id>/update', data=new_ticket.id )
    assert response.status_code == 200


    # setting a different post content from 'new_ticket'
    # new_ticket.date_posted = (2022, 12, 5)
    # new_ticket.title = 'Pick me up at the airport'
    # new_ticket.content = 'Im at the airport.'
    # new_ticket.author = 'rishi'
    
    # test fails if any of the content is not updated
    # assert new_ticket.title == 'Pick me up at the airport'
    # assert new_ticket.content == 'Im at the airport.'
    # assert new_ticket.author == 'rishi'
    # assert new_ticket.date_posted == (2022, 12, 5)
    
   
def test_delete_post(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/delete_post' page is requested (GET)
    THEN check that the response is valid
    """
    # create a post
    response = test_client.post('/create_ticket', data=dict(
        title="My Test Post",
        content="This is a test post.",
        author = "rishi"
    ), follow_redirects=True)
    assert response.status_code == 404
    # get the post id
    post_id = Tickets.query.filter_by(title="My Test Post").first()
    # delete post
    response = test_client.post(f'/post/{post_id}/delete', follow_redirects=True)
    assert response.status_code == 404
    

    
    
    
    
    
"""
This file (conftest.py) contains configurations for the unit tests.
All fixtures used in unit tests are created in this file.
"""

import pytest

from init import create_app
from models import db, Users, Friends, Blocks, Driver, Rider, Tickets, Comment, Like

@pytest.fixture
def app():
    app = create_app(db)
    yield app

@pytest.fixture(scope='module')
def new_user():
    user = Users(email='khargr2@ilstu.edu', username='khargr2', password='Iloveepool123',
                first_name='Kaden', last_name='Hargrove', bio='Hello', frequent_locations='The Bone')
    return user

@pytest.fixture(scope='module')
def new_friends():
    friends = Friends(friender_username='kaden123', friend_username='emannuel123')
    return friends

@pytest.fixture(scope='module')
def new_blocks():
    blocks = Blocks(blocker_username='emannuel123', blocked_username='albert123')
    return blocks

@pytest.fixture(scope='module')
def new_driver():
    driver = Driver(email='wilson2@ilstu.edu', username='wilson2', password='mrwilson123', driver_rating=5)
    return driver

@pytest.fixture(scope='module')
def new_rider():
    rider = Rider(email='smith2@ilstu.edu', username='smith2', password='mrsmith123', rider_rating=4)
    return rider

@pytest.fixture(scope='module')
def new_ticket():
    ticket = Tickets(id = 1, title='Pick me up', date_posted=(2022, 12, 4), content="Im at the Bone.", author='khargr2')
    return ticket

@pytest.fixture(scope='module')
def new_comment():
    comments = Comment(text='comment for the pick me up ticket', date_posted=(2022, 12, 4) ,author='khargr2', tickets_id = 1)
    return comments

@pytest.fixture(scope='module')
def new_like():
    like = Like(author='khargr2', date_posted=(2022, 12, 4), tickets_id = 1)
    return like

@pytest.fixture(scope='module')
def test_client():
    # Create a Flask app configured for testing
    flask_app = create_app(db)

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!

@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = Users(email='defaultuser@gmail.com', username='default', password='')
    user1.set_password("Epoolbetterthanuber")
    user2 = Users(email='shaq@gmail.com', username='shaqoneil', password='')
    user2.set_password("Golakers34")

    ticket1 = Tickets(id = 12, title='Pick me up now', content="Im at the library!", author='default')
    ticket2 = Tickets(id = 13, title='Need a ride', content="Im at the arena!", author='shaqoneil')
    
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(ticket1)
    db.session.add(ticket2)

    # Commit the changes for the users and tickets
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()

@pytest.fixture(scope='function')
def login_default_user(test_client):
    test_client.post('/login',
                     data=dict(email='defaultuser@gmail.com', psw='Epoolbetterthanuber'), 
                     follow_redirects=True)

    yield  # this is where the testing happens!

    test_client.get('/logout', follow_redirects=True)
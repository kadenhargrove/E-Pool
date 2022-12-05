import pytest

from init import create_app
from models import db, Users, Friends, Blocks, Driver, Rider, Tickets

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
    ticket = Tickets(title='Pick me up', date_posted=(2022, 12, 4), content="Im at the Bone.", author='khargr2')
    return ticket
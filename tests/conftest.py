import pytest

from init import create_app
from models import db, Users

@pytest.fixture
def app():
    app = create_app(db)
    yield app

@pytest.fixture(scope='module')
def new_user():
    user = Users(email='khargr2@ilstu.edu', username='khargr2', password='Iloveepool123',
                first_name='Kaden', last_name='Hargrove', bio='Hello', frequent_locations='The Bone')
    return user
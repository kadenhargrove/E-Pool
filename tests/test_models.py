"""
This file (test_models.py) contains the unit tests for the models.py file.
"""
from models import Users

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    user = Users(email='khargr2@ilstu.edu', username='khargr2', password='Iloveepool123',
                first_name='Kaden', last_name='Hargrove', bio='Hello', frequent_locations='The Bone')

    assert user.email == 'khargr2@ilstu.edu'
    assert user.username == 'khargr2'
    assert user.password == 'Iloveepool123'
    assert user.first_name == 'Kaden'
    assert user.last_name == 'Hargrove'
    assert user.bio == 'Hello'
    assert user.frequent_locations == 'The Bone'
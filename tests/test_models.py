"""
This file (test_models.py) contains the unit tests for the models.py file.
"""
from models import Users

def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, username, password, and other fields are defined correctly
    """

    assert new_user.email == 'khargr2@ilstu.edu'
    assert new_user.username == 'khargr2'
    assert new_user.password == 'Iloveepool123'
    assert new_user.first_name == 'Kaden'
    assert new_user.last_name == 'Hargrove'
    assert new_user.bio == 'Hello'
    assert new_user.frequent_locations == 'The Bone'

def test_set_password(new_user):
    """
    GIVEN an existing User
    WHEN a new password for the user is set
    THEN check the password is stored correctly and not as plaintext
    """
    new_user.set_password('NewPassword123')

    assert new_user.password != 'NewPassword123'
    assert new_user.check_password('NewPassword123')
    assert not new_user.check_password('NewPassword1234')
    assert not new_user.check_password('Iloveepool123')

def test_check_password(new_user):
    """
    GIVEN an existing User
    WHEN another new password for the user is set
    THEN check the password is stored correctly and not as plaintext
    """
    new_user.set_password('Foobar123')

    assert new_user.password != 'Foobar123'
    assert new_user.check_password('Foobar123')
    assert not new_user.check_password('Foobar1234')
    assert not new_user.check_password('NewPassword123')
    assert not new_user.check_password('Iloveepool123')
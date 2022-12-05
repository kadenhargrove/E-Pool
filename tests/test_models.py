"""
This file (test_models.py) contains the unit tests for the models.py file.
All new_* have been created in conftest.py
"""

# test User model
def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, username, password, and other fields are defined correctly
    """

    assert not new_user.email == 'khargr2@gmail.edu'
    assert new_user.email == 'khargr2@ilstu.edu'

    assert not new_user.username == 'khargr3'
    assert new_user.username == 'khargr2'

    assert not new_user.password == 'Iloveepool1234'
    assert new_user.password == 'Iloveepool123'

    assert not new_user.first_name == 'Kaden1'
    assert new_user.first_name == 'Kaden'

    assert not new_user.last_name == 'Hargrove1'
    assert new_user.last_name == 'Hargrove'

    assert not new_user.bio == 'Hello1'
    assert new_user.bio == 'Hello'

    assert not new_user.frequent_locations == ''
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

# test Friends model
def test_new_friends(new_friends):
    """
    GIVEN a Friends model
    WHEN a new Frienship is created
    THEN check the friender_username and friend_username fields are defined correctly
    """

    assert not new_friends.friender_username == 'kaden1234'
    assert new_friends.friender_username == 'kaden123'

    assert not new_friends.friend_username == 'emannuel1234'
    assert new_friends.friend_username == 'emannuel123'

# test Blocks model
def test_new_blocks(new_blocks):
    """
    GIVEN a Blocks model
    WHEN a new Blockship is created
    THEN check the blocker_username and blocked_username fields are defined correctly
    """

    assert not new_blocks.blocker_username == 'emannuel1234'
    assert new_blocks.blocker_username == 'emannuel123'
    
    assert not new_blocks.blocked_username == 'albert1234'
    assert new_blocks.blocked_username == 'albert123'

# test Driver model
def test_new_driver(new_driver):
    """
    GIVEN a Driver model
    WHEN a new Driver is created
    THEN check the email, username, password, and driver_rating fields are defined correctly
    """

    assert not new_driver.email == 'wilso@ilstu.edu'
    assert new_driver.email == 'wilson2@ilstu.edu'

    assert not new_driver.username == 'wilson1'
    assert new_driver.username == 'wilson2'

    assert not new_driver.password == 'yo123'
    assert new_driver.password == 'mrwilson123'

    assert not new_driver.driver_rating == 4
    assert new_driver.driver_rating == 5

# test Rider model
def test_new_rider(new_rider):
    """
    GIVEN a Rider model
    WHEN a new Rider is created
    THEN check the email, username, password, and rider_rating fields are defined correctly
    """

    assert not new_rider.email == 'smit@ilstu.edu'
    assert new_rider.email == 'smith2@ilstu.edu'

    assert not new_rider.username == 'smith1'
    assert new_rider.username == 'smith2'

    assert not new_rider.password == 'hey123'
    assert new_rider.password == 'mrsmith123'

    assert not new_rider.rider_rating == 3
    assert new_rider.rider_rating == 4

# test Tickets model
def test_new_ticket(new_ticket):
    """
    GIVEN a Ticket model
    WHEN a new Ticket is created
    THEN check the title, date_posted, content, and author fields are defined correctly
    """

    assert not new_ticket.title == 'Pick me up!!!'
    assert new_ticket.title == 'Pick me up'
    
    assert not new_ticket.date_posted == (2022, 12, 5)
    assert new_ticket.date_posted == (2022, 12, 4)

    assert not new_ticket.content == 'Im not at the Bone.'
    assert new_ticket.content == 'Im at the Bone.'

    assert not new_ticket.author == 'khargr1'
    assert new_ticket.author == 'khargr2'
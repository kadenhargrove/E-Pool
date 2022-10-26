# This files contains the parent class for the different epool users (drivers and riders)

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.myTickets = []
        self.friendList = []

    def add_friend(self, friend):
        self.friendList.append(friend)
    
    def delete_friend(self, friend):
        self.friendList.remove(friend)
# user.py
from observer import Observer

class User(Observer):
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def update(self, data):
        # Handle the weather data change notification
        # Send email notifications or take other actions
        pass

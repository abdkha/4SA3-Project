# In core/user_manager.py

class UserManager:
    def __init__(self):
        self.users = {}  # Dictionary to store user data

    def register_user(self, username, password):
        if username in self.users:
            return "Username already exists. Please choose another."
        self.users[username] = {'password': password, 'watchlist': []}
        return "Registration successful. You can now log in."

    def authenticate_user(self, username, password):
        if username in self.users and self.users[username]['password'] == password:
            return True
        return False

    def add_location_to_watchlist(self, username, location):
        if username in self.users:
            self.users[username]['watchlist'].append(location)

    def remove_location_from_watchlist(self, username, location):
        if username in self.users and location in self.users[username]['watchlist']:
            self.users[username]['watchlist'].remove(location)

    def get_watchlist(self, username):
        return self.users.get(username, {}).get('watchlist', [])

# Example usage in main.py
if __name__ == "__main__":
    user_manager = UserManager()

    # Register a user
    registration_message = user_manager.register_user("user123", "password123")
    print(registration_message)

    # Authenticate the user
    is_authenticated = user_manager.authenticate_user("user123", "password123")
    print("User authenticated:", is_authenticated)

    # Add a location to the user's watchlist
    user_manager.add_location_to_watchlist("user123", "New York")
    user_manager.add_location_to_watchlist("user123", "Los Angeles")

    # Get the user's watchlist
    watchlist = user_manager.get_watchlist("user123")
    print("User's watchlist:", watchlist)

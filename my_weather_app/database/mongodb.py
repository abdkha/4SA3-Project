# In database/mongodb.py

from pymongo import MongoClient

class MongoDB:
    def __init__(self, db_uri, db_name):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]

    def save_user(self, username, password):
        users_collection = self.db["users"]
        user_data = {"username": username, "password": password, "watchlist": []}
        users_collection.insert_one(user_data)

    def add_location_to_watchlist(self, username, location):
        users_collection = self.db["users"]
        users_collection.update_one(
            {"username": username},
            {"$addToSet": {"watchlist": location}}
        )

    def remove_location_from_watchlist(self, username, location):
        users_collection = self.db["users"]
        users_collection.update_one(
            {"username": username},
            {"$pull": {"watchlist": location}}
        )

    def get_watchlist(self, username):
        users_collection = self.db["users"]
        user_data = users_collection.find_one({"username": username})
        if user_data:
            return user_data.get("watchlist", [])
        return []

# Example usage in main.py
if __name__ == "__main__":
    db_uri = "mongodb://localhost:27017/"  # Replace with your MongoDB URI
    db_name = "my_weather_app_db"
    mongodb = MongoDB(db_uri, db_name)

    # Save user data
    mongodb.save_user("user123", "password123")

    # Add a location to a user's watchlist
    mongodb.add_location_to_watchlist("user123", "New York")

    # Get the user's watchlist
    watchlist = mongodb.get_watchlist("user123")
    print("User's watchlist:", watchlist)

# main.py
import re
import requests
import sys
sys.path.append('C:\\Users\\Tabish\\Desktop\\4SA3 - Software Architecture\\Project\\my_weather_app\\')
from getpass import getpass
from pymongo import MongoClient
from factory_module import Factory

# Initialize MongoDB
db_uri = "mongodb+srv://primoo357:#h#E67AP@mangodb.0xoamzf.mongodb.net/"
db_name = "my_weather_app_db"
client = MongoClient(db_uri)
db = client[db_name]
users_collection = db["users"]

# Function to create a new user
def create_new_user():
    print("Option A: Create a New User")
    username = input("I) Provide your username: ")
    # Check if a user with the same username already exists
    existing_user = users_collection.find_one({"username": username})
    if existing_user:
        print("Username already exists. Please choose a different username.")
        return
    first_name = input("II) Provide your first name: ")
    last_name = input("III) Provide your last name: ")
    email = input("IV) Provide your email address: ")

    # Password complexity validation
    while True:
        password = getpass("V) Type in a password: ")
        if not (len(password) >= 8 and re.search(r"\d", password) and re.search(r"[A-Z]", password) and re.search(r"[a-z]", password) and re.search(r"[!@#$%^&*]", password)):
            print("Password does not meet complexity requirements.")
        else:
            break

    # Store user data in MongoDB
    user_data = {
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        
    }
    users_collection.insert_one(user_data)
    print("Your account is now successfully created.")

# Function to log in as an existing user
def login_as_existing_user():
    while True:
        print("Option B: Login as an Existing User")
        username = input("Username: ")
        password = getpass("Password: ")

        try:
            # Check if the user exists in the database
            user = users_collection.find_one({"username": username, "password": password})
            if user:
                return username
            else:
                raise ValueError("Invalid username or password.")
        except ValueError as e:
            print(str(e))
            print("Choose an option:")
            print("A) Create a new user")
            print("B) Login as an existing user")
            choice = input("Enter your choice: ").strip().lower()
            if choice != 'b':
                return None

# Function to retrieve the user's watchlist
def retrieve_watchlist(username):
    user = users_collection.find_one({"username": username})
    watchlist = user.get("watchlist", [])
    return watchlist

# Function to fetch available locations from OpenWeatherMap API
# Function to fetch available locations from OpenWeatherMap API
def fetch_available_locations(query_location, country_code="CA"):
    api_key = "d1131243cce045daf69f3bb80c199ce3"  # Replace with your actual API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    # Initialize variables
    locations = []
    offset = 0
    batch_size = 25

    while True:
        # Parameters for the API request
        params = {
            'q': f'{query_location},{country_code}',
            'type': 'like',
            'sort': 'population',
            'cnt': batch_size,
            'start': offset,
            'appid': api_key
        }

        # Make the API request
        response = requests.get(base_url, params=params)
        data = response.json()

        # Extract location names from the API response
        batch_locations = [result['name'] for result in data.get('list', [])]

        # If no more locations, break the loop
        if not batch_locations:
            break

        locations.extend(batch_locations)
        offset += batch_size

        # Prompt the user to fetch more locations
        more_locations = input("Do you want to fetch more locations? (yes/no): ").lower()
        if more_locations != 'yes':
            break

    return locations


# Function to view available locations in Canada
def view_available_locations(username):
    # Prompt the user to enter a city in Canada
    user_input = input("Enter a city in Canada (e.g., Toronto,CA): ")
    query_location = user_input.strip()

    # Query OpenWeatherMap API to retrieve available locations in Canada
    available_locations = fetch_available_locations(query_location)

    return available_locations


# Function to fetch available locations from "cities" collection
def fetch_available_locations_from_cities(offset, batch_size):
    cities_collection = db["cities"]

    # Query the "cities" collection
    result = cities_collection.find({}, {"name": 1}).skip(offset).limit(batch_size)

    # Extract location names from the query result
    locations = [record["name"] for record in result]

    return locations

# Function to modify the user's watchlist
def modify_watchlist(username, factory):
    while True:
        print("Your current watchlist:")
        watchlist = retrieve_watchlist(username)
        if watchlist:
            for idx, location in enumerate(watchlist, 1):
                print(f"{idx}. {location}")
        else:
            print("No locations in the watchlist.")

        print("Enter the number you wish to remove from your watchlist. Or press 'z' to add a city from the available locations to add to your watchlist.")
        try:
            choice = input()
            if choice.lower() == 'z':
                view_and_add_locations_to_watchlist(username, factory)
            else:
                choice = int(choice)
                if 0 < choice <= len(watchlist):
                    selected_location = watchlist[choice - 1]
                    display_weather_info(selected_location, factory, print_format=True)

                    # Keep prompting the user to delete more locations until they want to go back
                    while True:
                        locations_to_remove = [selected_location]
                        locations_to_add = []
                        
                        modify_watchlist_helper(username, locations_to_add, locations_to_remove, factory)

                        another_modification = input("Do you want to modify more locations? (yes/no): ").lower()
                        if another_modification != 'yes':
                            break
                else:
                    print("Invalid choice.")
        except ValueError:
            print("Invalid input.")

# Function to view and add locations to the watchlist
def view_and_add_locations_to_watchlist(username, factory):
    while True:
        new_locations = view_available_locations(username)
        if not new_locations:
            print("No available locations in Canada to add to your watchlist.")
            return

        print("Available locations in Canada:")
        for idx, location in enumerate(new_locations, 1):
            print(f"{idx}. {location}")

        try:
            choice = input("Enter the number of the location to add to your watchlist (0 to exit), or press 'z' to add a city from the available locations: ")
            if choice == '0':
                return
            elif choice.lower() == 'z':
                city_input = input("Enter a city in Canada (e.g., Toronto,CA): ")
                location_to_add = fetch_available_locations(city_input)
                if location_to_add:
                    modify_watchlist_helper(username, location_to_add, [], factory)
                    print(f"{location_to_add[0]} added to your watchlist.")
                else:
                    print("No available locations in Canada to add to your watchlist.")
            else:
                choice = int(choice)
                if 0 < choice <= len(new_locations):
                    location_to_add = new_locations[choice - 1]
                    modify_watchlist_helper(username, [location_to_add], [], factory)
                    print(f"{location_to_add} added to your watchlist.")
                else:
                    print("Invalid choice.")
        except ValueError:
            print("Invalid choice.")

# Function to modify the user's watchlist
def modify_watchlist_helper(username, locations_to_add, locations_to_remove, factory):
    # Existing code for modifying the watchlist
    user = users_collection.find_one({"username": username})
    current_watchlist = set(user.get("watchlist", []))

    try:
        # Add new locations to the watchlist with correct formatting
        formatted_locations_to_add = []
        for location in locations_to_add:
            formatted_location = format_location(location)
            if formatted_location:
                current_watchlist.add(formatted_location)
                formatted_locations_to_add.append(formatted_location)
            else:
                print(f"Invalid format for location: {location}. Skipping.")

        # Remove locations from the watchlist
        formatted_locations_to_remove = []
        for location in locations_to_remove:
            formatted_location = format_location(location)
            if formatted_location:
                current_watchlist.discard(formatted_location)
                formatted_locations_to_remove.append(formatted_location)
            else:
                print(f"Invalid format for location: {location}. Skipping.")

        # Update the watchlist in the database
        users_collection.update_one({"username": username}, {"$set": {"watchlist": list(current_watchlist)}})

        # Display weather information for added locations
        for location in formatted_locations_to_add:
            try:
                display_weather_info(location, factory, print_format=True)
            except KeyError:
                print(f"Failed to retrieve weather information for {location}. Please check the format.")

        print("Watchlist modified successfully.")
    except ValueError:
        print("Invalid input.")

# Function to manage the user's profile
def manage_profile(username):
    while True:
        print("Manage Profile")
        print("A) Change Password")
        print("B) Change First Name")
        print("C) Change Last Name")
        print("D) Change E-Mail Address")
        print("E) Exit to Main Menu")
        print("F) Exit Program")
        menu_option = input("Enter your choice (A/B/C/D/E/F/G): ")

        if menu_option.lower() == "a":
            # Change Password
            while True:
                new_password = getpass("Enter your new password: ")
                if not (len(new_password) >= 8 and re.search(r"\d", new_password) and re.search(r"[A-Z]", new_password) and re.search(r"[a-z]", new_password) and re.search(r"[!@#$%^&*]", new_password)):
                    print("Password does not meet complexity requirements.")
                else:
                    users_collection.update_one({"username": username}, {"$set": {"password": new_password}})
                    print("Password changed successfully.")
                    break
        elif menu_option.lower() == "b":
            # Change First Name
            new_first_name = input("Enter your new first name: ")
            users_collection.update_one({"username": username}, {"$set": {"first_name": new_first_name}})
            print("First name changed successfully.")
        elif menu_option.lower() == "c":
            # Change Last Name
            new_last_name = input("Enter your new last name: ")
            users_collection.update_one({"username": username}, {"$set": {"last_name": new_last_name}})
            print("Last name changed successfully.")
        elif menu_option.lower() == "d":
            # Change E-Mail Address
            new_email = input("Enter your new email address: ")
            users_collection.update_one({"username": username}, {"$set": {"email": new_email}})
            print("Email address changed successfully.")
        elif menu_option.lower() == "e":
            # Exit to Main Menu
            return
        elif menu_option.lower() == "f":
            # Exit Program
            print("Thank you for using HELP.")
            exit()
        else:
            print("Invalid option. Please choose A, B, C, D, E, F, or G.")


# Function for error checking of formation location according to OpenWeatherMap API's standards
def format_location(location):
    # Remove any extra spaces
    location = location.strip()

    # If the location already matches the OpenWeatherMap API convention, return it
    if re.match(r'^[A-Za-z\s]+,[A-Za-z\s]+$', location):
        return location

    # If there are extra country codes, remove them
    parts = location.split(',')
    city = parts[0].strip()
    country = parts[1].strip() if len(parts) > 1 else 'CA'

    return f"{city},{country}"


# Function to display weather information for a location
def display_weather_info(location, factory, print_format=False):
    try:
        # Retrieve weather data
        wind_data = factory.createData(location, "wind")
        temperature_data = factory.createData(location, "temperature")
        humidity_data = factory.createData(location, "humidity")

        # Print API response for troubleshooting
        print(f"API Response for {location}:")
        print(wind_data.data)
        print(temperature_data.data)
        print(humidity_data.data)

        # Check if any of the data is None before calling the output method
        if wind_data and temperature_data and humidity_data:
            # Call the output method for each WeatherData object
            if print_format:
                print(f"Weather information for {location}:")
            wind_data.output()
            temperature_data.output()
            humidity_data.output()
        else:
            print(f"No weather information available for {location}. Check if the location format is correct.")
    except Exception as e:
        print(f"An error occurred while retrieving weather information for {location}: {str(e)}")


# Function to display weather information for a location in the watchlist
def display_weather_for_location_in_watchlist(username, factory):
    watchlist = retrieve_watchlist(username)

    if not watchlist:
        print("Your watchlist is empty.")
        return

    print("Locations in your watchlist:")
    for idx, location in enumerate(watchlist, 1):
        print(f"{idx}. {location}")

    try:
        choice = int(input("Enter the number of the location to modify (0 to go back): "))
        if 0 < choice <= len(watchlist):
            selected_location = watchlist[choice - 1]
            modify_watchlist_helper(username, [selected_location], [], factory)
        elif choice == 0:
            return
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid choice.")

# Function to fetch available locations from OpenWeatherMap API
def fetch_available_locations(query_location):
    api_key = "d1131243cce045daf69f3bb80c199ce3"  # Replace with your actual API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    # Parameters for the API request
    params = {
        'q': query_location,
        'type': 'like',
        'sort': 'population',
        'cnt': 10,  # Number of results to retrieve
        'appid': api_key
    }

    # Make the API request
    response = requests.get(base_url, params=params)
    data = response.json()

    # Extract location names from the API response
    locations = [result['name'] for result in data.get('list', [])]

    return locations

# Function to view available locations in Canada
def view_available_locations(username):
    # Prompt the user to enter a city in Canada
    user_input = input("Enter a city in Canada (e.g., Toronto,CA): ")
    query_location = user_input.strip()

    # Query OpenWeatherMap API to retrieve available locations in Canada
    available_locations = fetch_available_locations(query_location)

    return available_locations

# Create factory object
factory = Factory()

# Main program
while True:
    print("Choose an option:")
    print("A) Create a new user")
    print("B) Login as an existing user")
    print("E) Exit Program")  # Option to exit the program
    option = input("Enter your choice: ")

    if option.lower() == "a":
        create_new_user()
    elif option.lower() == "b":
        username = login_as_existing_user()
        if username:
            print(f"Welcome Username - {username} !")
            # User is logged in, display the menu
            while True:
                print("Main Menu")
                print("A) Retrieve Watchlist")
                print("B) View Available Locations")
                print("C) Modify Watchlist")
                print("D) Manage Profile")
                print("E) Exit Program")  # Option to exit the program
                menu_option = input("Enter your choice (A/B/C/D/E): ")

                if menu_option.lower() == "a":
                    watchlist = retrieve_watchlist(username)
                    if watchlist:
                        print("Your watchlist: ", ", ".join(watchlist))
                        display_weather_for_location_in_watchlist(username, factory)
                    else:
                        print("No locations added to your watchlist")
                # Main program (part)
                elif menu_option.lower() == "b":
                    offset = 0
                    batch_size = 25

                    while True:
                        # Query OpenWeatherMap API to retrieve available locations in Canada
                        available_locations = fetch_available_locations_from_cities(offset, batch_size)

                        if not available_locations:
                            print("No more available locations.")
                            break

                        print(f"Available locations in Canada (Batch {offset // batch_size + 1}):")
                        for idx, location in enumerate(available_locations, 1):
                            print(f"{idx}. {location}")

                        try:
                            choice = int(input(f"Enter 0 to see more locations, or any other number to stop: "))
                            if choice == 0:
                                offset += batch_size
                            else:
                                break
                        except ValueError:
                            print("Invalid input. Stopping.")
                            break
                    print("Returning to the main menu.")
                elif menu_option.lower() == "c":
                    modify_watchlist(username, factory)
                elif menu_option.lower() == "d":
                    manage_profile(username)
                elif menu_option.lower() == "e":
                    # Exit the program
                    print("Thank you for using HELP.")
                    exit()
                else:
                    print("Invalid option. Please choose A, B, C, D, or E.")
        else:
            print("Invalid username or password.")
    elif option.lower() == "e":
        # Exit the program
        print("Thank you for using HELP.")
        exit()
    else:
        print("Invalid option. Please choose 'A', 'B', or 'E'.")
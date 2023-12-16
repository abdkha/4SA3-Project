# factory_module.py

import requests

class Factory:
    def createData(self, location, data_type):
        if data_type == "temperature":
            return TemperatureData(location)
        elif data_type == "humidity":
            return HumidityData(location)
        elif data_type == "wind":
            return WindData(location)
        else:
            raise ValueError(f"Invalid data type: {data_type}")

class WeatherData:
    def __init__(self, location):
        self.location = location
        self.data = None  # Initialize data attribute

def fetch_data(self):
    api_key = "d1131243cce045daf69f3bb80c199ce3"
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    params = {
        'q': self.location,
        'appid': api_key
    }

    try:
        print(f"Fetching data for {self.location}...")
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        print(f"API Response for {self.location}:")
        print(response.json())  # Print the entire API response
        data = response.json()

        # Your existing data extraction logic...
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

class TemperatureData(WeatherData):
    def fetch_data(self):
        api_key = "d1131243cce045daf69f3bb80c199ce3"
        base_url = "http://api.openweathermap.org/data/2.5/weather"

        params = {
            'q': self.location,
            'appid': api_key
        }

        try:
            print(f"Fetching data for {self.location} (Temperature)...")
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            print(f"API Response for {self.location} (Temperature):")
            print(response.json())  # Print the entire API response
            data = response.json()

            # Extract temperature data from the API response
            temperature = data.get('main', {}).get('temp')
            self.data = f"Temperature for {self.location}: {temperature} K"
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Request Error: {err}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def output(self):
        if self.data is not None:
            print(self.data)
        else:
            print("No data available for this category.")

class HumidityData(WeatherData):
    def fetch_data(self):
        api_key = "d1131243cce045daf69f3bb80c199ce3"
        base_url = "http://api.openweathermap.org/data/2.5/weather"

        params = {
            'q': self.location,
            'appid': api_key
        }

        try:
            print(f"Fetching data for {self.location} (Humidity)...")
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            print(f"API Response for {self.location} (Humidity):")
            print(response.json())  # Print the entire API response
            data = response.json()

            # Extract humidity data from the API response
            humidity = data.get('main', {}).get('humidity')
            self.data = f"Humidity for {self.location}: {humidity}%"
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Request Error: {err}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def output(self):
        if self.data is not None:
            print(self.data)
        else:
            print("No data available for this category.")

            
class WindData(WeatherData):
    def fetch_data(self):
        api_key = "d1131243cce045daf69f3bb80c199ce3"
        base_url = "http://api.openweathermap.org/data/2.5/weather"

        params = {
            'q': self.location,
            'appid': api_key
        }

        try:
            print(f"Fetching data for {self.location} (Wind)...")
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            print(f"API Response for {self.location} (Wind):")
            print(response.json())  # Print the entire API response
            data = response.json()

            # Extract wind data from the API response
            wind_speed = data.get('wind', {}).get('speed')
            self.data = f"Wind for {self.location}: {wind_speed} m/s"
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Request Error: {err}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def output(self):
        if self.data is not None:
            print(self.data)
        else:
            print("No data available for this category.")
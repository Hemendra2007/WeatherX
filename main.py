import requests
import json
from datetime import datetime
import os

CONFIG_FILE = 'config.json'

def get_weather(city, units='metric'):
    api_key = "my_api_key_goes_here"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&appid={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def display_weather_data(weather_data, units):
    temp_label = "Temperature"
    if units == 'imperial':
        temp_label = "Temperature (°F)"
    elif units == 'metric':
        temp_label = "Temperature (°C)"
    
    temp = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    description = weather_data['weather'][0]['description']
    wind_speed = weather_data['wind']['speed']
    sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M:%S')
    sunset = datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M:%S')
    
    print(f"\nWeather Information:")
    print(f"{temp_label}: {temp:.2f}")
    print(f"Humidity: {humidity}%")
    print(f"Description: {description.capitalize()}")
    print(f"Wind Speed: {wind_speed} m/s")
    print(f"Sunrise: {sunrise}")
    print(f"Sunset: {sunset}\n")

def log_weather_data(city, weather_data):
    timestamp = datetime.now().isoformat()
    with open('weather_log.json', 'a') as file:
        log_entry = {
            'timestamp': timestamp,
            'city': city,
            'weather': weather_data,
            'logged_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        json.dump(log_entry, file)
        file.write('\n')

def review_last_log():
    try:
        with open('weather_log.json', 'r') as file:
            lines = file.readlines()
            if lines:
                last_log = json.loads(lines[-1])
                print("\nLast logged weather data:")
                print(f"Timestamp: {last_log['timestamp']}")
                print(f"Logged At: {last_log['logged_at']}")
                display_weather_data(last_log['weather'], 'metric')  # Default to metric for display
            else:
                print("No logs found.")
    except FileNotFoundError:
        print("No log file found.")

def clear_weather_log():
    try:
        with open('weather_log.json', 'w') as file:
            file.write('')  # Clearing the content of the log file
        print("Weather log cleared successfully.")
    except Exception as e:
        print(f"Error clearing the weather log: {e}")

def save_preferences(units, default_city):
    preferences = {
        'units': units,
        'default_city': default_city
    }
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(preferences, config_file)

def load_preferences():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as config_file:
                return json.load(config_file)
        except json.JSONDecodeError:
            print("Error loading preferences. Starting with default settings.")
            return {'units': 'metric', 'default_city': ''}
    else:
        return {'units': 'metric', 'default_city': ''}

def validate_city_input(city_input, default_city):
    if not city_input and not default_city:
        print("Input cannot be empty. Please try again.")
        return None
    return city_input or default_city

def main():
    preferences = load_preferences()
    print(f"Welcome to the Terminal Weather App! (Default unit: {preferences['units'].capitalize()})")
    
    while True:
        command = input("Enter 'fetch' to get weather data, 'review' to review last log, 'settings' to save preferences, 'clear' to clear logs, or 'exit' to quit: ").strip().lower()
        
        if command == 'exit':
            print("Goodbye!")
            break
        
        if command == 'clear':
            clear_weather_log()
            continue
        
        if command == 'review':
            review_last_log()
            continue
        
        if command == 'settings':
            default_city = input("Enter your default city (leave empty to skip): ").strip()
            unit_choice = input("Choose temperature unit (Celsius/Fahrenheit): ").strip().lower()
            if unit_choice == 'fahrenheit':
                units = 'imperial'
            elif unit_choice == 'celsius':
                units = 'metric'
            else:
                print("Invalid unit choice. Defaulting to Celsius.")
                units = 'metric'
            
            save_preferences(units, default_city)
            print("Preferences saved!")
            continue
        
        if command == 'fetch':
            city_input = input(f"Enter the city name(s) separated by commas (or press Enter to use default city: {preferences['default_city']}): ").strip()
            city_input = validate_city_input(city_input, preferences['default_city'])
            if not city_input:
                continue
            
            cities = [city.strip() for city in city_input.split(',')]
            units = preferences['units']
        
            for city in cities:
                weather_data = get_weather(city, units)
                
                if weather_data:
                    print(f"\nWeather data for {city} fetched successfully!")
                    display_weather_data(weather_data, units)
                    log_weather_data(city, weather_data)
                else:
                    print(f"\nCity '{city}' not found or API request failed.")
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()

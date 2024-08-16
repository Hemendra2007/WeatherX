import requests
import json
from datetime import datetime
import os

CONFIG_FILE = 'config.json'
API_KEY = "my_api_key_goes_here"  # API key directly in the script

def get_weather(city, units='metric'):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&appid={API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def get_forecast(city, units='metric'):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units={units}&appid={API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching weather forecast: {e}")
        return None

def display_weather_data(weather_data, units, wind_units='m/s'):
    temp_label = "Temperature"
    if units == 'imperial':
        temp_label = "Temperature (°F)"
    elif units == 'metric':
        temp_label = "Temperature (°C)"
    
    temp = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    description = weather_data['weather'][0]['description']
    wind_speed = convert_wind_speed(weather_data['wind']['speed'], wind_units)
    sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M:%S')
    sunset = datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M:%S')
    
    print(f"\nWeather Information:")
    print(f"{temp_label}: {temp:.2f}")
    print(f"Humidity: {humidity}%")
    print(f"Description: {description.capitalize()}")
    print(f"Wind Speed: {wind_speed} {wind_units}")
    print(f"Sunrise: {sunrise}")
    print(f"Sunset: {sunset}\n")

def display_forecast(forecast_data, units):
    print("\n7-Day Weather Forecast:")
    for entry in forecast_data['list']:
        dt = datetime.fromtimestamp(entry['dt'])
        temp = entry['main']['temp']
        description = entry['weather'][0]['description']
        print(f"{dt.strftime('%Y-%m-%d %H:%M:%S')}: {temp}°{get_unit_label(units)} - {description.capitalize()}")

def convert_wind_speed(speed, wind_units):
    if wind_units == 'km/h':
        return speed * 3.6
    elif wind_units == 'mph':
        return speed * 2.237
    return speed  # Default is m/s

def check_weather_alerts(weather_data, alerts, units):
    temp = weather_data['main']['temp']
    for alert in alerts:
        condition = alert['condition']
        threshold = alert['threshold']
        
        if (condition == 'above' and temp > threshold) or (condition == 'below' and temp < threshold):
            print(f"ALERT: Temperature is {temp:.2f}°{get_unit_label(units)}, which is {condition} {threshold}°!")

def get_unit_label(units):
    return 'F' if units == 'imperial' else 'C'

def set_weather_alert():
    condition = input("Set alert for temperature 'above' or 'below' a threshold? ").strip().lower()
    threshold = float(input(f"Enter the temperature threshold (in selected units): "))
    
    return {'condition': condition, 'threshold': threshold}

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

def delete_log_entry():
    try:
        with open('weather_log.json', 'r') as file:
            lines = file.readlines()
        
        if lines:
            print("Existing log entries:")
            for i, line in enumerate(lines):
                log_entry = json.loads(line)
                print(f"{i + 1}: {log_entry['timestamp']} - {log_entry['city']}")
            
            entry_to_delete = int(input("Enter the number of the log entry to delete: ")) - 1
            
            if 0 <= entry_to_delete < len(lines):
                del lines[entry_to_delete]
                with open('weather_log.json', 'w') as file:
                    file.writelines(lines)
                print("Log entry deleted successfully.")
            else:
                print("Invalid entry number.")
        else:
            print("No logs found.")
    except FileNotFoundError:
        print("No log file found.")

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
    alerts = []  # List to store weather alerts
    print(f"Welcome to the Terminal Weather App! (Default unit: {preferences['units'].capitalize()})")
    
    while True:
        command = input("Enter 'fetch' to get weather data, 'forecast' for 7-day forecast, 'review' to review last log, 'settings' to save preferences, 'alert' to set weather alerts, 'clear' to clear logs, 'delete' to delete a log entry, or 'exit' to quit: ").strip().lower()
        
        if command == 'exit':
            print("Goodbye!")
            break
        
        if command == 'clear':
            clear_weather_log()
            continue
        
        if command == 'review':
            review_last_log()
            continue
        
        if command == 'delete':
            delete_log_entry()
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
        
        if command == 'alert':
            alert = set_weather_alert()
            alerts.append(alert)
            print(f"Alert set: Temperature {alert['condition']} {alert['threshold']}°")
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
                    check_weather_alerts(weather_data, alerts, units)  # Check for alerts
                    log_weather_data(city, weather_data)
                else:
                    print(f"\nCity '{city}' not found or API request failed.")
        
        elif command == 'forecast':
            city_input = input(f"Enter the city name for 7-day forecast (or press Enter to use default city: {preferences['default_city']}): ").strip()
            city_input = validate_city_input(city_input, preferences['

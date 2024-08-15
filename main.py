import requests
import json
from datetime import datetime

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
    
    print(f"\nWeather Information:")
    print(f"{temp_label}: {temp:.2f}")
    print(f"Humidity: {humidity}%")
    print(f"Description: {description.capitalize()}")
    print(f"Wind Speed: {wind_speed} m/s\n")

def log_weather_data(city, weather_data):
    timestamp = datetime.now().isoformat()
    with open('weather_log.json', 'a') as file:
        log_entry = {
            'timestamp': timestamp,
            'city': city,
            'weather': weather_data
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
                display_weather_data(last_log['weather'], 'metric')  # Default to metric for display
            else:
                print("No logs found.")
    except FileNotFoundError:
        print("No log file found.")

def main():
    print("Welcome to the Terminal Weather App!")
    while True:
        command = input("Enter 'fetch' to get weather data, 'review' to review last log, or 'exit' to quit: ").strip().lower()
        
        if command == 'exit':
            print("Goodbye!")
            break
        
        if command == 'review':
            review_last_log()
            continue
        
        if command != 'fetch':
            print("Invalid command. Please try again.")
            continue
        
        city_input = input("Enter the city name(s) separated by commas: ").strip()
        
        if not city_input:
            print("Input cannot be empty. Please try again.")
            continue
        
        cities = [city.strip() for city in city_input.split(',')]
        
        unit_choice = input("Choose temperature unit (Celsius/Fahrenheit): ").strip().lower()
        if unit_choice == 'fahrenheit':
            units = 'imperial'
        elif unit_choice == 'celsius':
            units = 'metric'
        else:
            print("Invalid unit choice. Defaulting to Celsius.")
            units = 'metric'
        
        for city in cities:
            weather_data = get_weather(city, units)
            
            if weather_data:
                print(f"\nWeather data for {city} fetched successfully!")
                display_weather_data(weather_data, units)
                log_weather_data(city, weather_data)
            else:
                print(f"\nCity '{city}' not found or API request failed.")

if __name__ == "__main__":
    main()

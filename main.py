import requests

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

def main():
    print("Welcome to the Terminal Weather App!")
    while True:
        city = input("Enter the city name (or type 'exit' to quit): ").strip()
        
        if city.lower() == 'exit':
            print("Goodbye!")
            break
        
        if not city:
            print("City name cannot be empty. Please try again.")
            continue
        
        unit_choice = input("Choose temperature unit (Celsius/Fahrenheit): ").strip().lower()
        if unit_choice == 'fahrenheit':
            units = 'imperial'
        elif unit_choice == 'celsius':
            units = 'metric'
        else:
            print("Invalid unit choice. Defaulting to Celsius.")
            units = 'metric'
        
        weather_data = get_weather(city, units)
        
        if weather_data:
            print(f"\nWeather data for {city} fetched successfully!")
            display_weather_data(weather_data, units)
        else:
            print("\nCity not found or API request failed.")

if __name__ == "__main__":
    main()

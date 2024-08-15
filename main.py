import requests

def get_weather(city):
    api_key = "my_api_key_goes_here"
  
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
  
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    while True:
        city = input("Enter the city name (or type 'exit' to quit): ").strip()
        
        if city.lower() == 'exit':
            print("Goodbye!")
            break
        
        if not city:
            print("City name cannot be empty. Please try again.")
            continue
        
        weather_data = get_weather(city)
        
        if weather_data:
            print(f"Weather data for {city} fetched successfully!")
            print(f"Temperature: {weather_data['main']['temp'] - 273.15:.2f}°C")  # Basic temperature output for now
        else:
            print("City not found or API request failed.")

if __name__ == "__main__":
    main()

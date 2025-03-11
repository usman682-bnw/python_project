import requests
from datetime import datetime

API_KEY = "152f79e25b908e0d81c78ea3ac98dc6b"  # Replace with your OpenWeatherMap API key

def get_current_weather(city, api_key):
    """Fetch current weather data for a given city"""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            return {
                'city': data['name'],
                'country': data['sys']['country'],
                'temp': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'].capitalize(),
                'icon': data['weather'][0]['icon']
            }
        else:
            print(f"Error: {data['message']}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return None

def get_5_day_forecast(city, api_key):
    """Fetch 5-day weather forecast data"""
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            return data['list']
        else:
            print(f"Error: {data['message']}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return None

def process_forecast(forecast_data):
    """Process raw forecast data into daily summaries"""
    daily_forecast = {}
    
    for entry in forecast_data:
        date = datetime.strptime(entry['dt_txt'], "%Y-%m-%d %H:%M:%S")
        day = date.strftime("%A")  # Get weekday name
        temp = entry['main']['temp']
        description = entry['weather'][0]['description']
        
        if day not in daily_forecast:
            daily_forecast[day] = {
                'temps': [],
                'descriptions': [],
                'icon': entry['weather'][0]['icon']
            }
            
        daily_forecast[day]['temps'].append(temp)
        daily_forecast[day]['descriptions'].append(description)
    
    processed = []
    for day, data in daily_forecast.items():
        processed.append({
            'day': day,
            'min_temp': min(data['temps']),
            'max_temp': max(data['temps']),
            'description': max(set(data['descriptions']), key=data['descriptions'].count),
            'icon': data['icon']
        })
    
    return processed

def display_weather(current, forecast):
    """Display weather information in a readable format"""
    if current:
        print("\nCurrent Weather:")
        print(f"{current['city']}, {current['country']}")
        print(f"Temperature: {current['temp']}°C")
        print(f"Humidity: {current['humidity']}%")
        print(f"Conditions: {current['description']}")
        print(f"Weather Icon: http://openweathermap.org/img/wn/{current['icon']}@2x.png")

    if forecast:
        print("\n5-Day Forecast:")
        for day in forecast:
            print(f"\n{day['day']}:")
            print(f"Min: {day['min_temp']}°C | Max: {day['max_temp']}°C")
            print(f"Conditions: {day['description'].capitalize()}")
            print(f"Icon: http://openweathermap.org/img/wn/{day['icon']}@2x.png")

def main():
    print("Real-Time Weather Forecast Application")
    print("---------------------------------------")
    
    while True:
        city = input("\nEnter city name (or 'exit' to quit): ").strip()
        
        if city.lower() == 'exit':
            print("Exiting application...")
            break
            
        current = get_current_weather(city, API_KEY)
        forecast_data = get_5_day_forecast(city, API_KEY)
        
        if forecast_data:
            forecast = process_forecast(forecast_data)
            display_weather(current, forecast[:5])  # Show next 5 days
        else:
            display_weather(current, None)

if __name__ == "__main__":
    main()
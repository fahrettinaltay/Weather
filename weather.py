import requests, os, geocoder
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(dotenv_path='/Users/fahrettinaltay/Documents/env/openWeather.env')


class Weather:
    def __init__(self):
        self.api_key = os.getenv('REACT_APP_WEATHER_API_KEY')
        if not self.api_key:
            raise ValueError("API key not found. Please check your .env file.")
        self.api_url = f"http://api.openweathermap.org/data/2.5/weather"
        self.headers = {
            "accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0"
        }

    def getWeather(self):   
        city = GetLocation()
        params = {
            'q': city.getLocation(),
            'appid': self.api_key,
            'units': 'metric'
        }
        response = requests.get(self.api_url, headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json()
            sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')
            sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')

            return f"""
City: {data['name']}
Temperature: {data['main']['temp']}°C
Feels Like: {data['main']['feels_like']}°C
Min Temperature: {data['main']['temp_min']}°C
Max Temperature: {data['main']['temp_max']}°C
Humidity: {data['main']['humidity']}%
Pressure: {data['main']['pressure']} hPa
Wind Speed: {data['wind']['speed']} m/s
Wind Direction: {data['wind']['deg']}°
Cloudiness: {data['clouds']['all']}%
Sunrise: {sunrise}
Sunset: {sunset}
Weather: {data['weather'][0]['description'].capitalize()}
"""
        else:
            return f"Error: {response.status_code}, Message: {response.json().get('message', 'Unknown error')}"
    

class GetLocation:
    def __init__(self):
        self.location = geocoder.ip('me')

    def getLocation(self):
        address = self.location.address.split(',')
        return address[1].strip() if len(address) > 1 else None
        
weather = Weather()
weather_data = weather.getWeather()
print(weather_data)
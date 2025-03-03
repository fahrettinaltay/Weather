import requests
import os
import geocoder
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(dotenv_path='/Users/fahrettinaltay/Documents/env/openWeather.env')


class ILocationProvider:
    """Interface for location provider."""
    def get_location(self):
        raise NotImplementedError


class GeocoderLocationProvider(ILocationProvider):
    """Provides location information using the Geocoder library."""
    def get_location(self):
        location = geocoder.ip('me')
        if location.address:
            address = location.address.split(',')
            return address[1].strip() if len(address) > 1 else None
        return None


class IWeatherProvider:
    """Abstract class for weather API"""
    def get_weather(self, city):
        raise NotImplementedError


class OpenWeatherProvider(IWeatherProvider):
    """Retrieves weather data from OpenWeather API."""
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "http://api.openweathermap.org/data/2.5/weather"
        self.headers = {
            "accept": "application/json",
            "User-Agent": "Mozilla/5.0"
        }

    def get_weather(self, city):
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        response = requests.get(self.api_url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error: {response.status_code}, Message: {response.json().get('message', 'Unknown error')}"}


class WeatherService:
    def __init__(self, weather_provider: IWeatherProvider, location_provider: ILocationProvider):
        self.weather_provider = weather_provider
        self.location_provider = location_provider

    def get_weather_report(self):
        city = self.location_provider.get_location()
        if not city:
            return "Location not found."

        data = self.weather_provider.get_weather(city)
        if "error" in data:
            return data["error"]

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

api_key = os.getenv('REACT_APP_WEATHER_API_KEY')
weather_provider = OpenWeatherProvider(api_key)
location_provider = GeocoderLocationProvider()
weather_service = WeatherService(weather_provider, location_provider)

print(weather_service.get_weather_report())

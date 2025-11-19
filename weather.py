import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = os.getenv("WEATHER_BASE_URL")

def get_weather(city: str) -> str:
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return f"The weather in {city.capitalize()} is {response.json()['main']['temp']}"


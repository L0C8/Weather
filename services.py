import requests
import os
import json
import time
from utils import get_api_key
from datetime import datetime
import pytz

WEATHER_CACHE_FILE = os.path.join("data", "cached_weather.json")
WEATHER_CACHE_DURATION = 15 * 60

def fetch_weather():
    api_key = get_api_key("openweathermap")
    print(f"Using API key: {api_key}")
    if not api_key:
        return "Missing OpenWeatherMap API key."

    try:
        geo = requests.get("https://ipinfo.io/json").json()
        loc = geo.get("loc", "")
        city = geo.get("city", "Unknown")
        country = geo.get("country", "Unknown")

        if not loc:
            return "Could not determine location."

        lat, lon = loc.split(",")

        if os.path.exists(WEATHER_CACHE_FILE):
            with open(WEATHER_CACHE_FILE, "r") as f:
                cached = json.load(f)
                if (
                    time.time() - cached.get("timestamp", 0) < WEATHER_CACHE_DURATION
                    and cached.get("location") == loc
                ):
                    return format_weather(cached["data"])

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return f"Weather error: {data.get('message', 'unknown error')}"

        with open(WEATHER_CACHE_FILE, "w") as f:
            json.dump({"timestamp": time.time(), "location": loc, "data": data}, f)

        return format_weather(data)

    except Exception as e:
        return f"Weather error: {e}"

def get_timezone_and_time():
    try:
        geo = requests.get("https://ipinfo.io/json").json()
        timezone = geo.get("timezone")
        if not timezone:
            return "Unknown timezone"
        local_time = datetime.now(pytz.timezone(timezone)).strftime("%Y-%m-%d %H:%M:%S")
        print(local_time)
        return f"Timezone: {timezone}, Local time: {local_time}"
    except Exception as e:
        return f"Timezone error: {e}"

def format_weather(data):
    city = data.get("name", "Unknown")
    country = data.get("sys", {}).get("country", "")
    temp = data.get("main", {}).get("temp", "?")
    desc = data.get("weather", [{}])[0].get("description", "no data")
    return f"{city}, {country}: {temp}°C, {desc.capitalize()}"

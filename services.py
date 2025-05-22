import requests
import os
import json
import time
from utils import get_api_key

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

def format_weather(data):
    city = data.get("name", "Unknown")
    country = data.get("sys", {}).get("country", "")
    temp = data.get("main", {}).get("temp", "?")
    desc = data.get("weather", [{}])[0].get("description", "no data")
    return f"{city}, {country}: {temp}°C, {desc.capitalize()}"

def get_user_location():
    try:
        ipinfo_cache = "data/cached_ipinfo.json"
        if os.path.exists(ipinfo_cache):
            with open(ipinfo_cache, "r") as f:
                cached = json.load(f)
                if time.time() - cached.get("timestamp", 0) < 3 * 60 * 60:
                    return cached.get("geo", {})

        geo = requests.get("https://ipinfo.io/json").json()
        with open(ipinfo_cache, "w") as f:
            json.dump({"timestamp": time.time(), "geo": geo}, f)
        return geo
    except Exception:
        return {}
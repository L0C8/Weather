import requests
import os
import json
import time
from utils import get_api_key

WEATHER_CACHE_FILE = os.path.join("data", "cached_weather.json")
WEATHER_CACHE_DURATION = 15 * 60  # 15 minutes

def fetch_weather():
    api_key = get_api_key("openweathermap")
    if not api_key:
        return "Missing OpenWeatherMap API key."

    location = get_user_location()
    if not location or "loc" not in location:
        return "Unable to determine location."

    loc = location["loc"]
    city = location.get("city", "Unknown")
    country = location.get("country", "Unknown")
    lat, lon = loc.split(",")

    if os.path.exists(WEATHER_CACHE_FILE):
        with open(WEATHER_CACHE_FILE, "r") as f:
            cached = json.load(f)
            if (
                time.time() - cached.get("timestamp", 0) < WEATHER_CACHE_DURATION
                and cached.get("location") == loc
            ):
                return format_weather(cached["data"])

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        data = requests.get(url).json()

        if data.get("cod") != 200:
            return f"Weather error: {data.get('message', 'Unknown error')}"

        # Save to cache
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
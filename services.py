import requests, json, os
from datetime import datetime, timedelta

API_KEY = "your_openweathermap_key"
CITY = "Rome"
CACHE_PATH = "data/weather_cache.json"

def fetch_weather():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r") as f:
            cached = json.load(f)
            if datetime.fromisoformat(cached["timestamp"]) > datetime.now() - timedelta(minutes=30):
                return cached["weather"]

    try:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
        )
        data = response.json()
        weather_text = f"{CITY}: {data['main']['temp']}°C, {data['weather'][0]['description']}"
        with open(CACHE_PATH, "w") as f:
            json.dump({"timestamp": datetime.now().isoformat(), "weather": weather_text}, f)
        return weather_text
    except Exception as e:
        return f"Error: {e}"
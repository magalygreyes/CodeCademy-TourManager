import requests

def get_weather(city: str):
    """Look up current weather for a city using the free Open-Meteo API."""

    # Step 1: turn a city name into map coordinates
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo = requests.get(geo_url, params={"name": city, "count": 1}).json()

    if not geo.get("results"):
        return f"Sorry, I couldn't find a city called {city}."

    place = geo["results"][0]
    lat = place["latitude"]
    lon = place["longitude"]
    name = place["name"]
    country = place.get("country", "")

    # Step 2: use those coordinates to get the weather
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather = requests.get(weather_url, params={
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,wind_speed_10m",
    }).json()

    current = weather["current"]
    temp = current["temperature_2m"]
    wind = current["wind_speed_10m"]

    return f"{name}, {country}: {temp}°C, wind {wind} km/h."


# A quick self-test so we can run this file on its own
if __name__ == "__main__":
    print(get_weather("Osaka"))
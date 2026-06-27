import requests


def get_weather(city):
    """Look up current weather for a city using the free Open-Meteo API."""
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1},
    ).json()

    if not geo.get("results"):
        return "Sorry, I could not find a city called " + city

    place = geo["results"][0]
    lat = place["latitude"]
    lon = place["longitude"]
    name = place["name"]
    country = place.get("country", "")

    weather = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,wind_speed_10m",
        },
    ).json()

    current = weather["current"]
    temp = current["temperature_2m"]
    wind = current["wind_speed_10m"]

    return name + ", " + country + ": " + str(temp) + " C, wind " + str(wind) + " km/h."


def convert_currency(amount, from_currency, to_currency):
    """Convert money from one currency to another using the free Frankfurter API."""
    data = requests.get(
        "https://api.frankfurter.dev/v1/latest",
        params={"base": from_currency.upper(), "symbols": to_currency.upper()},
    ).json()

    rates = data.get("rates", {})
    target = to_currency.upper()

    if target not in rates:
        return "Sorry, I could not convert " + from_currency + " to " + to_currency

    converted = amount * rates[target]
    return str(amount) + " " + from_currency.upper() + " = " + format(converted, ".2f") + " " + target


if __name__ == "__main__":
    print(get_weather("Osaka"))
    print(convert_currency(18000, "JPY", "USD"))
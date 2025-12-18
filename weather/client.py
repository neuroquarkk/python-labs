import requests
from config import GEO_URL, WEATHER_URL


class WeatherClientError(Exception):
    pass


def get_coordinates(city_name: str) -> tuple[float, float, str, str]:
    try:
        response = requests.get(
            GEO_URL,
            params={"name": city_name, "count": 1, "format": "json"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        if "results" not in data:
            raise WeatherClientError(f"City '{city_name}' not found")

        location = data["results"][0]
        return (
            location["latitude"],
            location["longitude"],
            location["name"],
            location.get("country", "")
        )

    except requests.exceptions.RequestException as e:
        raise WeatherClientError(f"Network error while finding city: {e}")


def get_weather(lat: float, lon: float, unit: str = "metric") -> dict:
    unit = unit.lower()

    if unit == "metric":
        temp_unit = "celsius"
        wind_unit = "kmh"
    elif unit == "imperial":
        temp_unit = "fahrenheit"
        wind_unit = "mph"
    else:
        raise ValueError("Unit must be metric or imperial")

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,apparent_temperature,weather_code,wind_speed_10m,relative_humidity_2m",
        "temperature_unit": temp_unit,
        "wind_speed_unit": wind_unit
    }

    try:
        response = requests.get(WEATHER_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise WeatherClientError(f"Network error while fetching weather: {e}")


# coord = get_coordinates("mumbai")
# print(coord)
# print(get_weather(coord[0], coord[1]))

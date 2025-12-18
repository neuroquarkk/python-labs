from config import WEATHER_CODES


def format_weather_output(
    city: str,
    country: str,
    weather_data: dict[str, any],
    unit: str = "metric"
) -> None:
    current = weather_data.get("current", {})

    temp = current.get("temperature_2m", "N/A")
    feels_like = current.get("apparent_temperature", "N/A")
    humidity = current.get("relative_humidity_2m", "N/A")
    wind = current.get("wind_speed_10m", "N/A")
    code = current.get("weather_code", 0)

    if unit == "metric":
        temp_symbol = "°C"
        wind_symbol = "km/h"
    elif unit == "imperial":
        temp_symbol = "°F"
        wind_symbol = "mph"
    else:
        raise ValueError("Unit must be metric or imperial")

    condition = WEATHER_CODES.get(code, "Unknown")

    print("\n" + "=" * 40)
    print(f"WEATHER REPORT: {city}, {country}")
    print("=" * 40)
    print(f" Condition   : {condition}")
    print(f" Temperature : {temp}{temp_symbol}")
    print(f" Feels Like  : {feels_like}{temp_symbol}")
    print(f" Humidity    : {humidity}%")
    print(f" Wind Speed  : {wind} {wind_symbol}")
    print("=" * 40 + "\n")


def display_error(message: str):
    print(f"Error: {message}")

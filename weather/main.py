import argparse
import sys
from client import get_coordinates, get_weather, WeatherClientError
from ui import format_weather_output, display_error


def main():
    parser = argparse.ArgumentParser(description="CLI Weather Tool")
    parser .add_argument(
        "city",
        nargs="+",
        help="Name of the city"
    )

    parser.add_argument(
        "--unit",
        choices=["metric", "imperial"],
        default="metric",
        help="Unit system: metric (default) or imperial"
    )

    args = parser.parse_args()

    city_name = " ".join(args.city)

    try:
        coord_data = get_coordinates(city_name)
        weather_data = get_weather(coord_data[0], coord_data[1], args.unit)
        format_weather_output(
            coord_data[2], coord_data[3], weather_data, args.unit)
    except WeatherClientError as e:
        display_error(e)
        sys.exit(1)
    except Exception as e:
        display_error(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

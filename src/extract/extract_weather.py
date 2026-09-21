import requests
import json
from pathlib import Path

url = "https://archive-api.open-meteo.com/v1/archive"

START = "2016-01-01"
END = "2025-12-31"

cities = [
    {"city": "Chicago", "country_code": "US", "latitude": 41.8781, "longitude": -87.6298},
    {"city": "Las Vegas", "country_code": "US", "latitude": 36.1699, "longitude": -115.1398},
    {"city": "Los Angeles", "country_code": "US", "latitude": 34.0522, "longitude": -118.2437},
    {"city": "Miami", "country_code": "US", "latitude": 25.7617, "longitude": -80.1918},
    {"city": "New York", "country_code": "US", "latitude": 40.7128, "longitude": -74.0060}
]

output_folder = Path(__file__).resolve().parents[2] / "data" / "raw" / "raw_weather"
output_folder.mkdir(parents=True, exist_ok=True)

for city_info in cities:
    city = city_info["city"]
    lat = city_info["latitude"]
    lon = city_info["longitude"]

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": START,
        "end_date": END,
        "daily": "precipitation_sum,apparent_temperature_max,weathercode,windgusts_10m_max",
        "timezone": "auto"
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    city_clean = city.replace(" ", "")
    filename = output_folder / f"weather_{city_clean}_2016_2025.json"

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
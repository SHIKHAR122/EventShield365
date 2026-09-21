from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from config.api_key import TICKETMASTER_API_KEY

url = "https://app.ticketmaster.com/discovery/v2/events.json"
START = datetime.now()
END = START + relativedelta(months=12)
START = START.strftime("%Y-%m-%dT%H:%M:%SZ")
END = END.strftime("%Y-%m-%dT%H:%M:%SZ")

cities = [
    ("Chicago", "IL"),
    ("Las Vegas", "NV"),
    ("Los Angeles", "CA"),
    ("Miami", "FL"),
    ("New York", "NY")
]

output_folder = Path(__file__).resolve().parents[2] / "data" / "raw" / "raw_events"
output_folder.mkdir(parents=True, exist_ok=True)

for city, states in cities:
    params = {
        "apikey": TICKETMASTER_API_KEY,
        "city": city,
        "stateCode": states,
        "startDateTime": START,
        "endDateTime": END
    }
    response = requests.get(url, params=params)
    data = response.json()
    today = datetime.now().strftime("%Y-%m-%d")

    city_clean = city.replace(" ", "")
    filename = output_folder / f"events_{city_clean}_{today}.json"

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
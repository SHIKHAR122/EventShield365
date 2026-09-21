from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
import json
from pathlib import Path
import sys
import time

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

MAX_PAGES_PER_CITY = 10  

output_folder = Path(__file__).resolve().parents[2] / "data" / "raw" / "raw_events"
output_folder.mkdir(parents=True, exist_ok=True)

for city, states in cities:
    all_events = []

    for page in range(MAX_PAGES_PER_CITY):
        params = {
            "apikey": TICKETMASTER_API_KEY,
            "city": city,
            "stateCode": states,
            "startDateTime": START,
            "endDateTime": END,
            "page": page
        }
        response = requests.get(url, params=params)
        data = response.json()

        events_on_this_page = data.get("_embedded", {}).get("events", [])

        if not events_on_this_page:
            break

        all_events.extend(events_on_this_page)

        total_pages = data.get("page", {}).get("totalPages", 1)
        if page >= total_pages - 1:
            break

        time.sleep(0.3)  

    combined_data = {"events": all_events, "city": city}

    today = datetime.now().strftime("%Y-%m-%d")
    city_clean = city.replace(" ", "")
    filename = output_folder / f"events_{city_clean}_{today}.json"

    with open(filename, "w") as file:
        json.dump(combined_data, file, indent=4)

    print(f"{city}: saved {len(all_events)} events")
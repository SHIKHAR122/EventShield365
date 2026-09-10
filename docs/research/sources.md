# 📚 Project References & Documentation Sources

This document serves as a curated reading list and resource guide for building an event-weather risk analytics platform that integrates the **Ticketmaster Discovery API** with the **Open-Meteo Weather API**.

---

## 🛠️ API & Technical Documentation

### 1. Ticketmaster Discovery API
* **URL:** [https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/)
* **Description:** Official developer reference for searching, querying, and filtering live events, attraction metadata, and venue details globally.
* **Key Features Extracted:**
  * Venue geolocation coordinates (`latitude`, `longitude`).
  * Event schedule details (`dates.start.dateTime`, `dates.start.localTime`).
  * Classification hierarchies (`segment`, `genre`, `subGenre`) to gauge fan sensitivity.
  * Venue classification metadata (Indoor vs. Outdoor vs. Amphitheater).
* **Key Takeaways for Analytics:**
  * Precise geolocation mapping is required to query accurate hyper-local micro-forecasts.
  * Event classifications allow applying dynamic genre-based risk multipliers (e.g., classical theater vs. rock festival).

---

### 2. Open-Meteo Weather API
* **URL:** [https://open-meteo.com/](https://open-meteo.com/)
* **Description:** Free, high-resolution weather forecast API offering hourly model predictions based on national weather service models (e.g., GFS, ECMWF, DWD ICON).
* **Key Features Extracted:**
  * `precipitation` & `rain` (mm/hour)
  * `wind_gusts_10m` (km/h)
  * `apparent_temperature` (°C) — Heat index & wind chill
  * `weather_code` — WMO severe event classification codes
* **Key Takeaways for Analytics:**
  * Use hourly time-steps rather than daily summaries to align strictly with active event hours.
  * `apparent_temperature` provides a truer measurement of human physiological discomfort than dry-bulb temperature.

---

### 3. Open-Meteo Historical Forecast & Archive API
* **URL:** [https://open-meteo.com/en/docs/historical-forecast-api](https://open-meteo.com/en/docs/historical-forecast-api)
* **Description:** API providing archived forecasts and historical weather reanalysis data dating back decades.
* **Key Features Extracted:**
  * Historical weather snapshots at specific timestamps in past years.
  * Historical baseline metrics for localized climate comparison.
* **Key Takeaways for Analytics:**
  * Essential for backtesting risk models against past event attendance or documented cancellations.
  * Enables computing historical anomaly deltas (e.g., comparing forecast weather against 10-year local averages).

---

## 🏛️ Industry Safety Standards & Risk Frameworks

### 4. Outdoor Event Weather Safety Guide — HSE Blog
* **URL:** [https://www.hseblog.com/outdoor-event-weather-safety/](https://www.hseblog.com/outdoor-event-weather-safety/)
* **Description:** Health, Safety, and Environment (HSE) guide detailing operational protocols, severe weather hazards, and safety boundaries for live gatherings.
* **Key Features & Standards:**
  * Threshold definitions for heavy rain, high winds, extreme heat, and severe cold.
  * Lightning safety protocols (e.g., the 30/30 rule and monitoring safety radiuses).
* **Key Takeaways for Analytics:**
  * Wind speeds above 30–40 km/h present significant risks to temporary structures (tents, light rigs, banners).
  * Medical response requirements scale sharply when the apparent temperature exceeds 35°C or falls below 5°C.

---

### 5. Event Safety Alliance (ESA) — Weather Emergency Planning
* **URL:** [https://eu.taf.cz/why-every-live-event-needs-a-weather-emergency-plan](https://eu.taf.cz/why-every-live-event-needs-a-weather-emergency-plan)
* **Description:** Guidelines from the Event Safety Alliance on structural loading limits, weather emergency triggers, and operational stage holds.
* **Key Features & Standards:**
  * Structural wind limit stages (Operational Caution vs. Partial Hold vs. Full Evacuation).
  * Guidance on temporary stage rigging load reductions during severe gusts.
* **Key Takeaways for Analytics:**
  * Peak wind gusts (`wind_gusts_10m`) are a more important safety predictor than sustained average wind speeds.
  * WMO severe codes (95–99 for thunderstorms/hail) should automatically trigger severe risk flags regardless of precipitation volume.

---

### 6. The Financial Impact of Weather on Outdoor Events — Visual Crossing
* **URL:** [https://www.visualcrossing.com/resources/blog/outdoor-event-planning-for-unpredictable-weather-safer-smarter-venue-and-logistics-management/](https://www.visualcrossing.com/resources/blog/outdoor-event-planning-for-unpredictable-weather-safer-smarter-venue-and-logistics-management/)
* **Description:** Analytical perspective on how atmospheric conditions impact venue profitability, ticket sales drop-offs, and logistics operations.
* **Key Features & Standards:**
  * Quantifying attendance "no-show" drop-off rates due to light vs. heavy precipitation.
  * Logistics impact analysis (food & beverage sales, merchandise revenue losses).
* **Key Takeaways for Analytics:**
  * Light drizzle ($0.5 - 2.0 \text{ mm/hr}$) primarily affects drop-in ticket purchases and concessions.
  * Heavy rain ($>7.5 \text{ mm/hr}$) causes drastic attendance drop-offs for unseated outdoor events even among pre-paid ticket holders.

---

## 📊 Summary Matrix: Relevant Factors for Risk Scoring

| Variable | API Source | Inclusion Status | Reason / Analytics Role |
| :--- | :--- | :--- | :--- |
| **`venue.location`** | Ticketmaster | **Crucial** | Determines exact coordinates for spatial weather queries. |
| **`event.start/end`** | Ticketmaster | **Crucial** | Defines temporal window ($T_{\text{start}} - 2\text{h}$ to $T_{\text{end}} + 1\text{h}$) to isolate event hours. |
| **`precipitation`** | Open-Meteo | **Crucial** | Direct metric for audience comfort and attendance drop-offs. |
| **`wind_gusts_10m`** | Open-Meteo | **Crucial** | Primary metric for stage rigging and structural safety hazards. |
| **`apparent_temp`** | Open-Meteo | **Crucial** | Measures combined heat/humidity or wind chill exposure risks. |
| **`weather_code`** | Open-Meteo | **Crucial** | Fast-path severe weather detection (thunderstorms, hail, lightning). |
| *24h Daily Averages* | Derived | *Ignored* | Too broad; obscures sudden severe 1-hour storms during event times. |
| *Surface Pressure* | Open-Meteo | *Ignored* | Redundant when explicit precipitation and wind gust metrics are available. |
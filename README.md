# EventWeatherRisk

A weather-driven risk scoring system for outdoor live events, combining
real-time event data with historical climate probability to flag events
at high risk of weather-related disruption.

## The Problem

Event insurers, venue operators, and risk teams need to know: which
upcoming outdoor events are most likely to face weather disruption, and
how much risk should be priced in? This project builds a **weather risk
score** for live events by combining event data with the historical
probability of bad weather at that location and time of year.

## The Core Question

> Given an upcoming outdoor event's city, date, and venue type, what is
> its likelihood of weather-related disruption — and can we rank
> upcoming events by risk to flag the ones that need attention?

## Why This Matters

Outdoor event cancellation insurance is a real, active industry, but
risk assessment for it is usually manual or generic. This project
demonstrates how live event data and historical climate data can be
combined into a quantified, automatically-updating risk score —
something a risk or operations analyst could actually use to prioritize
review, rather than treating every outdoor event the same.

## Data Sources

| Source | Type | Purpose |
|---|---|---|
| **Ticketmaster Discovery API** | Live API | Upcoming events: city, venue, date, classification (music/sports/etc.), indoor/outdoor signal |
| **Open-Meteo Historical Weather API** | Live API | Historical climate probability (e.g., rainfall likelihood) for a given city and month |

Both APIs are free, require no payment, and are queried live — no static
CSVs, no manual downloads.

## Methodology

1. **Extract**: Pull upcoming outdoor-classified events from Ticketmaster
   for target cities; pull historical weather probability for each
   city/month from Open-Meteo
2. **Transform**: Clean event data (handle missing prices, inconsistent
   venue naming, duplicate listings), compute historical bad-weather
   probability per city/month, classify venues as outdoor/indoor
3. **Load**: Store cleaned event and weather data in PostgreSQL
4. **Analyze**: Compute a composite risk score per event, based on
   historical weather probability, venue type, and event category
5. **Present**: Power BI dashboard ranking upcoming events by risk,
   with a city-level weather-risk map

## Risk Score Components

- Historical probability of adverse weather for the event's city and
  month (from Open-Meteo)
- Venue type (outdoor/uncovered vs. indoor/covered)
- Event category sensitivity (e.g., outdoor sports vs. concerts may
  respond differently to disruption)

## Tech Stack

- **Python** — requests (API calls), Pandas, NumPy (cleaning, scoring)
- **PostgreSQL** — data storage, via SQLAlchemy
- **Power BI** — risk dashboard and city-level map
- **SQL** — aggregation and ranking queries

## Project Structure

```
eventweatherrisk/
├── data/
│   ├── raw/              # raw API pulls (event data, weather data)
│   └── processed/        # cleaned, merged data before DB load
├── src/
│   ├── extract/          # Ticketmaster + Open-Meteo API scripts
│   ├── transform/        # cleaning + risk score computation
│   ├── load/              # load into PostgreSQL
│   └── analysis/         # ranking, aggregation queries
├── sql/
│   └── schema.sql
├── notebooks/
├── config/
│   └── api_keys.py        # NEVER commit real keys — gitignored
└── README.md
```

## Limitations

- Historical weather probability is not a live forecast — for events
  far in the future, actual conditions may differ from historical
  averages
- Ticketmaster's outdoor/indoor classification is not always explicit
  and may need manual inference for some venues
- Risk score weighting (how much each factor contributes) is a
  reasoned judgment call, not a formally validated model

## Future Scope

- Automate with a scheduled pipeline (cron → Airflow) to keep risk
  scores current as new events are listed
- Add a live forecast layer for events within the short-term forecast
  window, alongside the historical baseline
- Deploy as a live, queryable dashboard or simple web app

## Status

🚧 In progress — Phase 1: data acquisition and API setup.

## Author

SHIKHAR SHARMA — data analytics portfolio project.
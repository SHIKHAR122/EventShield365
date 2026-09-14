# FEATURE DISCOVERY

This document identifies **what can be measured** to represent each hazard's
risk mechanism using available data. It does not define the final formula,
threshold, or score — that belongs in `feature_definitions.md` and
`scoring_methodology.md`. This file explores candidate measurements and
justifies which ones are worth carrying forward.

---

# Feature Discovery — Rainfall

## Business Problem

Identify the historical exposure of an event location to rainfall during
the month in which the event is scheduled.

## Related Risk Mechanism

```text
Heavy rainfall
      ↓
Water accumulation / ground saturation
      ↓
Slippery or muddy surfaces
      ↓
Mobility and access problems
      ↓
Operational disruption
```

## What Needs to Be Measured?

Potential measurements include:

- Frequency of rainfall
- Rainfall amount
- Rainfall intensity
- Rainfall duration
- Probability of rainfall

## Required Data

- Historical daily precipitation
- Historical daily rainfall
- Event city
- Event date
- Historical observation period

## Available API Data

Open-Meteo provides:

- `precipitation_sum`
- `rain_sum`
- `precipitation_hours`
- `precipitation_probability` for forecast data

| Candidate measure | Required data | Open-Meteo available? |
|---|---|---|
| Rainfall amount | `precipitation_sum` | Yes |
| Rain amount | `rain_sum` | Yes |
| Historical rain frequency | Historical `precipitation_sum` | Yes — can be derived |
| Historical rain probability | Historical precipitation observations | Yes — derived |
| Rain duration | `precipitation_hours` | Potentially |
| Forecast rain probability | `precipitation_probability` | Yes, for forecast data |

Historical rainfall probability is derived from historical precipitation
observations rather than directly retrieved from the API.

## Candidate Feature

`rain_probability_pct`

## Transformation

```text
Historical daily precipitation
      ↓
Apply selected rainfall threshold
      ↓
Classify Rain Day / Non-Rain Day
      ↓
Group by city and month
      ↓
Calculate proportion of Rain Days
      ↓
rain_probability_pct
```

Formula:

> **rain_probability_pct = (rain days / total historical days) × 100**

## Candidate Feature Evaluation

| Question | Answer |
|---|---|
| Does it represent the risk mechanism? | Yes |
| Is the data available? | Yes |
| Is it interpretable? | Yes |
| Is it available historically? | Yes |
| Is it available for future events? | Need to check (forecast probability is a separate field) |
| Does it introduce unnecessary complexity? | Low |
| Does it have business meaning? | Yes |

## Why This Feature?

The feature converts raw historical precipitation observations into an
interpretable city-month rainfall exposure measure.

## Limitations

The feature represents rainfall frequency but does not directly represent
rainfall severity or duration. Therefore, a location with frequent light
rainfall could receive a higher value than a location with infrequent but
extremely heavy rainfall. Further research is required to determine
whether an additional rainfall-intensity or duration feature is necessary.

---

# Feature Discovery — Extreme Heat

## Business Problem

Identify the historical exposure of an event location to physiologically
dangerous heat conditions during the month in which the event is scheduled.

## Related Risk Mechanism

```text
High air temperature + humidity + radiant heat
      ↓
Reduced ability of the body to cool itself
      ↓
Heat load accumulates with exposure duration and crowd density
      ↓
Heat-related illness (exhaustion, heat stroke)
      ↓
Operational disruption / medical incidents
```

## What Needs to Be Measured?

Potential measurements include:

- Air temperature
- Apparent ("feels like") temperature
- Frequency of high-heat days
- Duration of heat exposure within a day
- Humidity contribution to perceived heat

## Required Data

- Historical daily maximum temperature
- Historical daily apparent temperature
- Event city
- Event date
- Historical observation period

## Available API Data

Open-Meteo provides:

- `temperature_2m_max`
- `apparent_temperature_max`
- `relative_humidity_2m` (hourly, can be aggregated)

| Candidate measure | Required data | Open-Meteo available? |
|---|---|---|
| Raw daily max temperature | `temperature_2m_max` | Yes |
| Perceived ("feels like") temperature | `apparent_temperature_max` | Yes |
| Historical heat-risk frequency | Historical `apparent_temperature_max` | Yes — can be derived |
| Historical heat-risk probability | Historical apparent temperature observations | Yes — derived |
| Humidity contribution | `relative_humidity_2m` | Yes, hourly — would need aggregation |

## Candidate Feature

`heat_risk_pct`

## Transformation

```text
Historical daily apparent temperature
      ↓
Apply selected heat-risk threshold
      ↓
Classify Heat-Risk Day / Normal Day
      ↓
Group by city and month
      ↓
Calculate proportion of Heat-Risk Days
      ↓
heat_risk_pct
```

Formula:

> **heat_risk_pct = (heat-risk days / total historical days) × 100**

## Candidate Feature Evaluation

| Question | Answer |
|---|---|
| Does it represent the risk mechanism? | Yes |
| Is the data available? | Yes |
| Is it interpretable? | Yes |
| Is it available historically? | Yes |
| Is it available for future events? | Need to check (forecast apparent temperature is a separate field) |
| Does it introduce unnecessary complexity? | Low |
| Does it have business meaning? | Yes |

## Why This Feature?

Apparent temperature is prioritized over raw air temperature because it
incorporates humidity, which is a core driver of physiological heat load
per the WHO/NWS evidence — raw air temperature alone would understate
risk in humid coastal cities relative to dry ones at the same reading.

## Limitations

The feature does not account for crowd density, shade availability, or
event duration — all identified in the underlying risk mechanism as
compounding factors. A day with the same `heat_risk_pct` could represent
very different actual risk depending on event type (a 3-hour evening
concert vs. an all-day outdoor festival). Further research is required
to determine whether event-duration or event-type weighting should be
layered onto this feature downstream, rather than embedded within it.

---

# Feature Discovery — Thunderstorm

## Business Problem

Identify the historical exposure of an event location to thunderstorm
conditions during the month in which the event is scheduled, distinct
from ordinary rainfall.

## Related Risk Mechanism

```text
Thunderstorm system develops
      ↓
Simultaneous lightning, sudden gusts, heavy rain
      ↓
Fast onset, limited lead time
      ↓
Decision-time compression
      ↓
Mandatory show-stop / evacuation
```

## What Needs to Be Measured?

Potential measurements include:

- Occurrence of thunderstorm conditions (categorical, not amount-based)
- Frequency of thunderstorm days
- Probability of thunderstorm occurrence
- Severity/type of storm (ordinary vs. severe with hail)

## Required Data

- Historical daily weather classification
- Event city
- Event date
- Historical observation period

## Available API Data

Open-Meteo provides:

- `weathercode` (WMO categorical weather code, daily)

| Candidate measure | Required data | Open-Meteo available? |
|---|---|---|
| Thunderstorm occurrence (categorical) | `weathercode` (codes 95–99) | Yes |
| Historical storm frequency | Historical `weathercode` | Yes — can be derived |
| Historical storm probability | Historical weathercode observations | Yes — derived |
| Severe storm distinction (hail) | `weathercode` (codes 96, 99 specifically) | Yes — can be derived at finer granularity |

Unlike rainfall and heat, this hazard is not measured from a continuous
numeric variable — `weathercode` is categorical, so the "measurement" is
occurrence-based rather than amount-based.

## Candidate Feature

`storm_probability_pct`

## Transformation

```text
Historical daily weathercode
      ↓
Identify codes within thunderstorm range (95–99)
      ↓
Classify Storm Day / Non-Storm Day
      ↓
Group by city and month
      ↓
Calculate proportion of Storm Days
      ↓
storm_probability_pct
```

Formula:

> **storm_probability_pct = (storm days / total historical days) × 100**

## Candidate Feature Evaluation

| Question | Answer |
|---|---|
| Does it represent the risk mechanism? | Yes |
| Is the data available? | Yes |
| Is it interpretable? | Yes |
| Is it available historically? | Yes |
| Is it available for future events? | Need to check (forecast weathercode is a separate field) |
| Does it introduce unnecessary complexity? | Low |
| Does it have business meaning? | Yes |

## Why This Feature?

`weathercode` provides a direct categorical signal for thunderstorm
occurrence, which is more reliable than attempting to infer storms
indirectly from precipitation or wind spikes alone.

## Limitations

The feature treats all thunderstorm days as equivalent, even though
`weathercode` distinguishes ordinary thunderstorms (95) from storms with
hail (96, 99), which likely carry different severity. The current feature
does not capture storm duration, timing within the day, or intensity —
only occurrence. Further research is required to determine whether
severity-weighted storm classification is necessary.

---

# Feature Discovery — High Wind

## Business Problem

Identify the historical exposure of an event location to structurally
significant wind conditions during the month in which the event is
scheduled.

## Related Risk Mechanism

```text
High wind gusts occur
      ↓
Turbulence and secondary effects (debris, anchor loosening)
      ↓
Progressive structural strain over event duration
      ↓
Structural instability or failure
      ↓
Operational disruption / safety risk
```

## What Needs to Be Measured?

Potential measurements include:

- Sustained wind speed
- Wind gust speed
- Frequency of high-wind days
- Probability of high-wind occurrence

## Required Data

- Historical daily maximum wind speed
- Historical daily maximum wind gusts
- Event city
- Event date
- Historical observation period

## Available API Data

Open-Meteo provides:

- `windspeed_10m_max`
- `windgusts_10m_max` (availability in the historical archive specifically
  needs to be confirmed during data extraction)

| Candidate measure | Required data | Open-Meteo available? |
|---|---|---|
| Sustained wind speed | `windspeed_10m_max` | Yes, confirmed in historical archive |
| Gust wind speed | `windgusts_10m_max` | Likely — needs direct confirmation historically |
| Historical high-wind frequency | Historical wind data | Yes — can be derived |
| Historical high-wind probability | Historical wind observations | Yes — derived |

## Candidate Feature

`wind_risk_pct`

## Transformation

```text
Historical daily wind gusts (or sustained speed, if gusts unavailable)
      ↓
Apply selected wind-risk threshold
      ↓
Classify High-Wind Day / Normal Day
      ↓
Group by city and month
      ↓
Calculate proportion of High-Wind Days
      ↓
wind_risk_pct
```

Formula:

> **wind_risk_pct = (high-wind days / total historical days) × 100**

## Candidate Feature Evaluation

| Question | Answer |
|---|---|
| Does it represent the risk mechanism? | Yes |
| Is the data available? | Yes, with `windspeed_10m_max` as a confirmed fallback |
| Is it interpretable? | Yes |
| Is it available historically? | Yes (gusts pending confirmation) |
| Is it available for future events? | Need to check (forecast wind gusts is a separate field) |
| Does it introduce unnecessary complexity? | Low |
| Does it have business meaning? | Yes |

## Why This Feature?

Gusts, rather than sustained wind speed, are identified as the primary
driver of structural risk, so `windgusts_10m_max` is the preferred
underlying variable where confirmed available; `windspeed_10m_max` serves
as a documented fallback rather than a silent substitution.

## Limitations

The feature measures wind occurrence but does not represent the
progressive/cumulative nature of the mechanism — a structure exposed to
repeated moderate gusts across a multi-day event may be at real risk even
if no single day crosses the chosen threshold. The feature also does not
yet account for venue/structure type, which the underlying risk mechanism
identifies as a major factor in actual exposure. Further research is
required to determine whether a duration-weighted or structure-type-
weighted version of this feature is necessary.
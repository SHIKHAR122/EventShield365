# FEATURE DEFINITION

This document identifies and locks in the **features that should be measured** to represent in hazard's risk mechanism using the available data. It defines the final formula, threshold.

But before that i would like to clear the fact that i have not used any ML model or any ML algorithm to define the business features and the weight distribution - I used deterministic thresholds and a documented weighting scheme rather than ML, because I didn't have historical ground-truth labels on actual event disruptions to train against — building an ML model without that would just be fitting to noise. If historical disruption outcome data existed, this would be a natural candidate for a learned model instead of fixed weights." That's a stronger, more honest answer than pretending you used ML for the sake of it.

## FEATURE 1

> **rain_probability_pct = (rain days / total historical days) × 100**

## Why This Feature?

The feature converts raw historical precipitation observations into an interpretable city-month rainfall exposure measure.

## Which Raw Data Creates It?

The raw data used to create **rain_probability_pct** are as follows:

> `precipitation_sum`

> `rain_sum`

## Final Threshold

A day is classified as a **rain day** if `precipitation_sum ≥ 1.0mm`.

This threshold is chosen over the stricter 5mm alternative because 1.0mm is the standard meteorological convention (WMO) for defining a measurable rain day. Using the widely recognized standard makes the feature easier to justify and interpret than an arbitrary cutoff.

## Final Historical Period

Data is pulled from **2015–2024** (10 years). This range balances having enough years for a statistically meaningful probability with staying reasonably close to current climate conditions, rather than including decades-old data that may not reflect present-day rainfall patterns.

## Missing Data Handling

If a city-month has fewer than 20 valid daily records out of the expected ~300 (10 years × ~30 days), the feature is not computed for that city-month and is instead flagged as **insufficient data**, rather than calculated from an incomplete sample. Days with missing or null `precipitation_sum` values are excluded from both the numerator and denominator, not treated as zero rainfall.

## Output Format

- **Data type:** float
- **Range:** 0–100 (percentage)
- **Null value:** returned when the city-month does not meet the minimum valid-day requirement above

## Potential Limitations

The feature captures rainfall **frequency**, not **severity** — a city with frequent light rain could score higher than a city with rare but extreme rainfall events. This means `rain_probability_pct` alone may understate risk for locations prone to infrequent but intense rainfall.

## How It Is Exactly Calculated?

The following steps are used to define this business feature:

- Decide what counts as a rain day (see Final Threshold above)
- Pull historical daily precipitation data for the specific city and month, across all years in the historical period
- Count how many of those days cross the threshold
- Divide to get the probability:

```text
days which cross threshold / total number of days = probability
```

---

## FEATURE 2

> **storm_probability_pct = (stormy days / total historical days) × 100**

## Why This Feature?

`weathercode` provides a direct categorical signal for thunderstorm occurrence, which is more reliable than attempting to infer storms indirectly from precipitation or wind spikes alone.

## Which Raw Data Is Used?

weathercode is the raw data that has been used to calculate the storm probability.

## Final Threshold

A day is classified as a storm day if weathercode falls in {95, 96, 99}:

95 — Thunderstorm, slight or moderate, without hail

96 — Thunderstorm, slight or moderate, with hail

99 — Thunderstorm, heavy, with hail

## Final Historical Period

Data is pulled from **2015–2024** (10 years). This range balances having enough years for a statistically meaningful probability with staying reasonably close to current climate conditions, rather than including decades-old data that may not reflect present-day heavy storm patterns.

## How It Is Exactly Calculated?

The following steps are used to define this business feature:

- Decide what counts as a storm day (see Final Threshold above)
- Pull historical daily `weathercode` values for the specific city and month, across all years in the historical period
- Count how many of those days have a `weathercode` falling within {95, 96, 99}
- Divide to get the probability:

```text
days with weathercode in {95, 96, 99} / total number of days = probability
```

## Missing Data Handling

If a city-month has fewer than 20 valid daily `weathercode` records out of the expected ~300 (10 years × ~30 days), the feature is not computed for that city-month and is instead flagged as **insufficient data**, rather than calculated from an incomplete sample. Days with missing or null `weathercode` values are excluded from both the numerator and denominator, not treated as non-storm days.

## Output Format

- **Data type:** float
- **Range:** 0–100 (percentage)
- **Null value:** returned when the city-month does not meet the minimum valid-day requirement above

## Potential Limitations

The feature treats all storm days as equivalent, even though `weathercode` distinguishes ordinary thunderstorms (95) from storms with hail (96, 99), which likely carry different severity. The feature also does not capture storm duration, timing within the day, or how many separate storm events occurred — only whether at least one qualifying code was recorded that day. A city with one severe storm per month and a city with several minor storms per month could receive similar scores despite very different actual risk profiles.

---

## FEATURE 3

> **heat_risk_pct = (heat-risk days / total historical days) × 100**

## Why This Feature?

Apparent temperature is prioritized over raw air temperature because it incorporates humidity, which is a core driver of physiological heat load — raw air temperature alone would understate risk in humid coastal cities relative to dry ones at the same reading.

## Which Raw Data Creates It?

The raw data used to create **heat_risk_pct** are as follows:

> `apparent_temperature_max`

> `temperature_2m_max`

## Final Threshold

A day is classified as a **heat-risk day** if `apparent_temperature_max ≥ 35°C`.

This threshold is chosen because 35°C apparent temperature is a commonly referenced heat-caution level in public health guidance (WHO/NWS), rather than an arbitrary round number. Apparent temperature is used instead of raw `temperature_2m_max` because it reflects the actual physiological heat load, not just air temperature alone.

## Final Historical Period

Data is pulled from **2015–2024** (10 years). This range balances having enough years for a statistically meaningful probability with staying reasonably close to current climate conditions, rather than including decades-old data that may not reflect present-day heat patterns.

## How It Is Exactly Calculated?

The following steps are used to define this business feature:

- Decide what counts as a heat-risk day (see Final Threshold above)
- Pull historical daily `apparent_temperature_max` for the specific city and month, across all years in the historical period
- Count how many of those days cross the threshold
- Divide to get the probability:

```text
days which cross threshold / total number of days = probability
```

## Missing Data Handling

If a city-month has fewer than 20 valid daily records out of the expected ~300 (10 years × ~30 days), the feature is not computed for that city-month and is instead flagged as **insufficient data**, rather than calculated from an incomplete sample. Days with missing or null `apparent_temperature_max` values are excluded from both the numerator and denominator, not treated as non-heat-risk days.

## Output Format

- **Data type:** float
- **Range:** 0–100 (percentage)
- **Null value:** returned when the city-month does not meet the minimum valid-day requirement above

## Potential Limitations

The feature does not account for crowd density, shade availability, or event duration — all identified as compounding factors in the underlying risk mechanism. A day with the same `heat_risk_pct` could represent very different actual risk depending on event type (a 3-hour evening concert vs. an all-day outdoor festival), since this feature measures weather exposure only, independent of event characteristics.

---

## FEATURE 4

> **wind_risk_pct = (high-wind days / total historical days) × 100**

## Why This Feature?

Gusts, rather than sustained wind speed, are identified as the primary driver of structural risk (tents, stages, temporary structures), so `windgusts_10m_max` is the preferred underlying variable where confirmed available; `windspeed_10m_max` serves as a documented fallback rather than a silent substitution if gusts data proves unavailable in the historical archive.

## Which Raw Data Creates It?

The raw data used to create **wind_risk_pct** are as follows:

> `windgusts_10m_max`

> `windspeed_10m_max` (fallback)

## Final Threshold

A day is classified as a **high-wind day** if `windgusts_10m_max ≥ 50 km/h` (or `windspeed_10m_max ≥ 50 km/h` if gusts data is unavailable for that location/period).

This threshold is chosen as a commonly referenced structural-risk level for temporary event infrastructure (tents, stages, signage), rather than an arbitrary cutoff. The exact figure should be cross-checked against manufacturer/engineer wind ratings for typical temporary event structures if more precise validation is needed later.

## Final Historical Period

Data is pulled from **2015–2024** (10 years). This range balances having enough years for a statistically meaningful probability with staying reasonably close to current climate conditions, rather than including decades-old data that may not reflect present-day wind patterns.

## How It Is Exactly Calculated?

The following steps are used to define this business feature:

- Decide what counts as a high-wind day (see Final Threshold above)
- Pull historical daily `windgusts_10m_max` (or `windspeed_10m_max` if gusts unavailable) for the specific city and month, across all years in the historical period
- Count how many of those days cross the threshold
- Divide to get the probability:

```text
days which cross threshold / total number of days = probability
```

## Missing Data Handling

If a city-month has fewer than 20 valid daily records out of the expected ~300 (10 years × ~30 days), the feature is not computed for that city-month and is instead flagged as **insufficient data**, rather than calculated from an incomplete sample. Days with missing or null wind values are excluded from both the numerator and denominator, not treated as non-high-wind days.

## Output Format

- **Data type:** float
- **Range:** 0–100 (percentage)
- **Null value:** returned when the city-month does not meet the minimum valid-day requirement above

## Potential Limitations

The feature measures wind occurrence but does not represent the progressive/cumulative nature of the underlying risk mechanism — a structure exposed to repeated moderate gusts across a multi-day event may be at real risk even if no single day crosses the chosen threshold. The feature also does not account for venue/structure type, which is a major factor in actual exposure and is applied separately during scoring rather than embedded in this feature.

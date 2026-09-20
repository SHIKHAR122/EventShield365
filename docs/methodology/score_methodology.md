
---

# SCORING METHODOLOGY

This document defines how the four independently-calculated hazard features (`rain_probability_pct`, `heat_risk_pct`, `storm_probability_pct`, `wind_risk_pct`) combine into a single final risk score per event.

As stated in `feature_definitions.md`, no ML model or learned weighting is used here. All weights and thresholds are deterministic, reasoned judgment calls, documented explicitly below — not fitted from historical outcome data, since no ground-truth event-disruption labels are available.

---

## 1. Normalization

All four features (`rain_probability_pct`, `heat_risk_pct`, `storm_probability_pct`, `wind_risk_pct`) are already expressed on the same 0–100 scale by construction, since each is computed as a percentage of historical days crossing a threshold. No additional normalization (e.g., min-max scaling or z-scoring) is applied, since the features are already directly comparable on a common scale.

## 2. Weight Distribution

Weights are assigned based on **severity and irreversibility of consequence**, not frequency of occurrence — a hazard that occurs rarely but forces total event cancellation is weighted higher than a more frequent but less disruptive hazard.

| Hazard | Weight | Justification |
|---|---|---|
| Storm | 35% | Forces immediate, mandatory shutdown for safety/liability regardless of event type; highest-severity, least adaptable hazard |
| Rain | 30% | Most universally applicable disruptor across all event types; affects ground conditions, access, and mobility |
| Wind | 20% | Serious structural risk, but highly conditional on venue/structure type rather than universal |
| Heat | 15% | Real health risk, but rarely causes outright cancellation; impact concentrated in long-duration/high-exertion events |

**Total: 100%**

## 3. Venue Type Multiplier

Identical weather exposure carries very different actual risk depending on whether a venue is outdoor or indoor. A multiplier is applied to the combined weather score:

| Venue Type | Multiplier | Justification |
|---|---|---|
| Outdoor | 1.0 | Full weather exposure — no risk mitigation from structure |
| Indoor | 0.2 | Weather risk is substantially reduced but not zero (e.g., access/transportation to the venue can still be affected by severe weather) |

## 4. Final Formula

```
weighted_weather_score = (storm_probability_pct × 0.35)
                        + (rain_probability_pct × 0.30)
                        + (wind_risk_pct × 0.20)
                        + (heat_risk_pct × 0.15)

final_risk_score = weighted_weather_score × venue_type_multiplier
```

Output range: 0–100.

## 5. Risk Bands

| Risk Score | Category |
|---|---|
| 0–25 | Low |
| 25–50 | Medium |
| 50–75 | High |
| 75–100 | Severe |

These bands divide the 0–100 range into four equal quartiles as a starting methodology. They are treated as an initial, reasoned default rather than empirically validated cutoffs, since no historical disruption outcome data exists to calibrate them against actual event impact.

## 6. Sensitivity Check

Before finalizing this methodology, weights should be tested by shifting each hazard's weight by ±5% individually and re-ranking the top 10 riskiest events in the dataset. If the ranking remains largely stable under small weight perturbations, the methodology is considered robust. If small changes significantly reorder high-risk events, the weight distribution should be revisited before being treated as final. This check has not yet been executed and is planned as a validation step once real event and weather data has been loaded.

## 7. Limitations of the Scoring Methodology

- **Weights are reasoned, not empirically validated.** Without historical ground-truth data on actual event disruptions, there is no way to confirm these specific percentages are optimal — they represent a defensible judgment call, not a proven model.
- **Hazards are treated as independent, but can co-occur.** A single severe weather day may simultaneously qualify as a storm day, a rain day, and a high-wind day (a thunderstorm inherently brings rain and gusts). The current formula sums all four weighted contributions without adjusting for this overlap, which may inflate the combined score on days where multiple hazard definitions are triggered by the same underlying weather event.
- **Risk bands are evenly spaced by default**, not derived from any distribution analysis of actual computed scores. Once real event data is scored, the bands may need adjustment if scores cluster unevenly across the 0–100 range.
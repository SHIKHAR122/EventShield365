# WEATHER HAZARDS 

This document identifies the major weather hazards that can affect outdoor live events and explains why each hazard is relevant from an event-operations perspective.

The hazards are identified through research from official weather organizations, event-safety guidelines, and industry sources.

**The purpose of this research is to establish which weather conditions should be considered in EventShield365 before determining the measurable data features and risk-scoring methodology.**

---

# Weather Hazard 1: **RAIN**

## **Why It Matters**

**Rain is one of the most obvious weather hazards to consider when analysing weather-related risk for outdoor events.** It can directly affect outdoor events and, in extreme cases, may also create secondary operational problems for indoor events, such as issues with access, transportation, or surrounding site conditions.

**Therefore, rainfall is included as a hazard in the EventShield365 analysis.**

## **Evidence**

The YOUROPE article, **Risk Assessment Template: Heavy Rain**, provides evidence supporting the consideration of heavy rainfall as an event-related hazard:

https://yourope.org/know-how/wtb-17-risk-assessment-template-heavy-rain/

The article identifies several **site-specific exposure factors**, including:

- **Soil and ground type**
- **Drainage capacity**
- **Site slope**
- **Temporary surfaces**
- **Audience areas**
- **Access and egress routes**

It also identifies potential consequences across different phases of an event:

- **Ingress:** Slippery surfaces, delays, and queuing
- **Event operation:** Reduced mobility and potential medical incidents
- **Egress:** Congestion, falls, and difficulties with vehicle movement
- **Breakdown:** Site damage and difficulties with equipment recovery

**This supports the risk mechanism that rainfall can affect an event by changing ground conditions and creating operational problems with movement, access, and site management.**

---

## **Data Sources and Variables**

**Open-Meteo provides several variables that can be used to measure rainfall.** For the current analysis, the following variables are considered relevant:

> **`precipitation_sum`**
> **`rain_sum`**
> **`precipitation_probability_max`**

**Note:** `precipitation_probability_max` is not being directly used as a historical record in this analysis. Instead, the historical probability is calculated from past precipitation observations.

### **Historical Rainfall Probability**

For the historical analysis, **rainfall probability is derived from historical daily precipitation data rather than directly taken from an API probability field.**

The calculation is based on the fraction of historical days in a given **city-month** for which daily precipitation exceeded a selected threshold.

---

## **Step-by-Step Logic**

### **1. Define what counts as a "rain day"**

A threshold must first be selected to determine whether a particular day is considered a rain day.

**A commonly used meteorological threshold is 1.0 mm of precipitation in 24 hours.** However, the threshold should ultimately be selected based on the business objective of EventShield365.

A stricter threshold, such as **5 mm**, could be used if the objective is to identify rainfall that is more likely to create operational disruption rather than simply measurable rainfall.

### **2. Collect historical daily precipitation**

Pull historical daily `precipitation_sum` data for a specific city and month across multiple years.

**Example:**

For Miami in September, using data from **2015–2024**:

- 10 years of September data
- Approximately 30 days per September
- **300 daily observations**

### **3. Count days that crossed the threshold**

Suppose **96 out of 300 September days** had:

> **`precipitation_sum ≥ 1.0 mm`**

Those 96 observations are classified as rain days under the selected threshold.

### **4. Calculate historical rain probability**

The historical rain probability is calculated as:

> **Rain Probability (%) = Rain Days / Total Historical Days × 100**

For the example:

> **96 / 300 × 100 = 32%**

Therefore:

**The historical probability of a day in September experiencing at least 1.0 mm of precipitation in Miami would be estimated at 32%.**

This value is a **derived analytical feature**, not a value directly returned by the historical weather API.

---

## **Choosing the Rainfall Threshold**

**The rainfall threshold is an important modelling decision because it determines what the analysis considers meaningful rainfall.**

### **Lower Threshold — ≥ 0.1 mm**

- Captures very small amounts of measurable precipitation
- Produces a more sensitive rainfall indicator
- May identify conditions that have little operational impact

### **Higher Threshold — ≥ 5 mm**

- Captures more substantial rainfall
- Produces a lower rainfall frequency
- May provide a more operationally meaningful indicator of potentially disruptive rainfall

**The final threshold should be justified using the EventShield365 business objective and supporting evidence rather than selected arbitrarily.**

---

## **Potential Business Feature**

The primary candidate business feature for this hazard is:

> **`rain_probability_pct`**

### **Reasoning**

**Rainfall is a broadly applicable weather hazard across many types of outdoor events, including concerts, sports events, festivals, and marathons.**

Unlike some more specialised hazards, rainfall can affect a wide range of event operations through changes in ground conditions, access, mobility, and audience movement.

**Rainfall also provides a relatively direct historical signal because `precipitation_sum` is an observed weather variable rather than an inferred operational measure.**

Therefore:

> **`rain_probability_pct` is proposed as a candidate business feature for the rainfall hazard because it converts historical precipitation observations into an interpretable city-month exposure measure.**

**This is currently a candidate feature, not a finalized feature or risk score component. Further validation of the threshold, historical period, and business interpretation is required before it is included in the final scoring methodology.**

---

# Weather Hazard 2: **Extreme Heat**

## **Why It Matters**

**Extreme Heat can be ranked as the second highest hazard which affects the events** as it affects long-duration or physically demanding outdoor events (marathons, all-day festivals, sports) — public health risk, not just discomfort.

**Therefore, Extreme Heat is included as a hazard in the EventShield365 analysis.**

## **Evidence**

The YOUROPE Article "Risk Assessment Template: Heat (Heat Stress, High Thermal Load)" provides evidence supporting the consideration of heat as an event-related hazard:

https://yourope.org/know-how/wtb-19-risk-assessment-template-heat/

Another article of "National Weather Service (NWS)" and World Health Organization (WHO) provide us evidence going hand in hand with the article of YOUROPE, collectively they give us a good idea about the following matters:

[WHO ARTICLE](https://www.who.int/news/item/06-07-2026-advancing-heat-health-preparedness-during-mass-gatherings--practical-tools)
[NWS ARTICLE](https://www.weather.gov/safety/heat)

It identifies high thermal load as a hazard and says heat risk depends on factors such as:

- **Air temperature**
- **Solar/radiant heat**
- **Humidity**
- **Wind / ventilation**
- **Shade availability**
- **Water and cooling availability**
- **Crowd density**
- **Audience vulnerability**
- **Staffing**
- **Event phase**

## **Data Sources and Variables**

**Open-Meteo provides several variables that can be used to measure extreme heat.** For the current analysis, the following variables are considered relevant:

> **`temperature_2m_max`**
> **`apparent_temperature_max`**

**Note:** `apparent_temperature_max` is prioritized over raw `temperature_2m_max` as the primary heat-risk variable, since apparent temperature incorporates humidity into a single "feels like" figure — closer to the actual physiological heat load referenced in the WHO and NWS sources above than air temperature alone.

### **Historical Heat Risk Probability**

Following the same logic established for rainfall, heat risk is calculated as a threshold-crossing frequency rather than a raw average.

**1. Define what counts as a "heat risk day."**
A threshold must be selected — for example, `apparent_temperature_max ≥ 35°C`, a commonly referenced heat-caution level in public health guidance.

**2. Collect historical daily apparent temperature** for a specific city and month, across multiple years.

**3. Count days that crossed the threshold.**

**4. Calculate historical heat risk probability:**

> **Heat Risk Probability (%) = Heat Risk Days / Total Historical Days × 100**

**This value is a derived analytical feature, following the same construction method as `rain_probability_pct`.**

## **Potential Business Feature**

> **`heat_risk_pct`**

### **Reasoning**

**Extreme heat is not universally relevant across all event types the way rainfall is** — its impact is concentrated in long-duration or physically demanding outdoor events (marathons, all-day festivals, extended sports fixtures), consistent with the WHO and NWS guidance above identifying event duration and audience exertion as key risk modifiers.

Therefore:

> **`heat_risk_pct` is proposed as a candidate business feature because it converts historical apparent-temperature observations into an interpretable city-month exposure measure, distinct from rainfall because it reflects a different mechanism of harm (physiological heat load rather than ground/access disruption).**

**This is currently a candidate feature, not a finalized feature or risk score component.**

---

# Weather Hazard 3: **Thunderstorm (Lightning, Wind, Heavy Rain)**

## **Why It Matters**

**Thunderstorms are ranked as the highest-severity hazard considered in EventShield365**, distinct from ordinary rainfall because they typically force an immediate, mandatory operational stop rather than a gradual disruption.

**Therefore, thunderstorm risk is included as a hazard in the EventShield365 analysis, separate from general rainfall.**

## **Evidence**

The YOUROPE article, **Risk Assessment Template: Thunderstorm**, provides evidence supporting the consideration of thunderstorms as a distinct event-related hazard:

https://yourope.org/know-how/wtb-16-risk-assessment-template-thunderstorm/

The article identifies thunderstorms as a compound hazard type, including:

- **Cloud-to-ground lightning**
- **Strong gusts and squalls**
- **Heavy rainfall and local flooding**
- **Rapid weather changes with limited lead time**

It emphasizes that effective management depends on **early recognition, clear decision authority, predefined thresholds, and disciplined execution under time pressure** — reinforcing that thunderstorms require **predefined show-stop triggers**, not gradual response, unlike the ingress/egress-phase disruptions described for ordinary rain.

**This supports the risk mechanism that thunderstorms represent a categorically different type of risk from rainfall — one requiring immediate cessation of activity rather than operational adaptation.**

## **Data Sources and Variables**

**Open-Meteo provides a categorical variable that can be used to identify thunderstorm conditions.** For the current analysis, the following variable is considered relevant:

> **`weathercode`**

**Note:** Unlike rainfall and heat, thunderstorm risk is not derived from a continuous numeric threshold. Open-Meteo's `weathercode` field uses WMO (World Meteorological Organization) codes, where a defined range of codes (in the 95–99 range) explicitly corresponds to thunderstorm activity. This provides a more direct categorical signal than inferring storms from precipitation or wind data alone.

### **Historical Storm Probability**

**1. Define which weathercode values count as a "storm day."**
WMO codes 95–99 (thunderstorm, with or without hail) are the relevant range.

**2. Collect historical daily `weathercode`** for a specific city and month, across multiple years.

**3. Count days where the code falls within the storm range.**

**4. Calculate historical storm probability:**

> **Storm Probability (%) = Storm Days / Total Historical Days × 100**

## **Potential Business Feature**

> **`storm_probability_pct`**

### **Reasoning**

**Thunderstorms are proposed as a separate feature from rainfall because they carry a categorically different consequence** — supported directly by the YOUROPE evidence above, which treats thunderstorms as requiring predefined show-stop decision thresholds rather than the operational-adaptation response associated with ordinary rain.

Therefore:

> **`storm_probability_pct` is proposed as a candidate business feature because it captures a distinct, higher-severity risk mechanism (mandatory cessation) that would be diluted if merged into `rain_probability_pct`.**

**This is currently a candidate feature, not a finalized feature or risk score component.**

---

# Weather Hazard 4: **High Wind**

## **Why It Matters**

**High wind is considered a hazard distinct from rainfall and thunderstorms because its primary risk mechanism relates to physical infrastructure rather than ground conditions or lightning exposure.**

**Therefore, wind is included as a hazard in the EventShield365 analysis.**

## **Evidence**

The YOUROPE article, **Risk Assessment Template: High Winds**, provides evidence supporting the consideration of wind as a distinct event-related hazard:

https://yourope.org/know-how/wtb-18-risk-assessment-template-high-winds/

The article identifies that **high wind risk is frequently driven by gusts, turbulence, and secondary effects (debris, progressive loosening of anchors), not by average wind alone**, and that exposure depends on:

- **Local topography** (wind channels, ridgelines, open fields)
- **Density and type of temporary structures**
- **Degree of shielding**
- **Operational phase** (build-up with incomplete structures vs. show time at maximum occupancy)

**This supports the risk mechanism that wind primarily threatens temporary structures (stages, tents, screens) rather than affecting all event types uniformly** — reinforcing why wind should interact with venue/structure type in the final scoring methodology, rather than being applied as a flat, universal hazard.

## **Data Sources and Variables**

**Open-Meteo provides variables that can be used to measure wind conditions.** For the current analysis, the following variables are considered relevant:

> **`windspeed_10m_max`**
> **`windgusts_10m_max`**

**Note:** Consistent with the YOUROPE evidence above identifying gusts (not sustained average wind) as the primary driver of structural risk, `windgusts_10m_max` is prioritized as the main variable where available. `windspeed_10m_max` is confirmed present in Open-Meteo's historical archive; availability of `windgusts_10m_max` specifically in the historical archive should be verified directly during data extraction, with `windspeed_10m_max` as the fallback variable if gusts are not available historically.

### **Historical Wind Risk Probability**

**1. Define what counts as a "high wind day."**
A threshold must be selected — for example, `windgusts_10m_max ≥ 50 km/h`, though the exact figure should be validated against structural/engineering wind-rating references, consistent with the YOUROPE recommendation to use manufacturer/engineer wind ratings as a baseline.

**2. Collect historical daily wind data** for a specific city and month, across multiple years.

**3. Count days that crossed the threshold.**

**4. Calculate historical wind risk probability:**

> **Wind Risk Probability (%) = High Wind Days / Total Historical Days × 100**

## **Potential Business Feature**

> **`wind_risk_pct`**

### **Reasoning**

**Wind is proposed as a separate feature because it affects a different subset of events than rain, storms, or heat** — an event can face zero rain or heat risk while still facing significant wind exposure if it involves open ground and temporary structures, per the topography and structure-density factors identified in the YOUROPE evidence.

Therefore:

> **`wind_risk_pct` is proposed as a candidate business feature because it captures a structurally-driven risk mechanism that is largely independent of the other three hazards, and should be interpreted in combination with venue/structure type rather than as a standalone weather signal.**

**This is currently a candidate feature, not a finalized feature or risk score component.**

---

# Hazards Considered and Excluded (for the current version)

**Cold/Snow** and **fog/visibility** were reviewed but are not included as dedicated features in the current version of EventShield365.

The YOUROPE Weather Toolbox does include a corresponding template, **Risk Assessment Template: Cold and Snow** (https://yourope.org/know-how/wtb-20-risk-assessment-template-cold-and-snow/), confirming cold/snow is a recognized event-safety hazard in principle.

**However, cold/snow risk is not included as a current EventShield365 feature** because the five target cities selected for this analysis (New York, Los Angeles, Chicago, Las Vegas, Miami) skew warm-to-moderate in overall climate profile, meaning cold-risk exposure would only meaningfully activate for a narrow subset of winter events in a subset of these cities. This is treated as a candidate feature for future expansion if the city scope broadens to include more cold-climate locations, rather than an oversight.

**Fog/visibility risk is excluded on similar grounds** — its primary relevance is to events involving travel or movement logistics (e.g., air shows, races), which is not expected to represent a significant share of the events returned for the current city and category scope.

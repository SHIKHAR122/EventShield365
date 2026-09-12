# EVENTSHIELD365

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

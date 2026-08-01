# Telegram — @hvaccontrols
# Topic: Air-side — VAV Airflow Measurement Accuracy & Commissioning
# Date: Sat 01 Aug 2026

**Audience:** Specifiers, consultants, facility managers — market intelligence voice

**Hook:**

Airflow measurement is where VAV energy performance goes to die. Across new projects in Singapore, Hong Kong, and Dubai, the pattern repeats: the balancing report says 900 L/s, the BMS reads 1,050 L/s, and the difference is quietly absorbed into fan energy and comfort complaints. The sensor spec — not the VAV box spec — decides whether your demand-controlled ventilation saves the 25-35% outdoor air it promises [ASHRAE 62.1].

Three specification decisions separate projects that commission cleanly from those that fight drift for years:

1. **Averaging flow sensors over single-point probes.** A multipoint averaging array samples the duct cross-section; a single-point velocity probe reads one spot in a profile that shifts with every upstream fitting. Typical stated accuracy: ±2-3% of reading for averaging types versus ±5% or worse for single-point in real installations [ASHRAE 111].
2. **Respect the velocity pressure physics.** Pv = ½ρV² — velocity pressure collapses with the square of velocity. At minimum VAV flow (often 30% of design), the signal sits near the resolution floor of standard differential pressure transmitters. Specify the sensor range to the *minimum* flow, not the design flow.
3. **Plan the straight duct run.** Averaging sensors need clean, straight duct both sides of the station. A sensor squeezed between an elbow and a reheat coil reads fiction with confidence.

What this means for your next specification: require a commissioning baseline against a manual traverse [ASHRAE 111], insist on sensor range matched to turndown, and put the airflow station where the duct allows it to work — not where the drawings happen to have space.

Read the full analysis: ai.xinca.com/kb/q/24/?utm_source=telegram&utm_medium=channel&utm_campaign=hvac101

#VAV #AirflowMeasurement #Commissioning #DCV #BuildingControls

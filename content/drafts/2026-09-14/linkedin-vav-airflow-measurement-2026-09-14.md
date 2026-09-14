# LinkedIn Draft — XINCA Company Page — 2026-09-14

**Platform:** LinkedIn Company Page long-form
**Status:** DRAFT ONLY — Marc Sir posts manually from his personal profile
**Audience:** Professional network — consultants, facility managers, asset owners (analyst voice, citation-aware)
**Topic:** Air-side cluster — VAV airflow measurement: lab accuracy vs installed accuracy, k-factor drift, commissioning response
**Continuity:** Follows Sep 12 (variable-flow pumping, water-side) and Sep 7 (sensor data quality, controls) — this run covers the air-side measurement chain that feeds both control loops and ventilation compliance.

---

## Post (2249 chars — within LinkedIn's 3,000-char post limit; merged from Dify's two concatenated drafts — known defect)

**The Airflow Number You Specified Is Not the Airflow You Commissioned**

Every VAV terminal ships with an airflow sensor and a published accuracy, typically ±2–5% of reading. That number was measured in a laboratory: straight duct, fully developed flow profile, clean sensing element. The building you commission has none of those conditions.

Three sensing families dominate the market:

- **Pitot arrays** — the legacy workhorse. A few sampling points, a velocity-pressure signal, and a manufacturer k-factor that converts pressure to flow. Robust and inexpensive, but the k-factor assumes a flow profile your ductwork rarely delivers.
- **Thermal dispersion** — a heated element cooled by the airstream. Strong at low velocities, but the sensing surface loads up with dust over time and drifts.
- **Ultrasonic** — transit-time measurement with no obstruction and a wide turndown. Highest first cost, sensitive to acoustic noise.

Whatever the technology, the failure mode is shared: installation geometry. An elbow, a damper, or a takeoff close to the sensor distorts the velocity profile, and the published k-factor no longer describes the installed conditions. Field errors of 10–20% are routine where straight-duct requirements were never met.

The consequences are operational, not academic. Outdoor air fractions computed from inaccurate zone airflow break ventilation compliance. Control loops modulate against false feedback — hunting dampers, comfort complaints, wasted fan and coil energy. The energy model and the building quietly disagree.

**What closes the gap**

1. Specify sensors with documented installed performance, not only laboratory specs.
2. Commission airflow at minimum, mid and maximum flow against a balancer traverse — and enter the site-specific k-factor into the controller rather than the factory default.
3. Treat the BMS airflow point as a trend indicator until it has been verified in situ.

The gap between datasheet and duct is not a sensor failure. It is a commissioning decision — and it is made before the box is installed.

Full guide: https://help.xinca.com/a/air-side-vav-damper-selection/?utm_source=linkedin&utm_medium=company-page&utm_campaign=hvac101

#HVAC #AirSide #Commissioning #EnergyEfficiency

---

## Notes (housekeeping vs raw Dify output)

- **Merged from two concatenated Dify drafts** (known defect — same as Sep 5/7/10/12 runs; raw answer was 7,333 chars containing two complete drafts). Kept the analyst frame throughout, deduplicated the overlapping sensor-type paragraphs, kept Dify's worked framing of the 1,200-vs-900 CFM traverse anecdote OUT (first-person project claim, unverifiable — replaced with "routine where straight-duct requirements were never met").
- **Unverified figures dropped/hedged:** the ±2% lab / 15–20% ventilation-miss pairing was presented as established fact in raw draft 2 — retained only as the generic "±2–5% published accuracy" range (product-typical) and "10–20% field errors routine" (rule-of-thumb, consistent with the TG/X drafts). No fabricated citations; ASHRAE 62.1 named only as a compliance driver in general terms, no clause numbers invented.
- **LaTeX stripped**: raw draft 1 contained `$V = \sqrt{2p \Delta P / \rho}$` — replaced with plain-language description (LinkedIn renders LaTeX literally).
- **Emoji stripped**: raw drafts contained 📉🔧. No-emoji brand rule applied.
- **Footer replaced**: raw "Connect with me for more HVAC industry insights. Visit ai.xinca.com" — legacy domain; replaced with help.xinca.com link + LinkedIn UTM (verified live, 200 OK, 2026-09-14).
- No emoji, Australian spelling (modulates→n/a; "kilometres" n/a; checked: "commissioned", "modulates"), no competitor names.

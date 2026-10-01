# LinkedIn Draft — XINCA Company Page — 2026-10-01

**Platform:** LinkedIn Company Page long-form
**Status:** DRAFT ONLY — Marc Sir posts manually from his personal profile
**Audience:** Professional network — consultants, facility managers, asset owners (analyst voice, citation-aware)
**Topic:** IAQ cluster — humidity control and mould risk: why the RH design line is a health specification, and where part-load control fails
**Distinct from:** Sep 28 (damper authority, air-side), Sep 26 (valve authority, water-side), Sep 24 (CO₂ DCV ventilation), Sep 21 (actuator control signals), Sep 19 (DC aisle containment), Sep 17 (retrofit payback), Sep 14 (VAV airflow measurement), Sep 12 (variable-flow pumping), Sep 10 (PM2.5 filtration) — humidity/mould is a new sub-topic in the IAQ cluster.
**Note:** Composed locally this run — Dify app absent from VPS (direct API 401); voice/format follows the Sep 24/26 approved drafts.

---

## Post (within LinkedIn's 3,000-char post limit)

**Humidity Control Is a Health Specification, Not a Comfort Line**

Most performance briefs specify temperature bands with precision and treat relative humidity as a footnote. The health literature reads it the other way around.

WHO's guideline on dampness and mould (2009) is unambiguous: the presence of dampness or mould in a building is itself the health signal — the response is to act on the moisture source, not to argue about species or thresholds [WHO, 2009]. Standards follow the same logic. ANSI/ASHRAE 62.1 caps indoor design conditions at 65% RH, and ASHRAE 160 provides the moisture-control design analysis framework for verifying that a design can hold it [ANSI/ASHRAE Standard 62.1], [ASHRAE Standard 160].

The engineering reality is that humidity fails at part load. Cooling plant is sized for design-day conditions, but the latent job lives in the shoulder hours: DX coils cycle off at light load, chilled-water reset lifts supply water temperature, and the coil drifts away from dehumidifying duty exactly when outdoor dew points stay high [ASHRAE Handbook—Fundamentals]. The building holds temperature and quietly loses the moisture battle — the symptom surfaces later as mould on surfaces, not as an alarm on the BAS.

Three spec moves that carry the health case:

1. **Write the RH line into the performance brief.** The 65% ceiling is already the design condition — treat it as an acceptance criterion with monitoring attached, not a catalogue footnote.

2. **Spec the measurement.** RH sensing drifts with contamination, condensation and placement errors: return-air sensing wants a straight duct section, outdoor air wants an aspirated shield, and post-coil sensing wants to sit clear of the carryover zone [XINCA Knowledge Base: humidity sensor placement in AHUs].

3. **Tie moisture into the IAQ program.** Continuous monitoring for CO₂ and particulates earns its business case by one logic — health variables measured, not assumed. Humidity belongs on the same list [XINCA Knowledge Base: continuous IAQ monitoring for commercial buildings].

From Mumbai to Manila to the Gulf coast, the latent side of the load is the side that shows up in health complaints. The spec that carries an RH acceptance line is the one that does not grow its own problems.

Full take: https://help.xinca.com/a/iaq-monitoring-commercial-buildings/?utm_source=linkedin&utm_medium=company-page&utm_campaign=hvac101

#HVAC #IAQ #HealthyBuildings

---

## Notes (composition vs editorial rules)

- **Composed locally, no Dify raw output this run** — VPS Dify has no Havi content app (Sep 24 root-cause; this run's direct API call returned 401). Analyst voice per the platform table: data-aware, citation-heavy, no marketing language.
- **Citations:** ≥2 own-KB references included in brackets. WHO 2009, ASHRAE 62.1 and ASHRAE 160 are named standards without fabricated clause numbers. The 65% figure is the 62.1 indoor-design RH ceiling — no performance percentages claimed; mould outcomes vary by building, climate and operation.
- **No competitor names** — no vendor framing anywhere.
- **Link verified live (200 OK, 2026-10-01):** /a/iaq-monitoring-commercial-buildings/ with LinkedIn UTM. Single article link (no hub links); the humidity post's IAQ-program point ties directly to that article's monitoring business case.
- No emoji, Australian spelling (programme n/a — "program" retained as the established in-product term), no "AI-powered" claims.

---

## Fallback draft ends here

# Telegram Draft — @hvaccontrols — 2026-09-07

**Platform:** Telegram channel broadcast (@hvaccontrols)
**Audience:** Specifiers, consultants, facility managers (decision-maker voice)
**Topic:** Building controls / BMS cluster #4 — BMS sensor data quality: sensor selection, placement, calibration & verification (temperature, humidity, CO₂, differential pressure). Distinct from Aug 15 (BACnet protocol integration architecture) — sensors first.

---

## Post (caption ≤1024 chars — sendPhoto hard limit; no emoji)

High-end controllers, low-grade sensors — the fastest way to waste a BMS budget.

Before you specify your next BMS project:

1. Accuracy classes matter. Not all NTC 10k sensors are equal — a ±0.2°C class sensor earns its cost in critical zones.

2. Placement is part of the spec. A sensor in direct sunlight or beside a fresh-air intake doesn't represent the zone. For CO₂, ASHRAE 62.1 sets 0.9-1.8 m to capture the breathing zone.

3. Drift, not just commissioning. A humidity sensor can drift 1-2% RH per year; a drifting CO₂ sensor quietly defeats DCV. Verify against a calibrated reference on a schedule.

You cannot tune a PID loop to fix a bad sensor signal. The loop is only as good as its data.

https://help.xinca.com/kb/q/19?utm_source=telegram&utm_medium=channel&utm_campaign=hvac101

#BMS #HVACSpec #BuildingAutomation

---

## Hero Image (generated 2026-09-07, freestyle mode — Week 2 of 2-week experiment)

`content/assets/hero-sensor-data-quality-20260907.png` — 1280×1280 square (center-cropped from 16:9 render). GPT-Image-2 freestyle: close-up photograph of a duct temperature sensor being installed on a galvanised metal duct with a cordless drill, gloved hand, shallow depth of field. Dark navy panels top/bottom: headline "BMS SENSOR QUALITY" (SENSOR in orange), punchline "Only as good as its sensors" (sensors in orange), "xinca.com" footer bottom-right. No mascot, no cartoon clutter. Rendered text verified via vision_analyze: all English, no misspellings, no Chinese characters — no iteration needed (1/3 attempts).

## Notes
- No research brief (no `content/briefs/latest.json` — nil for this run; Dify used the HVAC KB directly).
- Dify app still ignores `inputs` (user_input_form: [] via /v1/parameters) — topic+platform embedded in the query (Aug 24 / Sep 5 pattern).
- Dify returned an IMAGE PROMPT this run (close-up sensor install photo) — used as the subject, wrapped in the freestyle brand harness (northstar-hero-image, no reference images).
- Angle chosen as cluster-4 successor to Aug 15 BACnet integration: sensor layer / data quality.
- Link: /kb/q/19 (AHU temperature sensor spec) — deepest fit for the specification angle.
- Australian spelling; no emoji; no competitor names.

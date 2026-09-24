# Telegram Draft — @hvaccontrols — 2026-09-24

**Platform:** Telegram channel broadcast (@hvaccontrols)
**Audience:** Specifiers, consultants, facility managers (decision-maker voice)
**Topic:** IAQ cluster — CO₂-based demand-controlled ventilation (DCV): CO₂ as an occupancy proxy; derived setpoints per ASHRAE 62.1 / EN 16798-1; NDIR sensor drift, calibration and placement; reset floors and the humid-climate latent trade-off
**Distinct from:** Sep 10 run (PM2.5 filtration — particulate control); Sep 12 (variable-flow pumping, water-side). Same IAQ cluster at the 14-day boundary, different sub-topic (CO₂/ventilation, not filtration).
**Note:** Composed locally this run — Dify app absent from VPS (no "Havi — HVAC Content Generator" app in the VPS Dify apps table; API call returned 401). Fourth consecutive local-composition run; voice/format follows the Sep 17/19/21 pattern.

---

## Post (target ≤ 1024 — sendPhoto hard limit; no emoji)

Ventilation on a fixed schedule pays for empty rooms — and starves full ones.

CO₂-based demand-controlled ventilation (DCV) resets outdoor air to actual occupancy:

1. CO₂ is an occupancy proxy. Indoor CO₂ tracks people and per-person outdoor air — the controller resets against it.

2. The setpoint is derived, not guessed. ASHRAE 62.1's DCV provisions reset zone ventilation from a CO₂ band derived from the per-person rate; EN 16798-1 sets categories as ppm above outdoor.

3. The sensor decides. NDIR units drift — budget field calibration and placement per design intent (breathing zone; return duct only if the design accounts for it).

4. Mind the floor: never below code minimum outdoor air. In humid climates less OA cuts latent load — not licence to starve the zone.

Classrooms and open-plan offices see the widest gap between scheduled and actual occupancy. That is where DCV earns its keep.

https://help.xinca.com/kb/q/29/?utm_source=telegram&utm_medium=channel&utm_campaign=hvac101

#IAQ #Ventilation #DCV

---

## Hero Image (generated 2026-09-24, mascot mode — Bro Woo + Inu Faa)

- File: `content/assets/hero-co2-dcv-ventilation-2026-09-24.png`
- Scene: Type A whiteboard lecture — one rising CO₂-vs-time line flattening at a dashed "SETPOINT" line (labels: CO2, TIME, SETPOINT), pointer in hand, Inu Faa seated beside. Headline "VENTILATE ON DEMAND", punchline "AIR FOLLOWS OCCUPANCY".
- QA: PASS 10/10 on vision_analyze (2026-09-24, first iteration): one slim Shiba with collar charm, glasses on Bro Woo, pure white flat-vector background; headline "VENTILATE ON DEMAND", punchline "AIR FOLLOWS OCCUPANCY", labels CO2/TIME/SETPOINT all rendered exactly; no Chinese characters; no extra elements.

## Notes (composition vs channel editorial direction)

- **Composed locally, no Dify raw output this run** — the "Havi — HVAC Content Generator" app does not exist on the VPS Dify (apps table lists only vertical chat apps + Monday HVAC Research workflows; API 401). See run summary.
- **No invented figures.** No ppm numbers are claimed; the CO₂-band/reset logic is attributed to [ANSI/ASHRAE Standard 62.1] and [EN 16798-1] without fabricated clause numbers.
- **Specifier framing** (what the control decision does to the next spec), not technician how-to. No vendor names anywhere.
- **Link verified live (200 OK, 2026-09-24)**: /kb/q/29/ — "How do CO₂ sensors work in demand-controlled ventilation?" — the tightest KB match for this topic.
- No emoji, Australian spelling (licence, economiser n/a), no competitor names.

---

## Fallback draft ends here

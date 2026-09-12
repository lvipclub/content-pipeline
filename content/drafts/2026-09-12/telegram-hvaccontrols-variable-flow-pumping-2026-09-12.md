# Telegram Draft — @hvaccontrols — 2026-09-12

**Platform:** Telegram channel broadcast (@hvaccontrols)
**Audience:** Specifiers, consultants, facility managers (decision-maker voice)
**Topic:** Water-side cluster #3 — variable-flow pumping: dP control of variable-speed pumps in variable-primary-flow (VPF) chilled water systems (sensor placement, setpoint reset, minimum speed floor, affinity-law energy)
**Distinct from:** Aug 6 run (valve authority & hydronic balancing) and Aug 22 run (low delta-T syndrome) — this run is the pump-side control strategy of the same water-side cluster.

---

## Post (caption 1001 chars ≤ 1024 — sendPhoto hard limit; no emoji)

Variable-primary-flow pumping is the default for new chilled water plants — but the dP control strategy decides whether the savings arrive.

Three decisions:

1. Sensor placement. A sensor near the pump room over-pressurises the whole network. Place it at the hydraulically most remote circuit, or have the BAS track the most-open valve and reset the setpoint until it sits near 90% open.

2. Reset the setpoint. A fixed dP setpoint sized for design load wastes energy every part-load hour. Reset by valve position or load, and the pumps ride the affinity laws: 20% slower is about half the power; 50% speed is close to one-eighth.

3. Minimum speed floor. Chillers need minimum evaporator flow, and the floor rises as more machines stage on. Commission it deliberately.

Spec the sensor location and reset sequence in your controls narrative.

https://help.xinca.com/a/water-side-control-valve-selection/?utm_source=telegram&utm_medium=channel&utm_campaign=hvac101

#Hydronics #ChilledWater #HVACSpec

---

## Hero Image (generated 2026-09-12, freestyle mode — Week 2 of 2-week experiment)

- File: `content/assets/hero-variable-flow-pumping-2026-09-12.png` (1280×1280 PNG)
- Subject (from Dify brief + freestyle brand harness): end-suction chilled-water pump with VFD cabinet, dP sensor loop, pump/system curve overlay — navy #1B2333 base, headline "VARIABLE-FLOW PUMPING", punchline "Slower saves power", xinca.com footer.
- See rotation file notes for generation route + QA result.

## Notes (housekeeping vs raw Dify output)

- **Raw Dify answer was 4,834 chars** — trimmed to 1001 for the 1,024-char sendPhoto limit. Kept the specifier framing and the three numbered decisions. Cut: the VPF-architecture explainer paragraph (folded into the opening line), the chiller-staging detail (folded into point 3), and the "welcome back to the series" preamble.
- **Emoji stripped**: raw answer contained 🧠📍💰🛡️ and a "Follow @hvaccontrols | Visit ai.xinca.com" promo line — removed (no-emoji brand rule; ai.xinca.com is the legacy domain).
- **Link added**: /a/water-side-control-valve-selection/ with TG UTM — verified live (200 OK, 2026-09-12). Raw output had no link.
- Claim check: cube-law figures are affinity-law arithmetic (0.8³ ≈ 0.51, 0.5³ ≈ 0.125). Dify's "60-80% pump energy reduction vs constant flow" claim was UNSOURCED and dropped. "Critical index circuit" / most-open-valve reset described as control practice, not tied to a specific standard. Minimum speed floor framed as commissioning practice; chiller minimum evaporator flow is the reason (chiller-freeze protection), not pump cavitation.
- No emoji, Australian spelling (over-pressurises), no competitor names.

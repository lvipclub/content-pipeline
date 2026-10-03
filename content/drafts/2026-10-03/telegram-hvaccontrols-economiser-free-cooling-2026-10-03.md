# Telegram Draft — @hvaccontrols — 2026-10-03

**Platform:** Telegram channel broadcast (@hvaccontrols)
**Audience:** Specifiers, consultants, facility managers (decision-maker voice)
**Topic:** Energy-efficiency cluster — economiser free cooling: changeover logic (dry-bulb vs enthalpy/dew point in humid climates), ASHRAE 90.1 high-limit cutouts, sensing integrity for differential enthalpy, silent mechanical failure (seized dampers), carrying changeover type + high-limit setpoint in performance briefs
**Distinct from:** Sep 17 run (retrofit payback — same energy cluster, different sub-topic: capital decision framework, not changeover operation); Sep 28 (air-side damper selection/authority); Oct 1 (IAQ humidity/mould). Economiser changeover has not been covered in the rotation.
**Note:** Composed locally this run — Dify app absent from VPS (direct API call to dify.olilo.com/v1 returned 401 "Access token is invalid"; tunnel not attempted this run). Eighth consecutive local-composition run; voice/format follows the Sep 24–Oct 1 approved drafts.

---

## Post (target ≤ 1024 — sendPhoto hard limit; no emoji)

Free cooling is decided at changeover — not at the damper.

1. Cool is not dry. 22°C air with a 20°C dew point hands the coil latent load — the chiller runs anyway. Humid coastal markets change over on enthalpy or dew point, never dry-bulb alone.

2. The high-limit is the ceiling. ASHRAE 90.1 drives economisers in most climate zones, with climate-dependent cutouts — the cutoff type decides how many free hours survive.

3. Two sensors, both honest. Differential enthalpy compares outdoor with return air — one drifted sensor flips the decision daily. Calibration is part of the measure.

4. The silent failure is mechanical. A damper seized at minimum position raises no alarm — only a plant that never quite free-cools. Trend OA signal vs mixed-air temperature.

Put changeover type and high-limit setpoint on one line of the brief — that line is the energy spec.

https://help.xinca.com/kb/q/25/?utm_source=telegram&utm_medium=channel&utm_campaign=hvac101

#EnergyEfficiency #FreeCooling #BuildingControls

---

## Hero Image

- File: `content/assets/hero-economiser-free-cooling-2026-10-03.png`
- Scene: Type A whiteboard lecture — Bro Woo pointing at a whiteboard carrying ONE simple chart (a single rising line crossed by a dashed changeover line; left zone labelled "FREE", right zone "HUMID"), Inu Faa seated beside him looking up. Headline "CHANGEOVER DECIDES", punchline "TRUST ENTHALPY" (orange), footer "xinca.com".
- QA: recorded in run summary (vision_analyze result).
- Generation: recorded in run summary.

## Notes (composition vs channel editorial direction)

- **Composed locally, no Dify raw output this run** — the "Havi — HVAC Content Generator" app does not exist on the VPS Dify (Sep 24 root-cause; this run's direct API call returned 401). See run summary.
- **No invented figures.** Only standard reference: [ANSI/ASHRAE/IES 90.1] — air-side economiser provisions with climate-dependent high-limit cutouts, named without clause numbers. No savings percentages claimed anywhere.
- **Specifier framing** (what goes on the next performance brief), not technician how-to. No vendor names anywhere.
- **Link verified live (200 OK, 2026-10-03):** /kb/q/25/ — "What is an economizer and how are its controls configured?" — the post's exact subject (page title uses US spelling; channel voice keeps Australian "economiser").
- No emoji, Australian spelling, no competitor names.

---

## Fallback draft ends here
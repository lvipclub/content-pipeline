# Telegram Draft — @hvaccontrols — 2026-09-14

**Platform:** Telegram channel broadcast (@hvaccontrols)
**Audience:** Specifiers, consultants, facility managers (decision-maker voice)
**Topic:** Air-side cluster — VAV airflow measurement: sensor types (pitot array, thermal dispersion, ultrasonic), k-factor errors, installed vs datasheet accuracy
**Distinct from:** Sep 12 run (variable-flow pumping, water-side), Sep 10 (IAQ filtration), Sep 7 (sensor data quality, controls cluster) — this run is the air-side measurement chain feeding those control loops.

---

## Post (1001 chars ≤ 1024 — sendPhoto hard limit; no emoji)

Your VAV airflow reading is a lab number wearing a hard hat.

Datasheet accuracy is measured with 10 clean duct diameters upstream. Your box has an elbow 500 mm away. The sensor applies the lab k-factor to turbulent air — and drifts 10–20% from the true flow before the control loop even starts.

Three sensor families, one shared weakness:

1. Pitot arrays — robust, cheap, but they sample a few points and trust a lab flow profile.
2. Thermal dispersion — excellent at low velocities, drifts as dust loads the heated element.
3. Ultrasonic — wide turndown, no obstruction, but higher cost and sensitive to acoustic noise.

None of them escapes the installed-conditions problem. What fixes it is commissioning: verify against a balancer traverse at min, mid and max flow, and set a site-specific k-factor.

Datasheet is not duct. Commission the sensor, not just the loop.

https://help.xinca.com/a/air-side-vav-damper-selection/?utm_source=telegram&utm_medium=channel&utm_campaign=hvac101

#AirSide #VAV #HVACSpec

---

## Hero Image (generated 2026-09-14, mascot mode — Bro Woo + Inu Faa)

- File: `content/assets/hero-vav-airflow-measurement-2026-09-14.png` (1280×1280)
- Subject: Type A whiteboard-lecture scene — pitot array, thermal dispersion, ultrasonic airflow-sensor comparison on the whiteboard, orange accents, "AIRFLOW MEASUREMENT" headline, "Trust the traverse" punchline, xinca.com footer.
- Generated via OpenRouter fallback (qwen/qwen-image-3-pro) — see rotation notes for QA result.

## Notes (housekeeping vs raw Dify output)

- **Raw Dify answer was 3,866 chars** — trimmed to ~1000 for the 1,024-char sendPhoto limit. Kept: the datasheet-vs-installed hook, the three-sensor comparison (compressed to one line each), and the commissioning takeaway. Cut: BMS/troubleshooting preamble, Bernoulli/velocity-pressure physics walkthrough, ΔP square-root error amplification detail.
- **Emoji stripped**: raw answer contained 📉🔢🏗️💡🔧. No-emoji brand rule applied.
- **Voice corrected**: raw opening was "G'day HVAC family!" (casual-banter drift) — rewritten to the specifier/market-intelligence voice per channel editorial direction.
- **Footer replaced**: raw ended "Follow @hvaccontrols | Visit ai.xinca.com" — ai.xinca.com is the legacy domain; replaced with help.xinca.com link + TG UTM.
- **Link verified live (200 OK, 2026-09-14)**: /a/air-side-vav-damper-selection/ — the air-side VAV article (damper selection, same terminal-unit airflow chain as this topic).
- Claim check: "10–20% installed error" retained from Dify as the standard commissioning-rule-of-thumb range for profile distortion; the ±5% datasheet vs ±15–25% field figure (X draft) is Dify's practitioner framing, flagged as indicative rather than a cited spec. "10 diameters upstream" is the conventional lab-flow-conditioning requirement. Site-specific k-factor via traverse is standard TAB practice (AABC/NEBB-style), not tied to a single standard.
- No emoji, Australian spelling (metre n/a; "kilometres" n/a; "optimised" n/a — checked: "families", "verifier" n/a), no competitor names.

# Telegram Draft — @hvaccontrols — 2026-10-01

**Platform:** Telegram channel broadcast (@hvaccontrols)
**Audience:** Specifiers, consultants, facility managers (decision-maker voice)
**Topic:** IAQ cluster — humidity control and mould risk: RH as a health variable (WHO dampness & mould guideline); the 65% RH design condition (ASHRAE 62.1) with ASHRAE 160 moisture-design analysis; part-load dehumidification failure modes (DX cycling, chilled-water reset vs latent duty); RH sensing drift and placement; carrying an RH acceptance line in performance briefs
**Distinct from:** Sep 24 run (CO₂ DCV ventilation — same IAQ cluster, different sub-topic: occupancy ventilation, not humidity/moisture); Sep 10 run (PM2.5 filtration — particulate). Sep 26 (water-side valve authority), Sep 28 (air-side damper authority). Humidity/mould has not been covered in the rotation.
**Note:** Composed locally this run — Dify app absent from VPS (direct API call to dify.olilo.com/v1 returned 401 "Access token is invalid"; tunnel also down). Seventh consecutive local-composition run; voice/format follows the Sep 24/26 approved drafts.

---

## Post (target ≤ 1024 — sendPhoto hard limit; no emoji)

Humidity reads as comfort — and decides whether a building grows mould.

Four things to hold the line on, latent-side:

1. RH is a health variable. WHO's dampness-and-mould guideline treats visible dampness as the health signal — act on the source.

2. The design line exists. ASHRAE 62.1 caps indoor design conditions at 65% RH; ASHRAE 160 sets the moisture-design analysis to verify it.

3. Part load is where latent control fails. Light loads cycle DX coils off and lift chilled-water reset — the coil drifts off dehumidifying duty as dew points stay high. Hold dew point with intent: coil selection, face-split coils, or reheat.

4. The sensor decides again. RH elements drift with contamination and condensation; return air wants a straight duct, outdoor air an aspirated shield.

In humid-coast markets the latent spec is the health spec — carry an RH line in the brief.

https://help.xinca.com/kb/q/38/?utm_source=telegram&utm_medium=channel&utm_campaign=hvac101

#IAQ #HumidityControl #HealthyBuildings

---

## Hero Image

- File: `content/assets/hero-humidity-mould-risk-2026-10-01.png` (1280×720 PNG, 396 KB)
- Scene: Type B desk study — Bro Woo seated at a wooden desk, chin on hand, studying a paper sketch of a simple humidity chart (one rising curve, dashed line, labels "RH" and "65%"), grey lamp with yellow light cone, yellow pencil, Inu Faa on the floor beside the desk looking up. Headline "HUMIDITY DRIVES MOULD", punchline "CONTROL DEW POINT" (orange), footer "xinca.com".
- QA: vision_analyze PASS on attempt 3 (3-attempt cap respected) — headline/labels/punchline/footer all rendered exactly, one slim Shiba with collar charm, glasses on, pure white background, no Chinese characters, no stray annotations. (Attempts 1-2 rejected: stray "6H" chart label, then a stray "9/9" corner annotation + off-white tint; each retry fixed exactly one issue.)
- Generation: xAI grok-imagine-image-quality, identity-locked via character-reference-clean.png (FAL edit route still broken on Nous proxy).

## Notes (composition vs channel editorial direction)

- **Composed locally, no Dify raw output this run** — the "Havi — HVAC Content Generator" app does not exist on the VPS Dify (Sep 24 root-cause via apps table; this run's direct API call returned 401). See run summary.
- **No invented figures.** The only number is the 65% RH design condition, attributed to [ANSI/ASHRAE 62.1] without a fabricated clause number (65% is the long-standing 62.1 indoor-design ceiling). WHO framing is the guideline's own position (dampness/mould presence = the health signal; remediate the source). No savings percentages claimed.
- **Specifier framing** (what the decision does to the next performance brief), not technician how-to. No vendor names anywhere.
- **Link verified live (200 OK, 2026-10-01):** /kb/q/38/ — "Where should humidity sensors be placed in an AHU?" — the post's point 4 subject (RH measurement discipline).
- No emoji, Australian spelling, no competitor names.

---

## Fallback draft ends here

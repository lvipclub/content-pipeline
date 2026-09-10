# Telegram Draft — @hvaccontrols — 2026-09-10

**Platform:** Telegram channel broadcast (@hvaccontrols)
**Audience:** Specifiers, consultants, facility managers (decision-maker voice)
**Topic:** IAQ cluster #3 — particulate control (PM2.5) in commercial buildings: filtration ratings (MERV-13 baseline, ISO ePM1), the filtration–energy trade-off, and smoke/haze-episode strategy
**Distinct from:** Aug 20 run (CO2-based DCV + sensor network) — this run is particulate/filtration, not CO2 control.

---

## Post (caption 981 chars ≤ 1024 — sendPhoto hard limit; no emoji)

Most filtration specs stop at MERV-13. But the building's particulate load — and the fan energy behind it — deserve a closer look.

Three things to know:

1. Look beyond MERV. ISO ePM1 shows sub-micron capture — the fraction that counts when haze or smoke rolls in.

2. Pressure drop is a design assumption. Higher-efficiency media adds static resistance; if the AHU wasn't sized for it, fans ramp up and energy climbs.

3. Smoke episodes need a plan. Minimum outdoor-air rates are code-mandated — closing dampers isn't an option. Pair demand-controlled ventilation with temporary filtration overrides (secondary filter banks or HEPA scrubbers).

What this means for your next project: specify against real particulate loads, model the fan energy penalty, and write the smoke-episode response into the O&M plan.

https://help.xinca.com/a/iaq-monitoring-commercial-buildings/?utm_source=telegram&utm_medium=channel&utm_campaign=hvac101

#IndoorAirQuality #HVACSpec #HealthyBuildings

---

## Hero Image (generated 2026-09-10, freestyle mode — Week 2 of 2-week experiment)

- File: `content/assets/hero-iaq-filtration-20260910.png` (1280×1280 PNG, 1.7 MB)
- Subject (from Dify hero prompt): close-up of an AHU filter rack — pristine white pleated filter beside a heavily soiled grey filter, digital differential-pressure gauge in the foreground — wrapped in the freestyle brand harness (navy #1B2333 base, headline "THE FILTRATION TRADE-OFF", punchline "Efficiency costs pressure", xinca.com footer). Gauge reads ΔP 0.8 → 2.1 in. w.g. (clean vs loaded).
- Route: the Nous managed gateway is DOWN (OAuth relogin required since 2026-09-09), so `image_generate` is unavailable in every local runtime — generated via the xAI `grok-imagine-image` provider at 2K (2816×1584 → centre-crop 1584² → 1280²; the corner xinca.com footer was re-overlaid via PIL because the centre crop removes it). Vision QA passed: all text correct English, no Chinese characters, no garbled strings.
- Alternative (NOT used): an OpenRouter `qwen/qwen-image-3-pro` 2K render exists at `~/.hermes/cache/images/openrouter_qwen_qwen-image-3-pro_20260910_091444_91afed08.png` — rejected because its gauge display renders a hex-like glitch ("FF8CO").

## Notes (housekeeping vs raw Dify output)

- **Raw Dify answer was 3,051 chars** — over the 1,024-char sendPhoto caption limit. Trimmed to 981 chars, keeping the specifier framing and the three numbered points. Cut: TEWI acronym (real term, but used unusually — replaced with lifecycle/fan-energy framing), pre-construction filter-loading-test paragraph (folded into point 2), and the ΔP-monitoring paragraph (folded into the closing line).
- **Emoji stripped**: raw answer contained 🔧 and a "Follow @hvaccontrols | Visit ai.xinca.com" promo line — removed (no-emoji brand rule; ai.xinca.com is the legacy domain).
- **Link added**: /a/iaq-monitoring-commercial-buildings/ with TG UTM — verified live (200 OK, 2026-09-10). Raw output had no usable link.
- Claim check: "MERV-13 baseline" attributable to ASHRAE post-pandemic guidance — softened from Dify's "ASHRAE now recommends MERV-13 minimum" in the X variant; here framed as "specs stop at MERV-13" (specification practice, not a standard claim). ISO ePM1 = ISO 16890 sub-micron classification — correct as written.
- No emoji, Australian spelling, no competitor names.

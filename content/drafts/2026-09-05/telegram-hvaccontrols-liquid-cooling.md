# Telegram Draft — @hvaccontrols — 2026-09-05

**Platform:** Telegram channel broadcast (@hvaccontrols)
**Audience:** Specifiers, consultants, facility managers (decision-maker voice)
**Topic:** Data centre cooling cluster #6 — the liquid-side frontier: D2C cold plates, CDU architecture, hybrid retrofit paths, ASHRAE liquid-cooling classes, waste-heat recovery. Distinct from Aug 13 (supply temps, aisle containment, TC 9.9 air-side envelopes): this run is liquid-side only.

---

## Post (caption 1,018 chars ≤1024 — sendPhoto hard limit; no emoji)

When racks pass 40 kW, air cooling runs out of road. The liquid-side frontier is here — and it changes how you specify the coolant loop.

Three things to know:

1. CDU architecture. Rack-mounted CDUs suit retrofit hot racks; row-level CDUs add capacity and redundancy.

2. Direct-to-chip. Cold plates ride on the CPU and GPU lids. Single-phase for reliability; two-phase for extreme spikes.

3. Hybrid retrofit. Keep CRAHs for memory and storage; route liquid to the high-TDP chips. No raised-floor surgery.

Under ASHRAE's liquid-cooling classes, warmer supply water extends free-cooling hours — and 40-60°C return water becomes a heat source for heat-pump recovery, district heating or hot water.

What this means for your next project: the CDU is the new critical component. High-density racks are coming; specify for the liquid side.

Read more: https://help.xinca.com/a/data-center-energy-efficiency/?utm_source=telegram&utm_medium=channel&utm_campaign=hvac101

#DataCentreCooling #LiquidCooling #BuildingControls

---

## Hero Image (generated 2026-09-05, mascot mode — Bro Woo + Inu Faa, Week 1 of 2-week experiment)

`content/assets/hero-liquid-cooling-20260905.png` — 1280×1280 square, flat vector, near-white background. Bro Woo walking forward with tablet showing orange server-rack + droplet icons, Inu Faa (one slim Shiba, yellow collar + orange lightning charm) beside him, flat grey cityscape with blue network lines behind. Headline "LIQUID COOLING" top, "The Liquid Frontier" footer (Liquid Frontier in orange), xinca.com bottom-right (added programmatically after center-crop).

## Notes
- Dify returned no IMAGE PROMPT line this run — hero scene constructed from the northstar-hero-image template (mascot mode, Type walking-forward scene) instead.
- FAL image_generate edit route failed (`file_download_error` on local reference path) → used documented xAI provider fallback from xinca-ip-hero-images skill (identity-locked edit route with local data-URI reference). Rendered 16:9 despite square request (edit route limitation) → center-cropped to 1:1, upscaled to 1280×1280, xinca.com watermark redrawn programmatically (crop removed it).
- Vision QA: one slim Shiba + orange ⚡ charm ✓, Bro Woo glasses ✓, all text correct (no gibberish) ✓, characters fully in frame after crop ✓. Minor deviations accepted: crew-neck (vs V-neck) sweater, off-white background.
- [LINK] verified live: `/a/data-center-energy-efficiency/` (200 OK). Last linked Aug 13 (23 days — acceptable reuse; only liquid-cooling-adjacent article).
- Body compressed from Dify's ~3,200-char output to 1,018-char caption: hook → 3 numbered points → ASHRAE classes + waste heat → spec takeaway → link → hashtags. Emoji stripped (Dify emitted 🌡️🔑🔧). Australian spelling. No competitor names.
- Style mode: **mascot** (run date 2026-09-05 is inside Week 1 window Aug 29–Sep 6).

# Telegram Draft — @hvaccontrols — 2026-09-19

**Platform:** Telegram channel broadcast (@hvaccontrols)
**Audience:** Specifiers, consultants, facility managers (decision-maker voice)
**Topic:** Data-centre cooling cluster — aisle containment retrofits: seal first (blanking panels, brush grommets, floor cutouts), then contain, verified at the rack inlet
**Distinct from:** Sep 17 run (HVAC retrofit payback, energy-efficiency), Sep 14 (VAV airflow measurement, air-side), Sep 12 (variable-flow pumping, water-side) — this run is the data-centre cooling cluster, sub-topic aisle containment (Sep 5 was liquid cooling; containment is a distinct mechanism).
**Note:** Composed locally this run — Dify app's upstream model provider (langgenius/mimo, api.xiaomimimo.com) read-timeout on every call, same outage as the Sep 17 run (see run summary); voice/format follows the Sep 17 approved draft.

---

## Post (target ≤ 1024 — sendPhoto hard limit; no emoji)

Two data halls, identical IT load, very different power bills. The difference is usually airflow containment, and the retrofit economics are more tractable than most owners expect.

Where the savings actually come from:

1. CRAH fan energy: sealed aisles let CRAH units run at part speed instead of fighting an open-room pressure war.
2. Higher supply-air temperatures: a contained return path lifts chiller efficiency.
3. The cheap dollars come first: blanking panels, brush grommets, floor cutout sealing, before any ductwork.

Hot-aisle containment wins where the return path is easy to close; cold-aisle wins where floor cutouts cannot be sealed economically. Verify with rack-inlet sensors against the ASHRAE TC 9.9 envelope, not by feel.

https://help.xinca.com/a/data-center-energy-efficiency/?utm_source=telegram&utm_medium=channel&utm_campaign=hvac101

#DataCentre #Containment #HVACSpec

---

## Hero Image (generated 2026-09-19, mascot mode — Bro Woo + Inu Faa)

- File: `content/assets/hero-dc-aisle-containment-2026-09-19.png`
- Subject: Type B desk-study scene — blueprint of a data hall with two rack rows and orange airflow arrows, OPEN/SEALED comparison card, "HOT AISLE OR COLD?" headline, "SEAL FIRST, THEN CONTAIN" punchline, xinca.com footer.
- Generated via xAI grok-imagine fallback (landscape, reference-image identity lock) — the default image_generate FAL edit route failed (reference download error on the Nous proxy, known issue). Vision QA passed first iteration: single slim Shiba with lightning-bolt collar, glasses on, all rendered text clean, no Chinese characters, flat vector on white.

## Notes (composition vs channel editorial direction)

- **Composed locally, no Dify raw output to trim.** Dify app "Havi Inqury Classifier + Knowledge + Chatbot" (the app DIFY_HAVI_APP_KEY resolves to) failed every call: upstream provider api.xiaomimimo.com read-timeout at 10 s, persistent across ~12 calls and one final single retry. Same outage as the Sep 17 run. Voice, structure and char budget follow the Sep 17 approved draft.
- **No invented figures.** No percentages or payback numbers claimed. Seal-first sequencing and rack-inlet verification are stated as engineering principles, not cited statistics. ASHRAE TC 9.9 named as the envelope driver — no clause numbers invented.
- **Hot-aisle vs cold-aisle** framed as an existing-building decision (retrofit constraints), not a catalogue preference — no vendor names anywhere.
- **Link verified live (200 OK, 2026-09-19)**: /a/data-center-energy-efficiency/ — this post's "where DC cooling energy goes" point is its entry context.
- No emoji, Australian spelling (economiser n/a this run; "modulate", "cutouts" fine), no competitor names.

---

## Fallback draft ends here

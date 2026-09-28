# Telegram Draft — @hvaccontrols — 2026-09-28

**Platform:** Telegram channel broadcast (@hvaccontrols)
**Audience:** Specifiers, consultants, facility managers (decision-maker voice)
**Topic:** Air-side cluster — damper selection and authority: opposed vs parallel blades and the installed characteristic; damper authority (≥0.3 recommended, <0.1 near-useless) as the air-side mirror of valve authority; two-position as parallel-blade's home ground; close-off and torque verified last, from the manufacturer's tables
**Distinct from:** Sep 26 run (control valve selection/authority — water-side). Air-side cluster at its 14-day boundary (last used Sep 14, VAV airflow measurement — sensors/traverse, different sub-topic). Also distinct from Aug 17 (VAV control) and Sep 21 (actuator control signals — no runtime/signal content here).
**Note:** Composed locally this run — Dify app absent from VPS (tunnel down today: connection refused; Sep 24 verification showed the app key 401s even with the tunnel up — no "Havi — HVAC Content Generator" app exists on the VPS Dify). Sixth consecutive local-composition run; voice/format follows the Sep 17–26 pattern.

---

## Post (target ≤ 1024 — sendPhoto hard limit; no emoji)

Dampers sized for face area alone don't modulate — they slam.

Three things to hold the line on, air-side:

1. Blades shape the curve. At the pressure drops a VAV box actually sees, parallel-blade dampers collapse toward quick-opening as one blade shields the next; opposed-blade holds a near-linear flow-versus-stroke curve.

2. Authority applies to air, not just water. A damper needs roughly a third of the branch pressure drop — an authority of 0.3 or better — for stable modulating control. Below 0.1 it does almost nothing until nearly closed.

3. Parallel-blade still earns its keep on two-position service, where linearity doesn't matter and cost does.

Close-off last: the actuator must hold worst-case differential with margin — verified from the manufacturer's close-off tables, not the headline torque figure.

https://help.xinca.com/a/air-side-vav-damper-selection/?utm_source=telegram&utm_medium=channel&utm_campaign=hvac101

#Dampers #AirSide #BuildingControls

---

## Hero Image

- File: `content/assets/hero-damper-selection-2026-09-28.png`
- Scene: Type A whiteboard lecture — one flow-vs-stroke graph: near-straight line labelled "OPPOSED" vs steep S-curve labelled "PARALLEL", "0.3" corner label, pointer in hand, Inu Faa seated beside. Headline "SIZE FOR AUTHORITY", punchline "LINEAR WINS".

## Notes (composition vs channel editorial direction)

- **Composed locally, no Dify raw output this run** — the "Havi — HVAC Content Generator" app does not exist on the VPS Dify (Sep 24 verification: 401 with tunnel up; today: tunnel down, connection refused). See run summary.
- **No invented figures.** The authority definition, the ≥0.3 recommendation and the <0.1 near-useless floor come from our own knowledge base (kb/q/5, "What is damper authority and how is it calculated?") — consistent with the ASHRAE Handbook treatment of damper authority, attributed without a fabricated clause number. The 1.5× close-off margin practice comes from our kb/q/1 close-off entry, framed as common practice via manufacturer tables. No savings percentages claimed.
- **Specifier framing** (what the selection decision does to the next spec), not technician how-to. No vendor names anywhere (close-off tables referenced generically — no Belimo/Honeywell/Siemens).
- **Link verified live (200 OK, 2026-09-28)**: /a/air-side-vav-damper-selection/ — "VAV Damper Selection for Commercial Buildings" — the post's exact subject.
- No emoji, Australian spelling, no competitor names, no "AI-powered" claims.

---

## Fallback draft ends here

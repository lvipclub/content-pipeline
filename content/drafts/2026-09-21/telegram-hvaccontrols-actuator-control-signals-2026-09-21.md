# Telegram Draft — @hvaccontrols — 2026-09-21

**Platform:** Telegram channel broadcast (@hvaccontrols)
**Audience:** Specifiers, consultants, facility managers (decision-maker voice)
**Topic:** Building controls cluster #4 — actuator control signal selection: on/off vs floating vs 0-10V/4-20mA modulating; matching signal type to the application; the ASHRAE Guideline 36 bus-communication note; retrofit implications (cable cores, point count)
**Distinct from:** Sep 7 run (BMS sensor data quality) and Aug 15 (BACnet integration architecture) — this is the actuator signal-selection layer; no prior run has covered actuator control signals.
**Note:** Composed locally this run — Dify app's upstream model provider still down (MiMo read-timeout, third consecutive run); voice/format follows the Sep 17/19 pattern.

---

## Post (target ≤ 1024 — sendPhoto hard limit; no emoji)

Signal choice is a spec decision — but most projects inherit it by default.

Let the application pick the actuator signal, not the other way around:

1. Open/close only — isolation dampers, smoke dampers, garage exhaust fans: on/off (2-position) with end-switch feedback.

2. Modulating where the controller has no analogue output — floating (3-point): open/close pulses, position inferred by the controller from pulse timing (typically 90-150 s full stroke). Economical and robust; the inference caveat belongs in the spec.

3. True proportional control — economisers, VAV boxes, critical temperature loops: 0-10V or 4-20mA modulating actuators with real position feedback.

And per ASHRAE Guideline 36, modulating actuators on large AHU dampers should also carry bus communication (BACnet MS/TP or Modbus RTU) — position, runtime and diagnostics reporting to the BMS for fault detection.

Signal type also fixes cable cores and point count. That is where the retrofit cost hides.

https://help.xinca.com/kb/q/28/?utm_source=telegram&utm_medium=channel&utm_campaign=hvac101

#HVACControls #Actuators #HVACSpec

---

## Hero Image (generated 2026-09-21, mascot mode — Bro Woo + Inu Faa)

- File: `content/assets/hero-actuator-control-signals-2026-09-21.png`
- Scene: Type A whiteboard lecture — three short signal rows ("ON/OFF", "FLOATING", "0-10V"), pointer in hand, Inu Faa seated beside. Headline "CONTROL SIGNALS", punchline "MATCH SIGNAL TO THE JOB".
- QA: PASS 10/10 on vision_analyze (backfilled 2026-09-24, first iteration): one slim Shiba with collar charm, glasses on Bro Woo, white flat-vector background; headline "CONTROL SIGNALS", punchline "MATCH SIGNAL TO THE JOB", labels ON/OFF, FLOATING, 0-10V + orange checkmark rendered exactly; no Chinese characters; no extra elements.

## Notes (composition vs channel editorial direction)

- **Composed locally, no Dify raw output this run** (MiMo provider outage, third consecutive run — see run summary). Voice, structure and char budget follow the Sep 17/19 approved drafts.
- **No invented figures.** The 90-150 s stroke time and the signal-family split are drawn from the knowledge-base entry linked below; ASHRAE Guideline 36 named as the bus-communication driver without fabricated clause numbers.
- **Signal selection framed as a specifier decision** (application-first), not a catalogue preference — no vendor names anywhere.
- **Link verified live (200 OK, 2026-09-21)**: /kb/q/28/ — "How do I select the appropriate damper actuator control signal" — the tightest KB match for this topic.
- No emoji, Australian spelling, no competitor names.

---

## Fallback draft ends here

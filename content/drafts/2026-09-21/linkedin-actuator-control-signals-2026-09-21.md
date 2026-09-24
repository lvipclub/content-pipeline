# LinkedIn Draft — XINCA Company Page — 2026-09-21

**Platform:** LinkedIn Company Page long-form
**Status:** DRAFT ONLY — Marc Sir posts manually from his personal profile
**Audience:** Professional network — specifiers, consulting engineers, facility managers, controls contractors (analyst voice, citation-aware)
**Topic:** Building controls cluster #4 — actuator control signal selection: the three signal families, the Guideline 36 bus-data layer, and the retrofit cost driver
**Distinct from:** Sep 7 run (BMS sensor data quality) and Aug 15 (BACnet integration architecture) — this is the actuator signal-selection layer; no prior run has covered it.
**Note:** Composed locally this run — Dify app's upstream model provider still down (MiMo read-timeout, third consecutive run); voice/format follows the Sep 17/19 pattern.

---

## Post (within LinkedIn's 3,000-char post limit)

**The Actuator Signal Decision Most Projects Inherit by Default**

Open a controls submittal from almost any project and you can trace the actuator control signals back to the project before it. Signal type is rarely specified from first principles — it is copied, and then the controller point count, the cable pulled to every device, and the data the BMS can see for the building's life are all consequences of that copy.

The application should make the choice, and the families stay simple:

**1. On/off (2-position).** Open/close only — isolation dampers, smoke dampers, garage exhaust fans. Simplest and cheapest, with end-switch feedback available for position status. Nothing more to configure.

**2. Floating (3-point).** For controllers without an analogue output that still need modulating control. Open/close pulses drive the actuator, and the controller tracks position by pulse timing — a full stroke typically takes 90–150 seconds. Economical and robust, with one caveat that belongs in the specification: the position is inferred, not measured, which is a different maintenance posture than true feedback.

**3. Modulating (0-10V or 4-20mA).** True proportional positioning with position feedback. The default choice for economisers, VAV boxes and any loop that must modulate rather than switch — and the only family that reports what the actuator is actually doing.

Then the layer most specifications still miss: ASHRAE Guideline 36 expects modulating actuators on large AHU dampers to also support bus communication (BACnet MS/TP or Modbus RTU), so actual position, runtime and diagnostic data reach the BMS for automated fault detection. Adding it at design stage is a spec line; retrofitting it into a commissioned plant is a project.

A power-side note that matters at replacement time: 24V AC and 24V DC actuators are not automatically interchangeable. Many modern 24V DC actuators will accept a 24V AC supply, but the reverse generally does not hold — verify against the manufacturer's specifications before mixing power types on a retrofit.

The through-line for specifiers: signal type fixes cable cores and controller point count. On a new build that is a line item; on a retrofit it is often the cost driver. Choose from the application backwards — on/off where switching is the job, floating where the controller constrains you, modulating where the loop needs feedback, and bus data where the BMS is expected to find faults before occupants notice them.

Full selection guide: https://help.xinca.com/kb/q/28/?utm_source=linkedin&utm_medium=company-page&utm_campaign=hvac101

Further reading from our knowledge base: [XINCA Knowledge Base: actuator control signals], [XINCA Knowledge Base: actuator power supplies], [XINCA Knowledge Base: spring-return selection].

#HVACControls #Actuators #BuildingAutomation

---

## Notes (composition vs editorial rules)

- **Composed locally, no Dify raw output this run** (MiMo provider outage — see run summary). Analyst voice per the platform table: data-aware, citation-aware, no marketing language.
- **Citations:** ≥2 own-KB references included in brackets. ASHRAE Guideline 36 named as the bus-communication driver without fabricated clause numbers. No performance percentages claimed anywhere — signal selection, the stroke time and the power-type caveat are stated as engineering facts per the knowledge base, not invented statistics.
- **No vendor names.** Signal families described generically (2-position, floating, modulating), consistent with the brand boundary rules.
- **Link verified live (200 OK, 2026-09-21)**: /kb/q/28/ with LinkedIn UTM. Single link (no hub links).
- No emoji, Australian spelling, no "AI-powered" claims.

---

## Fallback draft ends here

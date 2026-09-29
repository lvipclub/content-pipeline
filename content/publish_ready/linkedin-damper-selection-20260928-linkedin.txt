# LinkedIn Draft — XINCA Company Page — 2026-09-28

**Platform:** LinkedIn Company Page long-form
**Status:** DRAFT ONLY — Marc Sir posts manually from his personal profile
**Audience:** Professional network — consultants, facility managers, asset owners (analyst voice, citation-aware)
**Topic:** Air-side cluster — damper selection and authority: why the damper's share of branch pressure drop, not its face area, decides whether the installed system modulates
**Distinct from:** Sep 26 run (control valve selection/authority, water-side), Sep 24 (CO₂/DCV ventilation, IAQ), Sep 21 (actuator control signals, controls), Sep 19 (DC aisle containment, data centre), Sep 17 (retrofit payback, energy), Sep 14 (VAV airflow measurement, air-side) — this run is the air-side cluster at its 14-day boundary, sub-topic damper selection/authority (not airflow measurement, not VAV control sequences).
**Note:** Composed locally this run — Dify app absent from VPS; voice/format follows the Sep 17–26 approved drafts.

---

## Post (within LinkedIn's 3,000-char post limit)

**Blades Shape the Curve: The Damper Selection Detail That Decides Control Quality**

Dampers are often the least examined line in an air-side schedule — sized for duct geometry, then expected to modulate like a control valve. Installed performance says otherwise.

Damper authority is the open damper's share of the branch pressure drop at design airflow, directly analogous to valve authority in hydronic circuits. An authority of 0.3 or higher is recommended for stable modulating control; below 0.1, the damper contributes almost nothing until it is nearly closed [XINCA Knowledge Base: damper authority]. Select a characteristic from the catalogue, install the damper into a low-authority branch, and most of that characteristic ceases to exist [ASHRAE Handbook—Fundamentals].

The three selection decisions that matter:

1. **Blade arrangement shapes the installed curve.** Parallel-blade dampers rotate every blade the same way — at partial opening one blade shields the next, and the flow response runs steep and quick-opening. Opposed-blade arrangements keep the flow-versus-stroke relationship close to linear at the pressure drops modulating VAV terminals actually see. Parallel-blade remains the economical choice for two-position service, where linearity is irrelevant and cost is felt [XINCA Knowledge Base: parallel vs opposed-blade dampers].

2. **Authority is an air-side concept too.** A damper sized purely for face area sits in a near-zero-authority branch — the first half of actuator stroke achieves very little, and the loop tunes itself around a dead zone. Sizing for authority costs nothing at design stage; retuning a hunting loop costs commissioning time for the life of the building.

3. **Close-off closes the argument.** The actuator must hold the worst-case differential pressure with margin — common practice is at least 1.5 times the calculated close-off requirement, verified against the manufacturer's close-off tables for the actual blade type and seals, not the headline torque figure [XINCA Knowledge Base: damper close-off].

The discipline is cheap: select blades for the control service, size for authority, and verify close-off from the tables. The order matters — face area is a ducting decision, not a control decision.

Full guide: https://help.xinca.com/a/air-side-vav-damper-selection/?utm_source=linkedin&utm_medium=company-page&utm_campaign=hvac101

Further reading from our knowledge base: [XINCA Knowledge Base: parallel vs opposed-blade dampers], [XINCA Knowledge Base: damper authority], [XINCA Knowledge Base: damper actuator torque].

#HVAC #BuildingControls #AirSide

---

## Notes (composition vs editorial rules)

- **Composed locally, no Dify raw output this run** — VPS Dify has no Havi content app (see run summary). Analyst voice per the platform table: data-aware, citation-heavy, no marketing language.
- **Citations:** ≥2 own-KB references included in brackets (4 total). The 0.3/0.1 authority figures and the 1.5× close-off margin come from our own knowledge base entries, not invented; ASHRAE attribution is to the Handbook generally without a fabricated clause number. No performance percentages claimed — control-quality outcomes vary by system and load profile.
- **No competitor names** — close-off tables referenced generically ("the manufacturer's close-off tables"), no brands.
- **Link verified live (200 OK, 2026-09-28)**: /a/air-side-vav-damper-selection/ with LinkedIn UTM. Single article link (no hub links).
- No emoji, Australian spelling (analogous, economical, behaviour n/a), no "AI-powered" claims.

---

## Fallback draft ends here

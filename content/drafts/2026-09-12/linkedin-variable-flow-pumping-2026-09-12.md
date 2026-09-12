# LinkedIn Draft — XINCA Company Page — 2026-09-12

**Platform:** LinkedIn Company Page long-form
**Status:** DRAFT ONLY — Marc Sir posts manually from his personal profile
**Audience:** Professional network — consultants, facility managers, asset owners (analyst voice, citation-aware)
**Topic:** Water-side cluster #3 — variable-flow pumping: dP control of variable-speed pumps in VPF chilled water systems
**Continuity:** Follows the water-side thread (Aug 6 valve authority & balancing, Aug 22 low delta-T) — distinct angle: the pump-side control strategy and its energy physics.

---

## Post (2973 chars — within LinkedIn's 3,000-char post limit; merged from Dify's two concatenated drafts — known defect)

**Variable-Flow Pumping: The Control Strategy Behind the Cube-Law Savings**

If a chilled water plant still runs constant-speed pumps, the efficiency case for variable-primary-flow (VPF) is settled — variable-speed pumps on a single hydronic circuit, no decoupler, lower first cost and lower pump energy. What separates a high-performing VPF system from an expensive one is not the hardware. It is the differential pressure (dP) control strategy.

**Sensor placement: nearest point vs index circuit**

The most common defect is a dP sensor in or near the pump room. Installation is simple, but the reading under-represents the pressure at the far end of the network, so the pump over-speeds — and every valve in the building throttles away the excess.

Two placements fix this. The conventional one puts the sensor at the hydraulically most remote coil — the circuit with the highest calculated pressure drop back to the plant, not necessarily the physically furthest. The more intelligent option is the critical index approach: the building automation system watches every two-way control valve, identifies the most-open one (the circuit currently starved of pressure), and resets the dP setpoint upward just enough to bring that valve back to around 90% open — so the pump runs at the lowest speed the building actually needs.

**Setpoint reset: stop paying for design load at 3 a.m.**

A fixed dP setpoint sized for design conditions forces the pump to hold peak pressure every part-load hour. A trim-and-respond reset — lowering the setpoint while all valves sit below 90% open, responding when one climbs — keeps the system riding the load instead of chasing it.

**The physics: power follows the cube**

The affinity laws make small speed reductions disproportionately valuable. Flow tracks speed; pressure tracks speed squared; power tracks speed cubed. At 80% speed a pump draws roughly 51% of rated power. At 50% speed, about 12.5%. No other lever in the plant moves pump kilowatts this fast.

**The floor that protects the hardware**

There is a lower bound. Chillers require minimum evaporator flow, and pumps must stay within their stable operating range — so the control logic carries a minimum speed floor, typically 20–30% at commissioning, raised as more chillers stage on.

**What this means for your next project**

- Specifiers: document the dP sensor location and the reset sequence in the controls narrative — do not leave it to the controls contractor's interpretation.
- Facility managers: audit the existing plant. Where is the sensor, and is the setpoint fixed or reset? Those two answers price a large share of the annual pump energy.
- Everyone: commission it. A poorly tuned VPF system performs little better than the constant-flow plant it replaced.

Full guide: https://help.xinca.com/a/water-side-control-valve-selection/?utm_source=linkedin&utm_medium=company-page&utm_campaign=hvac101

#HVAC #Hydronics #EnergyEfficiency #FacilityManagement

---

## Notes (housekeeping vs raw Dify output)

- **Merged from two concatenated Dify drafts** (known defect — same as Sep 5/7/10 runs; raw answer was 7,523 chars containing both a Lady Havi-persona draft and an analyst draft). Kept the analyst frame throughout; persona voice is reserved for the channel, not the company page.
- **Unverified figures dropped:** "50-70% energy reduction vs constant-flow" and "60-80% pump motor energy reduction" (no source). Replaced with affinity-law arithmetic only (0.8³ ≈ 0.51; 0.5³ ≈ 0.125) — physics, not vendor claims.
- **Corrected a Dify error:** draft A called the critical index circuit "the hydraulically most remote point" — the two are distinct strategies (fixed remote sensor vs BAS-tracked most-open valve). Both are now described as separate options, matching the TG draft.
- **Emoji stripped**: raw drafts contained 🌊📍📉⚡⚠️🔑💡 and "Follow @hvaccontrols | Visit ai.xinca.com" promo lines (legacy domain) — replaced with a single link to /a/water-side-control-valve-selection/ + LinkedIn UTM (verified live, 200 OK, 2026-09-12).
- No emoji, Australian spelling (optimisation→n/a; "kilowatts", "over-speeds"), no competitor names.

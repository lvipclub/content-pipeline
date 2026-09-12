#!/usr/bin/env python3
"""compose.py — build the 3 Northstar drafts (2026-09-12, variable-flow pumping) with
the same length checks northstar-publish.py enforces (x_weight, tg <=1024)."""
import json, os, re

D = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.expanduser("~/workspace/content-pipeline")
SLUG = "variable-flow-pumping"
DATE = "2026-09-12"
ART = "https://help.xinca.com/a/water-side-control-valve-selection/"

TG_TEXT = """Variable-primary-flow pumping is the default for new chilled water plants — but the dP control strategy decides whether the savings arrive.

Three decisions:

1. Sensor placement. A sensor near the pump room over-pressurises the whole network. Place it at the hydraulically most remote circuit, or have the BAS track the most-open valve and reset the setpoint until it sits near 90% open.

2. Reset the setpoint. A fixed dP setpoint sized for design load wastes energy every part-load hour. Reset by valve position or load, and the pumps ride the affinity laws: 20% slower is about half the power; 50% speed is close to one-eighth.

3. Minimum speed floor. Chillers need minimum evaporator flow, and the floor rises as more machines stage on. Commission it deliberately.

Spec the sensor location and reset sequence in your controls narrative.

https://help.xinca.com/a/water-side-control-valve-selection/?utm_source=telegram&utm_medium=channel&utm_campaign=hvac101

#Hydronics #ChilledWater #HVACSpec"""

X_TEXT = """VPF pumping: the dP sensor belongs at the index circuit, not the pump room. Reset the setpoint by valve position, hold a minimum speed floor for the chiller, and the cube law does the rest — half speed ≈ one-eighth power. help.xinca.com/a/water-side-control-valve-selection/ #Hydronics #HVAC"""

X_FALLBACK = """VPF pumping: the dP sensor belongs at the index circuit, not the pump room. Reset the setpoint by valve position, hold a minimum speed floor for the chiller, and the cube law does the rest — half speed ≈ one-eighth power. #Hydronics #HVAC"""

LI_TEXT = """**Variable-Flow Pumping: The Control Strategy Behind the Cube-Law Savings**

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

#HVAC #Hydronics #EnergyEfficiency #FacilityManagement"""


def x_weight(t):
    urls = re.findall(r"https?://\S+|(?<![\w@/.])[a-z0-9-]+(?:\.[a-z0-9-]+)+/\S*", t)
    return len(t) - sum(max(0, len(u) - 23) for u in urls)


wtg, wx, wx2, wli = len(TG_TEXT), x_weight(X_TEXT), len(X_FALLBACK), len(LI_TEXT)
print(f"TG caption: {wtg} chars (limit 1024) -> {'OK' if wtg <= 1024 else 'TOO LONG'}")
print(f"X weighted: {wx} (limit 280) -> {'OK' if wx <= 280 else 'TOO LONG'}")
print(f"X fallback raw: {wx2}")
print(f"LinkedIn: {wli} chars (limit 3000) -> {'OK' if wli <= 3000 else 'TOO LONG'}")
if wtg > 1024 or wx > 280 or wli > 3000:
    raise SystemExit("FIX LENGTHS BEFORE WRITING")

tg = f"""# Telegram Draft — @hvaccontrols — {DATE}

**Platform:** Telegram channel broadcast (@hvaccontrols)
**Audience:** Specifiers, consultants, facility managers (decision-maker voice)
**Topic:** Water-side cluster #3 — variable-flow pumping: dP control of variable-speed pumps in variable-primary-flow (VPF) chilled water systems (sensor placement, setpoint reset, minimum speed floor, affinity-law energy)
**Distinct from:** Aug 6 run (valve authority & hydronic balancing) and Aug 22 run (low delta-T syndrome) — this run is the pump-side control strategy of the same water-side cluster.

---

## Post (caption {wtg} chars ≤ 1024 — sendPhoto hard limit; no emoji)

{TG_TEXT}

---

## Hero Image (generated {DATE}, freestyle mode — Week 2 of 2-week experiment)

- File: `content/assets/hero-{SLUG}-{DATE}.png` (1280×1280 PNG)
- Subject (from Dify brief + freestyle brand harness): end-suction chilled-water pump with VFD cabinet, dP sensor loop, pump/system curve overlay — navy #1B2333 base, headline "VARIABLE-FLOW PUMPING", punchline "Slower saves power", xinca.com footer.
- See rotation file notes for generation route + QA result.

## Notes (housekeeping vs raw Dify output)

- **Raw Dify answer was 4,834 chars** — trimmed to {wtg} for the 1,024-char sendPhoto limit. Kept the specifier framing and the three numbered decisions. Cut: the VPF-architecture explainer paragraph (folded into the opening line), the chiller-staging detail (folded into point 3), and the "welcome back to the series" preamble.
- **Emoji stripped**: raw answer contained 🧠📍💰🛡️ and a "Follow @hvaccontrols | Visit ai.xinca.com" promo line — removed (no-emoji brand rule; ai.xinca.com is the legacy domain).
- **Link added**: /a/water-side-control-valve-selection/ with TG UTM — verified live (200 OK, {DATE}). Raw output had no link.
- Claim check: cube-law figures are affinity-law arithmetic (0.8³ ≈ 0.51, 0.5³ ≈ 0.125). Dify's "60-80% pump energy reduction vs constant flow" claim was UNSOURCED and dropped. "Critical index circuit" / most-open-valve reset described as control practice, not tied to a specific standard. Minimum speed floor framed as commissioning practice; chiller minimum evaporator flow is the reason (chiller-freeze protection), not pump cavitation.
- No emoji, Australian spelling (over-pressurises), no competitor names.
"""

x = f"""# X Draft — @XincaHVAC — {DATE}

**Platform:** X (Twitter)
**Account:** @XincaHVAC (Sat rotation)
**Audience:** HVAC technicians, BMS integrators (practitioner voice)
**Topic:** Water-side cluster #3 — variable-flow pumping: dP sensor placement, setpoint reset, minimum speed floor, cube-law energy

---

## Post ({wx} weighted chars incl. URL — X counts the URL as 23; under 280)

{X_TEXT}

---

## Notes

- {wx} weighted chars incl. URL (t.co = 23) — under the 280 limit. No emoji, Australian spelling, no competitor names.
- Link verified live (200 OK, {DATE}): `/a/water-side-control-valve-selection/` — the water-side article; variable-flow pumping is the pump-side strategy of the same hydronic system.
- "half speed ≈ one-eighth power" is affinity-law arithmetic (0.5³ = 0.125) — safe as written.
- If the cold-account spam filter 403s on the help.xinca.com URL at publish time, fall back to the URL-free variant below (precedent: Aug 2026 runs).

**Fallback (URL-free, if 403):**
{X_FALLBACK}

---

## Fallback draft ends here
"""

li = f"""# LinkedIn Draft — XINCA Company Page — {DATE}

**Platform:** LinkedIn Company Page long-form
**Status:** DRAFT ONLY — Marc Sir posts manually from his personal profile
**Audience:** Professional network — consultants, facility managers, asset owners (analyst voice, citation-aware)
**Topic:** Water-side cluster #3 — variable-flow pumping: dP control of variable-speed pumps in VPF chilled water systems
**Continuity:** Follows the water-side thread (Aug 6 valve authority & balancing, Aug 22 low delta-T) — distinct angle: the pump-side control strategy and its energy physics.

---

## Post ({wli} chars — within LinkedIn's 3,000-char post limit; merged from Dify's two concatenated drafts — known defect)

{LI_TEXT}

---

## Notes (housekeeping vs raw Dify output)

- **Merged from two concatenated Dify drafts** (known defect — same as Sep 5/7/10 runs; raw answer was 7,523 chars containing both a Lady Havi-persona draft and an analyst draft). Kept the analyst frame throughout; persona voice is reserved for the channel, not the company page.
- **Unverified figures dropped:** "50-70% energy reduction vs constant-flow" and "60-80% pump motor energy reduction" (no source). Replaced with affinity-law arithmetic only (0.8³ ≈ 0.51; 0.5³ ≈ 0.125) — physics, not vendor claims.
- **Corrected a Dify error:** draft A called the critical index circuit "the hydraulically most remote point" — the two are distinct strategies (fixed remote sensor vs BAS-tracked most-open valve). Both are now described as separate options, matching the TG draft.
- **Emoji stripped**: raw drafts contained 🌊📍📉⚡⚠️🔑💡 and "Follow @hvaccontrols | Visit ai.xinca.com" promo lines (legacy domain) — replaced with a single link to /a/water-side-control-valve-selection/ + LinkedIn UTM (verified live, 200 OK, {DATE}).
- No emoji, Australian spelling (optimisation→n/a; "kilowatts", "over-speeds"), no competitor names.
"""

with open(f"{D}/telegram-hvaccontrols-{SLUG}-{DATE}.md", "w") as f:
    f.write(tg)
with open(f"{D}/x-xincahvac-{SLUG}-{DATE}.md", "w") as f:
    f.write(x)
with open(f"{D}/linkedin-{SLUG}-{DATE}.md", "w") as f:
    f.write(li)

spec = {
    "slug": SLUG,
    "set": "2026-09-13",
    "tg_draft": f"content/drafts/{DATE}/telegram-hvaccontrols-{SLUG}-{DATE}.md",
    "x_draft": f"content/drafts/{DATE}/x-xincahvac-{SLUG}-{DATE}.md",
    "li_draft": f"content/drafts/{DATE}/linkedin-{SLUG}-{DATE}.md",
    "hero": f"content/assets/hero-{SLUG}-{DATE}.png",
    "x_account": "XincaHVAC",
    "li_out": f"linkedin-{SLUG}-20260913-linkedin.txt",
    "keys": {
        "tg": f"telegram-hvaccontrols-{SLUG}-{DATE}",
        "x": f"x-xincahvac-{SLUG}-{DATE}",
        "li": f"linkedin-{SLUG}-{DATE}",
    },
    "log_key": f"northstar-{DATE}-{SLUG}",
    "label": "Sep 12 — Variable-flow pumping (water-side)",
}
with open(f"{D}/publish-spec.json", "w") as f:
    json.dump(spec, f, indent=1)
print("drafts + spec written to", D)

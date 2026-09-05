# LinkedIn Draft — XINCA Company Page — 2026-08-22

**Platform:** LinkedIn Company Page long-form
**Status:** DRAFT ONLY — Marc Sir posts manually from his personal profile
**Audience:** Professional network — specifiers, facility managers, building owners (analyst voice)
**Topic:** Water-side cluster #2 — low delta-T syndrome in chilled water systems

---

## Post

**The Silent Killer of Chilled Water Efficiency: Diagnosing and Curing Low Delta-T Syndrome**

In high-performance building services, we design chilled water systems for a specific temperature differential — often 6.7 K (12°F). Yet one of the most significant drains on a building's energy efficiency often hides in plain sight: low delta-T syndrome, where the actual difference between supply and return water sits far below design intent. It is not a random failure but a predictable outcome of common specification and control habits — and it forces pumps and chillers to work harder, consume more energy, and deliver less cooling than designed.

**The Anatomy of an Inefficient System**

Three culprits typically work in concert to erode system performance.

*First, oversized or improperly selected coils.* When a coil is specified with excessive rows or fin density for the required duty, it becomes overly effective — the coil achieves the required cooling with a smaller temperature drop, immediately depressing delta-T and returning water to the plant far cooler than the design return temperature [ASHRAE Handbook — HVAC Systems and Equipment].

*Second, two-way modulating control valves without proper authority.* These valves create a variable-flow system that places immense pressure on the pumping infrastructure. When individual zone valves throttle down to meet partial loads, system-wide pressure drop rises. Without pressure-independent control or a well-tuned variable speed drive, pumps run harder than necessary to maintain pressure at a few critical zones — mixing high-flow, low-delta-T water through the system. An oversized or low-authority valve may also spend most of its life "hunting" at low travel, bypassing the coil's heat transfer surface while returning water that is cool but not cool enough [CIBSE Guide B].

*Finally, pump curve selection.* A flat pump curve makes head highly sensitive to changes in flow, producing excessive pressure at low-flow conditions and forcing control valves to open more than required. A steep curve offers more stable pressure control across a wider flow range — a quiet but pivotal specification decision.

**The Compounding Cost**

The financial impact is severe and compounding. Pumping power follows the affinity law — power is roughly proportional to flow cubed. To deliver the same cooling (Q = m·c·ΔT) with a lower ΔT, mass flow must increase proportionally. A system designed for 6.7 K that operates at 4.4 K needs about 50% more water flow — and pumping power can rise to three times design. Operate at 3.3 K and the flow doubles, with pump energy climbing further still.

The chiller plant pays too. Increased total system flow can exceed the chiller's maximum design flow rate, triggering safety cutouts and effectively de-rating the plant's total cooling capacity. Part-load operation becomes less efficient, and the system's safety margin erodes exactly where the designer assumed it existed [CIBSE Guide B]. Maintaining design conditions is paramount to achieving rated performance across the entire cooling plant.

**A Prescription for Prevention**

Prevention begins at the design and specification stage:

1. **Right-size coils.** Resist the temptation to add "safety factors" by oversizing. Use accurate load calculations with realistic entering water temperatures and air-side conditions — not nominal ratings.
2. **Specify pressure-independent control.** For critical zones, maintain constant flow for a given control signal regardless of distribution-piping pressure fluctuations. Mandate a valve authority of at least 50% at design flow.
3. **Demand coil selection data.** Require terminal unit coils to be selected to meet the cooling capacity *at the specified minimum design flow rate and delta-T*. Reject submittals that only achieve capacity at excessively high flow rates.
4. **Select the right pump curve.** Analyse the system curve and specify a stable, steep characteristic for variable-flow operation, paired with differential pressure reset based on valve position rather than a fixed setpoint.
5. **Commission rigorously.** Commissioning is not a final step — it is integral. Flush and balance the hydronic system, calibrate every sensor, and verify design delta-T under real load conditions.

**Key Takeaway**

Low delta-T syndrome is not an inevitable consequence of an ageing system; it is a direct result of design and specification choices. By focusing on accurate coil selection, pressure-independent control, appropriate pump curves, and rigorous commissioning, engineers can deliver chilled water systems that perform as designed for their entire lifecycle.

For deeper technical detail on water-side selection — valve authority, hydronic balancing and pump sizing — search the XINCA HVAC controls knowledge base at help.xinca.com: https://help.xinca.com/a/water-side-control-valve-selection/

---

## Notes
- Dify returned TWO concatenated drafts (known defect, same as 2026-08-17/20 runs). Merged into one: Draft A structure (Anatomy → Compounding Cost → Prescription) as base; folded in Draft B's actionable spec-level detail (point 3: demand coil selection data; the "hunting" valve and "hides in plain sight" framing) and its 3.3 K doubling-flow scenario.
- Citation fixes: dropped the shaky "lower lift → reduced chiller efficiency" claim (technically wrong direction); kept the de-rating/part-load framing [CIBSE Guide B] and coil oversizing [ASHRAE Handbook]. No fabricated URLs — standards cited by name only.
- Word count ~620. Australian spelling (ageing, optimisation-free). No emoji. No competitor names. Link verified live (200 OK).

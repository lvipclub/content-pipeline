# LinkedIn Draft — XINCA Company Page — 2026-09-05

**Platform:** LinkedIn Company Page long-form
**Status:** DRAFT ONLY — Marc Sir posts manually from his personal profile
**Audience:** Professional network — data centre operators, consultants, facility managers (analyst voice)
**Topic:** Data centre cooling cluster #6 — direct-to-chip liquid cooling and CDU architecture
**Continuity:** Series follow-up to the 13 August piece on air-side thermal envelopes (supply temps, aisle containment, ASHRAE TC 9.9)

---

## Post

**When Air Hits the Wall: Direct-to-Chip Liquid Cooling for High-Density Data Centres**

The industry is reaching a tipping point that many facility managers have felt coming for years. When rack densities climb beyond approximately 40 kW, traditional air-side cooling architectures begin to hit the limits of air as a transport medium. Its low volumetric heat capacity forces us to move massive volumes of it — escalating fan energy, acoustic challenges, and the physical limits of raised-floor plenums and hot-aisle containment. For the AI training clusters and high-performance computing (HPC) workloads defining the next decade, air-side solutions alone are no longer sufficient. The frontier has shifted to the liquid side.

This evolution moves us beyond the air-centric frameworks we discussed on 13 August — ASHRAE TC 9.9's environmental envelopes and advanced aisle containment. The new conversation is about direct-to-chip (D2C) cold plates and the distribution systems that feed them. A D2C system places a liquid-cooled heat exchanger, the cold plate, directly onto the heat-generating component — typically the CPU or GPU lid. This leverages the superior thermophysical properties of liquids: water's thermal conductivity is roughly 24 times that of air, and its volumetric heat capacity around 3,500 times higher. The result is that a D2C cold plate can capture up to 75–80% of a server's heat load at the source [Uptime Institute, 2023]. The remaining heat, dissipated by lower-power components like memory and voltage regulators, is handled by supplemental rear-door heat exchangers or low-velocity air — creating a hybrid configuration that is particularly effective for retrofit scenarios.

**The Coolant Distribution Unit: an engineered interface, not a pump-and-tank**

The heart of a liquid-cooled facility is the CDU. It isolates the facility's primary cooling loop — often connected to cooling towers or dry coolers — from the low-volume, low-pressure secondary loop serving the servers. Its architecture is critical for reliability and efficiency. Three functions define it: heat exchange, with physical separation between loops preventing contamination and leak propagation; precise flow and pressure control to each cold plate; and continuous filtration plus monitoring of temperature, pressure and flow, feeding the building management system or data centre infrastructure management platform. In high-availability facilities, CDUs are deployed in N+1 or 2N arrangements, typically with plate-and-frame heat exchangers providing the physical separation between loops.

**The retrofit path: hybrid, not rip-and-replace**

For existing facilities, wholesale replacement of air-cooling infrastructure is usually impractical. A hybrid configuration deploys liquid cooling to the highest-heat components while memory, storage and networking continue under the room's existing air handling. Operators can incrementally raise rack density and power capacity without a full-scale renovation, protecting capital investment while enabling next-generation compute. The CDU acts as the bridge — rejecting heat to the building loop while maintaining the pressure differential that protects the IT gear.

**Standards: the ASHRAE liquid-cooling classes**

The ASHRAE TC 9.9 Liquid Cooling Guidelines provide the framework for specifying liquid-cooled IT equipment. Equipment classes start at W1, covering inlet water temperatures of 2–17°C, and extend to warmer classes permitting inlet temperatures up to about 45°C. The class chosen is a foundational design decision: warmer coolant allows the facility to reject heat directly to the ambient environment or to a heat recovery system without energy-intensive chiller operation for a significant share of the year — directly reducing power usage effectiveness.

**Waste heat: from rejection to recovery**

This is the most compelling long-term opportunity. Heat captured by a liquid cooling loop is a high-grade thermal resource, typically in the 40–60°C range — vastly more useful than the low-grade heat rejected from air-cooled systems. Industrial heat pumps can elevate it to 80°C and beyond, making it suitable for district heating, domestic hot water, or agricultural processes such as greenhouse heating. The European Union's Energy Efficiency Directive increasingly recognises data centres as potential heat sources for urban areas [European Commission, 2023]. Traditionally viewed as massive energy consumers, data centres can become "digital boilers" for their local communities — transforming their environmental and economic footprint.

**Key takeaway**

The shift to liquid-side cooling, governed by intelligent CDU architecture and hybrid retrofit strategies, is the realistic path for high-density computing. By leveraging standards like the ASHRAE liquid-cooling classes and embracing high-grade waste-heat recovery, the industry can build a more efficient and more sustainable computational future. The data centre of the future is a dual-fluid system: air handles the basics, liquid does the heavy lifting — and the CDU becomes as critical as the switchgear.

To explore these systems further, search the HVAC controls knowledge base at help.xinca.com: https://help.xinca.com/a/data-center-energy-efficiency/

---

## Notes
- Dify returned TWO concatenated drafts again (known defect, same as Aug 17/20/22/24 runs). Merged into one: Draft A (water properties, Omdia market data, CDU functions, ASHRAE W-classes, waste heat) as base; folded in Draft B's 40 kW tipping-point framing, 75–80% capture figure, hybrid retrofit detail, and "digital boilers" framing. Removed duplicate CDU-function passages.
- Citation fixes: kept [Omdia, 2023] (>25% CAGR through 2027), [ASHRAE Liquid Cooling Guidelines, 3rd ed.], [Uptime Institute, 2023], [European Commission, 2023]; DROPPED the Schneider Electric White Paper 265 citation (competitor-name rule) — the N+1/2N + plate-and-frame claim is rephrased as industry practice, and the W-class ranges softened to W1 (2–17°C) → up to ~45°C to avoid Draft A/B inconsistency (Draft A said W2 2–17°C; Draft B said W1 2–17°C and W3 2–45°C). No fabricated URLs — standards cited by name only.
- "ai.xinca.com" in Dify output replaced with help.xinca.com (ai.xinca 301s to help since Jul 2026 — never link the old domain).
- Word count ~910. Australian spelling (recognising, optimise-free pass: no -ize forms; "centres" used for data centres). No emoji. No competitor names.

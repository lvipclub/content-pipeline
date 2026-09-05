# LinkedIn — XINCA Company Page (Draft — Manual Post Required)
# Topic: Data centre cooling — supply temperature decisions, aisle containment & ASHRAE TC 9.9 thermal envelopes
# Date: Thu 13 Aug 2026

**Status:** Draft only — Marc Sir posts manually from personal profile

**Audience:** Analyst voice — data-backed, citation-heavy, market insight + engineering substance

**Headline:** Data Centre Cooling: Why Supply Temperature Decisions Are the Biggest Lever You're Not Turning

---

For years, the default assumption in critical facilities has been that IT equipment needs cold air, delivered relentlessly, at temperatures that feel more like a wine cellar than a server hall. That assumption is now the single largest cost driver standing between your facility and efficient operation.

The physics has not changed. What has changed is the thermal tolerance of the equipment and the commercial logic of every degree you refuse to raise.

**Aisle containment is table stakes**

Hot aisle containment (HAC) and cold aisle containment (CAC) are not new technologies. Properly sealed containment eliminates bypass airflow and recirculation, allowing computer room air handling (CRAH) units to deliver exactly what the rack needs. Without containment, supply air temperatures must be set lower to compensate for mixing losses. With containment, you can raise supply temperatures by 3-5°C without violating inlet conditions. That difference alone can translate into a 10-15% reduction in mechanical cooling energy.

Loose numbers? Not really. Industry data from hyperscale operators who publish their operational metrics shows that disciplined airflow management is worth the first 0.2 to 0.3 points of PUE improvement. It is the cheapest infrastructure upgrade available to an existing data centre, and it is frequently ignored because it does not require a new chiller or a control system replacement.

**ASHRAE TC 9.9 and the thermal envelope**

The publication of the ASHRAE Thermal Guidelines for Data Processing Environments [ASHRAE TC 9.9] transformed the industry's vocabulary. The A1-A4 classes define allowable and recommended operating envelopes for IT equipment:

- A1: 15-32°C allowable, with an 18-27°C recommended range
- A2: 10-35°C allowable
- A3: 5-40°C allowable
- A4: 5-45°C allowable

What these classes are not is a mandate to operate at the limit. They are procurement specifications. If you purchase servers rated for A3 or A4 environments, your facility can operate with far more economiser hours and far less compressor run time. Every hour your chillers are off is an hour of efficiency you do not have to pay for.

For existing facilities designed around A1, the practical move is to push the return air temperature, not just the supply. Warmer return air to the cooling plant improves chiller efficiency and increases waterside economiser utilisation. The supply temperature decision is therefore not merely an operational preference; it is a capital and energy strategy.

**The high-density problem**

Density is the disruptor. As processor thermal design power (TDP) climbs, racks at 20-30 kW and beyond become impractical for air cooling. Air simply cannot move enough heat at sensible temperature differentials without enormous fan energy. This is not a future problem. It is appearing now in AI training clusters and GPU-accelerated workloads.

Liquid cooling is the standard engineering response [EN 50600 | ASHRAE TC 9.9]. Direct-to-chip cooling, rear-door heat exchangers and immersion systems each have a role. Direct-to-chip is the most mature retrofit path, removing 70-80% of the heat at the source. Rear-door heat exchangers suit mixed estates where not every rack is high density. Immersion remains effective but is typically a new-build consideration.

The data point that matters: liquid cooling operates with coolant temperatures of 32-45°C at the rack. That temperature is high enough for year-round free cooling in most climates. A facility designed for liquid cooling can approach PUE values of 1.1 or lower, whereas a conventional air-cooled facility with the same IT load typically sits in the 1.3-1.5 range.

**PUE is a supply temperature decision**

PUE is frequently treated as a design metric, but it is actually an operational outcome. Every degree of supply air temperature increase reduces the temperature lift across the cooling plant. Reduced lift means improved coefficient of performance (COP) for chillers and more hours where the economiser can carry the load entirely.

Consider two identical facilities, one running supply air at 18°C and the other at 24°C. The latter will typically consume 20-30% less cooling energy annually in a temperate climate. Applied to a 10 MW IT load, that is a substantial operating expenditure reduction every year, without a single server upgrade.

The reticence is understandable. Facilities teams fear thermal events and the accountability that follows. The mitigation is not lower temperatures; it is instrumentation. Monitor inlet temperatures at the rack, maintain containment integrity and publish your thermal envelope to procurement. If you do not specify the thermal class of the equipment you buy, you are leaving efficiency on the table.

**The integration opportunity**

XINCA's view is that cooling is not an isolated mechanical system. It is one domain within the broader Internet of Things (IoT) and building automation system (BAS) estate. When supply temperature, airflow, coolant flow and IT load are managed as a single control problem, the efficiency gains compound. This is where XINCA's work in HVAC, IoT and connected intelligence intersects with the critical facilities sector.

**Key Takeaway**

The data centre industry has moved from "keep it cold" to "keep it within the envelope." Aisle containment, ASHRAE TC 9.9 thermal classes and liquid cooling are not competing strategies. They are a progression. The facilities that will lead the next decade are those that treat supply temperature as a strategic variable, measure inlet conditions continuously and procure equipment for the envelope they intend to run, not the one they inherited.

This article draws on XINCA's knowledge base: help.xinca.com/a/data-center-energy-efficiency/ and help.xinca.com/a/data-center-glycol-cooling/

#DataCentreCooling #PUE #CriticalFacilities

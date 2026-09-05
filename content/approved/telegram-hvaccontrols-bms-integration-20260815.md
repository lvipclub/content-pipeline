# Telegram — @hvaccontrols
- Date: 2026-08-15
- Cluster: 4 (Controls / BMS integration)
- Audience: specifiers, consultants, facility managers (decision-maker voice)
- Status: DRAFT — awaiting Marc Sir approval

---

Owners are starting to reject proprietary controls at handover — and the smart ones are specifying open protocols from day one. Here is what BACnet MS/TP vs IP means for your next project.

The shift is real. Facilities teams have been burned for years by vendor lock-in: you cannot change a controller without reworking the whole network, you cannot retrieve your own data without a costly software licence, and every service call becomes a negotiation. Tenders now demand open, standards-based systems.

BACnet makes openness achievable, but the transport layer matters more than most people realise. MS/TP runs over RS-485 serial wiring at 38.4 to 115.2 kbps — robust, cost-effective, right for small to mid-size plants and floor-level controllers. BACnet/IP runs over Ethernet — higher bandwidth, easier network management, scales across a campus. Not good versus bad: it is a question of scale, topology, and what the asset actually needs.

Specify BACnet/IP everywhere and you pay for network infrastructure a small boiler plant does not need. Specify MS/TP everywhere and you build a bottleneck for a site with thousands of points. The mature approach is a hybrid: BACnet/IP at the supervisory and integration level, MS/TP for field-level controllers and terminal equipment.

On sensor strategy, the common mistake is minimising sensor counts to save capital cost. False economy. A BMS is only as good as its sensing — if you do not measure zone temperature, humidity, CO2 and differential pressure where it matters, your control loops are flying blind and your energy reporting is fiction. On MS/TP, keep the baud rate consistent and limit devices per segment. On IP, isolate BMS traffic with VLANs.

When you write the specification, be explicit. Name BACnet as the standard, then go further: object types, point schedules, alarming and trending requirements, data ownership. If a vendor claims "BACnet compatible", ask which revision, which object types, which profiles. The marketing language dissolves quickly under those questions.

Key takeaway: open protocols, a hybrid BACnet architecture, a serious sensor strategy and a tightly written specification are lifecycle value. The rest get locked in.

→ help.xinca.com/a/building-controls-bms-integration/?utm_source=telegram&utm_medium=channel&utm_campaign=hvac101

#BACnet #BuildingControls #BMS

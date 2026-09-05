# X — @XincaHVAC
# Topic: IAQ — CO₂ monitoring accuracy, sensor placement, and demand-controlled ventilation
# Date: Mon 03 Aug 2026

**Audience:** HVAC technicians, BMS integrators, commissioning engineers — practitioner voice

**Draft:**

Why do two CO₂ sensors in the same room disagree by 300 ppm?

Usually not the sensor — it's placement and calibration assumptions:

1. NDIR self-calibration (ABC) assumes the space periodically sees ~400 ppm outdoor air. A room that never does drifts high over months, and the BMS over-ventilates quietly to compensate [ASHRAE 62.1].

2. A sensor beside a supply diffuser reads diluted supply air, not the breathing zone. The 62.1 rule of thumb: sense where occupants breathe, or in a return airstream that represents the occupied zone average.

3. No verification baseline. A reference-gas check at commissioning catches drift early; an unverified sensor reads fiction with confidence until a comfort complaint surfaces.

And the caveat that gets missed: CO₂ tracks people, not everything. It won't see VOCs from fit-out or PM2.5 ingress — it's an occupancy proxy for DCV, not a universal air-quality gauge.

DCV done right: NDIR, ±50 ppm accuracy class, breathing-zone placement, commissioning baseline, recalibration interval. The maths is in ASHRAE 62.1.

help.xinca.com/kb/q/29/?utm_source=x&utm_medium=social&utm_campaign=xincahvac

#CO2Monitoring #DCV #IAQ #Ventilation

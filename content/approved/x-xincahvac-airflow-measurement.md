# X — @XincaHVAC
# Topic: Air-side — VAV Airflow Sensor Drift & Commissioning
# Date: Sat 01 Aug 2026

**Audience:** HVAC technicians, BMS integrators, commissioning engineers — practitioner voice

**Draft:**

Why does your VAV airflow reading drift from the balancing report?

Three causes, in order of how often we see them:

1. Single-point velocity probes. The duct velocity profile moves with damper position and upstream fittings. A probe reading one spot tracks the profile, not the flow. Multipoint averaging arrays hold ±2-3% of reading; single-points drift far beyond that in real ductwork [ASHRAE 111].

2. Range mismatch. Velocity pressure scales with the square of velocity — at 30% minimum flow your 0-2 in. w.g. transmitter is reading near the noise floor. Range the sensor to the minimum flow, not the design flow.

3. No commissioning baseline. If the sensor was never traversed against a manual pitot grid after installation, you have no reference point to detect drift against. An unbaselined sensor reads fiction with confidence.

The fix on your next job: averaging sensor, range matched to turndown, and a traverse baseline in the TAB report. Costs hours, saves years of DCV arguments.

ai.xinca.com/kb/q/24/?utm_source=x&utm_medium=social&utm_campaign=xincahvac

#VAV #AirflowMeasurement #Commissioning #DCV #BACnet

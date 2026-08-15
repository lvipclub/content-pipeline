# Analysis — VAV Damper Selection Comic

## Purpose
Drive clicks from X to https://ai.xinca.com/a/air-side-vav-damper-selection/ — a 4-image comic (cover + 3 pages) posted with a hook. Audience: consulting engineers, commissioning agents, facility managers (trade professionals, English).

## Core message
A damper sized by duct diameter is the #1 VAV specification mistake. Size by free area, target 15-25% authority, spec BACnet actuators. Cost of getting it wrong (hunting, noise, actuator wear, rebalancing) far exceeds the <AUD 80 material delta.

## Comic angle (hook → problem → fix → payoff)
1. **Cover**: The damper is the smallest, most mis-specified part in VAV design. Bro Woo + Inu Faa at the whiteboard. "Right size. Right control."
2. **Problem**: "Size by duct diameter" is wrong — free area (75-85%) is what matters; oversized dampers hunt and wear below 15% stroke.
3. **Fix**: The authority rule — β = damper ΔP / branch ΔP, target 15-25% for linear modulating control.
4. **Payoff**: BACnet MS/TP actuators — position + torque feedback, predictive maintenance, daisy-chain wiring. CTA → full guide.

## Style (mascot mode — overrides generic baoyu style)
- Bro Woo + Inu Faa flat vector mascot style, pure white bg, black lines, orange-only accent
- Scene Type A (whiteboard) preferred for Inu Faa — validated 9/10 vs 7/10 desk
- Portrait 3:4 (X image post friendly)
- Text discipline: header ≤20 chars, punchline ≤25 chars, whiteboard labels = single words/abbreviations
- Hard negatives in every prompt: EXACTLY ONE dog, glasses ON, subtle hair, ⚡ charm visible, no photorealism/gradients/shadows, no extra text

## Character sheet
Skipped (established brand characters — spec already validated via Helen vision QA, browoo-whiteboard-concept 9/10; canonical descriptions in characters/characters.md drive page prompts).

## Tech facts to respect (no invented numbers)
- Free area ratio 75-85% (opposed-blade)
- Authority band 15-25% of branch ΔP; <10% → quick-opening distortion
- Minimum controllable stroke 10-15% ≈ 5-8% design flow
- Torque at 750 Pa can be 2-3× catalogue rating
- BACnet MS/TP: 15-25% premium, payback >50 terminals

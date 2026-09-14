#!/usr/bin/env python3
"""Char-count verification for 2026-09-14 drafts + hero prompt file writer."""
import re, os

D = os.path.expanduser('~/workspace/content-pipeline/content/drafts/2026-09-14')

# --- TG caption: text between "## Post" and "---"
tg = open(f'{D}/telegram-hvaccontrols-vav-airflow-measurement-2026-09-14.md').read()
m = re.search(r'## Post \(1001 chars[^)]*\)\n\n(.*?)\n\n---', tg, re.S)
tg_text = m.group(1) if m else ""
print(f"TG caption: {len(tg_text)} chars (limit 1024) -> {'OK' if len(tg_text) <= 1024 else 'OVER'}")

# --- X post: weighted chars (URL = 23 via t.co)
x = open(f'{D}/x-xincahvac-vav-airflow-measurement-2026-09-14.md').read()
m = re.search(r'## Post \(see Notes[^)]*\)\n\n(.*?)\n\n---', x, re.S)
x_text = m.group(1) if m else ""
url_pat = re.compile(r'https?://[^\s]+')
weighted = len(url_pat.sub('x' * 23, x_text))
print(f"X post: {weighted} weighted chars (limit 280) -> {'OK' if weighted <= 280 else 'OVER'}")
# fallback variant
m2 = re.search(r'Fallback \(URL-free, if 403\):\*\*\n(.*?)\n\n---', x, re.S)
if m2:
    fb = m2.group(1)
    print(f"X fallback: {len(fb)} chars (limit 280) -> {'OK' if len(fb) <= 280 else 'OVER'}")

# --- LinkedIn
li = open(f'{D}/linkedin-vav-airflow-measurement-2026-09-14.md').read()
m = re.search(r'## Post \((\d+) chars[^)]*\)\n\n(.*?)\n\n---', li, re.S)
li_text = m.group(2) if m else ""
print(f"LinkedIn post: {len(li_text)} chars (limit 3000) -> {'OK' if len(li_text) <= 3000 else 'OVER'}")
actual = m.group(1) if m else "?"
if li_text and m:
    print(f"  (header says {actual} — actual measured {len(li_text)})")

# --- brand checks on all three
issues = []
for name, txt in [("TG", tg_text), ("X", x_text), ("LI", li_text)]:
    for e in "📉🔢🏗️💡🔧🌊📍💰🛡️⚠️🔑🤖✅":
        if e in txt:
            issues.append(f"{name}: emoji {e}")
    for bad in ["ai.xinca.com", "Belimo", "Honeywell", "Siemens", "Johnson Controls", "G'day"]:
        if bad in txt:
            issues.append(f"{name}: banned string '{bad}'")
print("Brand checks:", issues if issues else "all clean")

# --- hero prompt (mascot mode, Type A whiteboard lecture, per northstar-hero-image template)
prompt = """Clean flat vector illustration. Pure white background. Landscape 16:9. Educational tone.

TEXT AT TOP: Bold black rounded sans-serif headline: "VAV AIRFLOW MEASUREMENT"

MAIN SCENE: Bro Woo stands pointing at a whiteboard with a marker — short black spiky hair (subtle, not exaggerated), thin rectangular black glasses, grey V-neck sweater over white collared shirt, dark grey trousers, black shoes. Exactly ONE SLIM Shiba Inu (Inu Faa) sits beside him looking up at the board — tan/cream fur, white chest/muzzle/paws, large pointed ears, curled tail, yellow collar with small orange lightning bolt charm. Whiteboard shows a simple airflow sensor comparison: three small duct cross-section sketches in a row — one with a pitot tube probe, one with a small heated element dot, one with two sound-wave arcs — labelled "PITOT", "THERMAL", "ULTRASONIC", with a simple curved airflow profile line above each. Black outlines only. Orange (#FF8C00) used ONLY on the diagram elements and 1-2 keywords. NO other colours except small yellow lamp if desk scene.

TEXT AT BOTTOM: "Trust the traverse" — exactly 2 words in orange. Bottom-right corner in tiny black font: "xinca.com".

STRICT RULES:
- Exactly ONE dog. No extras. No other animals. No duplicates.
- Bro Woo's hair: spiky but subtle. NOT a lightning bolt. NOT anime. NOT exaggerated.
- Bro Woo MUST wear glasses.
- Inu Faa MUST be slim and elegant, not round or chubby.
- Yellow collar with orange lightning bolt charm MUST be visible on Inu Faa.
- Pure white background. No shadows. No gradients. No textures.
- Clean flat vector style. NOT hand-drawn wobbly. NOT photorealism. NOT 3D render.
- Whiteboard text: 3-4 short labels maximum. NO paragraphs. NO dense text.
- Exactly the elements listed. Do NOT add extra characters, extra props, extra text.
- No Chinese characters in any rendered text."""

with open('/tmp/hero_prompt_vav_20260914.txt', 'w') as f:
    f.write(prompt)
print("\nHero prompt written to /tmp/hero_prompt_vav_20260914.txt")

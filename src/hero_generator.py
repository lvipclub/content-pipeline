"""
hero_generator.py — Engineering Field Reference Hero Image Generator
====================================================================
Generates hero images in "engineering logbook spread" style for XINCA ai articles.
Style: Open bound A3 logbook, two facing pages, dense written content, block diagrams,
formulae, comparison tables. Seasoned facilities engineer's handwriting.
Printable field reference aesthetic. 16:9 landscape for social platforms.

NO mascots, NO cartoon characters, NO coloured arrows — purely professional.

Usage:
    python hero_generator.py "Data Centre Cooling" dc-cooling
    python hero_generator.py "AI Building Energy Management" ai-energy

Requirements:
    - XAI_API_KEY (auto-loaded from ~/.config/last30days/.env)
    - grok-imagine-image-quality via xAI API

Output: hero-{slug}-logbook.png in ~/workspace/content-pipeline/content/assets/
"""

import os
import sys
import subprocess
import requests
import time
from pathlib import Path

# --- CONFIG ---
ASSETS_DIR = Path("/home/hermerr/workspace/content-pipeline/content/assets")
XAI_MODEL = "grok-imagine-image-quality"
XAI_API = "https://api.x.ai/v1/images/generations"

def get_xai_key():
    key = os.environ.get("XAI_API_KEY", "")
    if key:
        return key
    env_file = Path.home() / ".config" / "last30days" / ".env"
    if env_file.exists():
        for line in env_file.read_text().split("\n"):
            if line.startswith("XAI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def generate(prompt: str, output_path: Path) -> bool:
    xai_key = get_xai_key()
    if not xai_key:
        print("❌ XAI_API_KEY not found.")
        return False

    headers = {"Authorization": f"Bearer {xai_key}", "Content-Type": "application/json"}
    payload = {"model": XAI_MODEL, "prompt": prompt, "n": 1, "response_format": "url"}

    print(f"  🎨 Generating via {XAI_MODEL}...")
    try:
        resp = requests.post(XAI_API, headers=headers, json=payload, timeout=180)
    except Exception as e:
        print(f"  ❌ API failed: {e}")
        return False

    if resp.status_code != 200:
        print(f"  ❌ {resp.status_code}: {resp.text[:200]}")
        return False

    url = resp.json()["data"][0].get("url", "")
    if not url:
        print(f"  ❌ No URL in response")
        return False

    img_resp = requests.get(url, timeout=60)
    if img_resp.status_code == 200:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(img_resp.content)
        print(f"  ✅ {output_path.name} ({len(img_resp.content):,} bytes)")
        return True
    else:
        print(f"  ❌ Download failed: {img_resp.status_code}")
        return False


def build_logbook_prompt(topic: dict) -> str:
    """
    Build the standard logbook spread prompt.
    topic dict must have: title, slug, left_page_points (list of str),
    right_page_diagram_desc (str), comparison_table (str), sources (str), formulae (list of str).
    """
    title = topic["title"]
    left_points = "\n".join(f"'{p}'" for p in topic.get("left_page_points", []))
    formulae = "\n".join(f"'{f}'" for f in topic.get("formulae", []))
    diagram = topic.get("right_page_diagram_desc", "block diagram showing system components")
    table = topic.get("comparison_table", "comparison table with real numbers")
    sources = topic.get("sources", "Key references")
    highlight_terms = topic.get("highlight_terms", "")

    return (
        f"An open bound engineering logbook (hardcover, A3 spread, two facing pages) photographed from above, 16:9 landscape. "
        f"The spread is DENSELY filled with written content — a working reference sheet, not a poster. "
        f"Seasoned facilities engineer's handwriting: black fine-liner, confident block-capital headings, red pen for critical numbers. "
        f"Yellow highlighter marks key terms: {highlight_terms}. "
        f"Title across top of spread: '{title.upper()} — FIELD REFERENCE — 2026-07' in bold block letters. "

        f"LEFT PAGE — mostly written content with formulae: "
        f"{left_points} "
        f"Key formulae written prominently: {formulae} "
        f"Bottom of left page: '{sources}' in tiny script. "

        f"RIGHT PAGE — block diagrams and comparison table: "
        f"TOP HALF: a simple block diagram using rectangular blocks connected by single lines — NO coloured arrows, NO photo-realistic equipment. "
        f"Use dashed lines with text labels. {diagram}. "
        f"BOTTOM HALF: a hand-drawn comparison table with columns and real numbers: {table}. "

        f"Logbook spine visible in centre. Pages show slight wear and curled corners. "
        f"Mechanical pencil clipped to top of right page. Steel ruler and coffee mug at frame edge. "
        f"No cartoon characters, no mascots, no doodles. Purely professional engineering reference sheet. "
        f"Crisp, photorealistic, looks like a real engineer's field notebook that someone would print out and keep in their toolkit."
    )


# --- ARTICLE TOPICS ---

TOPICS = {
    "data-center-cooling": {
        "title": "Data Centre Cooling",
        "slug": "data-center-cooling",
        "highlight_terms": "PUE, Liquid Cooling, Airflow, DCIM, ASHRAE TC09.09",
        "formulae": [
            "PUE = P_total ÷ P_IT — circled in red, with values: Air 1.4–2.0, Liquid 1.03–1.15",
            "DCiE = 1/PUE × 100% — reciprocal metric",
            "Q = ṁ · cp · ΔT — liquid cooling heat transfer, cp water ≈ 4.18 kJ/(kg·K)",
            "ΔT approach = T_coolant_supply − T_chip_case — liquid achieves <5K",
        ],
        "left_page_points": [
            "Rack density capability: 5kW baseline → 15–25kW with containment (air) → 50–100kW+ with liquid.",
            "Cooling energy fraction: Air 30–50% of facility power, Liquid 3–15% of facility power.",
            "Hot aisle/cold aisle + containment = prerequisite before evaluating liquid cooling.",
            "DCIM + PMBus + rack PDU monitoring enables 5–15% additional firmware-level savings beyond hardware gains.",
            "AI GPU racks pushing 25kW+ — air ceiling at ~20–25kW per standard 42U rack.",
            "Free cooling (economiser): climate-dependent for air, year-round potential with warm-water liquid loops at 40–45°C supply.",
        ],
        "right_page_diagram_desc": (
            "Block diagram: 'IT Load → Rack PDU → Server → Cold Plate → CDU → Cooling Tower'. "
            "Each block is a simple rectangle. Connections are dashed single lines with text labels."
        ),
        "comparison_table": (
            "Factor | Air Cooling | Liquid Cooling. Rows: PUE (1.6 vs 1.1), Max kW/rack (25 vs 100+), "
            "Capex (Low vs High), Opex % (30-50% vs 3-15%), Water use (High vs Low-closed-loop), "
            "Maintenance (Fans/filters vs Pumps/chemistry)"
        ),
        "sources": "Gilbert Held 2011, ASHRAE TC09.09, The Green Grid PUE metric",
    },
    "ai-energy-management": {
        "title": "AI in Building Energy Management",
        "slug": "ai-energy-management",
        "highlight_terms": "BEMS, LSTM, Predictive Maintenance, Demand Response, Occupancy Control, Reinforcement Learning",
        "formulae": [
            "ŷ_t = f(x_{t-24}, x_{t-1}, T_outdoor, occupancy_t) — 24-hour ahead load forecast (LSTM)",
            "Q(s,a) ← Q(s,a) + α[r + γ·max Q(s',a') − Q(s,a)] — RL HVAC control policy (Q-learning)",
            "Reconstruction error = ||x − x̂||² — autoencoder anomaly detection threshold for fault alerts",
        ],
        "left_page_points": [
            "Traditional BMS: fixed schedules, dead-band control, reactive alarms. ML-driven BEMS: continuous optimisation, predictive fault detection, adaptive setpoints.",
            "LSTM networks for time-series load and occupancy forecasting — captures daily/weekly/seasonal patterns.",
            "CNN for spatial feature extraction from thermal imagery and sensor grids — detects hot spots and airflow anomalies.",
            "Reinforcement Learning (PPO, DQN) for optimal HVAC setpoint policy — learns from building thermal response.",
            "Demand response: shift cooling load to off-peak, reduce peak kW by 15–30% without comfort sacrifice.",
            "Fault detection: autoencoder reconstruction error > threshold → maintenance alert before equipment failure.",
        ],
        "right_page_diagram_desc": (
            "Block diagram: 'Sensors (T, RH, CO₂, occupancy) → Edge Gateway → BEMS Cloud → ML Inference Engine → HVAC Actuator Control'. "
            "Feedback loop arrow: 'measured energy use → model retraining → updated policy → improved efficiency'."
        ),
        "comparison_table": (
            "Aspect | Traditional BMS | ML-driven BEMS. Rows: Control Method (Fixed schedule vs Continuous optimisation), "
            "Fault Detection (Threshold alarms vs Anomaly auto-detection), "
            "Energy Saving (Baseline vs 15-30% reduction), "
            "Occupancy Response (None vs Real-time adaptive), "
            "Maintenance (Reactive vs Predictive)"
        ),
        "sources": "Senthil Kumar et al. 2026, Chou & Bui 2014, Villano et al. 2024, Ahmed & Kumar 2018",
    },
}


def main():
    xai_key = get_xai_key()
    if not xai_key:
        print("❌ XAI_API_KEY not set and not found in ~/.config/last30days/.env")
        print("   Set it: export XAI_API_KEY='xai-...'")
        return 1

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    topics = TOPICS.copy()

    # CLI override: python hero_generator.py "Title" slug
    if len(sys.argv) >= 3:
        title = sys.argv[1]
        slug = sys.argv[2]
        topics = {slug: {"title": title, "slug": slug, "highlight_terms": "", "formulae": [],
                         "left_page_points": [title], "right_page_diagram_desc": "system diagram",
                         "comparison_table": "comparison", "sources": "sources"}}

    for key, topic in topics.items():
        print(f"📝 {topic['title']}")
        prompt = build_logbook_prompt(topic)
        path = ASSETS_DIR / f"hero-{topic['slug']}-logbook.png"
        generate(prompt, path)
        time.sleep(0.5)
        print()

    print(f"✅ Done. Output: {ASSETS_DIR}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())

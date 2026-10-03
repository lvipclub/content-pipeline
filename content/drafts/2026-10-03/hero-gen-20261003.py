#!/usr/bin/env python3
"""hero-gen-20261003.py — Northstar hero: economiser-free-cooling (mascot mode, Type A whiteboard lecture).

Route: xAI fallback (FAL edit route broken on the Nous proxy — xinca-ip-hero-images pitfall,
409 idempotency CONFLICT + file_download_error on local reference paths).
Identity-locked via .ip-assets/characters/bro-woo-inu-faa/character-reference-clean.png (confirmed, rev 1).
Run with: ~/.hermes/hermes-agent/venv/bin/python3 from ~/.hermes/hermes-agent (repo root).
"""
import json, os, shutil, sys, urllib.request

sys.path.insert(0, "/Users/marcsir/.hermes/hermes-agent")
from hermes_cli.plugins import _ensure_plugins_discovered
from agent.image_gen_registry import get_provider

HERE = os.path.dirname(os.path.abspath(__file__))
PROMPT = open(os.path.join(HERE, "hero-prompt.txt"), encoding="utf-8").read()
REF = "/Users/marcsir/workspace/content-pipeline/.ip-assets/characters/bro-woo-inu-faa/character-reference-clean.png"
ASSET = "/Users/marcsir/workspace/content-pipeline/content/assets/hero-economiser-free-cooling-2026-10-03.png"

_ensure_plugins_discovered(force=True)
p = get_provider("xai")
res = p.generate(prompt=PROMPT, aspect_ratio="landscape", reference_image_urls=[REF])
print("result keys:", sorted(res.keys()))
img = res.get("image")
url = res.get("public_url") or (img if isinstance(img, str) else "")
print("url:", url)

if isinstance(img, str) and os.path.exists(img):
    data = open(img, "rb").read()
    print("source: local file from provider:", img)
else:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = urllib.request.urlopen(req, timeout=90).read()
    print("source: downloaded from url")

raw = os.path.join(HERE, "hero-raw.bin")
open(raw, "wb").write(data)
print("raw bytes:", len(data))

json.dump({"provider": "xai", "model": "grok-imagine-image-quality (edits route via reference)",
           "url": url, "raw_bytes": len(data), "reference": REF, "aspect": "landscape",
           "style_mode": "mascot"},
          open(os.path.join(HERE, "hero-gen-result.json"), "w"), indent=1)

# xAI serves JPEG bytes under .png URLs — convert to real PNG via sips.
r = os.system(f"/usr/bin/sips -s format png '{raw}' --out '{ASSET}' >/dev/null 2>&1")
ok = os.path.exists(ASSET) and os.path.getsize(ASSET) > 10000
print("sips rc:", r, "| asset:", ASSET, os.path.getsize(ASSET) if os.path.exists(ASSET) else "MISSING")
print("HERO_OK" if ok else "HERO_FAIL")

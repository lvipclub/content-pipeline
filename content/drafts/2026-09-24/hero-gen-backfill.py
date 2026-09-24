#!/usr/bin/env python3
"""hero-gen-backfill.py — generate a hero from an existing prompt file (backfill Sep 21 set).
Usage: hero-gen-backfill.py <prompt_file> <output_png>"""
import json, os, sys

sys.path.insert(0, "/Users/marcsir/.hermes/hermes-agent")

if not os.environ.get("XAI_API_KEY"):
    for ln in open(os.path.expanduser("~/.hermes/.env")):
        if ln.startswith("XAI_API_KEY="):
            os.environ["XAI_API_KEY"] = ln.split("=", 1)[1].strip().strip('"').strip("'")
            break
if not os.environ.get("XAI_API_KEY"):
    raise SystemExit("no XAI_API_KEY")

from hermes_cli.plugins import _ensure_plugins_discovered
from agent.image_gen_registry import get_provider

_ensure_plugins_discovered(force=True)
p = get_provider("xai")

prompt_file, out_png = sys.argv[1], sys.argv[2]
prompt = open(prompt_file).read()

res = p.generate(
    prompt=prompt,
    aspect_ratio="landscape",
    reference_image_urls=["/Users/marcsir/workspace/content-pipeline/.ip-assets/characters/bro-woo-inu-faa/character-reference-clean.png"],
)

with open(out_png + ".result.json", "w") as f:
    json.dump(res, f, indent=1, ensure_ascii=False, default=str)
print("IMAGE_URL:", res.get("image") or res.get("public_url"))

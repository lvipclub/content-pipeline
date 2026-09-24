#!/usr/bin/env python3
"""hero-gen-20260924.py — xAI grok-imagine fallback for the Northstar hero (identity-locked route,
verified 2026-08-10 / 2026-09-17 / 2026-09-19; the default FAL edit route fails on the Nous proxy)."""
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

prompt = open(os.path.expanduser(
    "~/workspace/content-pipeline/content/drafts/2026-09-24/hero-prompt.txt")).read()

res = p.generate(
    prompt=prompt,
    aspect_ratio="landscape",
    reference_image_urls=["/Users/marcsir/workspace/content-pipeline/.ip-assets/characters/bro-woo-inu-faa/character-reference-clean.png"],
)

out = os.path.expanduser("~/workspace/content-pipeline/content/drafts/2026-09-24/hero-gen-result.json")
with open(out, "w") as f:
    json.dump(res, f, indent=1, ensure_ascii=False, default=str)
img = res.get("image") or res.get("public_url")
print("IMAGE_URL:", img)
print("result keys:", list(res.keys()))

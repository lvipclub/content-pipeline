#!/usr/bin/env python3
"""Hero image via OpenRouter fallback WITH reference images (mascot identity lock).
Usage: northstar-20260914-hero.py PROMPT_FILE OUT_PNG [REF1 REF2 ...]
"""
import json, os, shutil, sys

PROMPT_FILE, OUT_PNG = sys.argv[1], sys.argv[2]
REFS = sys.argv[3:]

envp = os.path.expanduser("~/.hermes/.env")
for line in open(envp, encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    k, v = line.split("=", 1)
    os.environ.setdefault(k.strip(), v.strip())
os.environ.setdefault("HERMES_HOME", os.path.expanduser("~/.hermes"))

sys.path.insert(0, os.path.expanduser("~/.hermes/hermes-agent"))
os.chdir(os.path.expanduser("~/.hermes/hermes-agent"))

from hermes_cli.plugins import _ensure_plugins_discovered
_ensure_plugins_discovered(force=True)
from agent.image_gen_registry import get_provider

prompt = open(PROMPT_FILE, encoding="utf-8").read().strip()
kwargs = {"resolution": "2K"}
if REFS:
    kwargs["reference_image_urls"] = REFS

res = get_provider("openrouter").generate(
    prompt=prompt,
    aspect_ratio="landscape",
    model="qwen/qwen-image-3-pro",
    **kwargs)

print("SUCCESS:", res.get("success"))
print("IMAGE:", res.get("image"))
print("COST_USD:", res.get("cost_usd"))
print("ERROR:", res.get("error"))
if res.get("success") and res.get("image"):
    shutil.copy(res["image"], OUT_PNG)
    print("SAVED:", OUT_PNG)
else:
    print("FULL:", json.dumps(res, default=str)[:1500])
    sys.exit(1)

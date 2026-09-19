#!/usr/bin/env python3
"""Hero via xAI grok-imagine fallback (verified 2026-09-10 recipe) WITH reference images.
Usage: northstar-20260917-hero-xai.py PROMPT_FILE OUT_PNG [REF1 ...]"""
import importlib, json, os, shutil, subprocess, sys

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

p = get_provider("xai")
# 2K resolution is config-only -> monkeypatch (skill recipe)
mod = importlib.import_module(type(p).__module__)
mod._resolve_resolution = lambda: "2k"

prompt = open(PROMPT_FILE, encoding="utf-8").read().strip()
kwargs = {}
if REFS:
    kwargs["reference_image_urls"] = REFS
res = p.generate(prompt=prompt, aspect_ratio="landscape", **kwargs)

print("SUCCESS:", res.get("success"))
print("IMAGE:", res.get("image"))
print("PUBLIC_URL:", res.get("public_url"))
print("COST_USD:", res.get("cost_usd"))
print("ERROR:", res.get("error"))

img = res.get("image") or res.get("public_url")
if res.get("success") and img:
    tmp = "/tmp/northstar-hero-xai-raw"
    if img.startswith("http"):
        # files-cdn.x.ai blocks urllib -> curl (skill recipe)
        rc = subprocess.run(["curl", "-sL", "-m", "120", "-o", tmp, img]).returncode
        if rc != 0:
            print("CURL FAILED rc=", rc); sys.exit(1)
    else:
        shutil.copy(img, tmp)
    # xAI serves JPEG bytes under .png names -> normalise with sips
    rc = subprocess.run(["sips", "-s", "format", "png", tmp, "--out", OUT_PNG],
                        capture_output=True, text=True)
    if rc.returncode != 0:
        print("SIPS FAILED:", rc.stderr[:300]); sys.exit(1)
    print("SAVED:", OUT_PNG)
else:
    print("FULL:", json.dumps(res, default=str)[:1500])
    sys.exit(1)

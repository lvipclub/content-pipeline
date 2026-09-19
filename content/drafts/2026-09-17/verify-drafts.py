#!/usr/bin/env python3
"""Pre-validate 2026-09-17 drafts against northstar-publish.py constraints."""
import os, re, subprocess, sys

PIPE = os.path.expanduser("~/workspace/content-pipeline")
D = f"{PIPE}/content/drafts/2026-09-17"
CHECK = os.path.expanduser("~/.hermes/skills/social-media/content-auto-poster-ops/scripts/check-post-text.py")

def extract_section(text, header_prefix="## Post"):
    lines = text.splitlines()
    out, on = [], False
    for ln in lines:
        if not on and ln.strip().startswith(header_prefix):
            on = True; continue
        if on:
            if ln.strip() == "---": break
            out.append(ln)
    return "\n".join(out).strip()

def x_weight(t):
    urls = re.findall(r"https?://\S+|(?<![\w@/.])[a-z0-9-]+(?:\.[a-z0-9-]+)+/\S*", t)
    return len(t) - sum(max(0, len(u) - 23) for u in urls)

tg = extract_section(open(f"{D}/telegram-hvaccontrols-hvac-retrofit-payback-2026-09-17.md").read())
x_full = open(f"{D}/x-woofaasocial-hvac-retrofit-payback-2026-09-17.md").read()
x_text = extract_section(x_full)
li = extract_section(open(f"{D}/linkedin-hvac-retrofit-payback-2026-09-17.md").read())

print(f"tg_len={len(tg)} (limit 1024) -> {'OK' if len(tg) <= 1024 else 'OVER'}")
print(f"x_raw={len(x_text)} x_weight={x_weight(x_text)} (limit 280) -> {'OK' if x_weight(x_text) <= 280 else 'OVER'}")
print(f"li_len={len(li)} (limit 3000) -> {'OK' if len(li) <= 3000 else 'OVER'}")

# fallback variant weight (informational)
fb = []
on = False
for ln in x_full.splitlines():
    if "Fallback (URL-free" in ln: on = True; continue
    if on:
        if ln.strip() == "---": break
        fb.append(ln)
fb_text = "\n".join(fb).strip()
print(f"x_fallback_raw={len(fb_text)} x_fallback_weight={x_weight(fb_text)}")

for label, t in (("x", x_text), ("x-fallback", fb_text), ("tg", tg)):
    tmp = f"/tmp/ns-check-{label}.txt"
    open(tmp, "w").write(t)
    r = subprocess.run(["python3", CHECK, tmp], capture_output=True, text=True)
    print(f"escape-gate {label}: rc={r.returncode} {r.stdout.strip()[:200]}{r.stderr.strip()[:200]}")

if len(tg) > 1024 or x_weight(x_text) > 280 or len(li) > 3000:
    sys.exit(1)
print("ALL CONSTRAINTS OK")

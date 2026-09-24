#!/usr/bin/env python3
"""gen-20260924.py — call Havi Dify app via SSH tunnel (Northstar run 2026-09-24, Thu).
Usage: gen-20260924.py <platform>   (telegram | x | linkedin)"""
import json, os, sys, time, urllib.request

ENV = os.path.expanduser("~/.hermes/config/dify-local.env")
key = None
for ln in open(ENV):
    if ln.startswith("DIFY_HAVI_APP_KEY="):
        key = ln.split("=", 1)[1].strip().strip('"').strip("'")
if not key:
    sys.exit("no DIFY_HAVI_APP_KEY")

TOPIC = ("IAQ cluster — CO₂-based demand-controlled ventilation (DCV): CO₂ as an occupancy "
         "proxy; NDIR sensor accuracy, drift and placement; occupancy-based outdoor-air reset vs "
         "fixed ventilation schedules; ASHRAE 62.1 DCV requirements; typical 800–1,100 ppm control "
         "band context; energy trade-off in humid climates; classroom and open-plan office use "
         "cases. Distinct from Sep 10 run (PM2.5 filtration — particulate, not CO₂/ventilation). "
         "Audience: specifiers, consultants, facility managers.")
BRIEF = ""

platform = sys.argv[1]

def call():
    body = json.dumps({
        "inputs": {"topic": TOPIC, "platform": platform, "research_brief": BRIEF},
        "query": TOPIC if platform == "telegram" else f"Write the {platform} post. Topic: {TOPIC}",
        "response_mode": "blocking", "user": "havi-northstar-cron-20260924",
    }).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:18081/v1/chat-messages", data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=150) as r:
        data = json.loads(r.read())
    ans = (data.get("answer") or "").strip()
    with open(f"raw-{platform}.json", "w") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    print(f"[{platform}] OK in {time.time()-t0:.0f}s, answer {len(ans)} chars", flush=True)
    return ans

log = open("dify-run.log", "a")
ans = None
for attempt in (1, 2):
    try:
        print(f"[{platform}] call attempt {attempt} ...", flush=True)
        log.write(f"[{platform}] call attempt {attempt} ...\n"); log.flush()
        ans = call()
        break
    except Exception as e:
        print(f"[{platform}] attempt {attempt} failed: {str(e)[:200]}", flush=True)
        log.write(f"[{platform}] attempt {attempt} failed: {str(e)[:200]}\n"); log.flush()
        time.sleep(8 * attempt)
if ans:
    with open(f"dify-{platform}.txt", "w") as f:
        f.write(ans)
    log.write(f"[{platform}] DONE\n")

#!/usr/bin/env python3
"""gen-20260919.py — call Havi Dify app via SSH tunnel (Northstar run 2026-09-19, Sat).
Usage: gen-20260919.py <platform>   (telegram | x | linkedin)"""
import json, os, sys, time, urllib.request

ENV = os.path.expanduser("~/.hermes/config/dify-local.env")
key = None
for ln in open(ENV):
    if ln.startswith("DIFY_HAVI_APP_KEY="):
        key = ln.split("=", 1)[1].strip().strip('"').strip("'")
if not key:
    sys.exit("no DIFY_HAVI_APP_KEY")

TOPIC = ("Data centre cooling cluster - aisle containment retrofits: airflow management for "
         "existing raised-floor halls. Cover: hot-aisle vs cold-aisle containment economics and "
         "retrofit constraints; where containment savings come from (CRAH fan energy, higher "
         "supply-air temperatures, chiller efficiency); blanking panels, brush grommets and floor "
         "cutout sealing as the cheap first dollars; matching CRAH airflow to IT load with fan "
         "speed control; verification with rack-inlet temperature sensors against the ASHRAE "
         "TC 9.9 envelope. Distinct from prior runs: Sep 5 = data-centre liquid cooling; "
         "Sep 17 = HVAC retrofit payback (energy-efficiency cluster); Sep 14 = VAV airflow "
         "measurement (air-side). Audience: specifiers, consultants, facility managers.")
BRIEF = ""

platform = sys.argv[1]

def call():
    body = json.dumps({
        "inputs": {"topic": TOPIC, "platform": platform, "research_brief": BRIEF},
        "query": TOPIC if platform == "telegram" else f"Write the {platform} post. Topic: {TOPIC}",
        "response_mode": "blocking", "user": "havi-northstar-cron-20260919",
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
else:
    log.write(f"[{platform}] FAILED all attempts\n")
log.close()
print("DONE" if ans else "FAILED")
sys.exit(0 if ans else 1)

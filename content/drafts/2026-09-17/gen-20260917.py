#!/usr/bin/env python3
"""gen-20260917.py — call Havi Dify app 3x via SSH tunnel (Northstar run 2026-09-17, Thu)."""
import json, os, sys, time, urllib.request

ENV = os.path.expanduser("~/.hermes/config/dify-local.env")
key = None
for ln in open(ENV):
    if ln.startswith("DIFY_HAVI_APP_KEY="):
        key = ln.split("=", 1)[1].strip().strip('"').strip("'")
if not key:
    sys.exit("no DIFY_HAVI_APP_KEY")

TOPIC = ("Energy efficiency cluster - retrofit payback: where the savings actually are when "
         "upgrading an ageing HVAC plant. Cover: retro-commissioning (RCx) and controls sequence "
         "fixes as first-dollar leverage; the retrofit vs equipment-replacement decision (simple "
         "payback, remaining useful life, when replacement wins); monitoring-based commissioning "
         "and M&V with submetering so savings persist after handover; how codes (ASHRAE 90.1 / "
         "local building energy codes) raise the retrofit baseline. Distinct from prior runs: "
         "Sep 14 = VAV airflow measurement (air-side); Sep 12 = variable-flow pumping (water-side) "
         "and data-centre liquid cooling. Audience: specifiers, consultants, facility managers.")
BRIEF = ""

def call(platform):
    body = json.dumps({
        "inputs": {"topic": TOPIC, "platform": platform, "research_brief": BRIEF},
        "query": TOPIC if platform == "telegram" else f"Write the {platform} post. Topic: {TOPIC}",
        "response_mode": "blocking", "user": "havi-northstar-cron-20260917",
    }).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:18081/v1/chat-messages", data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=280) as r:
        data = json.loads(r.read())
    ans = (data.get("answer") or "").strip()
    with open(f"raw-{platform}.json", "w") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    print(f"[{platform}] OK in {time.time()-t0:.0f}s, answer {len(ans)} chars", flush=True)
    return ans

log = open("dify-run.log", "a")
outs = {}
for p in ("telegram", "x", "linkedin"):
    ans = None
    for attempt in (1, 2, 3):
        try:
            print(f"[{p}] call attempt {attempt} ...", flush=True)
            log.write(f"[{p}] call attempt {attempt} ...\n"); log.flush()
            ans = call(p)
            break
        except Exception as e:
            print(f"[{p}] attempt {attempt} failed: {str(e)[:200]}", flush=True)
            log.write(f"[{p}] attempt {attempt} failed: {str(e)[:200]}\n"); log.flush()
            time.sleep(8 * attempt)
    if ans:
        outs[p] = ans
        with open(f"dify-{p}.txt", "w") as f:
            f.write(ans)
    else:
        log.write(f"[{p}] FAILED all attempts\n"); log.flush()
log.write("ALL DONE\n" if len(outs) == 3 else f"PARTIAL: {list(outs)}\n")
log.close()
print("ALL DONE" if len(outs) == 3 else f"PARTIAL: {list(outs)}")

#!/usr/bin/env python3
"""Northstar pipeline 2026-09-14: air-side VAV airflow measurement, 3 platforms."""
import json, os, sys, urllib.request, urllib.error

KEY = None
for envfile in [os.path.expanduser('~/.hermes/config/dify-local.env'), os.path.expanduser('~/.hermes/.env')]:
    try:
        for line in open(envfile):
            if line.startswith('DIFY_HAVI_APP_KEY='):
                KEY = line.strip().split('=', 1)[1].strip().strip('"').strip("'")
                break
    except FileNotFoundError:
        pass
    if KEY:
        break

TOPIC = "VAV airflow measurement - sensor types (pitot, ultrasonic, thermal dispersion), k-factor errors, and why installed accuracy differs from datasheet accuracy"
DATE = "2026-09-14"
OUT = os.path.expanduser(f'~/workspace/content-pipeline/content/drafts/{DATE}')
os.makedirs(OUT, exist_ok=True)

def call_dify(platform):
    body = json.dumps({
        "inputs": {"topic": TOPIC, "platform": platform, "research_brief": ""},
        "query": f"Generate a {platform} post about: {TOPIC}",
        "response_mode": "blocking",
        "user": "havi-northstar-cron",
        "mode": "chatbot"
    }).encode()
    req = urllib.request.Request("http://127.0.0.1:18081/v1/chat-messages", data=body,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=280) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"http_error": e.code, "body": e.read().decode()[:500]}
    except Exception as e:
        return {"error": str(e)}

results = {}
for platform in ["telegram", "x", "linkedin"]:
    print(f"=== calling dify for {platform} ===", flush=True)
    resp = call_dify(platform)
    with open(f"{OUT}/raw-{platform}.json", "w") as f:
        json.dump(resp, f, indent=2, ensure_ascii=False)
    if "answer" in resp:
        results[platform] = resp["answer"]
        print(f"OK {platform}: {len(resp['answer'])} chars", flush=True)
    else:
        print(f"FAIL {platform}: {json.dumps(resp)[:300]}", flush=True)
        results[platform] = None

with open(f"{OUT}/dify-results.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print("\nDONE. Saved to", OUT)
for p, a in results.items():
    print(f"  {p}: {'OK' if a else 'MISSING'} ({len(a) if a else 0} chars)")

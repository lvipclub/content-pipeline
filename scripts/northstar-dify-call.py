#!/usr/bin/env python3
"""Northstar pipeline: call Havi Dify app for 3 platforms."""
import json, os, sys, glob, urllib.request, urllib.error

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

if not KEY:
    print("FATAL: no DIFY_HAVI_APP_KEY found"); sys.exit(1)
print(f"key_len={len(KEY)}")

def call_dify(topic, platform, brief=""):
    body = json.dumps({
        "inputs": {"topic": topic, "platform": platform, "research_brief": brief},
        "query": f"Generate a {platform} post about: {topic}",
        "response_mode": "blocking",
        "user": "havi-northstar-cron",
        "mode": "chatbot"
    }).encode()
    req = urllib.request.Request("http://127.0.0.1:18081/v1/chat-messages", data=body,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"http_error": e.code, "body": e.read().decode()[:500]}
    except Exception as e:
        return {"error": str(e)}

# Topic history from recent drafts
print("\n--- Topic history (recent draft dirs) ---")
for d in sorted(glob.glob(os.path.expanduser('~/workspace/content-pipeline/content/drafts/2026-*')), reverse=True)[:10]:
    slugs = set()
    for f in os.listdir(d):
        for plat in ('telegram-', 'x-', 'linkedin-'):
            if f.startswith(plat) and f.endswith('.md'):
                slugs.add(f[len(plat):-3])
    print(os.path.basename(d), '->', slugs or os.listdir(d)[:6])

topic = sys.argv[1] if len(sys.argv) > 1 else "ping test"
platform = sys.argv[2] if len(sys.argv) > 2 else "telegram"
resp = call_dify(topic, platform)
print("\n--- Dify call ---")
if "answer" in resp:
    print("OK, answer length:", len(resp["answer"]))
    print(resp["answer"][:600])
else:
    print(json.dumps(resp)[:800])

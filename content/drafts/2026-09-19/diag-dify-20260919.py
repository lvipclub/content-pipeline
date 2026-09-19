#!/usr/bin/env python3
"""diag-dify-20260919.py — capture the 400 body from the Havi Dify app + /info + /parameters."""
import json, os, urllib.request, urllib.error

ENV = os.path.expanduser("~/.hermes/config/dify-local.env")
key = None
for ln in open(ENV):
    if ln.startswith("DIFY_HAVI_APP_KEY="):
        key = ln.split("=", 1)[1].strip().strip('"').strip("'")
if not key:
    raise SystemExit("no key")

BASE = "http://127.0.0.1:18081/v1"

def get(path):
    req = urllib.request.Request(f"{BASE}{path}", headers={"Authorization": f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read().decode()[:1500]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:1500]
    except Exception as e:
        return None, str(e)[:300]

def post(body):
    req = urllib.request.Request(f"{BASE}/chat-messages", data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return r.status, r.read().decode()[:1200]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:1200]
    except Exception as e:
        return None, str(e)[:300]

print("== /info ==")
print(get("/info"))
print("== /parameters (input schema) ==")
print(get("/parameters"))
print("== POST full payload ==")
b1 = {"inputs": {"topic": "test topic", "platform": "telegram", "research_brief": ""},
      "query": "test", "response_mode": "blocking", "user": "diag"}
print(post(b1))
print("== POST minimal ==")
print(post({"inputs": {}, "query": "ping", "response_mode": "blocking", "user": "diag"}))

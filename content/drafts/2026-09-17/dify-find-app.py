#!/usr/bin/env python3
"""List Dify apps on the VPS via console API (tunnel 18081) — find the HVAC Content Generator app."""
import json, os, sys, urllib.request

ENV = os.path.expanduser("~/.hermes/config/dify-local.env")
vals = {}
for ln in open(ENV):
    ln = ln.strip()
    if ln and not ln.startswith("#") and "=" in ln:
        k, v = ln.split("=", 1)
        vals[k.strip()] = v.strip().strip('"').strip("'")

email, pw = vals.get("DIFY_LOCAL_EMAIL"), vals.get("DIFY_LOCAL_PASSWORD")
BASE = "http://127.0.0.1:18081"

# login
body = json.dumps({"email": email, "password": pw, "remember_me": True}).encode()
req = urllib.request.Request(f"{BASE}/console/api/login", data=body,
                             headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=30) as r:
    tok = json.loads(r.read())
access = tok.get("data", tok).get("access_token") or tok.get("access_token")
print("LOGIN OK, token len:", len(access or ""))

hdr = {"Authorization": f"Bearer {access}"}
# list apps (paginated)
apps = []
page = 1
while page <= 5:
    req = urllib.request.Request(f"{BASE}/console/api/apps?page={page}&limit=30", headers=hdr)
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    items = data.get("data", [])
    apps.extend(items)
    if len(items) < 30:
        break
    page += 1

print(f"TOTAL APPS: {len(apps)}")
for a in apps:
    print(f"- {a.get('name')} | mode={a.get('mode')} | id={a.get('id')}")

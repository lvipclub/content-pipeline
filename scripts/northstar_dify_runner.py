#!/usr/bin/env python3
"""Northstar run helper — call the Havi Dify App for all three platforms.

NOTE: the Dify app currently ignores `inputs` (user_input_form: []), so the
topic + platform are embedded in the `query` string. `inputs` are still sent
(harmless) for forward-compatibility.

Usage: northstar_dify_runner.py <topic> <out_dir> [platform ...]
Writes raw-<platform>.json into <out_dir> as each call completes.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

TUNNEL = "http://127.0.0.1:18081"

PLATFORM_PROMPT = {
    "telegram": (
        "Platform: Telegram — channel broadcast for @hvaccontrols. "
        "Audience: specifiers, consultants, facility managers (decision-maker voice). "
        "Write the post caption (hard limit 1024 characters), no emoji, Australian English. "
        "Open with the market/engineering insight, not a summary of a document. "
        "Then include a short hero-image prompt describing ONE clear visual scene for this post."
    ),
    "x": (
        "Platform: X (Twitter) — one post for @WoofaaSocial (IAQ / healthy buildings lane). "
        "Audience: IAQ professionals, WELL consultants, facility engineers (practitioner voice). "
        "Under 280 characters, no emoji, Australian English. One punchy hook and one concrete fact."
    ),
    "linkedin": (
        "Platform: LinkedIn — Company Page long-form post. "
        "Audience: professional network, brand authority (analyst voice, data-backed, citation-heavy). "
        "Write the post (roughly 1200-2500 characters), no emoji, Australian English."
    ),
}


def load_key() -> str:
    for path in (os.path.expanduser("~/.hermes/config/dify-local.env"),
                 os.path.expanduser("~/.hermes/.env")):
        try:
            with open(path) as fh:
                for line in fh:
                    m = re.match(r"\s*DIFY_HAVI_APP_KEY\s*=\s*(\S+)", line)
                    if m:
                        return m.group(1)
        except FileNotFoundError:
            continue
    sys.exit("DIFY_HAVI_APP_KEY not found")


def call(platform: str, topic: str, key: str) -> dict:
    query = f"{PLATFORM_PROMPT[platform]}\n\nTopic: {topic}\n\nGenerate the post now."
    body = {
        "inputs": {"topic": topic, "platform": platform, "research_brief": ""},
        "query": query,
        "response_mode": "blocking",
        "user": "northstar-havi",
    }
    req = urllib.request.Request(
        f"{TUNNEL}/v1/chat-messages",
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=420) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    topic = sys.argv[1]
    out_dir = sys.argv[2]
    platforms = sys.argv[3:] or ["telegram", "x", "linkedin"]
    key = load_key()
    os.makedirs(out_dir, exist_ok=True)
    for p in platforms:
        if os.path.exists(os.path.join(out_dir, f"raw-{p}.json")):
            print(f"[{p}] already present, skipping", flush=True)
            continue
        for attempt in (1, 2):
            t0 = time.time()
            print(f"[{p}] call attempt {attempt} ...", flush=True)
            try:
                data = call(p, topic, key)
                with open(os.path.join(out_dir, f"raw-{p}.json"), "w") as fh:
                    json.dump(data, fh, ensure_ascii=False, indent=2)
                print(f"[{p}] OK in {time.time()-t0:.0f}s, answer {len(data.get('answer',''))} chars", flush=True)
                break
            except urllib.error.HTTPError as e:
                print(f"[{p}] HTTP {e.code}: {e.read().decode('utf-8','replace')[:300]}", flush=True)
            except Exception as e:  # noqa: BLE001
                print(f"[{p}] ERR: {e} ({time.time()-t0:.0f}s)", flush=True)
            if attempt == 1:
                time.sleep(15)
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    main()

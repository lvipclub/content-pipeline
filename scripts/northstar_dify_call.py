#!/usr/bin/env python3
"""Call the Havi Dify App (VPS, via SSH tunnel 127.0.0.1:18081) for Northstar HVAC content.

Usage: northstar_dify_call.py <platform> <topic> [research_brief]
  platform: telegram | x | linkedin
Prints the full JSON answer (or error JSON) to stdout.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request

TUNNEL = "http://127.0.0.1:18081"


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


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    platform = sys.argv[1]
    topic = sys.argv[2]
    brief = sys.argv[3] if len(sys.argv) > 3 else ""

    key = load_key()
    body = {
        "inputs": {
            "topic": topic,
            "platform": platform,
            "research_brief": brief,
        },
        "query": "Generate the post",
        "response_mode": "blocking",
        "user": "northstar-havi",
    }
    req = urllib.request.Request(
        f"{TUNNEL}/v1/chat-messages",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        print(json.dumps({"error": f"HTTP {e.code}", "detail": e.read().decode("utf-8", "replace")},
                         ensure_ascii=False))
        sys.exit(1)
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()

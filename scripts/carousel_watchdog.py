#!/usr/bin/env python3
"""
Watchdog for Carousel Article Pipeline
Checks if pipeline is stuck and alerts if >2h since last Dify call without completion.

Usage (cron): python3 carousel_watchdog.py
Silent exit 0 when everything is fine. Outputs alert message on stuck pipeline.
"""
import json
import os
import sys
from typing import Optional
import time
import urllib.request
from datetime import datetime, timezone

STATE_FILE = os.path.expanduser("~/workspace/content-pipeline/state/carousel-pipeline.json")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
TG_ALERT_TARGET = os.environ.get("TG_ALERT_TARGET", "@hvaccontrols")
if not TG_BOT_TOKEN:
    print("TG_BOT_TOKEN env var not set - cannot send alerts")
    sys.exit(1)
STUCK_THRESHOLD_HOURS = 2


def load_state() -> Optional[dict]:
    if not os.path.exists(STATE_FILE):
        return None
    with open(STATE_FILE) as f:
        return json.load(f)


def send_tg_alert(message: str):
    """Send alert to Marc Sir via Telegram."""
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_ALERT_TARGET,
        "text": f"⚠️ Carousel Pipeline Alert\n\n{message}",
    }
    data = json.dumps(payload).encode()
    try:
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
            if result.get("ok"):
                print(f"Alert sent: {message[:80]}")
                return True
    except Exception as e:
        print(f"Alert failed: {e}")
    return False


def main():
    state = load_state()
    if not state:
        print("No state file — pipeline has never run")
        return

    steps = state.get("steps", {})
    dify_at = steps.get("dify_called", {}).get("at")
    deployed = steps.get("deployed", {}).get("done", False)
    topic = state.get("topic", "unknown")

    if deployed:
        print(f"Pipeline completed successfully for: {topic}")
        return

    if not dify_at:
        print("No Dify call timestamp — state file may be corrupted")
        return

    # Calculate hours since last activity
    try:
        last_at = datetime.fromisoformat(dify_at)
        now = datetime.now(timezone.utc)
        hours_since = (now - last_at).total_seconds() / 3600
    except Exception:
        print("Could not parse timestamp")
        return

    if hours_since < STUCK_THRESHOLD_HOURS:
        print(f"Pipeline in progress ({hours_since:.1f}h) — within threshold")
        return

    # Find the stuck step
    stuck_step = None
    for step_name, step_data in steps.items():
        if not step_data.get("done", False):
            stuck_step = step_name
            break

    artifacts = state.get("artifacts", {})
    slug = state.get("slug", "unknown")

    if stuck_step:
        message = (
            f"Pipeline stuck for {topic!r} (slug: {slug})\n"
            f"Stuck at step: {stuck_step}\n"
            f"Hours since Dify call: {hours_since:.1f}h\n"
            f"Manual check: {STATE_FILE}"
        )
        print(message)
        send_tg_alert(message)
    else:
        print(f"All steps complete but deploy not confirmed ({hours_since:.1f}h)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Watchdog for Carousel Article Pipeline — consolidated cron member.

Checks if the pipeline is stuck (Dify called but no deploy >2h later).
SILENT when healthy — prints ONLY when the pipeline is stuck.
Alert delivery is handled by the parent cron's delivery (no bot token needed).
Exit 0 always — no_agent cron semantics: empty stdout = silent.
"""
import json
import os
from typing import Optional
from datetime import datetime, timezone

STATE_FILE = os.path.expanduser("~/workspace/content-pipeline/state/carousel-pipeline.json")
STUCK_THRESHOLD_HOURS = 2


def load_state() -> Optional[dict]:
    if not os.path.exists(STATE_FILE):
        return None
    with open(STATE_FILE) as f:
        return json.load(f)


def main():
    state = load_state()
    if not state:
        return  # never ran — nothing to watch (silent)

    steps = state.get("steps", {})
    dify_at = steps.get("dify_called", {}).get("at")
    deployed = steps.get("deployed", {}).get("done", False)
    topic = state.get("topic", "unknown")

    if deployed or not dify_at:
        return  # completed, or no run in progress (silent)

    try:
        last_at = datetime.fromisoformat(dify_at)
        hours_since = (datetime.now(timezone.utc) - last_at).total_seconds() / 3600
    except Exception:
        return

    if hours_since < STUCK_THRESHOLD_HOURS:
        return  # in progress (silent)

    stuck_step = next((n for n, s in steps.items() if not s.get("done", False)), None)
    slug = state.get("slug", "unknown")

    print(f"🔴 Carousel pipeline stuck for {topic!r} (slug: {slug})")
    print(f"   Stuck at step: {stuck_step}")
    print(f"   Hours since Dify call: {hours_since:.1f}h")
    print(f"   State: {STATE_FILE}")


if __name__ == "__main__":
    main()

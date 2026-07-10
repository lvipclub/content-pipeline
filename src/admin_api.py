"""
admin_api.py — Content Pipeline Admin API Server
Serves the web admin dashboard API for article approval, scheduling, and publishing.
Replaces prior review_cron.py (TG-based approval).
Port: 8420 for localhost access only.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

PIPELINE_DIR = Path(os.environ.get("PIPELINE_DIR", "/home/hermerr/workspace/content-pipeline"))
STATE_FILE = PIPELINE_DIR / ".pipeline_state.json"
PUBLISH_LOG = PIPELINE_DIR / ".publish_log.json"
CONFIG_FILE = PIPELINE_DIR / ".config.yaml"
ASSETS_DIR = PIPELINE_DIR / "content" / "assets"

def load_json(path):
    if path.exists():
        return json.loads(path.read_text())
    return {}

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    # Backup before write
    if path.exists():
        backup = path.with_suffix(".json.bak")
        backup.write_text(path.read_text())
    path.write_text(json.dumps(data, indent=2, default=str))

class AdminHandler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, data, status=200):
        body = json.dumps(data, default=str).encode()
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _error(self, msg, status=400):
        self._json({"error": msg}, status)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        # Serve admin dashboard HTML at root or /admin/
        if self.path in ("/", "/admin/", "/index.html"):
            return self._serve_html()
        elif self.path == "/api/drafts":
            return self._list_drafts()
        elif self.path == "/api/publish-log":
            return self._publish_log()
        elif self.path == "/api/pipeline-health":
            return self._pipeline_health()
        else:
            self._error("Not found", 404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length > 0 else {}

        if self.path == "/api/approve":
            return self._approve(body)
        elif self.path == "/api/reject":
            return self._reject(body)
        elif self.path == "/api/schedule":
            return self._schedule(body)
        elif self.path == "/api/linkedin-url":
            return self._linkedin_url(body)
        elif self.path == "/api/regen-image":
            return self._regen_image(body)
        elif self.path == "/api/dify-asin-check":
            return self._dify_asin_check(body)
        else:
            self._error("Not found", 404)

    # --- API methods ---

    def _list_drafts(self):
        state = load_json(STATE_FILE)
        drafts_dir = PIPELINE_DIR / "content" / "drafts"
        drafts = []
        if drafts_dir.exists():
            for f in sorted(drafts_dir.glob("*.md"), key=os.path.getmtime, reverse=True):
                slug = f.stem.replace("-draft", "")
                content = f.read_text()
                drafts.append({
                    "slug": slug,
                    "path": str(f),
                    "preview": content[:2000],
                    "full_text": content,
                    "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
                    "status": state.get(slug, {}).get("status", "pending_review"),
                    "platforms": state.get(slug, {}).get("target_platforms", []),
                    "thumbnail": f"/articles/hero-{slug}-logbook.png" if (ASSETS_DIR / f"hero-{slug}-logbook.png").exists() else None
                })
        self._json({"drafts": drafts, "count": len(drafts)})

    def _approve(self, body):
        slug = body.get("slug")
        auto_schedule = body.get("auto_schedule", False)
        if not slug:
            return self._error("slug required")

        draft = PIPELINE_DIR / "content" / "drafts" / f"{slug}-draft.md"
        approved = PIPELINE_DIR / "content" / "approved" / f"{slug}-draft.md"

        if not draft.exists():
            return self._error(f"Draft not found: {slug}")

        # Move to approved
        approved.write_text(draft.read_text())
        draft.unlink()

        # Update state
        state = load_json(STATE_FILE)
        state[slug] = state.get(slug, {})
        state[slug]["status"] = "approved"
        state[slug]["approved_at"] = datetime.now(timezone.utc).isoformat()
        state[slug]["approved_by"] = "admin_dashboard"

        # Auto-schedule: find next available slot
        next_slot = None
        if auto_schedule:
            now = datetime.now(timezone.utc)
            # Collect all existing scheduled times
            existing_times = []
            for s, v in state.items():
                sched = v.get("schedule", {})
                for p, t in sched.items():
                    try:
                        existing_times.append(datetime.fromisoformat(t))
                    except:
                        pass

            # Find next slot: HK hours 09-18, max 2 posts/day, min 3h apart
            # Simple algorithm: round up to nearest hour, then find gap
            candidate = now.replace(minute=0, second=0, microsecond=0)
            candidate = candidate.replace(hour=max(9, candidate.hour + 1))
            if candidate.hour > 18:
                candidate = candidate.replace(day=candidate.day + 1, hour=9)

            # Ensure 3h gap from last scheduled
            if existing_times:
                last = max(existing_times)
                if (candidate - last).total_seconds() < 10800:  # 3h
                    candidate = last + timedelta(hours=3)

            # Cap at 2 per day
            same_day = [t for t in existing_times if t.date() == candidate.date()]
            if len(same_day) >= 2:
                candidate = candidate.replace(day=candidate.day + 1, hour=9)

            state[slug]["schedule"] = {"x": candidate.isoformat(), "telegram": candidate.isoformat()}
            next_slot = candidate.isoformat()

        save_json(STATE_FILE, state)

        self._json({"ok": True, "slug": slug, "status": "approved", "next_slot": next_slot})

    def _reject(self, body):
        slug = body.get("slug")
        notes = body.get("notes", "")

        if not slug:
            return self._error("slug required")

        state = load_json(STATE_FILE)
        state[slug] = state.get(slug, {})
        state[slug]["status"] = "rejected"
        state[slug]["rejected_at"] = datetime.now(timezone.utc).isoformat()
        state[slug]["reject_notes"] = notes
        save_json(STATE_FILE, state)

        self._json({"ok": True, "slug": slug, "status": "rejected", "notes": notes})

    def _schedule(self, body):
        slug = body.get("slug")
        platform = body.get("platform")
        scheduled_at = body.get("scheduled_at")

        if not all([slug, platform, scheduled_at]):
            return self._error("slug, platform, scheduled_at required")

        state = load_json(STATE_FILE)
        state[slug] = state.get(slug, {})
        state[slug].setdefault("schedule", {})
        state[slug]["schedule"][platform] = scheduled_at
        save_json(STATE_FILE, state)

        self._json({"ok": True, "slug": slug, "platform": platform, "scheduled_at": scheduled_at})

    def _linkedin_url(self, body):
        slug = body.get("slug")
        url = body.get("url")

        if not all([slug, url]):
            return self._error("slug, url required")

        log = load_json(PUBLISH_LOG)
        log.setdefault(slug, {})
        log[slug]["linkedin_url"] = url
        log[slug]["linkedin_posted"] = datetime.now(timezone.utc).isoformat()
        save_json(PUBLISH_LOG, log)

        self._json({"ok": True, "slug": slug, "linkedin_url": url})

    def _publish_log(self):
        log = load_json(PUBLISH_LOG)
        self._json({"log": log})

    def _pipeline_health(self):
        state = load_json(STATE_FILE)
        drafts_dir = PIPELINE_DIR / "content" / "drafts"
        pending = len(list(drafts_dir.glob("*.md"))) if drafts_dir.exists() else 0

        approved = sum(1 for v in state.values() if v.get("status") == "approved")
        rejected = sum(1 for v in state.values() if v.get("status") == "rejected")
        published = sum(1 for v in state.values() if v.get("status") == "published")
        scheduled = sum(1 for v in state.values() if v.get("schedule", {}))

        self._json({
            "pending_drafts": pending,
            "approved_total": approved,
            "rejected_total": rejected,
            "published_total": published,
            "scheduled": scheduled,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

    def _regen_image(self, body):
        slug = body.get("slug", "")
        if not slug:
            return self._error("slug required")

        script = PIPELINE_DIR / "src" / "hero_generator.py"
        if not script.exists():
            return self._error("hero_generator.py not found", 500)

        try:
            result = subprocess.run(
                [sys.executable, str(script), slug.replace("-", " ").title(), slug],
                capture_output=True, text=True, timeout=120, cwd=str(PIPELINE_DIR)
            )
            self._json({"ok": True, "slug": slug, "output": result.stdout[-500:] if result.stdout else ""})
        except subprocess.TimeoutExpired:
            self._error("Image generation timed out", 500)
        except Exception as e:
            self._error(str(e), 500)

    def _dify_asin_check(self, body):
        """Run the Dify book ASIN checker."""
        script = PIPELINE_DIR / "src" / "dify_asin_checker.py"
        if not script.exists():
            return self._error("dify_asin_checker.py not found. Build it first.", 500)

        try:
            result = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True, text=True, timeout=600, cwd=str(PIPELINE_DIR)
            )
            output = result.stdout
            found = output.count("✅ ASIN found")
            self._json({"ok": True, "output": output, "found": found})
        except subprocess.TimeoutExpired:
            self._error("ASIN check timed out (600s)", 500)
        except Exception as e:
            self._error(str(e), 500)

    def _serve_html(self):
        html_path = PIPELINE_DIR / "src" / "admin" / "index.html"
        if html_path.exists():
            content = html_path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self._error("Dashboard HTML not found", 500)

    def log_message(self, format, *args):
        # Quiet logging
        pass


if __name__ == "__main__":
    port = int(os.environ.get("ADMIN_API_PORT", 8420))
    server = HTTPServer(("127.0.0.1", port), AdminHandler)
    print(f"Admin API running on http://127.0.0.1:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.shutdown()

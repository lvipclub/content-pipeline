#!/usr/bin/env python3
"""
Carousel Article Posting Pipeline — Host-Side Script
Phase 3: Dify → grok-imagine hero → Playwright screenshots → Astro deploy → state file

Usage:
  python3 carousel_pipeline.py [--topic "keyword phrase"] [--resume]

Runs as a no_agent Hermes cron. State file enables idempotent resume.
"""
from __future__ import annotations  # py3.9 compat: PEP 604 annotations are lazy strings
import json
import os
import sys
import time
import shutil
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime, timezone

# ── Config ──────────────────────────────────────────────────
# T2.5 (2026-08-18): VPS Dify via SSH tunnel (18081 -> VPS :8081). MMM Dify retired for
# VPS-bound apps; cron env is sanitized so the env override is unreliable — default here.
DIFY_BASE    = os.environ.get("DIFY_BASE_URL", "http://127.0.0.1:18081/v1")
DIFY_APP_ID  = os.environ.get("DIFY_CAROUSEL_APP_ID", "")
DIFY_API_KEY = os.environ.get("DIFY_CAROUSEL_API_KEY", "")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")  # optional — announcement folded into Helen's morning brief
TG_CHANNEL   = "@hvaccontrols"
AIXINCA_REPO = os.environ.get("AIXINCA_REPO", os.path.expanduser("~/workspace/ai-xinca"))
CONTENT_PIPELINE = os.environ.get("CONTENT_PIPELINE", os.path.expanduser("~/workspace/content-pipeline"))
STATE_FILE   = os.path.join(CONTENT_PIPELINE, "state", "carousel-pipeline.json")
OUTPUT_DIR   = os.path.join(CONTENT_PIPELINE, "output")

# ── Dify creds fallback (C3: cron subprocess env is sanitized — the
#    gateway does NOT inherit ~/.hermes/.env, so DIFY_CAROUSEL_* would be
#    empty and every Dify call would 401 -> silent no-op). Load from the
#    canonical stores like ai-xinca-carousel-daily.sh does:
#      1. ~/.hermes/.env (DIFY_CAROUSEL_APP_ID / DIFY_CAROUSEL_API_KEY)
#      2. content-pipeline/state/dify-carousel-creds.json (legacy)
def _load_dify_creds() -> tuple[str, str]:
    app_id, api_key = DIFY_APP_ID, DIFY_API_KEY
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                v = v.strip().strip('"').strip("'")
                if k == "DIFY_CAROUSEL_APP_ID" and not app_id:
                    app_id = v
                elif k == "DIFY_CAROUSEL_API_KEY" and not api_key:
                    api_key = v
    if not app_id or not api_key:
        creds_path = os.path.expanduser(
            "~/workspace/content-pipeline/state/dify-carousel-creds.json")
        if os.path.exists(creds_path):
            try:
                with open(creds_path, "r", encoding="utf-8") as f:
                    cd = json.load(f)
                app_id = app_id or str(cd.get("app_id", ""))
                api_key = api_key or str(cd.get("api_key", ""))
            except Exception:
                pass
    return app_id, api_key

DIFY_APP_ID, DIFY_API_KEY = _load_dify_creds()

# Slide spec
SLIDE_FORMAT = (1080, 1350)  # width × height for LinkedIn
SLIDE_TYPES  = ["hook", "problem", "concept", "comparison", "cta"]
ACCENT       = "#7EBEC5"
DARK_BG      = "#0a1628"
DARK_BG2     = "#112240"

def ensure_dirs():
    os.makedirs(os.path.join(CONTENT_PIPELINE, "state"), exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return None

def save_state(step: str, done: bool, extra: dict = None):
    state = load_state() or {}
    now = datetime.now(timezone.utc).isoformat()
    state.setdefault("steps", {})
    state["steps"][step] = {"done": done, "at": now}
    state.setdefault("artifacts", {})
    if extra:
        state["artifacts"].update(extra)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def step_done(step: str) -> bool:
    state = load_state()
    if not state:
        return False
    return state.get("steps", {}).get(step, {}).get("done", False)


# ── Step 1: Pick Topic ──────────────────────────────────────
def pick_topic(manual: str = None) -> str | None:
    """Pick a topic from Leni's research or manual input."""
    if manual:
        return manual

    # Check Leni's Monday brief
    brief_dir = os.path.join(CONTENT_PIPELINE, "leni-briefs")
    if os.path.isdir(brief_dir):
        briefs = sorted(Path(brief_dir).glob("*.md"), reverse=True)
        if briefs:
            with open(briefs[0]) as f:
                content = f.read()
            # Extract first suggested topic (simple heuristic)
            for line in content.split("\n"):
                if line.startswith("##") and "topic" in line.lower():
                    continue
                if line.startswith("- ") or line.startswith("* "):
                    topic = line[2:].strip().strip('"').strip("'")
                    if len(topic) > 10:
                        return topic
            # Fallback: use first non-empty line after "Topics" heading
            in_topics = False
            for line in content.split("\n"):
                if "topic" in line.lower() and line.startswith("##"):
                    in_topics = True
                    continue
                if in_topics and line.strip() and not line.startswith("#"):
                    return line.strip().lstrip("-* ").strip('"').strip("'")

    # Check topic queue
    queue_file = os.path.join(CONTENT_PIPELINE, "topic-queue.txt")
    if os.path.exists(queue_file):
        with open(queue_file) as f:
            lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
            if lines:
                topic = lines[0]
                # Rotate queue (remove first line)
                with open(queue_file, "w") as f:
                    f.write("\n".join(lines[1:]) + "\n")
                return topic

    return None  # No topic — skip this run


# ── Step 2: Call Dify Workflow ──────────────────────────────
def call_dify_workflow(topic: str) -> dict | None:
    """Call Dify advanced-chat workflow and get output JSON."""
    import urllib.request
    import urllib.error

    url = f"{DIFY_BASE}/chat-messages"
    payload = {
        "inputs": {"topic": topic},
        "query": f"Generate a carousel article about: {topic}",
        "response_mode": "blocking",
        "user": "carousel-pipeline",
    }
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json",
    }

    for attempt in range(3):
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode(),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=180) as resp:
                result = json.loads(resp.read())
                answer = result.get("answer", "")
                # Parse JSON from answer (Dify Answer node output)
                try:
                    output = json.loads(answer)
                except json.JSONDecodeError:
                    # Try extracting JSON from markdown code block
                    if "```json" in answer:
                        block = answer.split("```json")[1].split("```")[0]
                        output = json.loads(block)
                    elif "```" in answer:
                        block = answer.split("```")[1].split("```")[0]
                        output = json.loads(block)
                    else:
                        output = {"raw_answer": answer, "error": "Could not parse JSON from Dify output"}

                # Validate required fields
                required = ["article", "slides", "hero_prompt", "slug"]
                missing = [k for k in required if k not in output]
                if missing:
                    print(f"WARNING: Dify output missing fields: {missing}")
                    output["_missing_fields"] = missing

                return output

        except urllib.error.HTTPError as e:
            body = e.read().decode() if e.fp else ""
            print(f"Dify HTTP {e.code}: {body[:200]}")
            if attempt < 2:
                wait = [10, 20, 40][attempt]
                print(f"Retrying in {wait}s...")
                time.sleep(wait)
        except Exception as e:
            print(f"Dify error: {e}")
            if attempt < 2:
                time.sleep(10)

    return None


# ── Step 3: Generate Hero Image (xAI grok-imagine via OAuth) ──
def _xai_oauth_token() -> str:
    """Resolve the xAI OAuth access token (same path as the gateway + heartbeat).

    hermes_cli.auth uses PEP 604 unions (crashes on system python 3.9), so the
    token is fetched through the hermes-agent venv python instead.
    """
    venv_py = os.path.expanduser("~/.hermes/hermes-agent/venv/bin/python3")
    if not os.path.exists(venv_py):
        venv_py = "python3"
    code = (
        "from hermes_cli.auth import resolve_xai_oauth_runtime_credentials;"
        "import json;"
        "print(resolve_xai_oauth_runtime_credentials("
        "force_refresh=True, refresh_skew_seconds=1800)['api_key'])"
    )
    try:
        r = subprocess.run(
            [venv_py, "-c", code], capture_output=True, text=True, timeout=90
        )
        token = r.stdout.strip()
        if r.returncode != 0 or not token or "." not in token:
            print(
                "xAI OAuth token error: "
                f"{r.stderr.strip()[:200] or 'empty token'}"
            )
            return ""
        return token
    except Exception as e:
        print(f"xAI OAuth token error: {e}")
        return ""


def generate_hero_image(hero_prompt: str, slug: str) -> str | None:
    """Generate hero image via xAI grok-imagine (OAuth — included in Premium+)."""
    import urllib.request

    token = _xai_oauth_token()
    if not token:
        print("xAI OAuth token unavailable — skipping hero image generation")
        return None

    payload = {"model": "grok-imagine-image", "prompt": hero_prompt, "n": 1}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    for attempt in range(2):
        try:
            req = urllib.request.Request(
                "https://api.x.ai/v1/images/generations",
                data=json.dumps(payload).encode(),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=240) as resp:
                result = json.loads(resp.read())
                image_url = (result.get("data") or [{}])[0].get("url")
                if not image_url:
                    raise RuntimeError(f"no image url in response: {str(result)[:200]}")

                out_path = os.path.join(
                    AIXINCA_REPO, "public/articles", f"{slug}-hero.png"
                )
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                # imgen.x.ai CDN blocks urllib (CF 1010) — download via curl.
                # CDN is flaky (connection resets/stalls): bound every attempt,
                # retry transient errors, and cap the whole download via
                # subprocess timeout so a stall can't blow the step budget.
                dl = subprocess.run(
                    [
                        "curl", "-sL4", "--connect-timeout", "10",
                        "--max-time", "45", "--retry", "2",
                        "--retry-all-errors", "--retry-delay", "2",
                        "-o", out_path, image_url,
                    ],
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                if (
                    dl.returncode != 0
                    or not os.path.exists(out_path)
                    or os.path.getsize(out_path) < 1000
                ):
                    raise RuntimeError(
                        f"curl download failed rc={dl.returncode} {dl.stderr[:120]}"
                    )
                print(
                    f"Hero image saved: {out_path} ({os.path.getsize(out_path)} bytes)"
                )
                return out_path
        except Exception as e:
            print(f"grok-imagine error: {e}")
            if attempt < 1:
                time.sleep(5)

    return None


# ── Step 4: Render Slide HTMLs ──────────────────────────────
SLIDE_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width={width},height={height}">
<style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{width}px;height:{height}px;overflow:hidden;font-family:'Inter','Segoe UI',system-ui,sans-serif}}
.badge{{display:inline-block;font-size:12px;padding:4px 14px;border-radius:99px;font-weight:600;letter-spacing:.08em;text-transform:uppercase}}
.slide-num{{position:absolute;top:32px;right:32px;font-size:11px;font-family:monospace;letter-spacing:.15em;text-transform:uppercase}}
.accent-bar-top{{position:absolute;top:0;left:0;width:100%;height:4px}}
.accent-bar-bottom{{position:absolute;bottom:0;left:0;width:100%;height:2px;background:linear-gradient(90deg,{accent}40,{accent},{accent}40)}}
{styles}
</style></head><body>{body}</body></html>"""

def render_slide_htmls(slides: list, slug: str) -> list[str]:
    """Render individual HTML files for each slide, ready for screenshots."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    paths = []
    for i, slide in enumerate(slides):
        slide_type = SLIDE_TYPES[i] if i < len(SLIDE_TYPES) else f"slide-{i+1}"
        pos = i + 1
        total = len(slides)

        title = slide.get("title", f"Slide {pos}")
        badge = slide.get("type", slide_type).title()
        key_point = slide.get("key_point", "")

        # Determine visual style based on slide type
        if slide_type == "hook":
            bg = f"background:linear-gradient(180deg,{DARK_BG},{DARK_BG2},{DARK_BG})"
            text_color = "#fff"
            badge_bg = f"background:rgba(126,190,197,.2);color:{ACCENT};border:1px solid rgba(126,190,197,.3)"
            slide_num_color = f"color:rgba(126,190,197,.3)"
            body_html = f"""
<div style="{bg};width:{SLIDE_FORMAT[0]}px;height:{SLIDE_FORMAT[1]}px;position:relative;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:64px 48px">
<div class="accent-bar-top" style="background:{ACCENT}"></div>
<div class="slide-num" style="{slide_num_color}color:rgba(126,190,197,.3)">Slide {pos} / {total}</div>
<div style="margin-bottom:32px"><span class="badge" style="{badge_bg}">{badge}</span></div>
<h1 style="font-family:'Trebuchet MS',Trebuchet,Helvetica,Arial,sans-serif;font-size:{'52' if slide_type=='hook' else '44'}px;font-weight:800;color:#fff;line-height:1.15;margin-bottom:24px;max-width:900px">{title}</h1>
<p style="font-size:20px;color:rgba(255,255,255,.55);max-width:560px">{key_point}</p>
<div class="accent-bar-bottom"></div>
</div>"""
        elif slide_type == "cta":
            avatar_path = os.path.join(
                AIXINCA_REPO, "public", "avatars", "lady-havi.jpg"
            )
            body_html = f"""
<div style="background:linear-gradient(180deg,{DARK_BG},{DARK_BG2},{DARK_BG});width:{SLIDE_FORMAT[0]}px;height:{SLIDE_FORMAT[1]}px;position:relative;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:64px 48px">
<div class="accent-bar-top" style="background:{ACCENT}"></div>
<div class="slide-num" style="color:rgba(126,190,197,.3)">Slide {pos} / {total}</div>
<div style="margin-bottom:28px"><span class="badge" style="{badge_bg}">CTA</span></div>
<h1 style="font-family:'Trebuchet MS',Trebuchet,Helvetica,Arial,sans-serif;font-size:48px;font-weight:800;color:#fff;line-height:1.15;margin-bottom:20px;max-width:900px">{title}</h1>
<p style="font-size:20px;color:rgba(255,255,255,.55);max-width:640px;line-height:1.6;margin-bottom:36px">{key_point}</p>
<img src="file://{avatar_path}" style="width:170px;height:170px;border-radius:50%;border:3px solid rgba(126,190,197,.55);object-fit:cover;margin-bottom:14px"/>
<div style="font-size:15px;font-weight:700;letter-spacing:.18em;color:{ACCENT};margin-bottom:28px">LADY HAVI</div>
<div style="display:inline-block;background:{ACCENT};color:{DARK_BG};font-weight:700;font-size:19px;padding:16px 44px;border-radius:99px;margin-bottom:16px">Read the Full Guide →</div>
<div style="font-size:15px;color:rgba(255,255,255,.45)">ai.xinca.com/a/{slug}/</div>
<div style="position:absolute;bottom:44px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:10px;color:rgba(255,255,255,.7);font-size:16px">
<svg width="20" height="20" viewBox="0 0 24 24" fill="#fff"><path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg>
<span>Subscribe on Telegram — HVAC Controls 101</span>
</div>
<div class="accent-bar-bottom"></div>
</div>"""
        elif slide_type == "problem" or slide_type == "comparison":
            bg = "background:#fff"
            text_color = "#333"
            badge_bg = f"background:rgba(126,190,197,.2);color:{ACCENT};border:1px solid rgba(126,190,197,.3)"
            slide_num_color = f"color:rgba(126,190,197,.4)"
            body_html = f"""
<div style="{bg};width:{SLIDE_FORMAT[0]}px;height:{SLIDE_FORMAT[1]}px;position:relative;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:64px 48px;border:1px solid #e5e5e5">
<div class="accent-bar-top" style="background:{ACCENT}"></div>
<div class="slide-num" style="color:rgba(126,190,197,.4)">Slide {pos} / {total}</div>
<div style="margin-bottom:32px"><span class="badge" style="{badge_bg}">{badge}</span></div>
<h2 style="font-family:'Trebuchet MS',Trebuchet,Helvetica,Arial,sans-serif;font-size:48px;font-weight:800;color:#333;line-height:1.18;margin-bottom:24px;max-width:900px">{title}</h2>
<p style="font-size:19px;color:#666;max-width:560px;line-height:1.6">{key_point}</p>
<div class="accent-bar-bottom"></div>
</div>"""
        else:  # concept
            bg = "background:linear-gradient(135deg,#f8f9fa,#fff)"
            text_color = "#333"
            badge_bg = f"background:rgba(126,190,197,.2);color:{ACCENT};border:1px solid rgba(126,190,197,.3)"
            slide_num_color = f"color:rgba(126,190,197,.4)"
            body_html = f"""
<div style="{bg};width:{SLIDE_FORMAT[0]}px;height:{SLIDE_FORMAT[1]}px;position:relative;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:64px 48px;border:1px solid #e5e5e5">
<div class="accent-bar-top" style="background:{ACCENT}"></div>
<div class="slide-num" style="color:rgba(126,190,197,.4)">Slide {pos} / {total}</div>
<div style="margin-bottom:32px"><span class="badge" style="{badge_bg}">{badge}</span></div>
<h2 style="font-family:'Trebuchet MS',Trebuchet,Helvetica,Arial,sans-serif;font-size:44px;font-weight:800;color:#333;line-height:1.18;margin-bottom:24px;max-width:900px">{title}</h2>
<p style="font-size:18px;color:#666;max-width:560px;line-height:1.6">{key_point}</p>
<div class="accent-bar-bottom"></div>
</div>"""

        # Build full HTML
        html = SLIDE_HTML_TEMPLATE.format(
            width=SLIDE_FORMAT[0],
            height=SLIDE_FORMAT[1],
            accent=ACCENT,
            styles="",
            body=body_html,
        )

        out_path = os.path.join(OUTPUT_DIR, f"{slug}-slide-{pos:02d}.html")
        with open(out_path, "w") as f:
            f.write(html)
        paths.append(out_path)
        print(f"  Slide {pos} HTML: {out_path}")

    return paths


# ── Step 5: Screenshot Slides (Playwright) ──────────────────
def screenshot_slides(slide_htmls: list[str], slug: str) -> list[str]:
    """Screenshot each slide HTML at 1080×1350 using Playwright."""
    from playwright.sync_api import sync_playwright

    png_dir = os.path.join(AIXINCA_REPO, "public/articles/slides")
    os.makedirs(png_dir, exist_ok=True)

    png_paths = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for html_path in slide_htmls:
            filename = os.path.basename(html_path).replace(".html", ".png")
            png_path = os.path.join(png_dir, filename)

            page = browser.new_page(viewport={"width": SLIDE_FORMAT[0], "height": SLIDE_FORMAT[1]})
            page.goto(f"file://{html_path}", wait_until="networkidle")
            page.wait_for_timeout(1500)  # Font loading
            page.screenshot(path=png_path, full_page=False)
            page.close()

            size_kb = os.path.getsize(png_path) / 1024
            png_paths.append(png_path)
            print(f"  Screenshot: {filename} ({size_kb:.0f} KB)")

        browser.close()

    # Create ZIP bundle
    zip_path = os.path.join(png_dir, "slides-bundle.zip")
    subprocess.run(
        ["zip", "-j", zip_path] + png_paths,
        cwd=png_dir, check=False, capture_output=True
    )
    if os.path.exists(zip_path):
        zip_kb = os.path.getsize(zip_path) / 1024
        print(f"  ZIP bundle: slides-bundle.zip ({zip_kb:.0f} KB)")

    return png_paths


# ── Step 5b: Copy PNGs to /public/articles/slides with nice names ──
def copy_pngs_with_nice_names(slides: list, slug: str) -> list[str]:
    """Copy PNGs to standard locations with descriptive names."""
    png_dir = os.path.join(AIXINCA_REPO, "public/articles/slides")
    os.makedirs(png_dir, exist_ok=True)

    result = []
    for i, slide in enumerate(slides):
        pos = i + 1
        slide_type = SLIDE_TYPES[i] if i < len(SLIDE_TYPES) else f"slide-{pos}"
        topic_words = slug.replace("-", " ").split()[:2]
        topic_short = "-".join(topic_words)
        nice_name = f"{pos:02d}-{slide_type}-{topic_short}.png"
        nice_path = os.path.join(png_dir, nice_name)

        # Find the matching HTML-derived PNG
        html_name = f"{slug}-slide-{pos:02d}.png"
        src_path = os.path.join(png_dir, html_name)
        if os.path.exists(src_path):
            shutil.copy2(src_path, nice_path)
            result.append(nice_path)
            print(f"  Copied: {nice_name}")

    return result


# ── Step 6: Post TG Notification ────────────────────────────
def post_tg_notification(article: dict, slug: str, slides: list):
    """Post article hook to @hvaccontrols Telegram channel."""
    title = article.get("title", "New Article")
    description = article.get("description", "")
    article_url = f"https://ai.xinca.com/a/{slug}/"

    hook = f"🔥 {title}\n\n{description}\n\n→ {article_url}"

    # Add hashtags
    hashtags = article.get("hashtags", [])
    if not hashtags:
        hashtags = ["#HVAC", "#BuildingServices"]
    hook += "\n\n" + " ".join(f"#{t}" for t in hashtags)

    import urllib.request
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHANNEL,
        "text": hook,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    data = json.dumps(payload).encode()
    headers = {"Content-Type": "application/json"}

    try:
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
            if result.get("ok"):
                print(f"TG posted: message_id={result['result']['message_id']}")
                return result["result"]["message_id"]
            else:
                print(f"TG error: {result}")
    except Exception as e:
        print(f"TG post failed: {e}")

    return None


# ── Step 7: Build & Deploy ──────────────────────────────────
def build_and_deploy(slug: str):
    """npm run build → git push gh-pages."""
    os.chdir(AIXINCA_REPO)

    # Build
    print("Building Astro...")
    result = subprocess.run(["npm", "run", "build"], capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        print(f"Build FAILED:\n{result.stderr[-500:]}")
        return False
    print("Build OK")

    # Git commit
    subprocess.run(["git", "add", "-A"], check=False)
    commit_msg = f"Auto: carousel article — {slug}"
    result = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True)
    print(f"Git commit: {result.stdout.strip()[:80]}")

    # Push master
    result = subprocess.run(["git", "push", "origin", "master"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Push master failed: {result.stderr[:200]}")

    # Deploy to gh-pages
    import tempfile
    tmpdir = tempfile.mkdtemp()
    dist_dir = os.path.join(AIXINCA_REPO, "dist")
    if os.path.isdir(dist_dir):
        for item in os.listdir(dist_dir):
            s = os.path.join(dist_dir, item)
            d = os.path.join(tmpdir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)

    cname = os.path.join(tmpdir, "CNAME")
    with open(cname, "w") as f:
        f.write("ai.xinca.com")

    subprocess.run(["git", "init"], cwd=tmpdir, check=False)
    subprocess.run(["git", "checkout", "-b", "gh-pages"], cwd=tmpdir, check=False)
    subprocess.run(["git", "add", "-A"], cwd=tmpdir, check=False)
    subprocess.run(["git", "commit", "-m", f"deploy: carousel {slug}"], cwd=tmpdir, check=False, capture_output=True)

    gh_url = "https://github.com/lvipclub/ai-xinca.git"
    result = subprocess.run(
        ["git", "push", "-f", gh_url, "gh-pages"],
        cwd=tmpdir, capture_output=True, text=True
    )
    if result.returncode == 0:
        print("Deployed to gh-pages ✅")
    else:
        print(f"Deploy failed: {result.stderr[:200]}")

    shutil.rmtree(tmpdir, ignore_errors=True)
    return True


# ── Step 8: Create Astro Page from Dify Output ──────────────
def create_astro_page(article: dict, slug: str) -> str | None:
    """
    Create a basic Astro article page from Dify output.
    The article dict should have: title, description, body_markdown.
    Falls back to a generic page if Dify output is sparse.
    """
    title = article.get("title", slug.replace("-", " ").title())
    description = article.get("description", "")
    body = article.get("body_markdown", article.get("body", ""))

    astro_path = os.path.join(AIXINCA_REPO, "src/pages/a", f"{slug}.astro")
    if os.path.exists(astro_path):
        print(f"Astro page already exists: {astro_path} — skipping creation")
        return astro_path

    # Minimal Astro article page (matching existing pattern)
    content = f"""---
// a/{slug}.astro — Auto-generated carousel article
import BaseLayout from '../../layouts/BaseLayout.astro';

const pageTitle = {json.dumps(title)};
const pageDescription = {json.dumps(description)};
const canonicalUrl = "https://ai.xinca.com/a/{slug}/";

const jsonLd = {{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": pageTitle,
  "description": pageDescription,
  "author": {{ "@type": "Organization", "name": "XINCA" }},
  "publisher": {{ "@type": "Organization", "name": "XINCA", "url": "https://ai.xinca.com" }},
  "datePublished": "{datetime.now().strftime('%Y-%m-%d')}",
  "mainEntityOfPage": canonicalUrl
}};

---
<BaseLayout title={{pageTitle}} description={{pageDescription}} ogImage="https://ai.xinca.com/articles/{slug}-hero.png" ogType="article">
  <script type="application/ld+json" set:html={{JSON.stringify(jsonLd)}}></script>
  <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <h1 class="text-3xl md:text-5xl font-extrabold text-[#333] mb-4" style="font-family:'Trebuchet MS',Trebuchet,Helvetica,Arial,sans-serif">{{pageTitle}}</h1>
    <p class="text-lg text-[#666] mb-8">{{pageDescription}}</p>
    <div class="prose prose-lg max-w-none">
      {body}
    </div>
    <div class="mt-8">
      <a href="https://t.me/hvaccontrols" target="_blank" rel="noopener" class="inline-flex items-center gap-2 text-sm bg-[#2ea3f2] text-white px-5 py-2.5 rounded-lg hover:bg-[#2589d9] transition-colors">
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.161c-.18 1.897-.962 6.502-1.359 8.627-.168.9-.5 1.201-.82 1.23-.697.064-1.226-.46-1.901-.903-1.056-.692-1.653-1.123-2.678-1.799-1.185-.781-.417-1.21.258-1.911.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.139-5.062 3.345-.479.329-.913.489-1.302.481-.428-.009-1.252-.242-1.865-.441-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.831-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635.099-.002.321.023.465.139.121.098.154.228.17.32.016.092.036.303.02.466z"/></svg>
        Subscribe on Telegram — HVAC Controls 101
      </a>
    </div>
  </main>
</BaseLayout>
"""
    os.makedirs(os.path.dirname(astro_path), exist_ok=True)
    with open(astro_path, "w") as f:
        f.write(content)
    print(f"Created Astro page: {astro_path}")
    return astro_path


# ── Main Pipeline ───────────────────────────────────────────
def main(topic: str = None, resume: bool = False):
    ensure_dirs()

    # Check if a run is already in progress
    if not resume and step_done("deployed"):
        state = load_state()
        last_run = state["steps"]["deployed"]["at"]
        print(f"Previous run completed at {last_run}. Nothing to do.")
        return

    # ── Step 1: Pick Topic ──
    if not step_done("dify_called") or resume:
        topic = pick_topic(topic)
        if not topic:
            print("No topic available — skipping run")
            return
        print(f"Topic: {topic}")
    else:
        state = load_state()
        topic = state.get("topic", "unknown")

    # ── Step 2: Call Dify ──
    if not step_done("dify_called") or resume:
        print(f"Calling Dify workflow for: {topic}")
        output = call_dify_workflow(topic)
        if not output:
            print("Dify workflow failed — aborting")
            return
        save_state("dify_called", True)
        # Save full output for inspection
        out_file = os.path.join(OUTPUT_DIR, f"{topic.replace(' ', '-')[:40]}.json")
        with open(out_file, "w") as f:
            json.dump(output, f, indent=2)
        print(f"Dify output saved: {out_file}")
    else:
        # Load from saved state
        state = load_state()
        out_file = state.get("artifacts", {}).get("dify_output_file")
        if out_file and os.path.exists(out_file):
            with open(out_file) as f:
                output = json.load(f)
        else:
            print("No saved Dify output — restarting from step 2")
            output = call_dify_workflow(topic)
            if not output:
                return
            out_file = os.path.join(OUTPUT_DIR, f"{topic.replace(' ', '-')[:40]}.json")
            with open(out_file, "w") as f:
                json.dump(output, f, indent=2)
            save_state("dify_called", True, {"dify_output_file": out_file})

    slug = output.get("slug", topic.replace(" ", "-")[:50])
    slides = output.get("slides", [])
    article = output.get("article", {})
    hero_prompt = output.get("hero_prompt", "")

    print(f"Slug: {slug}")
    print(f"Slides: {len(slides)}")

    # ── Step 3: Hero Image ──
    if hero_prompt and not step_done("hero_generated"):
        print("Generating hero image...")
        hero_path = generate_hero_image(hero_prompt, slug)
        save_state("hero_generated", True, {"hero_path": hero_path})

    # ── Step 4: Render Slide HTMLs ──
    if not step_done("slides_rendered"):
        print(f"Rendering {len(slides)} slides...")
        slide_htmls = render_slide_htmls(slides, slug)
        save_state("slides_rendered", True, {"slide_htmls": slide_htmls})
    else:
        state = load_state()
        slide_htmls = state.get("artifacts", {}).get("slide_htmls", [])

    # ── Step 5: Screenshots ──
    if not step_done("screenshots_taken"):
        print("Screenshotting slides...")
        screenshot_slides(slide_htmls, slug)
        copy_pngs_with_nice_names(slides, slug)
        save_state("screenshots_taken", True)

    # ── Step 6: TG Notification (optional) ──
    # Announcement is folded into Helen's daily brief (it reads the state file);
    # a direct channel post only happens if TG_BOT_TOKEN is configured.
    if TG_BOT_TOKEN and not step_done("tg_posted"):
        print("Posting TG notification...")
        tg_id = post_tg_notification(article, slug, slides)
        save_state("tg_posted", True, {"tg_message_id": tg_id})

    # ── Step 7: Create Astro Page ──
    if article:
        create_astro_page(article, slug)

    # ── Step 8: Build & Deploy ──
    if not step_done("deployed"):
        print("Building and deploying...")
        success = build_and_deploy(slug)
        if success:
            save_state("deployed", True)
            print(f"\n✅ Pipeline complete: https://ai.xinca.com/a/{slug}/")
            print(f"   Carousel: https://ai.xinca.com/a/{slug}/carousel/")
        else:
            print("Deploy failed — state saved for retry")
    else:
        print("Already deployed — skipping")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Carousel Article Pipeline")
    parser.add_argument("--topic", help="Article topic (keyword phrase)")
    parser.add_argument("--resume", action="store_true", help="Resume from last incomplete step")
    args = parser.parse_args()
    main(topic=args.topic, resume=args.resume)

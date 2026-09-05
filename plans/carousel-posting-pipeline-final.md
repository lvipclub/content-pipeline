# Carousel Article Posting Pipeline — FINAL Plan
**Date:** 2026-07-28  
**Version:** 3.0 (post Codi/Qui review + Marc Sir revisions)  
**Status:** Pending Marc Sir approval

---

## Marc Sir Directives (incorporated)

1. 3-6 slides (not 5-7). Default 5.
2. Carousel hosted on help.xinca.com first, then copy-paste to LinkedIn/X.
3. Dify handles as much as possible — TG posting, hook drafting, article writing. Hermes only for browser/git/filesystem operations Dify literally cannot do.
4. TG channel @hvaccontrols gets the article hook posted by Dify, not a sterile admin ping.
5. help.xinca.com footer gets a TG subscribe button.
6. Hermes cron primary, Dify Schedule secondary. State-file idempotent resume + watchdog cron for failure detection.
7. **Article slugs:** 3 focus keywords, not full title. E.g. `control-valve-hydronic-balancing` not `water-side-control-valve-selection`.

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    DIFY WORKFLOW (80% of pipeline)            │
│                                                              │
│  [Hermes Cron triggers Dify]                                 │
│         │                                                    │
│         ▼                                                    │
│  [KB Retrieval: HVAC a71b5439]                               │
│         │                                                    │
│         ▼                                                    │
│  [LLM Havi: Write Article] ─── [LLM Havi: Carousel Slides]   │
│         │                          │                         │
│         ▼                          ▼                         │
│  [LLM Havi: Hero Prompt]    [LLM Havi: TG Hook + CTA]        │
│         │                          │                         │
│         │                          ▼                         │
│         │               [HTTP Request: TG Bot API]            │
│         │               → @hvaccontrols hook posted           │
│         │                                                    │
│         ▼                                                    │
│  [Answer: Output JSON — article + slides + hero prompt]      │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼ (JSON written to ~/workspace/content-pipeline/output/)
┌──────────────────────────────────────────────────────────────┐
│                    HERMES CRON (20% — browser + git + deploy) │
│                                                              │
│  1. Read Dify output JSON                                    │
│  2. Generate hero image (FAL REST API)                       │
│  3. Create Astro page (src/pages/a/{3-keyword-slug}.astro)   │
│  4. Render slides as isolated HTML (one .html per slide)     │
│  5. Screenshot each slide at 1080×1350 (Playwright)          │
│  6. Compress PNGs (pngquant)                                 │
│  7. Build + deploy (npm run build → git push gh-pages)       │
│  8. Update articles.json metadata                            │
│  9. Update state file → success                              │
│                                                              │
│  STATE FILE: ~/workspace/content-pipeline/state/carousel.json│
│  WATCHDOG: cron runs 30min after, alerts if stuck >2h        │
└──────────────────────────────────────────────────────────────┘
```

**Why this split:**
- Dify cannot: browser screenshot, git push, npm build, filesystem operations
- Dify can: all LLM reasoning, HTTP API calls (TG Bot API), KB retrieval
- Hermes cron with state file: idempotent resume, survives Colima restarts

---

## Phase 1 — Manual Carousel Page (Hermes builds, ~2h)

**Goal:** Working proof-of-concept for the control valve article.

**Article slug:** `control-valve-hydronic-balancing` (3 focus keywords)

### Slide Spec

| # | Type | Hook Line | Content |
|---|------|-----------|---------|
| 1 | Hook | "5 Pitfalls in Water-Side Control Valve Selection" | Sub-text: "And how they sabotage your energy savings" |
| 2 | Problem | "Why 'Size by Pipe Size' is Wrong" | Valve authority dictates sizing, not pipe diameter |
| 3 | Concept | "What is Valve Authority?" | β = ΔP_valve / (ΔP_valve + ΔP_circuit). Target β > 0.3 |
| 4 | Comparison | "Globe vs Ball vs PICV" | Equal Percentage characteristics win for coil control |
| 5 | CTA | "Ready to optimise your hydronic balancing?" | Lady Havi avatar + help.xinca.com logo + URL |

**Format:** 1080×1350px cards. XINCA teal (#7EBEC5) + dark navy (#0a1628). No AI image gen — HTML/CSS rendering for accurate text/formulas.

### Implementation

1. Create `src/pages/a/control-valve-hydronic-balancing/carousel.astro`
2. Build 5 slide HTML cards with `aspect-ratio: 1080/1350`
3. Social share OG tags
4. `npm run build` → deploy gh-pages → verify cache-bust
5. Update redirect from old slug if needed

---

## Phase 2 — Lightbox + Download (Hermes builds, ~1h)

**Per-slide:**
- Click → lightbox (full 1080×1350 view)
- "Download Slide (PNG)" button
- "Copy for LinkedIn" → copies image URL

**Page-level:**
- Pre-built ZIP download (static file, no client-side JS library needed)
- "Open in LinkedIn" link → `https://www.linkedin.com/sharing/share-offsite/?url=...`

**Implementation:**
- Isolated `.html` files (one per slide, minimal markup, 1080×1350 fixed dims) for screenshot pipeline
- Browser screenshots via Playwright → `public/articles/carousel/{slug}-{n}.png`
- `pngquant --quality=65-80` compression → <500KB per slide
- Pre-build ZIP at deploy time → serve as static asset

---

## Phase 3 — Dify Workflow (automated pipeline)

### 3a: Dify App Provisioning

| Parameter | Value |
|-----------|-------|
| App name | Carousel Article Generator |
| Mode | `advanced-chat` (for KB retrieval + LLM chaining) |
| KB linked | HVAC (a71b5439) via Knowledge Retrieval node |
| API key | Generated after publish |
| Model | deepseek-v4-pro (all LLM nodes) |

### 3b: Workflow Nodes

```
[Start: {topic} — keyword or theme string]
    │
    ▼
[Knowledge Retrieval: HVAC KB a71b5439]
  - Query: {{topic}}
  - Top K: 5
  - Score threshold: 0.5
    │
    ▼
[LLM: Write Article]  ← persona: Havi (Lady Havi, HVAC domain expert)
  - Input: topic + KB context
  - Output: structured JSON with {title, description, slug (3 keywords), 
    body_markdown, tables, citations}
  - Slug rule: extract 3 focus keywords from article, hyphenate, 
    max 4 words total. E.g. "control valve and hydronic balancing" 
    → slug = "control-valve-hydronic-balancing"
  - Australian English, XINCA brand voice
  - 800-1500 words
  - No competitor names (Belimo, Honeywell, JCI, Siemens)
  - "ecommerce partner of authorised supplier" framing
  - Lady Havi CTA at end
    │
    ▼
[LLM: Generate Hero Image Prompt]
  - Notebook-style hero matching existing brand (see ai-xinca-content ref images)
  - Input: article title + topic
  - Output: FAL.ai prompt string for image_generate
    │
    ▼
[LLM: Generate 3-6 Carousel Slides]
  - Input: article JSON
  - Output: JSON array [{type, title, key_point, visual_hint}]
  - Slide types: hook, problem, concept, comparison, CTA
  - Each title ≤8 words, key_point ≤25 words each
    │
    ▼
[LLM: Draft TG Hook + CTA]
  - Target: @hvaccontrols public channel
  - Format: Lady Havi voice, 1-2 sentence hook, 
    CTA to read full article at help.xinca.com/a/{slug}/
  - Hashtags: 3-5 relevant HVAC hashtags
    │
    ▼
[HTTP Request: Post to TG Channel]
  - Method: POST
  - URL: https://api.telegram.org/bot{TOKEN}/sendMessage
  - Body: {chat_id: "@hvaccontrols", text: "{hook + CTA}", 
           parse_mode: "HTML", 
           disable_web_page_preview: false}
  - NO template variables in URL (static only — HTTP Request node limitation)
  - Token resolved via Dify secret/env variable
    │
    ▼
[Answer: Output JSON]
  - {article: {...}, slides: [...], hero_prompt: "...", slug: "...", 
     tg_post_id: "..."}
```

### 3c: Host-Side Script (Hermes Cron)

**Cron schedule:** Weekly (e.g. Monday 03:00 HKT, after Leni's research pipeline settles)

**State file:** `~/workspace/content-pipeline/state/carousel-pipeline.json`
```json
{
  "run_id": "2026-07-28-0300",
  "topic": "control valve hydronic balancing",
  "slug": "control-valve-hydronic-balancing",
  "steps": {
    "dify_called": {"done": true, "at": "ISO8601"},
    "hero_generated": {"done": false, "at": null},
    "slides_rendered": {"done": false, "at": null},
    "screenshots_taken": {"done": false, "at": null},
    "deployed": {"done": false, "at": null}
  },
  "artifacts": {
    "hero_path": null,
    "slide_htmls": [],
    "slide_pngs": [],
    "articles_json_updated": false
  }
}
```

**Script flow** (`no_agent: true` Python script, avoids Hermes agent 600s timeout):

```python
# 1. Pick topic (from Leni brief or manual)
topic = read_leni_brief() or read_topic_queue() or skip_run()

# 2. Call Dify workflow → wait for output JSON
output = call_dify_workflow(topic, app_id, api_key)
save_state("dify_called", done=True)

# 3. Generate hero image via FAL REST API
hero = generate_fal_image(output["hero_prompt"], reference_image)
save_state("hero_generated", done=True, hero_path=hero.path)

# 4. Render isolated slide HTML files
slide_htmls = render_slide_htmls(output["slides"])
save_state("slides_rendered", done=True, slide_htmls=slide_htmls)

# 5. Screenshot each slide (Playwright)
slide_pngs = screenshot_slides(slide_htmls, slug)
save_state("screenshots_taken", done=True, slide_pngs=slide_pngs)

# 6. Compress → deploy to help.xinca.com
compress_pngs(slide_pngs)  # pngquant --quality=65-80
create_astro_page(output["article"], slug)
update_articles_json(output["article"], slug)
npm_build_and_deploy(slug)
save_state("deployed", done=True)
```

**Idempotent resume:** If cron fires again later (e.g. Colima restarted), reads state file → skips completed steps → resumes from first `done: false`.

**Watchdog cron** (30 min after main cron, `no_agent: true`):
```bash
#!/bin/bash
# Check if carousel pipeline is stuck
STATE_FILE="$HOME/workspace/content-pipeline/state/carousel-pipeline.json"
if [ -f "$STATE_FILE" ]; then
    LAST_RUN=$(jq -r '.steps.dify_called.at // "1970-01-01"' "$STATE_FILE")
    HOURS_SINCE=$(( ($(date +%s) - $(date -jf "%Y-%m-%dT%H:%M:%S" "${LAST_RUN:0:19}" +%s)) / 3600 ))
    DEPLOYED=$(jq -r '.steps.deployed.done' "$STATE_FILE")
    
    if [ "$DEPLOYED" != "true" ] && [ "$HOURS_SINCE" -gt 2 ]; then
        # Alert Marc Sir via TG
        curl -s -X POST "https://api.telegram.org/bot$TG_TOKEN/sendMessage" \
            -d "chat_id=@hvaccontrols" \
            -d "text=Carousel pipeline stuck at step $(jq -r '.steps | to_entries | map(select(.value.done != true)) | .[0].key' $STATE_FILE) for ${HOURS_SINCE}h. Manual check needed."
    fi
fi
```

---

## help.xinca.com TG Subscribe Button (separate task)

Add to `BaseLayout.astro` footer (or article footer):

```html
<div class="mt-6 pt-4 border-t border-gray-200">
  <a href="https://t.me/hvaccontrols" target="_blank" rel="noopener"
     class="inline-flex items-center gap-2 text-sm bg-[#2ea3f2] text-white px-5 py-2.5 rounded-lg hover:bg-[#2589d9] transition-colors">
    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
      <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.161c-.18 1.897-.962 6.502-1.359 8.627-.168.9-.5 1.201-.82 1.23-.697.064-1.226-.46-1.901-.903-1.056-.692-1.653-1.123-2.678-1.799-1.185-.781-.417-1.21.258-1.911.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.139-5.062 3.345-.479.329-.913.489-1.302.481-.428-.009-1.252-.242-1.865-.441-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.831-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635.099-.002.321.023.465.139.121.098.154.228.17.32.016.092.036.303.02.466z"/>
    </svg>
    Subscribe on Telegram — HVAC Controls 101
  </a>
</div>
```

Placement: below Lady Havi CTA in article template. Benefits every article automatically.

---

## Slug Convention (enforced)

**Rule:** 3 focus keywords, hyphenated, max 4 words.

| Full Title | Slug |
|------------|------|
| Control Valve Selection and Hydronic Balancing for Commercial HVAC | `control-valve-hydronic-balancing` |
| The Coolant Trade-Off That Transforms Data Centre Economics | `data-centre-glycol-cooling` |
| Modern BMS Integration: From Traditional DDC to IoT-Enabled Building Controls | `bms-integration-iot-controls` |

Dify LLM node generates slug from article title as part of output JSON. Validation in Code node:

```python
def main(slug: str) -> dict:
    parts = slug.split("-")
    if not (2 <= len(parts) <= 4):
        return {"error": f"Slug must have 2-4 parts, got {len(parts)}"}
    return {"slug": slug.lower()}
```

---

## Error Handling Matrix

| Failure Point | Detection | Recovery |
|--------------|-----------|----------|
| Leni brief empty (no topic) | read_leni_brief() returns None | Use last week's brief or pre-curated topic queue; skip run if queue empty |
| Dify workflow timeout | HTTP timeout after 120s | Retry × 3 with exponential backoff (10s/20s/40s); if all fail → state file marked `dify_called: false` → watchdog alerts |
| FAL API fails | HTTP non-200 or timeout | Retry × 2; skip hero image → use generic fallback banner |
| Playwright screenshot fails | Exit code ≠ 0 | Retry individual slide; skip failed slide → deploy with partial carousel |
| npm build fails | Exit code ≠ 0 | Log error; state file marked `deployed: false` → watchdog alerts |
| git push fails | Exit code ≠ 0 | Retry × 3 (`gh auth setup-git` → `git push`); watchdog alerts on final failure |
| Duplicate slug | articles.json already has slug | Append `-2` suffix; log warning |
| TG post fails | HTTP non-200 | Retry × 2; non-blocking — article still goes live without TG hook |

**Watchdog catches:** any step stuck `done: false` for >2h → TG alert to Marc Sir.

---

## Phase 4 — Shopify Product Integration (manual, Marc Sir)

Carousel slide images at permanent URLs (`help.xinca.com/articles/carousel/{slug}-{n}.png`). Marc Sir can manually add to shop.xinca.com product descriptions:

```html
<img src="https://help.xinca.com/articles/carousel/control-valve-hydronic-balancing-3.png" 
     alt="Valve Authority formula: β = ΔP_valve / (ΔP_valve + ΔP_circuit)" />
```

Alt text follows Shopify-GMC rules: keyword-rich, descriptive, ≤125 chars.

---

## Success Criteria

1. ✅ Carousel page at `help.xinca.com/a/control-valve-hydronic-balancing/carousel/` — 5 slides loading correctly
2. ✅ Each slide: lightbox + download PNG + copy-link
3. ✅ TG subscribe button in help.xinca.com footer
4. ✅ Dify workflow: topic → article JSON + slides JSON + TG hook posted to @hvaccontrols
5. ✅ Hermes cron: generates hero → screenshots slides → deploys → state file updated
6. ✅ Watchdog: alerts if pipeline stuck >2h
7. ✅ Marc Sir can copy-paste slides to LinkedIn in <2 minutes
8. ✅ Slug follows 3-keyword convention

---

## Timeline

| Phase | Deliverable | Est. |
|-------|------------|------|
| TG button | Footer subscribe button on help.xinca.com | 15 min |
| 1 | Carousel page (manual example) | 2h |
| 2 | Lightbox + download + screenshot pipeline | 1.5h |
| 3a | Dify app + workflow | 3h |
| 3b | Host script (state file + deploy + watchdog) | 2h |
| 3c | Cron jobs (main + watchdog) | 30 min |
| **Total** | | **~9h** |

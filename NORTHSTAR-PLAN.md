# Project Northstar — HVAC Autonomous Content-to-Commerce Pipeline

**Version:** 1.0 (Draft for Qui's feasibility review)
**Date:** 2026-07-14
**Status:** Pending Qui's gap analysis

---

## Why "Northstar"

The HVAC Knowledge Base on Dify is the knowledge north — all content research, creation, and publishing radiates from it. GA4 tracking closes the loop back to shop.xinca.com conversions. Simple, memorable, easy to reference in cron names, skills, and future sessions.

---

## Architecture Decision: Dify vs Hermes Crons

**Dify Apps = the brain** (content generation, RAG-powered synthesis, platform-aware copywriting)

**Hermes crons = the hands** (scheduling, API calls to Dify, multi-platform posting via xurl/TG Bot API/LinkedIn API, state management)

Dify Chatbot/Workflow apps are excellent for **one-shot generation** from KB context + input parameters. They are NOT schedulers, publishers, or state managers. The right architecture is:

```
Cron triggers → calls Dify App API → receives generated content → publishes to platforms
```

This means Dify replaces the **LLM reasoning** inside crons, not the crons themselves. The crons become thin shells: "fetch input → call Dify → post output." Much lighter, cheaper, and more consistent.

---

## Blockers (Fix Before Any Phase Work)

### B1. Telegram Delivery — `TELEGRAM_BOT_TOKEN` Not Set

**Root cause:** `~/.hermes/.env` has all Telegram config commented out. The gateway runs (launchd, PID 65380), but the Telegram adapter has no bot token and no home channel configured. 6 crons fail with "no delivery target resolved."

**Fix:**
1. Uncomment and set `TELEGRAM_BOT_TOKEN=...` (prime bot: @i58500hpbot — get token from @BotFather)
2. Set `TELEGRAM_HOME_CHANNEL=...` (the chat/channel ID for cron delivery — likely `-1003754936715` from `allowed_chats`)
3. Restart gateway: `hermes gateway restart`
4. Verify: `hermes gateway status` shows Telegram connected

**Until fixed:** Route social cron output to `origin` (WebUI) or `local`.

### B2. Model Pin Drift (2 crons failing every run)

**Root cause:** Auto-Post Scheduled Articles (every 30 min) and Havi Related Articles (Sat 10:00) were created with `provider=custom, model=qwen3.7-max`. Global config now has `provider=deepseek, model=deepseek-v4-pro`. Hermes' drift protection blocks the unpinned jobs.

**Fix:**
```
cronjob action=update job_id=6f1221419836 provider=deepseek model=deepseek-v4-pro
cronjob action=update job_id=70f7c071ae7c provider=deepseek model=deepseek-v4-pro
```

**Note:** Once the Dify Apps replace content generation, these crons become thin publishing shells and the model pin becomes less critical. Still fix now to stop the error loop.

### B3. Missing Env Vars

**B3a. Drive→Dify Ingestion — DIFY_DATASET_KEY**
- **Current:** Pipeline tries to push to cloud Dify (dify.ai)
- **Found:** `DIFY_DATASET_KEY=ds-VQiygcrRvbjiQ0mP3uHU5Hir` — already exists in `~/.hermes/config/dify-local.env` and works against local Dify (`http://127.0.0.1/v1`)
- **Fix:** Update `drive-dify-pipeline.sh` to source `dify-local.env` instead of the cloud config, and set `DIFY_API_BASE=http://127.0.0.1/v1`
- **Verification:** Local Dify is running (Colima, port 80). HVAC KB has 261 documents, 9.6M words, fully indexed.

**B3b. Translation Sync — NOUS_API_KEY**
- **Current:** Script expects `NOUS_API_KEY` but it's not set in `.env`
- **Available alternatives:** DeepSeek (`DEEPSEEK_API_KEY` set) and xAI (`XAI_API_KEY` set) are both available
- **Fix options:**
  - **Option A (fast):** Switch Translation Sync to use DeepSeek for translations (no new key needed)
  - **Option B (Dify):** Build a Dify Translation App — takes product data as input, translates via LLM node, outputs JSON. Cron calls Dify API instead of running the Python script directly. This is actually a good Dify fit: simple "input → translate → output" workflow.
- **Recommendation:** Fix Option A immediately (unblock the nightly sync), then migrate to Option B (Dify Translation App) in Phase 1.

### B4. Paused Crons — Merge Into Dify Apps

Marc's decision: **Yes, absorb all paused cron roles into Dify apps.**

| Paused Cron | Role | Absorbed Into |
|-------------|------|---------------|
| Content Calendar (13e691c7d56e) | Daily X+TG content posts | Havi Dify App — generates content, cron publishes |
| Havi Daily Market Scan (7b20651ba495) | Tavily HVAC scan → Wiki | Leni Dify App — research phase |
| DC Pulse Weekly Brief (cf03d02ebf24) | Leni research brief | Leni Dify App — absorbed entirely |
| HVAC-101 Content Miner (3839a7b785e2) | 3 posts/week from textbook | Havi Dify App — KB already has the textbook content |
| Helen Daily Kanban (1dbaf5b309f1) | Kanban snapshot | Keep paused (not HVAC-related, revisit separately) |

---

## Phase 1: Foundation (Week 1–2)

### 1A. Dify App: "Havi — HVAC Content Generator"

**Type:** Chatbot (NOT Chatflow — Chatflow API is broken on free tier, confirmed in dify-cloud-setup skill). Chatbot handles RAG natively via the Context panel.

**Platform:** Local Dify at `http://127.0.0.1` (Colima, Mac mini)

**KB:** HVAC KB (`a71b5439-4a43-4796-97f5-a63e102ea526`, 261 docs, 9.6M words)

**System Prompt** (migrated from existing Havi prompts):

```
You are Lady Havi, the friendly host of ai.xinca.com. You create educational HVAC content for publishing on multiple platforms.

## Voice
- Australian English spelling (-ise, -our, -re, double consonants)
- No emoji in output text
- No competitor brand names (Belimo, Honeywell, JCI, Siemens)
- No "AI-powered" claims
- Practitioner-first tone: write like a senior engineer explaining to a junior colleague

## Content Types
When given a {platform} parameter, adapt your output:

### platform=x — Short post (Hook-Punchline-CTA)
- Hook: 1 line, provocative or practical
- Punchline: 1-2 sentences of HVAC domain insight
- CTA: Link to shop.xinca.com product if relevant
- Max 280 characters (URL counts as 23 chars)
- No hashtags in body

### platform=linkedin — Long-form analyst post
- 800-1500 words
- Lead with market insight or trend data
- Include at least 2 citations from the knowledge base
- "What does this mean for your next spec/project?" framing
- Links go in first comment, not post body (LinkedIn suppresses URL reach)
- Format: clean markdown, copy-paste ready

### platform=telegram — Channel broadcast post
- 3-line hook
- Hero image description (for image_generate)
- Link to ai.xinca.com content page with UTM
- 2-3 hashtags at end, PascalCase
- TG channel is @hvaccontrols, target audience: specifiers and decision-makers

## Product Linking
When the topic maps to a product category:
- Air-side (dampers, VAV, airflow) → damper-actuators, VAV controllers
- Water-side (valves, actuators, hydronics) → control-valves, globe valves
- Controls (sensors, BMS, thermostats) → temperature sensors, flow sensors
- Always include: "See product pairing → shop.xinca.com/products/{handle}?utm_source={platform}&utm_medium=social&utm_campaign=hvac101"
- If no specific product matches, link to search: shop.xinca.com/search?q={topic}?utm_source={platform}&utm_medium=social&utm_campaign=hvac101

## Brand Guardrails
- IAQ = human health only (CO₂, VOCs, PM2.5, ventilation)
- Schneider Electric ≠ HVAC (electrical infrastructure, not air/water)
- Never compare brands by name — compare by spec
- No "authorized distributor" claims — use "ecommerce partner of authorized suppliers"
```

**Input Parameters:**
- `topic` — the HVAC topic to write about (e.g., "VAV box sizing", "CO₂ monitoring in schools")
- `platform` — one of: `x`, `linkedin`, `telegram`
- `research_brief` (optional) — Leni's curated research for context
- `product_context` (optional) — relevant products from the catalogue

**Output:** Clean markdown text — copy-paste ready, no post-processing needed. The cron that calls this app receives the text and posts it via xurl/TG Bot API/LinkedIn.

**Hero Images:** Dify cannot generate images. The publishing cron calls `image_generate` separately using the hero image description from Havi's output. This is a two-step: Dify produces the text + image prompt → cron generates the image → cron posts text + image.

### 1B. Dify App: "Leni — HVAC Research Engine"

**Type:** Chatbot app

**Platform:** Local Dify

**KB:** HVAC KB (same as Havi's, read-only)

**System Prompt** (migrated from Leni's existing prompts + leni-x-explore skill):

```
You are Leni, a research analyst specializing in HVAC, building automation, IAQ, and data centre cooling. You produce structured research briefs from multiple data sources for downstream content generation.

## Input Sources
You will receive:
1. A `curated_posts` JSON — Leni's daily X curation (16 keyword sets, 10 quality filters applied). This is pre-filtered, high-signal social content.
2. Optional `web_search_results` — Tavily or Dify web search output on trending HVAC/IAQ topics
3. Access to the HVAC Knowledge Base (261 documents, 9.6M words)

## Output: Research Brief (JSON-structured)

{
  "date": "YYYY-MM-DD",
  "generated_at": "ISO8601",
  "sections": {
    "trending_topics": [
      {"topic": "...", "signal_strength": "HIGH|MED|LOW", "sources": ["..."], "content_angles": ["..."]}
    ],
    "x_curation": {
      "total_scanned": N,
      "filtered_in": N,
      "top_posts_for_havi": [
        {"url": "...", "author": "@...", "topic": "...", "reply_angle": "...", "account": "@xincahvac|@woofaasocial"}
      ]
    },
    "linkedin_content_ideas": [
      {"title": "...", "angle": "...", "source_citations": ["..."], "target_audience": "specifiers|engineers|facility_managers"}
    ],
    "hvac101_topics": [
      {"vertical": "air|water|fluid", "topic": "...", "product_category": "..."}
    ],
    "market_intel": [
      {"insight": "...", "region": "...", "confidence": "HIGH|MED|LOW", "source": "..."}
    ]
  },
  "priority": ["ranked list of what Havi should write about today, with rationale"]
}

## Rules
- Every factual claim must carry a KB or web citation in [brackets]
- No unsourced assertions
- LinkedIn content ideas must target the specifier/decision-maker audience (market intelligence, not technician tips)
- X reply angles must be 1-2 sentences max, domain-anchored (not generic "great post!")
- Flag duplicates: if the same topic appeared in the last 7 days, mark as "REPEAT — skip or find new angle"
- Australian English spelling
```

**Input Parameters:**
- `curated_posts_json` (optional) — the pre-filtered X curation JSON from Leni's scraping pipeline
- `web_search_query` (optional) — "HVAC IAQ building automation trends this week"

**Output:** Structured JSON brief consumed by Havi's Dify App as the `research_brief` input variable.

**LinkedIn Priority Shift:** Leni's primary output format is now LinkedIn analyst posts (800-1500 words, data-backed, citation-heavy). X becomes secondary — short TL;DR threads that link to the LinkedIn deep-dive. Marc Sir posts from personal profile (4-10x reach over Company Page); Company Page gets 1 institutional reply.

### 1C. GA4 on ai.xinca.com

**Current state:** No GA4/gtag found on the Astro site.

**Action:**
1. Create GA4 property for ai.xinca.com (if one doesn't exist)
2. Add gtag.js to the Astro layout's `<head>`:
   ```html
   <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
   <script>
     window.dataLayer = window.dataLayer || [];
     function gtag(){dataLayer.push(arguments);}
     gtag('js', new Date());
     gtag('config', 'G-XXXXXXXXXX');
   </script>
   ```
3. Set up conversion events to track:
   - `click_to_shop` — all shop.xinca.com CTA clicks
   - `content_view` — article/FAQ/QA page views (with content ID)
   - `subscribe_tg` — clicks on t.me/hvaccontrols
   - `subscribe_linkedin` — clicks on LinkedIn Company Page
   - `search_query` — Fuse.js search queries on ai.xinca.com
   - `chatbot_interact` — Dify Chat Widget interactions
4. UTM parameters on all outbound links:
   - `?utm_source={platform}&utm_medium=social&utm_campaign=hvac101&utm_content={content_id}`

### 1D. Fix Translation Sync (Immediate)

**Option A (fast fix, do now):** Switch from `NOUS_API_KEY` to `DEEPSEEK_API_KEY` or `XAI_API_KEY` for translations. Both are available in `.env`.

**Option B (Phase 1):** Build a Dify Translation App:
- Input: product data (title, body_html, handle) + target locale
- LLM node translates fields
- Output: JSON with translated fields
- Cron calls Dify API instead of running the Python script directly
- This is a good Dify fit: simple deterministic pipeline

### 1E. Fix Content Pipeline (End-to-End Test)

The pipeline has never completed a full cycle (draft → approve → publish_ready → publish). Two drafts exist, four LinkedIn-ready text files, zero published.

**Fix:** Pin the Auto-Post cron (B2), then publish the two existing drafts as a full end-to-end test:
1. `ai-building-energy-management.md` → LinkedIn (long-form) + X (threaded TL;DR) + TG (hook+link)
2. `data-center-energy-efficiency.md` → same flow
3. Verify each post appears on the target platform
4. Verify GA4 tracks the clicks

---

## Phase 2: Integration (Week 2–3)

### 2A. Connect Leni → Havi Data Flow

```
Leni Dify App (research)
  ↓ outputs JSON brief to file
Hermes cron "northstar-leni-research" (daily 08:00 HKT)
  ↓ reads brief, injects as research_brief variable
Havi Dify App (content generation)
  ↓ outputs platform posts
Hermes cron "northstar-havi-generate" (daily 09:00 HKT)
  ↓ delivers drafts for Marc Sir review
Marc Sir approves
  ↓
Hermes cron "northstar-publish" (triggered)
  ↓ posts to: TG @hvaccontrols, X (@XincaHVAC/@WoofaaSocial), LinkedIn
```

### 2B. Review & Approval Workflow

1. Havi Dify App generates drafts → saved to `content-pipeline/content/drafts/YYYY-MM-DD/`
2. Marc Sir reviews in WebUI (or TG once delivery is fixed)
3. Approved → moves to `content/approved/` → `northstar-publish` cron picks up
4. Rejected → moves to `content/rejected/` with feedback note for prompt tuning

### 2C. Product Catalogue → Dify KB

**Goal:** Havi's Dify App can query for product matches when generating posts.

**Steps:**
1. Export products from Shopify Admin API (title, description, handle, tags, product_type, price)
2. Create a new Dify KB "Xinca Product Catalogue" on local Dify
3. Upload product descriptions as individual .md documents
4. Havi's system prompt includes: "When generating a post, search the Product Catalogue KB for the most relevant product. If found, include the product link."

**Fallback for Shopify collection 404s:** The hvac-101-content-machine skill documents that Shopify collection URLs can return real 404 even when collections exist. Use product-specific URLs (`/products/{handle}`) instead of collection URLs (`/collections/{slug}`).

---

## Phase 3: Autonomy + Conversion Tracking (Week 3–4)

### 3A. Cron Consolidation

**New crons to create:**

| Cron Name | Schedule | What It Does |
|-----------|----------|--------------|
| `northstar-leni-research` | Daily 08:00 HKT | Calls Leni Dify App → fetches X curation + web search → produces research brief JSON |
| `northstar-havi-generate` | Daily 09:00 HKT | Reads Leni's brief → calls Havi Dify App → generates 3 platform drafts → delivers for review |
| `northstar-publish` | On-demand trigger | Reads approved content → posts to TG/X/LinkedIn with staggered timing |
| `northstar-ga4-weekly` | Mon 09:00 HKT | Fetches GA4 metrics → produces conversion report |

**Crons to retire** (absorbed into Dify apps):

| Cron | Absorbed By |
|------|-------------|
| Content Calendar (13e691c7d56e) — paused | `northstar-havi-generate` |
| Havi Daily Market Scan (7b20651ba495) — paused | `northstar-leni-research` |
| DC Pulse Weekly Brief (cf03d02ebf24) — paused | `northstar-leni-research` |
| HVAC-101 Content Miner (3839a7b785e2) — paused | `northstar-havi-generate` |
| Havi X Shortlist (342560a585c5) — active Tue/Fri | `northstar-leni-research` (daily instead of Tue/Fri) |
| Weekly Research Brief (5396edf943ec) — active Wed | `northstar-leni-research` (daily) |
| Leni X Curation (b93ac65d8f16) — active daily | Script stays; its output feeds into Leni Dify App |
| Havi X Daily (99d6a94b30ec) — active daily | Script stays; reposting is a publishing action, not content generation |

**Crons to keep as-is:**
- Leni 10pm Wiki Ingestion (318a312bcce0)
- Havi Related Articles (70f7c071ae7c) — pin model, keep
- Auto-Post Scheduled Articles (6f1221419836) — pin model, keep (becomes thin publisher)
- Helen Daily 7AM Brief (00fb1dbdc1c5) — non-HVAC, separate concern
- All Codi maintenance crons (backup, health, updates)
- Drive→Dify Ingestion (0f9f162d2e8b) — fix env, switch to local Dify

### 3B. GA4 A/B Testing Framework

**Tests to run:**

| Test | Variable A | Variable B | Metric |
|------|-----------|-----------|--------|
| Hero image style | Notebook aesthetic (Path A) | Bro Woo + Inu Faa hand-drawn (Path B) | shop.xinca.com click-through |
| CTA placement | In-post body | End-of-post only | Conversion rate |
| TG hook style | Market intelligence (specifier voice) | Practitioner pain-point (engineer voice) | Forwards + clicks |
| Posting time | 10:00 HKT | 18:00 HKT | Engagement by platform |
| LinkedIn format | Analyst deep-dive (800-1500 words) | Shorter practitioner piece (400-600 words) | Profile views + connection requests |

**Implementation:** Each variant gets a unique `utm_content` parameter. GA4 segments by `utm_content` to compare conversion paths.

### 3C. End-to-End Autonomy Goal

**Target state:** Marc Sir's involvement is approval-only (review drafts, sign off). Everything else runs autonomously:

```
Weekly: Leni Dify App researches → brief
Daily: Havi Dify App generates → drafts
Review: Marc Sir approves → triggers publish
Hourly: Auto-Post picks up approved content → distributes to all platforms
Continuous: GA4 tracks conversions → weekly report → informs content strategy
```

**Marc Sir's touch points reduced to:**
1. Review daily drafts (5-10 min)
2. Review weekly GA4 report (5 min)
3. Strategic direction changes (as needed)

---

## Phase 4: Growth (Ongoing, Month 2+)

### 4A. TG Subscriber Acquisition (@hvaccontrols)

- Daily posts from Havi Dify App (TG format: 3-line hook + hero + link)
- Cross-promo from @XincaHVAC and @WoofaaSocial (1/week each, rotating)
- Outbound community seeding in existing TG HVAC/engineering groups
- Lady Havi as the channel's face — consistent visual branding
- **Target:** 100 subscribers Month 1, 500 Month 3, 1,000 Month 5 (TG Ads eligibility)

### 4B. LinkedIn Growth

- 2 long-form analyst posts/week from Leni's research output
- Marc Sir posts from personal profile (4-10x reach)
- 1 institutional reply from XINCA Company Page
- Target: organic growth from content quality — LinkedIn's algorithm rewards substantive, citation-heavy posts

### 4C. X Engagement

- 1-2 original posts/day from Havi Dify App
- Repost (RT) remains the primary engagement mechanic for cold accounts (reply 403 workaround)
- @mention + URL for high-value commentary
- Gradual warm-up to lift cold-reply restriction

### 4D. Conversion Funnel (The Business Goal)

```
HVAC101 Content (TG/X/LinkedIn)
  → shop.xinca.com visit (tracked via UTM)
   → product view (GA4 enhanced ecommerce event)
    → add_to_cart
     → purchase
```

**Tracked in GA4 conversion path report:** Which content types, platforms, and topics drive the most revenue.

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Local Dify goes down (Colima crash, Mac restart) | Medium | Blocks all content generation | Health-check cron monitoring; fallback to direct LLM call via cron if Dify is unreachable |
| Dify Chatbot API returns timeout on complex KB queries | Medium | Degraded content quality | Tune KB retrieval settings (top_k, score_threshold). 261 docs, 9.6M words may need chunk optimization |
| LinkedIn anti-bot blocks automated posting | High | LinkedIn content stuck | Spec-sheet pattern: Dify generates the text, Marc Sir copy-pastes manually. Full automation via LinkedIn API is unreliable |
| X cold-reply restriction persists | High | Limited engagement on X | RT-first strategy; focus on LinkedIn where outbound links don't suppress reach |
| Product catalogue KB falls out of sync with Shopify | Medium | Wrong product links | Weekly sync cron: Shopify API → Dify KB update |
| GA4 data lag (24-48h for conversion paths) | Low | Delayed feedback on A/B tests | Weekly reports only (not daily); accept lag for strategic decisions |
| Dify app prompts drift from skill files | Medium | Inconsistent output | Single source of truth: Dify app system prompt is the canonical version. Update the corresponding Hermes skill to reference the Dify app, not duplicate |

---

## Migration Checklist

- [ ] B1: Set TELEGRAM_BOT_TOKEN in .env, restart gateway
- [ ] B2: Pin model on jobs 6f1221419836 and 70f7c071ae7c
- [ ] B3a: Switch Drive→Dify to local Dify (source diffy-local.env)
- [ ] B3b: Fix Translation Sync (switch to DeepSeek key)
- [ ] B4: Decision recorded — merge paused crons into Dify apps
- [ ] 1A: Create Havi Dify App on local Dify (Chatbot type, link HVAC KB)
- [ ] 1B: Create Leni Dify App on local Dify (Chatbot type, link HVAC KB)
- [ ] 1C: Add GA4 to ai.xinca.com Astro site
- [ ] 1D: Build Dify Translation App (or fix script with alternative key)
- [ ] 1E: Publish 2 existing drafts as end-to-end test
- [ ] 2A: Build Leni→Havi data flow cron
- [ ] 2B: Set up approval workflow (drafts → review → approved → publish)
- [ ] 2C: Ingest product catalogue into Dify KB
- [ ] 3A: Create new crons, retire absorbed ones
- [ ] 3B: Configure GA4 conversion events + UTM parameters
- [ ] 3C: First weekly GA4 report
- [ ] 4A-D: Growth phase (subscriber acquisition, A/B testing, conversion funnel)

---

## Qui's Review Questions

1. **Dify Chatbot API reliability:** The HVAC KB has 261 documents with hybrid search + reranking. Will the Chatbot API return fast enough for cron-scheduled generation? Is there a risk of timeout?

2. **Leni → Havi data handoff:** The plan passes a JSON brief between apps. Is Dify's variable injection robust enough for structured JSON? Or should we use a file-based bridge (write JSON → cron reads → passes as string)?

3. **Product catalogue KB sync:** How to keep the Dify "Xinca Product Catalogue" KB in sync with Shopify? Manual upload is not sustainable for 200+ products. Is there a Dify API for programmatic document upsert?

4. **Hero image generation:** Dify cannot generate images. The plan splits this into a two-step cron (Dify → text + image prompt → `image_generate`). Is there a smoother integration? Could the Dify app output be piped directly into an image_gen pipeline?

5. **Content recycling detection:** The HVAC101 Content Miner had a known issue with repeating sources. Dify's KB retrieval may surface the same documents repeatedly. How to implement "don't use this source again this month" deduplication?

6. **Cost comparison:** Dify API calls vs direct LLM calls through Hermes crons. Is routing through Dify cheaper (no Hermes agent loop overhead) or more expensive (extra API call)?

7. **Fallback design:** If local Dify is unreachable, should the cron fall back to direct LLM generation via Hermes? Or stop and alert?

8. **Translation as Dify App:** The Translation Sync script is ~740 lines of Python with Shopify GraphQL integration. Can a Dify workflow replicate this complexity (GraphQL queries, pagination, locale-aware field mapping)? Or is the script + DeepSeek key fix simpler and more reliable?

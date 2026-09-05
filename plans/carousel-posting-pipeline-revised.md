# Carousel Article Posting Pipeline — Revised Plan
**Date:** 2026-07-28  
**Author:** Hermes (Helen)  
**Review:** Codi + Qui  

---

## Context

Gemini suggested a LinkedIn PDF Carousel method (5-7 slides, 1080×1350 vertical) for the control valve article. Marc Sir wants:
1. 3-6 slides (not 5-7)
2. Carousel hosted on help.xinca.com first (brand-controlled surface)
3. Lightbox/download links for visitors AND Marc Sir's copy-paste workflow
4. A reusable Dify pipeline, starting from Leni's topic research → Havi article creation → carousel generation → deploy → TG ping

---

## Phase 1 — Carousel Page: Manual Example (Hermes builds, ~2h)

**Goal:** Ship a working carousel for the control valve article as the proof-of-concept.

**Deliverable:** `help.xinca.com/a/water-side-control-valve-selection/carousel/` — 5 vertical slides stacked on a page.

**Slide Spec:**
- Format: 1080×1350px vertical card
- Rendering: HTML/CSS (NOT AI image gen — formulas/tables can't be hallucinated)
- Brand: XINCA teal (#7EBEC5), dark navy (#0a1628), Lady Havi CTA on last slide
- Each slide is a self-contained `infocard`-style card

**5 Slides (curated from Gemini's suggestion):**

| # | Type | Content |
|---|------|---------|
| 1 | Hook | "5 Pitfalls in Water-Side Control Valve Selection" → "And how they sabotage your energy savings" |
| 2 | Problem | "Size by Connection Pipe Size is Wrong" — visual pipe≠valve comparison; authority concept |
| 3 | Concept | Valve Authority formula β = ΔP_valve / (ΔP_valve + ΔP_circuit); target β > 0.3 |
| 4 | Comparison | Globe vs Ball vs PICV — simplified table; Equal Percentage focus |
| 5 | CTA | "Ready to optimise your hydronic balancing?" + help.xinca.com logo + Lady Havi |

**Implementation:**
1. Create `src/pages/a/water-side-control-valve-selection/carousel.astro` — Astro page
2. Each slide: HTML `<div>` with aspect-ratio: 1080/1350, styled with infocard patterns
3. Social share OG tags for X/LinkedIn preview
4. `npm run build` → deploy to gh-pages → verify with cache-bust

---

## Phase 2 — Lightbox + Download Links (Hermes builds, ~1h)

**Goal:** Each slide has a lightbox viewer + individual download, plus full PDF export.

**Per-Slide:**
- Click to open lightbox (full-res 1080×1350 view)
- "Download Slide" button → saves PNG
- "Copy for LinkedIn" → copies image URL

**Page-Level:**
- "Download All Slides (PDF)" → combines all slides into one PDF
- "Download All Slides (ZIP)" → zips individual PNGs

**Image Generation:**
- Browser screenshot each slide at 1080×1350 viewport
- Save to `public/articles/carousel/control-valve-{n}.png`
- These permanent URLs are the "copy-paste" assets for LinkedIn/X

**Shopify Integration (manual):**
- Marc Sir can manually add carousel images to shop.xinca.com product descriptions via `src` URL from help.xinca.com

---

## Phase 3 — Dify Workflow (Automated Pipeline, ~4h)

**Architecture:** Dify handles LLM reasoning (research → article → carousel content). Hermes cron + host scripts handle image generation, deployment, and TG notification.

```
┌─────────────────────────────────────────────────────────┐
│                    HERMES CRON (Host)                    │
│  Schedules + deploys + notifies                         │
└─────────────────────────────────────────────────────────┘
         │ trigger                    │ deploy + notify
         ▼                            ▼
┌─────────────────────┐    ┌──────────────────────────┐
│   DIFY WORKFLOW     │    │   help.xinca.com DEPLOY    │
│   (LLM reasoning)   │    │   + TG @hvaccontrols     │
└─────────────────────┘    └──────────────────────────┘
```

### Workflow Trigger Options

**Option A: Hermes Cron → Dify API (RECOMMENDED)**
- Hermes cron fires weekly → calls Dify `/v1/workflows/run` with topic as input
- Survives Colima restarts, detectable failures, retry-capable
- Proven pattern: `leni-dify-research-cron.sh` with self-healing

**Option B: Dify Schedule Trigger (`trigger-schedule` node)**
- Dify v1.15+ has built-in `trigger-schedule` node (Celery Beat cron)
- **Caveat:** If Colima/container is down at trigger time → execution missed with NO catch-up
- Acceptable as secondary trigger, not primary

**Decision:** Option A as primary. Option B as convenience fallback for when the stack is healthy.

### Workflow Nodes

```
[Start: topic = Leni's keyword / trending theme]
    │
    ▼
[LLM: Havi — Write Full Article]
  - Persona: Lady Havi, HVAC domain expert
  - Output: 800-1500 word article with: title, description, 
    body (h2/h3), tables, citations, CTA
  - Australian English, XINCA brand voice
  - KB-enriched via HVAC KB (a71b5439)
    │
    ▼
[LLM: Havi — Generate Hero Image Prompt]
  - Notebook-style hero prompt (matching existing brand style)
  - Output: detailed image_gen prompt
    │
    ▼
[LLM: Havi — Generate 3-6 Carousel Slides]
  - Input: article content
  - Output: JSON array of slides with:
    {type, title, key_point, visual_description, layout_hint}
  - Slide types: hook, problem, concept, comparison, CTA
    │
    ▼
[Code Node: Validate]
  - Slide count: 3-6
  - Title ≤8 words, key_point ≤25 words
  - No competitor names
    │
    ▼
[Answer Node: Output JSON]
  - Article JSON + slides JSON + hero image prompt
```

### Host-Side Script (Hermes Cron)

```
cron: "Weekly Carousel Article" (e.g., Mon 06:00 HKT)

1. Pick topic: from Leni's Mon research brief OR Marc Sir manual input
2. Call Dify workflow → get article + slides JSON
3. Generate hero image: FAL.ai via image_generate (reference existing notebook style)
4. Create Astro page: src/pages/a/{slug}.astro using ai-xinca-content template
5. Render carousel slides as HTML: src/pages/a/{slug}/carousel.astro
6. Screenshot slides: browser at 1080×1350 → public/articles/carousel/{slug}-{n}.png
7. Build + deploy: npm run build → git push gh-pages + master
8. Notify: TG message to @hvaccontrols
   "New article published: {title}
   help.xinca.com/a/{slug}/
   Carousel slides: help.xinca.com/a/{slug}/carousel/
   Ready for LinkedIn/X posting. Review + approve?"
```

### Integration Points

| Step | Runs In | Tool |
|------|---------|------|
| Topic research | Hermes cron (existing) | Leni: xurl search + Dify enrichment |
| Article writing | Dify | Havi LLM (deepseek-v4-pro) |
| Carousel content | Dify | Havi LLM |
| Hero image gen | Hermes | FAL.ai via image_generate |
| Slide image capture | Hermes | Browser screenshot |
| Deploy to help.xinca.com | Hermes | git push + npm build |
| TG notification | Hermes | curl to TG Bot API |

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Slide rendering | HTML/CSS, NOT AI image gen | Formulas, tables, text must be accurate |
| Image capture | Browser screenshot at 1080×1350 | Reliable text; no hallucination |
| Slide count | 5 (default), 3-6 range | Marc Sir prefers 3-6; 5 is sweet spot |
| Article model | deepseek-v4-pro | No Gemini/Claude (geo-banned HK) |
| Schedule trigger | Hermes cron primary, Dify Schedule secondary | Colima restarts lose Dify-only triggers |
| KB enrichment | HVAC KB (a71b5439) | Domain context for Havi's writing |
| TG channel | @hvaccontrols (via @olilo2bot) | Existing channel, Marc Sir monitors |

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Formulas render poorly in screenshots | Unicode math + CSS; test before final |
| Dify workflow timeout (article writing) | Split into multiple LLM nodes; 15s Code node limit is the real constraint |
| Cloudflare caches stale carousel | Cache-bust with `?v=N` param |
| FAL.ai hero image doesn't match notebook style | Use reference image from existing article heros |
| Slide images too large for LinkedIn | Compress PNG to <500KB; test upload |
| Colima down → Dify Schedule misses trigger | Hermes cron is the primary; Dify Schedule is secondary only |

---

## Timeline

| Phase | Deliverable | Est. Time |
|-------|------------|-----------|
| 1 | Carousel page (manual example) | 2h |
| 2 | Lightbox + download links | 1h |
| 3a | Dify workflow (article + carousel) | 3h |
| 3b | Host script (deploy + notify) | 1h |
| 3c | Cron job + testing | 1h |
| **Total** | | **~8h** |

---

## Success Criteria

1. Carousel page at `help.xinca.com/a/water-side-control-valve-selection/carousel/` loads 5 slides correctly
2. Each slide has lightbox + download + copy-link
3. Dify workflow accepts topic → outputs article + carousel JSON
4. Cron job: topic → deploy → TG ping on @hvaccontrols
5. Marc Sir can copy-paste slide images to LinkedIn Document Post in <2 minutes

# Qui Qualification Review — Carousel Article Posting Pipeline (Revised Plan)
**Date:** 2026-07-28
**Plan:** `/Users/marcsir/workspace/content-pipeline/plans/carousel-posting-pipeline-revised.md`
**Status:** 🔴 Escalate

---

## Executive Summary

The plan has sound architecture (Dify for generation, Hermes for orchestration, HTML/CSS for rendering) and passes all **brand compliance** checks (no competitor names, no emoji, no "AI-powered", no American English spelling, no "authorised distributor" framing). However, it has **six blocking gaps** that prevent autonomous execution: no human review gate, zero error handling in the 8-step host script, an underspecified Phase 2 download implementation, a missing KB retrieval node in the Dify workflow, slide count hardcoded to 5 despite Marc Sir's 3–6 mandate, and no slug-collision detection. These must be resolved before any Phase 3 automation work begins. Phases 1–2 can proceed with the warnings patched.

---

## Focus Area Verdicts

| Focus Area | Verdict | Key Issue |
|------------|---------|-----------|
| Brand Compliance (competitor names, emoji, spelling, framing) | 🟢 Proceed | Clean — no violations found |
| Slide Count Compliance (3–6) | 🔴 Blocking | Hardcoded to 5 in deliverables; 3–6 range acknowledged but not enforced in output |
| Phase 1 — Manual Carousel Example | 🟡 Patch Then Proceed | 3 warnings (Cv in table, avatar path, naming inconsistency) |
| Phase 2 — Lightbox + Download | 🔴 Blocking | 1h estimate is unrealistic; no library/pattern specified for ZIP + PDF |
| Phase 3 — Dify Workflow Automation | 🔴 Blocking | 4 blockers (no review gate, no error handling, missing KB node, no slug dedup) |
| ChatWidget / CTA Honesty | 🟢 Proceed | CTA doesn't promise AI; no violation |
| Shopify GMC Implications | 🟡 Conditional | Plan mentions product image reuse but ignores alt text / GMC feed compliance |
| User Experience (download flow, TG notification) | 🟡 Conditional | Download UX underspecified; TG notification too verbose for Marc Sir |

---

## Detailed Findings

### 1. 🔴 BLOCKING — No Human Review Gate Before Deployment
**Location:** Lines 140–155 (Host-Side Script)
**Evidence:** The pipeline goes: topic → Dify → deploy → TG ping. The TG message (line 154) says "Review + approve?" but the content is already **live** on help.xinca.com at that point. Marc Sir cannot review before publication.
**Impact:** A hallucinated formula, incorrect valve spec, or misattributed citation goes live without human inspection. For HVAC engineering content with actual formulas (β = ΔP_valve / …), this is a reputational risk.
**Fix:** Insert a staging step: deploy to a `/staging/` subpath, TG-ping Marc Sir with the staging URL for approval, then promote to production on his signal. Or: generate + screenshot slides locally, TG-ping with attached preview PNGs for approval, THEN deploy.

### 2. 🔴 BLOCKING — Zero Error Handling in 8-Step Host Script
**Location:** Lines 140–155
**Evidence:** Eight sequential steps with no error handling, no retry logic, no dead-letter queue, no rollback:
1. Pick topic — no fallback if Leni's research brief is empty
2. Call Dify — no retry on timeout/500
3. Generate hero image — no handling for FAL safety filter rejection
4. Create Astro page — no handling for template rendering failure
5. Render carousel slides — no handling for missing slide data
6. Screenshot slides — no handling for browser crash / render timeout
7. Build + deploy — no handling for git push failure mid-push
8. TG notification — no handling for bot API failure

**Impact:** Any single step failure silently aborts the pipeline with no alert. Marc Sir won't know a scheduled article was skipped until he checks manually.
**Fix:** Wrap each step in a try/catch or `||` fallback. On failure, log the error, skip remaining steps, and send a TG error notice. Add a retry counter at the Dify call level.

### 3. 🔴 BLOCKING — Phase 2 Download Implementation Underspecified
**Location:** Lines 48–68
**Evidence:** The plan promises in 1 hour:
- Lightbox viewer per slide
- "Download Slide" → PNG (requires Canvas API + `toBlob()` or server-side conversion)
- "Copy for LinkedIn" → copies image URL
- "Download All Slides (PDF)" → requires jsPDF or server-side PDF assembly
- "Download All Slides (ZIP)" → requires JSZip or server-side archive

No library is named. No implementation approach is specified. The current carousel page is Astro (static HTML). Client-side ZIP + PDF generation with JSZip + jsPDF is non-trivial — conservatively 4–6 hours for production quality, not 1 hour.
**Impact:** Phase 2 will run over budget by 3–5×, blocking Phase 3 start.
**Fix:** Either (a) scope Phase 2 to server-side PNG generation only (skip ZIP/PDF for v1), (b) extend estimate to 4h and specify JSZip + jsPDF approach, or (c) use a simple `<a download>` per slide with the pre-generated PNG URLs (fastest, 90% of the value).

### 4. 🔴 BLOCKING — Dify Workflow Missing KB Retrieval Node
**Location:** Line 113 vs workflow diagram (lines 104–136)
**Evidence:** Line 113 claims "KB-enriched via HVAC KB (a71b5439)". The workflow diagram shows:
```
[Start] → [LLM: Havi — Write Full Article] → [LLM: Hero Image Prompt] → [LLM: Carousel Slides] → [Code Node: Validate] → [Answer]
```
There is **no knowledge retrieval node** between Start and the first LLM node. The LLM has no way to access KB context. In Dify, a Knowledge Retrieval node must precede any LLM node that needs RAG.
**Impact:** Havi writes articles from training data only — no XINCA-specific domain context, no product references, no previously published article cross-links. The "KB-enriched" claim is vaporware.
**Fix:** Insert a Dify Knowledge Retrieval node after Start, querying the HVAC KB (dataset a71b5439) with the topic as input. Pass retrieved chunks as context to the first LLM node.

### 5. 🔴 BLOCKING — Slide Count Hardcoded to 5 Despite 3–6 Mandate
**Location:** Lines 22, 30, 177, 213
**Evidence:**
- Line 22: "5 vertical slides stacked on a page" (deliverable)
- Line 30: "**5 Slides** (curated from Gemini's suggestion):" (table header)
- Line 177: "Slide count: 5 (default), 3-6 range" (acknowledges range but hardcodes 5)
- Line 213: "loads 5 slides correctly" (success criterion)

Marc Sir explicitly said 3–6 (line 11). The `social-carousel` skill's table supports 3–6 with slide 6 as optional Bonus. The plan should NOT hardcode a count — it should derive the count from available content.
**Impact:** If a future article only has 3 formula/table-worthy points, the pipeline will either force-thin slides 4–5 or fail validation. If an article has 6 strong points, slide 6 gets dropped.
**Fix:** Remove all hardcoded "5" references. Use "3–6" throughout. The Phase 1 example can still be 5 slides for this specific article, but label it "Example: 5 slides" not "5 Slides" as a fixed spec.

### 6. 🔴 BLOCKING — No Slug Collision / Duplicate Detection
**Location:** Entire plan
**Evidence:** The host script (step 4) creates `src/pages/a/{slug}.astro`. If the cron picks a topic that was already published (or Leni suggests a duplicate), it will overwrite the existing article with no warning.
**Impact:** Existing article content silently replaced. Broken internal links from other articles' "Related Articles" sections. SEO ranking loss.
**Fix:** Before step 4, check `src/data/articles.json` for existing slug. If exists, skip and log. Alternatively, add a `--force` flag for intentional overwrites.

---

### 7. 🟡 CONDITIONAL — XINCA Framing Not Specified in Dify Prompt
**Location:** Lines 108–113
**Evidence:** The Dify LLM prompt says "Australian English, XINCA brand voice" but does not include the specific rule: XINCA is the "ecommerce partner of authorised supplier" — **not** "authorised distributor." Without this in the prompt, LLMs default to "authorised distributor" language which is factually incorrect.
**Impact:** Generated articles may contain wrong legal framing.
**Fix:** Add to the LLM prompt: "XINCA is the ecommerce partner of authorised HVAC suppliers, not an authorised distributor. Never use 'authorised distributor' or similar language."

### 8. 🟡 CONDITIONAL — Lady Havi Avatar File Path Not Specified
**Location:** Line 38 (Slide 5 CTA)
**Evidence:** The CTA slide says "+ Lady Havi" but doesn't specify which avatar image to use. The `social-carousel` reference says "Lady Havi avatar (bottom-right)" but no file path.
**Impact:** Implementer may use emoji or wrong image. User instructions say "use real avatar JPGs, never emoji."
**Fix:** Specify path like `/articles/havi-avatar.jpg` or identify the canonical avatar file in `public/articles/`.

### 9. 🟡 CONDITIONAL — TG Notification Too Verbose for Marc Sir
**Location:** Lines 151–154
**Evidence:** The TG notification says:
```
New article published: {title}
help.xinca.com/a/{slug}/
Carousel slides: help.xinca.com/a/{slug}/carousel/
Ready for LinkedIn/X posting. Review + approve?
```
Marc Sir's auto-preference is "terse — no narration." The question "Review + approve?" and the preamble "Ready for…" are narration.
**Impact:** Minor annoyance; Marc Sir skips reading verbose messages.
**Fix:** Condense to:
```
{title}
help.xinca.com/a/{slug}/
🖼 carousel: help.xinca.com/a/{slug}/carousel/
```
Wait — no emoji. Use:
```
{title}
a/{slug}/
slides: a/{slug}/carousel/
```

### 10. 🟡 CONDITIONAL — Image File Naming Inconsistency
**Location:** Line 63 vs 148
**Evidence:** Phase 1 says `control-valve-{n}.png` (hardcoded slug). Phase 3 says `{slug}-{n}.png` (parameterised). Inconsistent pattern.
**Impact:** If Phase 1 is used as template for Phase 3, naming will differ.
**Fix:** Standardise on `{slug}-carousel-{n}.png` (as used in social-carousel skill and OG tag example).

### 11. 🟡 CONDITIONAL — No Social Caption Generation in Pipeline
**Location:** Phase 3 host script (lines 140–155)
**Evidence:** The pipeline generates article + carousel slides but does NOT generate LinkedIn post text, X thread text, or TG channel caption. The `social-carousel` skill has templates for all three. Marc Sir's success criterion (line 217) is "copy-paste slide images to LinkedIn Document Post in <2 minutes" — having the caption pre-generated is essential to hit this.
**Impact:** Marc Sir must manually write captions, defeating the "<2 minutes" success criterion.
**Fix:** Add a Dify LLM node or host-side step to generate social captions alongside the article. Feed them into the TG notification or save them to the carousel page.

### 12. 🟡 CONDITIONAL — Shopify GMC Image Implications Ignored
**Location:** Lines 67–68
**Evidence:** Plan says "Marc Sir can manually add carousel images to shop.xinca.com product descriptions via `src` URL from help.xinca.com." No mention of:
- Alt text requirements for GMC feed compliance
- Image dimensions (GMC has minimum 100×100, recommended 800×800)
- Whether carousel PNGs at 1080×1350 are appropriate for product pages
- SEO implications of hotlinking images from a different domain
**Impact:** If carousel images are added to product pages without proper alt text, GMC may disapprove products. 1080×1350 portrait images may break product page layouts.
**Fix:** If this integration is pursued, create 1:1 cropped versions for product pages with SEO-friendly alt text. Document alt text format in the plan.

### 13. 🟡 CONDITIONAL — Hermes Cron Reliability When Colima/Dify Is Down
**Location:** Lines 90–100
**Evidence:** The plan correctly identifies that Option B (Dify Schedule) fails silently when Colima is down. But Option A (Hermes cron) depends on Dify being reachable at step 2 — if Dify is down when the cron fires, the pipeline still fails. The plan doesn't address this.
**Impact:** Cron fires, Dify API returns 502, pipeline aborts, no article published that week. No retry.
**Fix:** Add a retry loop (3 attempts, 5-minute backoff) at the Dify API call step. If all retries fail, send a TG error alert and record the failed topic for next week's run.

### 14. 🟡 CONDITIONAL — Cloudflare Cache-Bust Mechanism Underspecified
**Location:** Line 191
**Evidence:** "Cache-bust with `?v=N` param" — no explanation of how N is generated, how it propagates to TG links and social posts, or how N is prevented from colliding.
**Impact:** If `?v=N` is not consistently applied across all references, Marc Sir or social viewers may see stale content.
**Fix:** Use timestamp: `?v=20260728` (date-based). Ensure all generated links (TG notification, social captions) include the param.

---

### 15. 🟢 ADVISORY — No Content Decay / Recycling Strategy
**Location:** Not addressed
**Evidence:** No plan for what happens when a carousel is reposted months later. Does the pipeline regenerate with fresh hooks? Does it detect that the article was already carousel-ed?
**Fix:** Track carousel generation in `articles.json` with a `carousel_date` field. On re-trigger, compare dates and regenerate if >90 days old.

### 16. 🟢 ADVISORY — No Emergency Pause / Post-Retraction Workflow
**Location:** Not addressed
**Evidence:** If an error is discovered in a published carousel (wrong formula, competitor name slip), there's no documented process to take down or correct the carousel page.
**Fix:** Document: "To retract: delete `src/pages/a/{slug}/carousel.astro`, rebuild, redeploy. To fix: correct source, rebuild, redeploy with cache-bust."

### 17. 🟢 ADVISORY — No GA4 / Analytics Tracking
**Location:** Not addressed
**Evidence:** No mention of tracking carousel page views, slide downloads, or click-through to the main article. The carousel is a conversion funnel for LinkedIn → help.xinca.com → shop.xinca.com.
**Fix:** Add GA4 `gtag` events for: `carousel_view`, `slide_download`, `cta_click`.

### 18. 🟢 ADVISORY — Deploy Script Reference Missing
**Location:** Line 44, 149
**Evidence:** Plan says "`npm run build` → deploy to gh-pages → verify with cache-bust." ai-xinca-content-publishing skill documents a `scripts/deploy.sh` at `npm run deploy` that handles build + gh-pages push + commit + GSC ping. The plan should reference this.
**Fix:** Change "`npm run build` → deploy" to "`npm run deploy`" and reference the existing deploy script.

### 19. 🟢 ADVISORY — Slide 4 References "Globe vs Ball vs PICV" — Check for Cv Formula Context
**Location:** Line 37
**Evidence:** Slide 4 says "Globe vs Ball vs PICV — simplified table; Equal Percentage focus." The `social-carousel` worked example uses "Globe Valve vs PICV" (3 columns, 4 rows). "Ball" valves are less common in hydronic control — verify this is intentional vs a Gemini hallucination.
**Impact:** Low — the content is for the manual Phase 1 example, not automated. But worth flagging for accuracy review.

---

## Implementation Status vs. Plan

| Item | Plan Claims | Actual State | Gap |
|------|-------------|--------------|-----|
| KB enrichment in Dify | "KB-enriched via HVAC KB (a71b5439)" | No Knowledge Retrieval node in workflow diagram | 🔴 |
| Phase 2 in 1 hour | "Lightbox + download links (~1h)" | ZIP + PDF generation requires JSZip + jsPDF; no library specified | 🔴 |
| Error handling | (none claimed) | 8 sequential steps, zero try/catch or retry | 🔴 |
| Slide count = 5 | Default 5, range 3-6 | Hardcoded to 5 in deliverables and success criteria | 🔴 |
| Deploy mechanism | "npm run build → deploy to gh-pages" | Deploy script exists at `npm run deploy` | 🟢 |
| ChatWidget honesty | CTA says "Ready to optimise…" | No AI chatbot promise — accurate | 🟢 |
| Competitor names | No violations | Verified: 0 hits for Belimo/Honeywell/JCI/Siemens | 🟢 |
| Australian English | Compliant | Verified: 0 American spelling hits | 🟢 |
| Emoji | Compliant | Verified: 0 emoji in plan | 🟢 |
| "AI-powered" language | Compliant | Verified: 0 hits | 🟢 |
| "Authorised distributor" | Compliant | Verified: 0 hits | 🟢 |
| "Coming soon" language | Compliant | Verified: 0 hits | 🟢 |

---

## Verdict & Recommendations

### 🔴 Phase 3: Dify Workflow Automation — BLOCKED
**Required before execution:**
1. Insert Dify Knowledge Retrieval node (a71b5439) before the first LLM node
2. Add human review staging step (staging deploy → TG approval → production promote)
3. Add error handling + retry to all 8 host-script steps
4. Add slug collision check before article creation
5. Remove all hardcoded "5 slides" references; parameterise to 3–6

### 🟡 Phase 2: Lightbox + Download — PATCH THEN PROCEED
**Required before execution:**
1. Specify JSZip + jsPDF approach OR descope ZIP/PDF to v2
2. Extend estimate to 4h if keeping full scope
3. Standardise image file naming to `{slug}-carousel-{n}.png`

### 🟡 Phase 1: Manual Carousel Example — PATCH THEN PROCEED
**Required before execution:**
1. Specify Lady Havi avatar file path
2. Label as "Example: 5 slides for control valve article" (not a fixed spec)
3. Add XINCA framing rule to Dify prompt templates used for content

---

## Brand Boundary Cross-Reference Audit

| Rule | Regex | Hits in Plan | Severity |
|------|-------|-------------|----------|
| No competitor names | `Belimo|Honeywell|JCI|Siemens|Johnson Controls|Schneider` | **0** | ✅ |
| Australian English only | `\borganize\b|\bcolor\b|\bfavor\b|authorized|realized` | **0** | ✅ |
| No AI-powered language | `AI.powered|AI Powered|ai-powered` | **0** | ✅ |
| No "authorised distributor" | `authori[sz]ed distributor` | **0** | ✅ |
| No emoji | Unicode emoji range | **0** | ✅ |
| No "coming soon" | `coming soon` | **0** | ✅ |
| No counts ("50+", etc.) | `\b\d+\+` (false positive on "v1.15+" — OK) | **0** real | ✅ |
| XINCA ecommerce partner framing | `ecommerce partner|authorised supplier` | **0** (rule not in plan) | 🟡 |

**Verdict:** The plan is clean on prohibitive rules but **does not proactively include** the correct "ecommerce partner of authorised supplier" framing — it only avoids the wrong one. This must be added to the Dify LLM prompt.

---

**Signed:** Qui (QA Auditor)
**Recommendation to Marc Sir:** Block Phase 3 automation until the 6 blocking gaps are resolved. Phase 1–2 can proceed with warnings patched. The architecture is sound; the execution details need hardening.

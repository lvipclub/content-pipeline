# Ghost-draft audit — 2026-10-03 (content-auto-poster cron tick)

Tick result: **no due articles** — `.pipeline_state.json` has 0 `approved` entries (42 published, 27 draft).

## True ghost drafts (pitfall 15 — approved/ files with zero state registration)

- `content/approved/x-xincahvac-20260813.md` — "Data centre cooling — supply temperature, aisle
  containment & ASHRAE TC 9.9 thermal envelopes" (Thu 13 Aug 2026). Header says "Flagged for Marc
  Sir approval." Never registered in `.pipeline_state.json`, absent from `.publish_log.json`.
- `content/approved/telegram-hvaccontrols-20260813.md` — TG companion of the same piece. Same
  status: unregistered, unpublished.

Both are 7+ weeks stale and superseded in topic by the Northstar Sep 19 aisle-containment cluster
(`*-dc-aisle-containment-2026-09-19`, status: draft, awaiting approval). No schedule entry exists
for either file, so the auto-poster correctly never picked them up.

## Not ghosts (verified against state)

- `telegram-hvaccontrols-{airflow-measurement,co2-monitoring,energy-efficiency,iaq-monitoring}.md`,
  `x-xincahvac-{airflow-measurement,co2-monitoring}.md`, `x-woofaasocial-{co2-dcv,energy-efficiency}.md`
  — legacy copies of content state tracks as `published` under different slugs
  (e.g. `2026-08-01-airflow-measurement`, `2026-08-03-co2-monitoring`, early July batch).
  State status is the authoritative published/dedup signal (skill pitfall 13).

## Recommended disposition (for orchestrator / Marc decision)

- Delete the two 20260813 files, or register + approve them if the piece is still wanted as a
  distinct post (note: overlaps Sep 19 draft topic; likely delete).
- Optionally refile the legacy copies under an `approved/archive/` subdir to keep `approved/`
  meaning "pending publication" only.

No action was taken by the auto-poster beyond this note.

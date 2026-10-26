---
project: caliCortado
status: legacy
status_reason: Replaced by meowmery, a smaller second-brain plan (owner decision in chat, 2026-10-23; not yet in the runbook)
resume_trigger: n/a. Don't resume; reuse parts from meowmery if needed
last_activity: 2026-10-01
last_reviewed: 2026-10-23
repo: https://github.com/purrMonster/caliCortado
related: ["[[meowmery]]", "[[purrbrews-containers]]", "[[luwak]]"]
tags: [project]
---

# caliCortado

## What it is
The first second-brain plan: Obsidian on iPhone and Mac, with encrypted self-hosted sync, reliable capture, tested recovery, private remote access, direct search and cited local AI answers. Every layer (data, embeddings/retrieval, inference, display) was planned to deploy independently behind its own Traefik domain. Stack: Python 3.12 offline tooling, OpenAPI contracts, Docker Compose fixtures; LiveSync/CouchDB proposed for sync.

## Current state
| Area | State | Evidence |
|---|---|---|
| Plan | 12 epics, 50 stories, 8 sprints | [plan.md](plan.md), [map.md](map.md) |
| Code | Partial: offline foundation, 7 API contracts, domain-API drafts and a sync compatibility harness; no product service | [calicortado/](calicortado/), [contracts/](contracts/), [examples/](examples/) |
| Release | None (no tags or images) | `git tag` is empty |
| Deployment | Not deployed | [README](README.md) "no services have been deployed" |
| Tests / CI | 28 tests and doc/contract checks pass locally (`python3 tools/check.py`, rerun 2026-10-23); no CI | [runbook 2026-10-01](runbook.md#2026-10-01--local-sync-compatibility-investigation--cal-009) |
| Sync evidence | Headless encrypted LiveSync peer passed 9 upstream tests and 6 integration checks through Traefik; filesystem bridge, restart, conflicts and devices untested | [docs/operations/sync.md](docs/operations/sync.md) |

## Open points
Kept for the record. None of these get done unless meowmery needs them.
- CAL-005: live DNS relocation and probe never activated; drafts only ([LIVE-RELOCATION.md](examples/domain-api/LIVE-RELOCATION.md)).
- CAL-009: filesystem bridge with restart, rename/delete and wrong-key checks never built.
- CAL-007: production identity never decided; fixtures use temporary BasicAuth.
- The Vikunja board (62 tasks) still shows CAL-005 and CAL-009 as In progress.
- The owner's local Windows checkout shows line-ending-only changes on every file (CRLF); no `.gitattributes` exists.

## Branches
- None besides `main`.

## Key decisions
- 2026-09-26 · Calicortado is the second brain; all other scope removed · [runbook](runbook.md#2026-09-26--calicortado-is-the-second-brain)
- 2026-09-26 · Backlog of 12 epics/50 stories with independently deployable layers · [runbook](runbook.md#2026-09-26--sprint-backlog-and-independently-deployable-product-layers)
- 2026-09-27 · E01 foundation (scope, inventory, offline workspace, contracts) · [runbook](runbook.md#2026-09-27--e01-foundation-started)
- 2026-09-29 · All infrastructure preparation stays here until deployment readiness · [runbook](runbook.md#2026-09-29--keep-all-preparation-in-calicortado--cal-005)
- 2026-10-01 · Pin the upstream LiveSync bridge rather than writing a custom sync · [runbook](runbook.md#2026-10-01--local-sync-compatibility-investigation--cal-009)

## How to resume
Don't resume. Close it out instead:
1. Merge this card.
2. Add a final runbook entry recording the 2026-10-23 replacement by meowmery.
3. Close CAL-005 and CAL-009 on the Vikunja board as won't-do, or archive the board.
4. Archive this repository on GitHub.
5. If meowmery adopts Obsidian LiveSync, start from [examples/sync-compat](examples/sync-compat/README.md) and its version matrix.

## Decisions to remake
- The whole delivery shape: per-layer domains, a separate-machine relocation test and identity gates before anything was usable. That ceremony is why the project stalled. meowmery starts from a vault plus a dashboard instead.
- Sync: LiveSync + plain-file bridge versus git-based Obsidian sync. meowmery's current plan is git.

## Questions for Roastmaster
- Archive the repo now, or after meowmery's first milestone is running?
- Keep the Vikunja project for reference, or delete it?
- Should the plain-language proposal and SVG diagrams move into meowmery as reference?

## Card history
- 2026-10-23 · created by Claude (bengalTiger), from the repo at f18ba5b plus the owner's 2026-10-23 decision

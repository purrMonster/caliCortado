# Working in Calicortado

Calicortado is the second-brain project. Keep all documents and work focused on its capture, sync, retrieval, privacy and recovery needs.

Read README.md, map.md, plan.md, and the relevant design and runbook sections before changing files. User instructions take precedence.

## Scope and ownership

- Keep product intent and application design here. Deployment configuration belongs in the separate infrastructure repository.
- Inspect Git status before working in a repository and preserve unrelated edits.
- Infrastructure changes travel through Git: commit, push, then nodes pull main. Do not copy configuration directly to servers. Node sudo belongs to the user.
- Links to infrastructure run one way from here. Do not add mentions of Calicortado to infrastructure documentation.
- Keep notes, credentials, private exports, personal records and exact location data out of tracked documents. Use synthetic notes for tests.
- Do not initialize a remote, publish or deploy merely because a plan describes doing so.

## Decisions and evidence

- Distinguish user requirements, proposed design, implementation and observed results.
- plan.md owns the Vikunja-shaped sprint backlog, component epics, story dependencies and delivery gates; projects/second-brain.md owns architecture. Recovery and remote-access documents contain only the supporting work this project requires.
- Log every decision in runbook.md as it is made: story ID, date, context, options, choice, reason, status, consequences and evidence or next verification. Reference an existing decision explicitly when reusing it; record no new decision when appropriate. Never defer decision logging to sprint-end cleanup.
- Documentation is required for story completion. Each deployable component needs its contract, endpoint/auth configuration, state ownership, setup, checks, failures, upgrade/rollback and recovery instructions. Future documentation paths in stories are deliverables, not existing evidence.
- Keep inter-layer calls behind individually configured domain addresses through Traefik. Do not introduce cross-layer filesystem mounts, hardcoded host addresses, raw database calls or shared-network trust as shortcuts. Log any proposed boundary change before implementation.
- Update map.md when state, dependencies or the next action changes.
- Check completion boxes only with evidence. Configuration is not proof of a running or recoverable service.
- Keep implementation evidence in its owning repository and link to it from here. Never include credentials or raw private logs.

## Work rhythm

Prefer one bounded step that moves the current phase forward. Resolve routine reversible choices within scope; ask only for information that affects the outcome.

End each session with changed files, verified results, unresolved items and one concrete next action. Leave a handoff in runbook.md. Use the existing documents instead of introducing another tracker.

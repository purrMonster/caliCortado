# Calicortado sprint plan and Vikunja backlog

Status: E01 completed locally, 2026-09-27. **CAL-001–004 are Done with [dated evidence](docs/acceptance/e01.md); live E01 completion and CAL-005 pickup are verified; no deployment was performed.** Remaining stories are planned. The existing import archive is the sanitized all-Backlog snapshot; identifying text has been sanitized without synchronizing execution state.

## Release definition

First working complete release: Obsidian editing on iPhone and Mac; encrypted self-hosted sync; reliable local and API capture; independently recoverable data; private remote access; CPU-based semantic/full-text search; local grounded AI answers; and a responsive Calicortado display. AI answers are included in v0.1, even though runtime inference may be unavailable when its host sleeps. Direct search and local capture remain useful without it.

User-confirmed CAL-001 scope: retain Obsidian as the offline editor and build the Calicortado display for capture/search/answers. The user owns device setup; endpoint defaults derive from DOMAIN, set by the deployment environment, with per-layer URL overrides. A custom native editor/sync engine is not in this estimate. The architecture makes the display replaceable without changing data or AI services.

Shared household rollout, automatic archive/digests, arbitrary agents/actions, external document integrations and bulk imports are deferred. Small real-note onboarding is allowed only after its recovery gates. Synthetic data can be used throughout development.

**Required architecture:** independently deployable layers communicate using configured domain URLs through Traefik. A shared filesystem, a shared Docker network or a raw database connection is not an inter-layer interface. See [architecture and domain register](projects/second-brain.md).

## Vikunja representation

**Import artifact, 2026-09-27:** upload the generated [Vikunja ZIP](exports/vikunja/calicortado-vikunja-import.zip) through the native Vikunja export importer. [JSON](exports/vikunja/data.json) and [instructions](exports/vikunja/README.md) are included separately. The supplied instance reports v2.6.0 with this importer enabled. The Markdown remains the planning source; the ZIP is derived, not a live task board.

Use one project named **Calicortado**. Epics are ordinary parent tasks labeled `type:epic`; stories are ordinary tasks labeled `type:story` with a subtask/parent relation. Hard dependencies use **Blocked by** relations; story IDs below are stable planning keys, not server-assigned task IDs.

For each story, copy its outcome, start instructions, steps, acceptance checklist and documentation/runbook requirements into the **Description**. Map the metadata to Title, Priority, Labels, Assignees, Dates and Relations. Sprint membership is a label, not an assumed native sprint object; story points are an `estimate:N` label plus description text, not an invented API field.

- Labels: `release:v0.1`, `component:<name>`, `sprint:S0` through `sprint:S7`, `type:story` or `type:epic`, `estimate:N`.
- Kanban buckets: **Backlog → Ready → In progress → Review → Done**, plus **Blocked**. Configure the Done bucket deliberately.
- Initial state: Backlog, unassigned, not done, no start/end/due dates. “High” and “Normal” are task priorities, not severity labels.
- A story is independently pickable when its listed blockers are complete and its required inputs are available. Self-contained does not mean dependency-free.
- Proposed work-in-progress limit: one implementation story per implementer, plus one review. This plan does not itself authorize parallel agents.
- Native task numbers, actual assignees and sprint dates are resolved when the live board is created. The instance's v2.6.0 import schema was checked on 2026-09-27; archive-local IDs are remapped by the importer. This Markdown itself is not a native import file.
- When transferred, keep stable IDs in titles. Record the live project/task mapping here, use Vikunja for execution status, and link every task to its durable evidence/runbook entry. Do not maintain contradictory status lists.

This mapping uses documented [Vikunja tasks](https://vikunja.io/help/tasks/), [task relations](https://vikunja.io/help/task-relations/) and [views](https://vikunja.io/help/views/), checked 2026-09-26. No account or external write was used.

## Sprint rhythm

Plan eight ordered sprint goals, initially using **two-week planning windows** once access and capacity are known. These are proposed timeboxes, not a sixteen-week delivery promise. Estimates are relative effort, not hours or validated velocity. Re-estimate after S0; split a story before pickup if it cannot fit a sprint, preserving its parent outcome and blocker relations. Never mark incomplete acceptance complete to fit a timebox.

At sprint planning, choose only Ready stories within observed capacity. At review, demonstrate the working increment, review documentation and runbook evidence, record unfinished work and propose the next sprint. Elapsed observation windows can span sprints without occupying an implementer full-time.

| Sprint | Goal | Stories in suggested pickup order | Points | Exit demonstration |
|---|---|---|---:|---|
| S0 | Scope, workspace and contracts | CAL-001, CAL-002, CAL-003, CAL-004 | 13 | An agreed release definition and implementable contracts; no deployment implied. |
| S1 | Private domains, identity and sync feasibility | CAL-005, CAL-006, CAL-007, CAL-008, CAL-009, CAL-046 | 24 | Authenticated domain routes, encrypted sync/bridge proof and observability baseline. |
| S2 | Data service and capture | CAL-010, CAL-011, CAL-012, CAL-013, CAL-014, CAL-015, CAL-016, CAL-017 | 32 | Durable notes and idempotent iPhone/Mac/web capture through APIs. |
| S3 | Recovery and away-from-home use | CAL-018, CAL-019, CAL-020, CAL-021, CAL-022, CAL-023, CAL-024, CAL-025 | 25 | A fresh-client restore, observed backups and mobile-data capture/sync. |
| S4 | Embeddings and retrieval | CAL-026, CAL-027, CAL-028, CAL-029, CAL-030, CAL-031, CAL-032, CAL-033 | 28 | Useful, authorized direct search independent of the AI host. |
| S5 | Local inference and grounded answers | CAL-034, CAL-035, CAL-036, CAL-037, CAL-038, CAL-039, CAL-040, CAL-041 | 28 | Cited answers with bounded failures and reproducible evaluations. |
| S6 | Display and product walkthrough | CAL-042, CAL-043, CAL-044, CAL-045 | 12 | A responsive independently hosted interface for capture, search and answers. |
| S7 | Distributed rehearsal and release | CAL-047, CAL-048, CAL-049, CAL-050 | 14 | Machine separation, full restore, user trial and documentation acceptance. |

Total provisional effort: **176 points across 50 stories**. This is a sizing aid, not a budget or schedule commitment.

The critical path is contracts → domains/identity → sync/data → capture/recovery/remote → retrieval → grounded answers → display → distributed release. Inference discovery and display development against mocks can be pulled earlier once their blockers pass; their acceptance still requires real integration. Sprints group delivery goals; epics group components.

The 14-day capture trial begins at CAL-017; seven daily backup observations start at CAL-019; phone storage is checked initially and after 30 days. CAL-049 reports actual elapsed evidence. Development with synthetic notes can continue during observation, but failed usability/recovery gates block release or real-data expansion until resolved.

## Definition of Ready

The story has an assigned implementer, available inputs, completed blockers, agreed interface version and authorized target. Read its referenced architecture and component guides. Record any missing permission or owner decision as a specific blocker; continue independent work. Production deployment requires the standing access matrix; user-reserved sudo remains a user step.

## Definition of Done

Every story, including documentation and discovery stories, needs:

1. Its stated outcome demonstrated against the acceptance checklist, with dated evidence and exact code/config/model versions where applicable.
2. Required automated checks plus meaningful integration/manual checks. A mock proves a contract, not a deployment.
3. Updated component documentation: purpose, ownership, endpoints/auth, inputs/outputs, state, setup, operation, failure diagnosis, tests, upgrade/rollback and recovery as applicable.
4. A dated **runbook.md** entry linking the story. Log **every decision** with context, chosen option, alternatives, reason, status, consequences and verification. Reuse an existing decision by explicit reference; record “no new decision” when appropriate. Do not defer decision logging to the end of a sprint.
5. A reviewable change set, rollback/removal path, and a task completion comment linking sanitized evidence and the runbook. Infrastructure evidence stays in its owning repository; links only run from here.
6. A reviewer/owner acknowledgment for acceptance requiring a human/device. Unavailable access, failed tests and unobserved time windows mean Blocked or In progress, not Done.

A proposal is not an accepted user choice, a successful configuration render is not a live test, and a passing note restore is not proof of all service recovery.

## Component epics

Each epic is a parent task, initially Backlog/High/unassigned with no dates. Its description is the component outcome below plus its child-story list. Labels are `type:epic`, `release:v0.1` and the component label. An epic is Done only when every child passes, its component contract and operations guide are reviewed, and its decisions/evidence are linked in the runbook.

| Parent task title | Component label | Completed outcome | Children |
|---|---|---|---|
| [CAL-E01] Delivery foundation and contracts | `component:foundation` | A documented release baseline, permissions and testable interfaces exist. | CAL-001, CAL-002, CAL-003, CAL-004 |
| [CAL-E02] Traefik edge and identity | `component:edge` | Every layer has a private domain, authenticated route and denied bypass. | CAL-005, CAL-006, CAL-007, CAL-008 |
| [CAL-E03] Vault sync and data service | `component:data` | Encrypted client sync and a portable, authorized data API work. | CAL-009, CAL-010, CAL-011, CAL-012, CAL-013 |
| [CAL-E04] Capture clients and ingestion | `component:capture` | iPhone and Mac captures survive offline use, retries and conflicts. | CAL-014, CAL-015, CAL-016, CAL-017 |
| [CAL-E05] Backup and recovery service | `component:recovery` | Notes and service state can be recovered without the failed host. | CAL-018, CAL-019, CAL-020, CAL-021 |
| [CAL-E06] Private remote access | `component:remote` | Authorized devices use the product away from home without publishing backend services. | CAL-022, CAL-023, CAL-024, CAL-025 |
| [CAL-E07] Embedding service | `component:embedding` | A separately deployable CPU embedding API provides versioned vectors. | CAL-026, CAL-027, CAL-028, CAL-029 |
| [CAL-E08] Retrieval and index service | `component:search` | Authorized hybrid search returns current source snippets without inference. | CAL-030, CAL-031, CAL-032, CAL-033 |
| [CAL-E09] Local inference service | `component:inference` | A separately deployable authenticated inference endpoint works and fails predictably. | CAL-034, CAL-035, CAL-036, CAL-037 |
| [CAL-E10] Grounded answer service | `component:answers` | A read-only answer API cites authorized, current notes. | CAL-038, CAL-039, CAL-040, CAL-041 |
| [CAL-E11] Calicortado display | `component:display` | One responsive web interface provides capture, direct search and cited answers. | CAL-042, CAL-043, CAL-044, CAL-045 |
| [CAL-E12] Operations and release verification | `component:operations` | The system is observable, movable across machines, documented and accepted. | CAL-046, CAL-047, CAL-048, CAL-049, CAL-050 |

## Pick-up instructions

The detailed cards below are ready to copy into Vikunja descriptions. All referenced `docs/`, `contracts/`, `services/`, `clients/`, `display/` and `tests/` paths are **deliverables to create during the story**, not claims that implementations already exist. Paths are relative to this project unless explicitly infrastructure-owned. Read [AGENTS.md](AGENTS.md) before implementation. Each card repeats its closure requirement so it can be picked up alone.

## CAL-E01 — Delivery foundation and contracts

### CAL-001 — Release scope and owner choices are recorded

| Vikunja field | Value |
|---|---|
| Title | [CAL-001] Release scope and owner choices are recorded |
| Parent task | CAL-E01 — Delivery foundation and contracts |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:foundation`, `sprint:S0`, `estimate:2` |
| Bucket / done | Done / true (live state verified) |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | None |
| Estimate | 2 relative points; re-estimate at pickup |

**Completed outcome:** As the product owner, I have one explicit definition of the first complete release so implementation does not drift.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the delivery foundation and contracts component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** User confirms the proposed Obsidian-based release and who can perform iPhone/Mac setup.

**Implementation steps:**

1. Read README.md, design.md and projects/second-brain.md; retain the Obsidian editing plus Calicortado search/answers interface as the planning baseline.
2. Record included features, deferred shared use/automation/imports, privacy boundaries and each unresolved choice with its affected story.
3. Record capture, foreground sync, indexing, recovery and AI latency targets as proposed or accepted; identify owners for device tests.

**Acceptance checklist:**

- [x] Release checklist covers capture, offline editing, sync, recovery, remote access, search and AI answers.
- [x] Obsidian-based versus standalone-native scope is explicitly resolved before dependent implementation starts.
- [x] No unresolved decision is silently converted into approval; blocked rollout work is named while synthetic-data development can continue.
- [x] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** README.md release scope; design.md user outcomes; plan.md release gates.

**Runbook decisions to record:** Product shape, included/deferred features and measurable targets. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Verified 2026-09-27:** [E01 evidence](docs/acceptance/e01.md) and [runbook decisions](runbook.md). All checks refer to the offline foundation or documented inventory, not deployed services.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-001` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-002 — Host, repository and secret-access baseline is documented

| Vikunja field | Value |
|---|---|
| Title | [CAL-002] Host, repository and secret-access baseline is documented |
| Parent task | CAL-E01 — Delivery foundation and contracts |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:foundation`, `sprint:S0`, `estimate:3` |
| Bucket / done | Done / true (live state verified) |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-001 |
| Estimate | 3 relative points; re-estimate at pickup |

**Completed outcome:** As an implementer, I can identify permitted targets and their capacity without guessing about live deployment.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the delivery foundation and contracts component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** Authorized host access, chosen domain, budget, restart permissions and user-run sudo arrangement.

**Implementation steps:**

1. Inspect local Git state and only authorized hosts; record revisions, CPU/RAM/disk, inference hardware, domain ownership, existing Traefik and identity versions.
2. Create a permission matrix for inspect/configure/restart/deploy, sudo handoffs, downtime windows and spending; record credential locations by reference only.
3. Record data, compute, GPU and display placement candidates and unavailable dependencies; do not initialize a remote or deploy as discovery.

**Acceptance checklist:**

- [x] Inventory distinguishes observed, user-reported and unknown values with timestamps.
- [x] Each deployment story has a named permitted target or is explicitly blocked; secrets never appear in evidence.
- [x] Local version-control and repository ownership choices are recorded, including the one-way infrastructure documentation boundary.
- [x] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/operations/environment.md; docs/operations/access.md; map.md.

**Runbook decisions to record:** Initial placements, capacity constraints, repository ownership and access boundaries. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Verified 2026-09-27:** [E01 evidence](docs/acceptance/e01.md) and [runbook decisions](runbook.md). All checks refer to the offline foundation or documented inventory, not deployed services.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-002` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-003 — Reproducible development workspace and documentation checks pass

| Vikunja field | Value |
|---|---|
| Title | [CAL-003] Reproducible development workspace and documentation checks pass |
| Parent task | CAL-E01 — Delivery foundation and contracts |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:foundation`, `sprint:S0`, `estimate:3` |
| Bucket / done | Done / true (live state verified) |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-001 |
| Estimate | 3 relative points; re-estimate at pickup |

**Completed outcome:** As a contributor, I can start a synthetic local environment and verify documentation without a production account.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the delivery foundation and contracts component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Choose and pin application runtime/tooling; create modules for data, capture, embeddings, retrieval, inference adapter, answers and display with explicit ownership.
2. Add synthetic vaults, fake identity and inference fixtures, test commands and a local domain/TLS development recipe.
3. Add checks for Markdown links, contract validity, secret placeholders and clean-start instructions; keep generated notes outside source control.

**Acceptance checklist:**

- [x] A fresh authorized checkout can run documented checks using synthetic data only.
- [x] A deliberate broken documentation link and invalid API contract fail the relevant checks.
- [x] No production secret, private note or live host is required; deferred services can use contract mocks.
- [x] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/development.md; component README skeletons; documented check commands.

**Runbook decisions to record:** Runtime, package management, repository layout and documentation validation approach. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Verified 2026-09-27:** [E01 evidence](docs/acceptance/e01.md) and [runbook decisions](runbook.md). All checks refer to the offline foundation or documented inventory, not deployed services.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-003` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-004 — Versioned service contracts and authorization matrix are approved for implementation

| Vikunja field | Value |
|---|---|
| Title | [CAL-004] Versioned service contracts and authorization matrix are approved for implementation |
| Parent task | CAL-E01 — Delivery foundation and contracts |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:foundation`, `sprint:S0`, `estimate:5` |
| Bucket / done | Done / true (live state verified) |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-001, CAL-003 |
| Estimate | 5 relative points; re-estimate at pickup |

**Completed outcome:** As a component implementer, I can build against complete contracts independently of the other components.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the delivery foundation and contracts component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Translate the architecture endpoint register into OpenAPI schemas and examples for data, index storage, capture, embeddings, retrieval and answers; define the inference adapter and the sync/backup protocol exceptions.
2. Specify IDs, vault scoping, subject/audience/scopes, revisions, exclusion flags, cursors/tombstones, request limits, pagination and structured errors.
3. Define idempotency, request tracing, retry/cancellation behavior, timeouts and backward-compatible changes; provide authorized and denied fixtures.

**Acceptance checklist:**

- [x] Each interface has request/response and failure examples with no raw host/IP dependency.
- [x] Contract tests demonstrate wrong-audience, missing-scope, wrong-vault and malformed-request rejection in fixtures.
- [x] The runbook contains the chosen identity propagation and note/change-log semantics; remaining prototype questions have explicit fallback gates.
- [x] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** contracts/*.yaml; docs/contracts.md; docs/security.md.

**Runbook decisions to record:** API boundaries, data ownership, service/user identity, failure semantics and versioning. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Verified 2026-09-27:** [E01 evidence](docs/acceptance/e01.md) and [runbook decisions](runbook.md). All checks refer to the offline foundation or documented inventory, not deployed services.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-004` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

## CAL-E02 — Traefik edge and identity

### CAL-005 — Domain registry and private DNS resolve every layer

| Vikunja field | Value |
|---|---|
| Title | [CAL-005] Domain registry and private DNS resolve every layer |
| Parent task | CAL-E02 — Traefik edge and identity |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:edge`, `sprint:S1`, `estimate:3` |
| Bucket / done | In progress / false (live state verified) |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-002, CAL-004 |
| Estimate | 3 relative points; re-estimate at pickup |

**Pickup 2026-09-27:** [Registry and verification procedure](docs/operations/endpoints.md) prepared. Private DNS/router evidence is pending; live tracker pickup is verified. Acceptance remains unchecked. See [runbook](runbook.md).

**Completed outcome:** As an operator, I can move a layer by changing its endpoint mapping rather than application code.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the traefik edge and identity component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** Actual domain and authority to prepare DNS changes; applying live changes requires the access matrix.

**Implementation steps:**

1. Allocate every proposed hostname from projects/second-brain.md using the actual domain and check collisions with existing services.
2. Define per-environment URLs, DNS records, certificate ownership and host assignment; make all service endpoints configuration values.
3. Test resolution from a client and two isolated service networks; document DNS changes and rollback.

**Acceptance checklist:**

- [ ] Every named layer resolves to its intended ingress; configured URLs contain domains rather than LAN IPs.
- [ ] A test hostname can be moved to another ingress without rebuilding its caller.
- [ ] Private routing and certificate issuance are documented without exposing real private inventory in public records.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/operations/endpoints.md; endpoint configuration examples; map.md.

**Runbook decisions to record:** Final hostnames, DNS ownership, TTL and certificate strategy. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-005` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-006 — Traefik routes enforce TLS and reject direct-port bypass

| Vikunja field | Value |
|---|---|
| Title | [CAL-006] Traefik routes enforce TLS and reject direct-port bypass |
| Parent task | CAL-E02 — Traefik edge and identity |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:edge`, `sprint:S1`, `estimate:5` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-005 |
| Estimate | 5 relative points; re-estimate at pickup |

**Completed outcome:** As a client or service, I reach every layer through its domain and cannot evade its ingress policy.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the traefik edge and identity component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Implement reusable Traefik HTTP route templates and target-local ingress; use synthetic backends until components land.
2. Define TLS to remote upstreams, allowed hosts, body limits, timeout/streaming profiles and separate health/admin access.
3. Test DNS/SNI, untrusted certificates, unknown Host headers, raw ports and authorized cross-host requests; record user-run firewall steps.

**Acceptance checklist:**

- [ ] Allowed domain traffic succeeds with verified certificates; untrusted upstream TLS fails closed.
- [ ] Unknown hostnames and forbidden direct ports do not reach component APIs; TLS is not treated as authorization.
- [ ] Streaming route test does not buffer the entire response, and configuration rollback restores the previous route.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/operations/traefik.md; infrastructure-owned route templates and implementation evidence.

**Runbook decisions to record:** Ingress topology, upstream trust, route policies and direct-access restrictions. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-006` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-007 — Human and machine identities are enforced end to end

| Vikunja field | Value |
|---|---|
| Title | [CAL-007] Human and machine identities are enforced end to end |
| Parent task | CAL-E02 — Traefik edge and identity |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:edge`, `sprint:S1`, `estimate:5` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-004, CAL-006 |
| Estimate | 5 relative points; re-estimate at pickup |

**Completed outcome:** As a note owner, my identity and vault permissions cannot be supplied by an untrusted header.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the traefik edge and identity component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Implement the chosen human session and separately scoped machine credentials from CAL-004; keep browser credentials out of server configuration.
2. Configure allowed audiences, authorized caller edges and vault access; strip untrusted proxy identity headers and validate at the destination.
3. Test revocation, expiry, service impersonation, login outage and a request made by a permitted service for a forbidden user/vault.

**Acceptance checklist:**

- [ ] Browser, sync client and machine flows each authenticate using their documented mechanism.
- [ ] A forged identity header, wrong audience or overbroad vault request fails at the service even behind Traefik.
- [ ] Identity outage fails closed for remote APIs while already-local Obsidian editing still works.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/security.md; docs/operations/identity.md; synthetic access-test matrix.

**Runbook decisions to record:** Session mechanism, machine credential rotation, subject propagation and authorization enforcement. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-007` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-008 — Cross-domain browser and API behavior passes a reusable smoke suite

| Vikunja field | Value |
|---|---|
| Title | [CAL-008] Cross-domain browser and API behavior passes a reusable smoke suite |
| Parent task | CAL-E02 — Traefik edge and identity |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:edge`, `sprint:S1`, `estimate:3` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-006, CAL-007 |
| Estimate | 3 relative points; re-estimate at pickup |

**Completed outcome:** As an integrator, I can add a layer without inventing its security and browser behavior again.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the traefik edge and identity component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Create an executable smoke matrix covering the domain registry, human route, machine route, health route and disallowed caller.
2. Configure narrowly allowed frontend origins, cookies/CSRF where applicable and preflight behavior; no wildcard credentialed CORS.
3. Exercise request IDs, cancellation, timeouts and representative size/rate limits across ingress.

**Acceptance checklist:**

- [ ] Allowed-origin calls work; unapproved origins cannot make credentialed browser API calls.
- [ ] Service auth independently rejects unauthorized non-browser calls; CORS is never the sole access control.
- [ ] The same domain smoke suite is reusable as each later component replaces its stub.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** tests/contracts/edge scenarios; docs/operations/verification.md.

**Runbook decisions to record:** Browser trust model, rate limits and per-route timeout profiles. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-008` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

## CAL-E03 — Vault sync and data service

### CAL-009 — Encrypted Obsidian sync and bridge compatibility are proven

| Vikunja field | Value |
|---|---|
| Title | [CAL-009] Encrypted Obsidian sync and bridge compatibility are proven |
| Parent task | CAL-E03 — Vault sync and data service |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:data`, `sprint:S1`, `estimate:5` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-004, CAL-007 |
| Estimate | 5 relative points; re-estimate at pickup |

**Completed outcome:** As a note owner, I know the selected sync stack can preserve my files before I rely on it.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the vault sync and data service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** Access to test iPhone/Mac sessions or user-run device checks.

**Implementation steps:**

1. Use disposable iPhone/Mac vaults and pinned Obsidian/LiveSync/CouchDB/bridge versions; reach sync only through sync.<domain>.
2. Exercise both directions, concurrent edits, rename/delete and missing encryption metadata; compare the bridge mirror with client bytes.
3. Record real foreground/background behavior and encryption/path-obfuscation evidence; evaluate a fallback if the bridge fails.

**Acceptance checklist:**

- [ ] A synthetic note reaches the other foreground client within the proposed 60-second target, with visible conflicts rather than silent loss.
- [ ] The bridge decrypts and round-trips Unicode notes byte-for-byte; a decryption failure is detectable.
- [ ] Compatibility/version matrix and proceed/fallback decision are recorded before real-note migration.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** projects/second-brain.md compatibility result; docs/operations/sync.md.

**Runbook decisions to record:** Pinned sync versions, bridge feasibility, encryption and fallback choice. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-009` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-010 — Durable vault service runs behind the sync domain

| Vikunja field | Value |
|---|---|
| Title | [CAL-010] Durable vault service runs behind the sync domain |
| Parent task | CAL-E03 — Vault sync and data service |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:data`, `sprint:S2`, `estimate:5` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-009, CAL-008 |
| Estimate | 5 relative points; re-estimate at pickup |

**Completed outcome:** As a note owner, I have a restartable sync service with clearly owned persistent state.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the vault sync and data service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Deploy the validated sync and bridge as the data component with durable paths, least-privilege accounts and explicit startup/readiness order.
2. Separate vault credentials and administration; keep the bridge mirror local to the data component and block other layers from mounting it.
3. Implement mirror freshness/decryption status and documented restart/upgrade rollback; keep real imports out until recovery passes.

**Acceptance checklist:**

- [ ] Restarting the component retains synthetic notes and access rules; missing state fails visibly instead of silently initializing an empty vault.
- [ ] Only the data component accesses its local mirror; external reads/writes use data.<domain>.
- [ ] CouchDB admin routes and plaintext mirror cannot be reached by a normal sync user through unintended routes.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/operations/data.md; state-directory inventory; projects/recoverability.md.

**Runbook decisions to record:** Durable volume layout, readiness, admin boundary and sync/bridge ownership. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-010` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-011 — Vault read and change-feed APIs expose consistent authorized revisions

| Vikunja field | Value |
|---|---|
| Title | [CAL-011] Vault read and change-feed APIs expose consistent authorized revisions |
| Parent task | CAL-E03 — Vault sync and data service |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:data`, `sprint:S2`, `estimate:5` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-010, CAL-004 |
| Estimate | 5 relative points; re-estimate at pickup |

**Completed outcome:** As retrieval software on another machine, I can read permitted notes and resume changes without filesystem access.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the vault sync and data service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Implement note catalog/content endpoints and a persistent cursor-based change feed through data.<domain>, using the CAL-004 schema.
2. Maintain stable note IDs, revision/content hashes, vault IDs, indexability metadata and deletion/exclusion tombstones; define rename mapping and crash recovery.
3. Handle bridge filesystem changes with atomic read/snapshot rules; reject stale cursors with a documented rescan path.

**Acceptance checklist:**

- [ ] A client on a separate network reads only allowed vaults using HTTPS; no shared mount is needed.
- [ ] Restart, rename, delete and exclusion changes produce consistent revisions and resumable events without silently losing a change.
- [ ] Path traversal, unknown vaults and note-ID substitution are rejected; `_noai/` content is unavailable to indexing credentials.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** contracts/data.yaml; docs/data-model.md; docs/operations/data.md.

**Runbook decisions to record:** Stable IDs, revision allocation, change-feed retention and rescan semantics. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-011` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-012 — Create-only data writes preserve capture identity across retries

| Vikunja field | Value |
|---|---|
| Title | [CAL-012] Create-only data writes preserve capture identity across retries |
| Parent task | CAL-E03 — Vault sync and data service |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:data`, `sprint:S2`, `estimate:5` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-011 |
| Estimate | 5 relative points; re-estimate at pickup |

**Completed outcome:** As a capture client, I can safely retry after a timeout without creating duplicate notes.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the vault sync and data service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Implement scoped create-only inbox writes through data.<domain> with a stable capture ID, payload hash and durable idempotency record.
2. Make file publication and idempotency recovery crash-safe, including the interval between file creation and acknowledgement.
3. Define local Shortcut fallback reconciliation with the same ID and test mirror/sync races; reject conflicting reuse of an ID.

**Acceptance checklist:**

- [ ] Repeated identical requests, lost acknowledgements and process crashes result in exactly one logical captured note after reconciliation.
- [ ] An existing note cannot be overwritten, and a reused ID with different content returns a conflict.
- [ ] Malformed paths, disallowed vaults and oversized content leave no partial file or leaked note body in logs.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** contracts/data.yaml create operations; docs/operations/capture-recovery.md.

**Runbook decisions to record:** Capture identity format, retention, atomicity and offline reconciliation policy. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-012` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-013 — Consistent recovery export and portable data package are available

| Vikunja field | Value |
|---|---|
| Title | [CAL-013] Consistent recovery export and portable data package are available |
| Parent task | CAL-E03 — Vault sync and data service |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:data`, `sprint:S2`, `estimate:3` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-012 |
| Estimate | 3 relative points; re-estimate at pickup |

**Completed outcome:** As a backup worker, I can obtain a verified recovery set without reading another layer's filesystem.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the vault sync and data service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Provide a scoped snapshot/export operation or data-local backup agent with a consistent manifest covering notes, data-service metadata and idempotency state.
2. Specify how sync users/configuration/history are captured or reconstructed; isolate secrets from ordinary portable Markdown export.
3. Provide checksums and a documented restore/import boundary; expose export only through an authorized domain route.

**Acceptance checklist:**

- [ ] Concurrent edits cannot produce an undocumented mixed recovery set; manifest records source revisions and exclusions.
- [ ] Export contains enough state for the agreed restore scope, while ordinary user export contains no credentials.
- [ ] An export can be downloaded and verified from an isolated backup worker without shared mounts.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** contracts/data.yaml export operations; docs/operations/export.md; projects/recoverability.md.

**Runbook decisions to record:** Snapshot consistency, encrypted recovery artifacts and sync-history preservation. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-013` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

## CAL-E04 — Capture clients and ingestion

### CAL-014 — iPhone local capture works offline without filing decisions

| Vikunja field | Value |
|---|---|
| Title | [CAL-014] iPhone local capture works offline without filing decisions |
| Parent task | CAL-E04 — Capture clients and ingestion |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:capture`, `sprint:S2`, `estimate:3` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-009 |
| Estimate | 3 relative points; re-estimate at pickup |

**Completed outcome:** As the user, I can save typed or dictated text to one inbox in under ten seconds.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the capture clients and ingestion component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** User/device access for Shortcut installation, dictation permissions and on-device timing.

**Implementation steps:**

1. Build and document the iPhone Shortcut using the agreed Obsidian capture method and unique capture identity.
2. Offer an available Action-button/Lock-Screen entry point, preserve text on error and add only the minimal inbox layout.
3. Measure capture time, airplane-mode behavior and app storage on synthetic notes; document permissions and installation.

**Acceptance checklist:**

- [ ] Typed and dictated sample captures need no folder/tag/title selection and meet the agreed timing target.
- [ ] Airplane mode and a failed handoff preserve the text with a visible recovery path.
- [ ] The Shortcut can be installed from its documented artifact; setup and storage results are recorded.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** clients/iphone capture artifact; docs/user/iphone.md; design.md storage baseline.

**Runbook decisions to record:** Capture entry point, dictation/privacy settings and local failure behavior. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-014` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-015 — Mac capture and two-device offline editing are verified

| Vikunja field | Value |
|---|---|
| Title | [CAL-015] Mac capture and two-device offline editing are verified |
| Parent task | CAL-E04 — Capture clients and ingestion |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:capture`, `sprint:S2`, `estimate:3` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-010, CAL-014 |
| Estimate | 3 relative points; re-estimate at pickup |

**Completed outcome:** As the user, I can capture from the Mac and reconcile notes written offline on either device.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the capture clients and ingestion component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Provide a documented Mac Shortcut/hotkey using the same inbox and capture ID rules.
2. Exercise separate offline edits, same-note conflicts, reconnect and archive availability on iPhone and Mac.
3. Measure storage and foreground sync; document conflict resolution that preserves both versions.

**Acceptance checklist:**

- [ ] A fresh Mac setup following the guide captures a note that reaches the iPhone.
- [ ] Offline edits and a concurrent conflict preserve both intended texts and a visible resolution path.
- [ ] Text archives remain locally readable on both devices; attachment limits do not remove text silently.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** clients/mac capture artifact; docs/user/mac.md; docs/user/conflicts.md.

**Runbook decisions to record:** Mac entry point, conflict procedure and phone storage filtering. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-015` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-016 — Capture API accepts scoped idempotent writes over its own domain

| Vikunja field | Value |
|---|---|
| Title | [CAL-016] Capture API accepts scoped idempotent writes over its own domain |
| Parent task | CAL-E04 — Capture clients and ingestion |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:capture`, `sprint:S2`, `estimate:5` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-012, CAL-008 |
| Estimate | 5 relative points; re-estimate at pickup |

**Completed outcome:** As a client without filesystem access, I can create an inbox note through capture.<domain>.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the capture clients and ingestion component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Implement a stateless capture service with per-device credentials that calls the data API; persist state only in the owning data service.
2. Apply payload limits, validation, rate limits and stable request IDs; record operational metadata without note content.
3. Test retries, data-service outage, invalid tokens, Unicode, traversal and payload mismatch; return saved/pending/failed states honestly.

**Acceptance checklist:**

- [ ] Accepted capture is acknowledged as durable only after data-service confirmation; pending is distinct from saved.
- [ ] Revoked or wrong-vault credentials cannot create notes; retries match CAL-012 behavior.
- [ ] Capture and data run in separate containers/networks using their domain URLs and no shared volume.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** contracts/capture.yaml; services/capture README; docs/operations/capture.md.

**Runbook decisions to record:** Capture acknowledgement semantics, token scope and request limits. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-016` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-017 — Online capture and offline fallback reconcile one logical note

| Vikunja field | Value |
|---|---|
| Title | [CAL-017] Online capture and offline fallback reconcile one logical note |
| Parent task | CAL-E04 — Capture clients and ingestion |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:capture`, `sprint:S2`, `estimate:3` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-014, CAL-015, CAL-016 |
| Estimate | 3 relative points; re-estimate at pickup |

**Completed outcome:** As the user, I can use the same capture action at home, away or offline without losing or duplicating text.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the capture clients and ingestion component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** Device actions and a short supervised capture acceptance session.

**Implementation steps:**

1. Extend the device actions to attempt capture.<domain> while retaining the local capture ID and text until success is known.
2. Reconcile ambiguous timeouts and local fallback with the data service once connectivity returns.
3. Test delayed server success, repeated taps/retries, revoked tokens and a stopped bridge; start a documented capture trial.

**Acceptance checklist:**

- [ ] A timeout after a server commit followed by local fallback leaves one logical note after sync reconciliation.
- [ ] No capture is reported saved everywhere while the bridge is stalled; users see a truthful pending state.
- [ ] The user can recover a failed capture without reading logs; trial start date and known limitations are recorded.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/user/capture.md; docs/operations/capture-recovery.md; trial evidence.

**Runbook decisions to record:** Retry/fallback UX, pending-state display and trial start. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-017` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

## CAL-E05 — Backup and recovery service

### CAL-018 — Recovery inventory and usable backup target are established

| Vikunja field | Value |
|---|---|
| Title | [CAL-018] Recovery inventory and usable backup target are established |
| Parent task | CAL-E05 — Backup and recovery service |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:recovery`, `sprint:S3`, `estimate:3` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-002, CAL-013 |
| Estimate | 3 relative points; re-estimate at pickup |

**Completed outcome:** As the owner, I know what can be restored, how much loss is acceptable and where independent copies reside.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the backup and recovery service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** User recovery targets and an authorized, available independent storage destination.

**Implementation steps:**

1. Inventory notes, sync config/history, credentials, data metadata/idempotency, future index config and optional chat state.
2. Confirm destination health/capacity and independence; revisit recorded disk warnings rather than assuming the proposed backup-host target is suitable.
3. Agree RPO/RTO, retention, credential recovery and copy policy; select a supported HTTPS repository protocol behind backup.<domain>.

**Acceptance checklist:**

- [ ] Every authoritative state item has a capture/rebuild method and an owner.
- [ ] User-approved recovery targets and destination evidence are recorded; missing hardware remains explicitly blocked.
- [ ] Backup credential access does not depend solely on the machine/vault being restored.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** projects/recoverability.md; docs/operations/backup.md; recovery-set manifest.

**Runbook decisions to record:** Backup destination/protocol, retention, loss/downtime targets and credential custody. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-018` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-019 — Scheduled encrypted backups reach an authenticated domain endpoint

| Vikunja field | Value |
|---|---|
| Title | [CAL-019] Scheduled encrypted backups reach an authenticated domain endpoint |
| Parent task | CAL-E05 — Backup and recovery service |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:recovery`, `sprint:S3`, `estimate:5` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-018, CAL-006 |
| Estimate | 5 relative points; re-estimate at pickup |

**Completed outcome:** As an operator, I have scheduled recoverable snapshots and a clear failure signal.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the backup and recovery service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Configure the data-local backup worker or scoped snapshot consumer to send encrypted recovery sets to backup.<domain> through Traefik.
2. Use scoped writer versus maintenance credentials, repository locking and safe prune coordination; document restore-tool versions.
3. Test interrupted upload, target outage, stale mirror and missing sources; begin seven daily observations.

**Acceptance checklist:**

- [ ] A repository check and sample download validate a complete backup; an empty source list cannot look successful.
- [ ] Unauthorized writers/readers are rejected and backups require no cross-machine filesystem mount.
- [ ] A missed/failed backup emits one actionable incident; notification failure cannot conceal backup status.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/operations/backup.md; scheduled-job definitions in infrastructure; sanitized backup evidence.

**Runbook decisions to record:** Backup schedule, prune/lock coordination, alert rules and credential separation. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-019` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-020 — An isolated full restore succeeds with a fresh sync client

| Vikunja field | Value |
|---|---|
| Title | [CAL-020] An isolated full restore succeeds with a fresh sync client |
| Parent task | CAL-E05 — Backup and recovery service |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:recovery`, `sprint:S3`, `estimate:5` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-019 |
| Estimate | 5 relative points; re-estimate at pickup |

**Completed outcome:** As the owner, I can recover my notes and service access after loss of the data host.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the backup and recovery service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Simulate data-host loss in an isolated environment; retrieve recovery material without using the failed host.
2. Restore notes, metadata/idempotency and sync permissions/configuration; keep outbound automation disabled.
3. Connect a fresh test client, compare representative files, verify denied vault access and replay an old capture ID.

**Acceptance checklist:**

- [ ] Notes and attachments match recorded checksums; the fresh client syncs successfully.
- [ ] Forbidden vault access stays denied and old capture IDs do not duplicate data after restore.
- [ ] Measured recovery point/time meet the accepted targets or the story remains open with a corrective task.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/operations/restore.md; restore exercise report; projects/recoverability.md.

**Runbook decisions to record:** Restore order, history limitations, recovery exceptions and readiness to accept real notes. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-020` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-021 — Backup observation and baseline-before-import gate pass

| Vikunja field | Value |
|---|---|
| Title | [CAL-021] Backup observation and baseline-before-import gate pass |
| Parent task | CAL-E05 — Backup and recovery service |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:recovery`, `sprint:S3`, `estimate:2` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-020 |
| Estimate | 2 relative points; re-estimate at pickup |

**Completed outcome:** As the owner, I can rely on repeated backups before placing valuable notes in the system.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the backup and recovery service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** Seven elapsed daily runs and access to the independent recovery kit.

**Implementation steps:**

1. Collect seven actual scheduled successes with backup identifiers and freshness checks; do not substitute accelerated test runs for elapsed days.
2. Verify recovery kit access and an independent baseline procedure for any future imports.
3. Document retention verification and periodic restore cadence; mark only the observed coverage as proven.

**Acceptance checklist:**

- [ ] Seven dated scheduled backups and at least one verified restore are linked.
- [ ] Failure-signal evidence and baseline-before-import instructions are usable by another operator.
- [ ] Unobserved failure cases and excluded history remain explicit; no fleet-wide claim is made.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** projects/recoverability.md evidence; docs/user/imports.md; runbook recovery handoff.

**Runbook decisions to record:** Operational backup acceptance and permitted scope of real-data onboarding. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-021` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

## CAL-E06 — Private remote access

### CAL-022 — Remote-access decision and permitted route set are recorded

| Vikunja field | Value |
|---|---|
| Title | [CAL-022] Remote-access decision and permitted route set are recorded |
| Parent task | CAL-E06 — Private remote access |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:remote`, `sprint:S3`, `estimate:2` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-002, CAL-007 |
| Estimate | 2 relative points; re-estimate at pickup |

**Completed outcome:** As the owner, I have a chosen remote-access approach with explicit exposure and device rules.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the private remote access component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** User chooses remote-access approach and grants account/device setup access.

**Implementation steps:**

1. Compare the existing Tailscale proposal and the user's alternative against sync-client auth, privacy, CGNAT, costs and pause/revocation.
2. List only user-facing domains plus required DNS/identity dependencies; exclude embedding, data, inference and backup service routes from ordinary device access.
3. Record the decision and rollout/rollback steps; retain local usability during rollout.

**Acceptance checklist:**

- [ ] The owner chooses the approach with current compatibility/cost evidence.
- [ ] Route and endpoint allowlists identify permitted users/devices and forbidden backends.
- [ ] No remote exposure is inferred from having a domain name or certificate.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** projects/remote-access.md; docs/operations/remote.md.

**Runbook decisions to record:** Remote transport, exposure boundaries, device policy and maintenance. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-022` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-023 — Private remote routing, DNS and revocation work

| Vikunja field | Value |
|---|---|
| Title | [CAL-023] Private remote routing, DNS and revocation work |
| Parent task | CAL-E06 — Private remote access |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:remote`, `sprint:S3`, `estimate:3` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-022, CAL-008 |
| Estimate | 3 relative points; re-estimate at pickup |

**Completed outcome:** As an authorized device, I can resolve and reach only the required product domains from outside home.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the private remote access component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Implement the selected transport and split DNS, including resolver reachability and required auth endpoints.
2. Apply source-address-aware host/service rules; do not rely on a shared server's port 443 as a per-service boundary.
3. Test from an independent client network and revoke a test device; document recovery after route rollback.

**Acceptance checklist:**

- [ ] Allowed user domains resolve and connect; data/embedding/inference/backup backends and unrelated services remain denied.
- [ ] Device revocation and invalid credentials deny new access as specified; route logs identify the tested path.
- [ ] No public tunnel or direct-port route exposes a backend contrary to the access decision.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/operations/remote.md; endpoint access matrix and verification evidence.

**Runbook decisions to record:** Final routes, split DNS, revocation behavior and source-address enforcement. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-023` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-024 — iPhone mobile-data sync and capture survive remote outages

| Vikunja field | Value |
|---|---|
| Title | [CAL-024] iPhone mobile-data sync and capture survive remote outages |
| Parent task | CAL-E06 — Private remote access |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:remote`, `sprint:S3`, `estimate:3` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-017, CAL-023 |
| Estimate | 3 relative points; re-estimate at pickup |

**Completed outcome:** As the user, I can capture and sync away from home and continue locally when connectivity fails.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the private remote access component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** iPhone/mobile-data and Mac testing with user consent for device settings.

**Implementation steps:**

1. Test iPhone and Mac away from LAN; measure actual sync/capture and authentication behavior.
2. Stop the remote transport, capture offline, reconnect and verify reconciliation; test manual pause and its explicit resume condition.
3. Record device setup, screenshots with private data redacted, and a simple troubleshooting path.

**Acceptance checklist:**

- [ ] Mobile-data note creation reaches the Mac and a Mac edit reaches the iPhone.
- [ ] Transport outage loses no captured text and reconnection creates no duplicates.
- [ ] Manual pause behavior is documented and tested; no unverified background-sync promise is made.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/user/remote.md; projects/remote-access.md results.

**Runbook decisions to record:** Device on-demand settings, manual override and observed remote limitations. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-024` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-025 — Remote onboarding and lost-device procedure are independently usable

| Vikunja field | Value |
|---|---|
| Title | [CAL-025] Remote onboarding and lost-device procedure are independently usable |
| Parent task | CAL-E06 — Private remote access |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:remote`, `sprint:S3`, `estimate:2` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-024 |
| Estimate | 2 relative points; re-estimate at pickup |

**Completed outcome:** As an operator, I can onboard or revoke a device using documented steps without the original implementer.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the private remote access component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Write the minimal install/login/sync checklist, recovery steps and credential rotation scope.
2. Walk through a fresh test-device enrollment and lost-device revocation including capture tokens and sync credentials.
3. Document logout/session limits and any copies already on the lost device that revocation cannot erase.

**Acceptance checklist:**

- [ ] A fresh test device can be enrolled from the guide and reach only its allowed endpoints.
- [ ] Revoked device credentials fail across the intended paths and surviving devices still work.
- [ ] Guide links to restore instructions and states local-copy limitations clearly.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/user/onboarding.md; docs/operations/lost-device.md.

**Runbook decisions to record:** Enrollment, credential rotation and revocation limitations. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-025` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

## CAL-E07 — Embedding service

### CAL-026 — Embedding model and compatibility contract are selected

| Vikunja field | Value |
|---|---|
| Title | [CAL-026] Embedding model and compatibility contract are selected |
| Parent task | CAL-E07 — Embedding service |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:embedding`, `sprint:S4`, `estimate:2` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-004, CAL-021, CAL-024 |
| Estimate | 2 relative points; re-estimate at pickup |

**Completed outcome:** As a search implementer, I know the model languages, dimensions and resource budget before building an index.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the embedding service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** User confirms note languages; no raw personal notes are required for selection.

**Implementation steps:**

1. Confirm note languages and evaluate small local CPU candidates using synthetic representative queries.
2. Record model license, digest, dimensions, tokenization, maximum input and expected compute/memory budget.
3. Define version changes as a new index generation; measure the selected candidate independently of inference-host.

**Acceptance checklist:**

- [ ] Chosen model handles the agreed languages and fits the observed CPU/memory budget.
- [ ] Embedding contract declares model/version/dimensions and behavior for oversized or invalid input.
- [ ] A reproducible synthetic scorecard supports the selection; no private corpus is exported.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/embedding-model.md; contracts/embeddings.yaml; model scorecard.

**Runbook decisions to record:** Model/license, languages, vector dimensions and reindex policy. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-026` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-027 — Embedding API runs behind its own authenticated domain

| Vikunja field | Value |
|---|---|
| Title | [CAL-027] Embedding API runs behind its own authenticated domain |
| Parent task | CAL-E07 — Embedding service |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:embedding`, `sprint:S4`, `estimate:3` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-026, CAL-008 |
| Estimate | 3 relative points; re-estimate at pickup |

**Completed outcome:** As retrieval on another machine, I can obtain vectors from embed.<domain> without knowing its host.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the embedding service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Package a pinned CPU embedding service with bounded batch size and resource settings.
2. Expose the contracted endpoint and readiness through Traefik with scoped service authentication.
3. Test warm/cold start, Unicode inputs, invalid batches and CPU-only execution using domain calls.

**Acceptance checklist:**

- [ ] Authorized cross-network requests return the selected version and expected vector dimensions.
- [ ] Browser/user credentials and wrong-audience machine tokens cannot invoke the API.
- [ ] Changing EMBEDDING_BASE_URL relocates the dependency without code edits.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** services/embeddings README; docs/operations/embeddings.md.

**Runbook decisions to record:** Service limits, startup/download handling and endpoint deployment. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-027` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-028 — Embedding overload and model outages are bounded

| Vikunja field | Value |
|---|---|
| Title | [CAL-028] Embedding overload and model outages are bounded |
| Parent task | CAL-E07 — Embedding service |
| Priority | Normal |
| Labels | `type:story`, `release:v0.1`, `component:embedding`, `sprint:S4`, `estimate:3` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-027 |
| Estimate | 3 relative points; re-estimate at pickup |

**Completed outcome:** As an operator, embedding work cannot exhaust the host or block ordinary note capture.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the embedding service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Implement concurrency/queue bounds, deadlines, cancellation and retryable error responses.
2. Simulate missing model files, worker failure and overload while sync and capture remain active.
3. Measure CPU/RAM and redact text from logs and metrics.

**Acceptance checklist:**

- [ ] Overload returns a documented bounded error instead of unbounded memory growth.
- [ ] Model failure marks readiness unhealthy and does not interrupt sync/capture.
- [ ] Cancelling a request releases work as designed; no note text is logged.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/operations/embeddings.md failure table; resource-test report.

**Runbook decisions to record:** Queue/concurrency, timeout limits and operational failure behavior. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-028` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-029 — Embedding service upgrade and relocation are reproducible

| Vikunja field | Value |
|---|---|
| Title | [CAL-029] Embedding service upgrade and relocation are reproducible |
| Parent task | CAL-E07 — Embedding service |
| Priority | Normal |
| Labels | `type:story`, `release:v0.1`, `component:embedding`, `sprint:S4`, `estimate:2` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-028 |
| Estimate | 2 relative points; re-estimate at pickup |

**Completed outcome:** As an operator, I can replace the embedding host or version without silently corrupting the index.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the embedding service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Install the same digest on a second isolated worker and run the synthetic compatibility suite.
2. Document rollback and model-cache recreation; require explicit model-version changes to start a new index generation.
3. Verify consumers reject mismatched dimensions/version rather than mixing vectors.

**Acceptance checklist:**

- [ ] The documented deployment recipe works on the second worker using the same domain contract.
- [ ] Dimension/model mismatch is rejected with a clear error.
- [ ] Upgrade/rollback instructions record required index rebuild behavior.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/operations/embeddings.md upgrade section; compatibility fixtures.

**Runbook decisions to record:** Embedding upgrade, cache policy and compatibility gate. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-029` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

## CAL-E08 — Retrieval and index service

### CAL-030 — Derived index store is isolated behind a data-layer domain

| Vikunja field | Value |
|---|---|
| Title | [CAL-030] Derived index store is isolated behind a data-layer domain |
| Parent task | CAL-E08 — Retrieval and index service |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:search`, `sprint:S4`, `estimate:5` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-011, CAL-026, CAL-007 |
| Estimate | 5 relative points; re-estimate at pickup |

**Completed outcome:** As retrieval software, I can persist and query a rebuildable index without direct database access.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the retrieval and index service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Implement index.<domain> as a data-layer API owning derived storage, schema migrations, vault partitions and embedding generation metadata.
2. Provide scoped batch upsert/delete and authorized lexical/vector query operations; keep database ports private inside the component.
3. Return revision/version metadata and enforce subject/vault scoping in storage queries; define an atomic generation switch.

**Acceptance checklist:**

- [ ] Indexer and query credentials have different permissions and cross-vault access fails.
- [ ] The database can be moved with its API without changing retrieval code; callers use no SQL port/shared volume.
- [ ] Model generations cannot be mixed, and a failed generation build leaves the last valid generation available.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** contracts/index.yaml; docs/data-model.md index ownership; docs/operations/index.md.

**Runbook decisions to record:** Derived store backend, partitioning, schema migration and generation cutover. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-030` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-031 — Incremental indexing consumes the remote change feed safely

| Vikunja field | Value |
|---|---|
| Title | [CAL-031] Incremental indexing consumes the remote change feed safely |
| Parent task | CAL-E08 — Retrieval and index service |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:search`, `sprint:S4`, `estimate:5` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-011, CAL-027, CAL-030 |
| Estimate | 5 relative points; re-estimate at pickup |

**Completed outcome:** As the owner, new and changed notes become searchable while excluded/deleted text is removed.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the retrieval and index service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Build a resumable indexer calling data, embed and index domains; chunk by headings with stable hashes and bounded queues.
2. Process create/edit/delete/exclusion tombstones and cursor expiry; handle a full rescan and a crashed partial batch.
3. Exclude generated content, private flags, binary/conflict files; version every indexed revision and checkpoint only after durable writes.

**Acceptance checklist:**

- [ ] An unchanged re-run performs zero new embeddings and duplicate events are harmless.
- [ ] Edits, deletes and exclusions converge within the proposed five-minute healthy-system target.
- [ ] Restart or expired cursor recovers without losing changes; source failures do not silently declare a stale index current.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** services/retrieval indexer README; docs/operations/indexing.md.

**Runbook decisions to record:** Chunking, polling/reconciliation intervals, cursor checkpoints and exclusion handling. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-031` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-032 — Search API returns authorized current source snippets

| Vikunja field | Value |
|---|---|
| Title | [CAL-032] Search API returns authorized current source snippets |
| Parent task | CAL-E08 — Retrieval and index service |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:search`, `sprint:S4`, `estimate:5` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-031 |
| Estimate | 5 relative points; re-estimate at pickup |

**Completed outcome:** As the user, I can retrieve useful notes without an LLM or access to the data host.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the retrieval and index service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Implement search.<domain>/v1/search with hybrid ranking, bounded pagination and stable note/revision links.
2. Revalidate source permissions, indexability and revisions before returning snippets; stale deleted/excluded content must not leak while indexing catches up.
3. Provide degraded behavior for embedding/index/data failures; use lexical search only when its authorization/freshness checks still pass.

**Acceptance checklist:**

- [ ] Synthetic relevant notes meet the documented retrieval target and link to the correct current source.
- [ ] Wrong-vault queries, newly excluded notes and deleted revisions do not appear even with a deliberately stale index.
- [ ] Search remains usable with inference unavailable; failures distinguish empty results from unavailable dependencies.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** contracts/search.yaml; docs/search-evaluation.md; docs/operations/search.md.

**Runbook decisions to record:** Ranking, freshness enforcement, result limits and degraded-search policy. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-032` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-033 — Search quality, privacy and rebuild acceptance pass

| Vikunja field | Value |
|---|---|
| Title | [CAL-033] Search quality, privacy and rebuild acceptance pass |
| Parent task | CAL-E08 — Retrieval and index service |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:search`, `sprint:S4`, `estimate:3` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-029, CAL-032, CAL-020 |
| Estimate | 3 relative points; re-estimate at pickup |

**Completed outcome:** As the owner, I have evidence that search is useful, private and disposable.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the retrieval and index service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Create a versioned synthetic query set with exact, semantic, no-answer, multilingual if needed and cross-vault cases.
2. Rebuild the index from an isolated restored vault and compare expected authorized results.
3. Inject duplicate events, index outage and model-version mismatch; document tuning and unresolved limitations.

**Acceptance checklist:**

- [ ] At least 20 fixed queries pass the declared acceptance rubric, including all isolation and exclusion cases.
- [ ] Index rebuild from restored data succeeds without recovering old vector storage.
- [ ] Inference remains stopped throughout the direct-search test and source links still work.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/search-evaluation.md scorecard; docs/operations/index.md rebuild recipe.

**Runbook decisions to record:** Search acceptance thresholds, tuning choices and remaining retrieval limitations. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-033` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

## CAL-E09 — Local inference service

### CAL-034 — Inference runtime and local model fit are verified

| Vikunja field | Value |
|---|---|
| Title | [CAL-034] Inference runtime and local model fit are verified |
| Parent task | CAL-E09 — Local inference service |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:inference`, `sprint:S5`, `estimate:2` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-002, CAL-004 |
| Estimate | 2 relative points; re-estimate at pickup |

**Completed outcome:** As an operator, I know which local runtime/model can serve answers without compromising existing workloads.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the local inference service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** Authorized inference-host inspection and owner acceptance of availability/latency target.

**Implementation steps:**

1. Inspect authorized inference hardware/runtime and competing workloads; select a pinned model with appropriate license/context budget.
2. Benchmark synthetic prompts for cold/warm latency and memory; establish one-concurrent-request starting limits.
3. Record asleep/offline behavior, machine authentication options and a rollback path without changing production state.

**Acceptance checklist:**

- [ ] Model digest/license, actual resource evidence and prompt/context budget are documented.
- [ ] Owner accepts an availability/latency target based on measurements; no automatic wake or cloud fallback is assumed.
- [ ] The selected runtime supports the required contracted inference behavior or a bounded adapter is specified.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/inference-model.md; docs/operations/inference.md.

**Runbook decisions to record:** Model, hardware budget, runtime adapter and accepted availability. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-034` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-035 — Machine inference endpoint exposes only permitted generation operations

| Vikunja field | Value |
|---|---|
| Title | [CAL-035] Machine inference endpoint exposes only permitted generation operations |
| Parent task | CAL-E09 — Local inference service |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:inference`, `sprint:S5`, `estimate:5` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-034, CAL-008 |
| Estimate | 5 relative points; re-estimate at pickup |

**Completed outcome:** As the answer service, I can request local generation through infer.<domain> with a scoped identity.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the local inference service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Implement the minimal runtime adapter or authenticated proxy; keep model pull/delete and runtime administration off the service route.
2. Configure inference TLS, streaming timeouts and caller restrictions; close unauthorized direct runtime access.
3. Test valid streaming, wrong audience, forbidden methods and unauthenticated/direct-port requests.

**Acceptance checklist:**

- [ ] The answer-service identity can generate but cannot manage models or host state.
- [ ] Unauthorized domain and direct-port calls fail; user-facing login cookies are not used as machine credentials.
- [ ] Inference host can be addressed solely through INFERENCE_BASE_URL with verified TLS.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** contracts/inference.yaml; services/inference-adapter README; docs/operations/inference.md.

**Runbook decisions to record:** Inference auth mechanism, allowed operations and proxy streaming settings. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-035` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-036 — Inference cancellation, overload and sleep failure are predictable

| Vikunja field | Value |
|---|---|
| Title | [CAL-036] Inference cancellation, overload and sleep failure are predictable |
| Parent task | CAL-E09 — Local inference service |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:inference`, `sprint:S5`, `estimate:3` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-035 |
| Estimate | 3 relative points; re-estimate at pickup |

**Completed outcome:** As the user, a sleeping or busy inference host does not leave the product hanging.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the local inference service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Implement bounded concurrency, cancellation propagation, request/body/context limits and a deadline.
2. Simulate asleep/offline runtime, mid-stream disconnect and queue saturation using synthetic prompts.
3. Verify generation failure cannot block direct search or restart/wake the workstation implicitly.

**Acceptance checklist:**

- [ ] Every injected failure completes within its configured deadline with a documented error.
- [ ] Cancelled/disconnected requests release runtime work where supported; limitations are explicit.
- [ ] Search/capture remain available while inference is down, and there is no cloud or wake side effect.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/operations/inference.md failure matrix; load/cancellation results.

**Runbook decisions to record:** Runtime limits, cancellation guarantees and sleep/outage behavior. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-036` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-037 — Inference upgrade and alternate-host deployment are documented and tested

| Vikunja field | Value |
|---|---|
| Title | [CAL-037] Inference upgrade and alternate-host deployment are documented and tested |
| Parent task | CAL-E09 — Local inference service |
| Priority | Normal |
| Labels | `type:story`, `release:v0.1`, `component:inference`, `sprint:S5`, `estimate:3` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-036 |
| Estimate | 3 relative points; re-estimate at pickup |

**Completed outcome:** As an operator, I can replace the AI host while keeping the answer contract stable.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the local inference service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Deploy the selected adapter/runtime on an authorized isolated target or equivalent second test host.
2. Run the same stream/auth/error contract suite and record resource differences.
3. Write upgrade, rollback and model-cache recovery steps; protect any existing chat state if its runtime integration changes.

**Acceptance checklist:**

- [ ] Contract behavior passes against both endpoint placements without answer-service code changes.
- [ ] Version/digest and rollback commands are recorded with any platform restrictions.
- [ ] Any stateful existing-chat change has backup/restore evidence or remains excluded from rollout.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/operations/inference.md portability and upgrade evidence.

**Runbook decisions to record:** AI placement, platform differences and stateful-upgrade constraints. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-037` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

## CAL-E10 — Grounded answer service

### CAL-038 — Answer API retrieves authorized notes and returns valid citations

| Vikunja field | Value |
|---|---|
| Title | [CAL-038] Answer API retrieves authorized notes and returns valid citations |
| Parent task | CAL-E10 — Grounded answer service |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:answers`, `sprint:S5`, `estimate:5` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-032, CAL-035 |
| Estimate | 5 relative points; re-estimate at pickup |

**Completed outcome:** As the user, I can ask a question and receive an answer grounded in notes I can access.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the grounded answer service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Implement answers.<domain>/v1/answers with server-validated user context; call search and inference through configured domains.
2. Bound prompt size and source count, delimit untrusted note content and attach note ID/revision citations.
3. Revalidate source permission/currentness before response; avoid durable conversation storage in v1 unless explicitly chosen.

**Acceptance checklist:**

- [ ] Every rendered citation maps to an authorized supplied source; invented citation IDs are rejected.
- [ ] No relevant evidence produces an explicit insufficient-evidence response rather than a fabricated personal fact.
- [ ] The service has no direct vault mount/database access and no write/admin/action tools.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** contracts/answers.yaml; services/answers README; docs/answer-behavior.md.

**Runbook decisions to record:** Grounding prompt, source budget, citation validation and conversation retention. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-038` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-039 — Answer streaming and inference-unavailable fallback preserve source access

| Vikunja field | Value |
|---|---|
| Title | [CAL-039] Answer streaming and inference-unavailable fallback preserve source access |
| Parent task | CAL-E10 — Grounded answer service |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:answers`, `sprint:S5`, `estimate:3` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-038, CAL-036 |
| Estimate | 3 relative points; re-estimate at pickup |

**Completed outcome:** As the user, I can stop an answer or read its sources even when generation fails.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the grounded answer service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Implement stream events for sources, content, completion/error and request ID; cancellation reaches downstream inference.
2. On inference failure return a documented unavailable state plus authorized snippets where retrieval succeeded.
3. Handle permissions/revision changes mid-request and avoid returning text generated from sources that are no longer permitted.

**Acceptance checklist:**

- [ ] Cancelling in a test client terminates the answer stream and downstream work within the accepted bound.
- [ ] Sleeping inference returns useful source access without falsely reporting a completed answer.
- [ ] Changed authorization/exclusion invalidates the response safely; partial output behavior is documented.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** contracts/answers.yaml streaming examples; docs/operations/answers.md.

**Runbook decisions to record:** Stream protocol, fallback, cancellation and mid-request permission changes. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-039` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-040 — Grounding and prompt-injection acceptance suite passes

| Vikunja field | Value |
|---|---|
| Title | [CAL-040] Grounding and prompt-injection acceptance suite passes |
| Parent task | CAL-E10 — Grounded answer service |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:answers`, `sprint:S5`, `estimate:5` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-039, CAL-033 |
| Estimate | 5 relative points; re-estimate at pickup |

**Completed outcome:** As the owner, I have repeatable evidence that answers respect data boundaries.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the grounded answer service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Create at least 20 synthetic cases covering answerable, no-answer, conflicting, multilingual if required, malicious-note and wrong-vault questions.
2. Include notes asking the model to reveal secrets or invoke nonexistent tools; verify policy outside the model.
3. Score citation validity, supported claims, abstention and latency under a pinned model/prompt; record failures and correction.

**Acceptance checklist:**

- [ ] All unauthorized-vault/exclusion tests and citation-integrity checks pass; no action capability is available.
- [ ] Every required no-evidence case reports insufficient evidence; grounding quality meets the recorded rubric.
- [ ] Re-running the suite records model/prompt versions and variability instead of asserting identical generated text.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** tests/answers synthetic cases; docs/answer-evaluation.md.

**Runbook decisions to record:** Evaluation rubric, accepted answer limitations and prompt revisions. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-040` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-041 — Answer service operational handoff is complete

| Vikunja field | Value |
|---|---|
| Title | [CAL-041] Answer service operational handoff is complete |
| Parent task | CAL-E10 — Grounded answer service |
| Priority | Normal |
| Labels | `type:story`, `release:v0.1`, `component:answers`, `sprint:S5`, `estimate:2` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-040, CAL-037 |
| Estimate | 2 relative points; re-estimate at pickup |

**Completed outcome:** As an operator, I can deploy or disable answers without affecting capture or search.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the grounded answer service component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Document environment URLs, credential references, dependency health, resource budget and stateless startup.
2. Test disabling answers, rotating its credentials and upgrading/rolling back the service against contract fixtures.
3. Document what logs retain and how to diagnose a failed request without reading note contents.

**Acceptance checklist:**

- [ ] Answers can be stopped/removed while direct search and capture continue working.
- [ ] Credential rotation and rollback succeed using documented commands.
- [ ] No prompt, note body or generated answer is retained in routine operational logs by default.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/operations/answers.md; services/answers README.

**Runbook decisions to record:** Answer deployment, retention, credential rotation and rollback. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-041` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

## CAL-E11 — Calicortado display

### CAL-042 — Responsive authenticated display shell runs on an independent host

| Vikunja field | Value |
|---|---|
| Title | [CAL-042] Responsive authenticated display shell runs on an independent host |
| Parent task | CAL-E11 — Calicortado display |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:display`, `sprint:S6`, `estimate:3` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-008, CAL-004 |
| Estimate | 3 relative points; re-estimate at pickup |

**Completed outcome:** As the user, I have one private app.<domain> entry point on iPhone and Mac.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the calicortado display component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Build a small responsive display with Capture, Search and Ask views, accessible keyboard/focus behavior and clear sign-in/sign-out.
2. Use the selected identity contract and configured domain endpoints; never embed service credentials or host/IP assumptions in browser assets.
3. Provide loading, offline and unavailable states with no custom offline note editor or hidden cache of private results.

**Acceptance checklist:**

- [ ] The shell works at iPhone and desktop sizes and can be hosted separately from data and AI.
- [ ] Expired sessions require reauthentication; browser assets contain no machine secrets.
- [ ] Every navigation and primary control is usable by keyboard with readable labels and focus.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** display README; docs/user/interface.md; docs/operations/display.md.

**Runbook decisions to record:** Frontend stack, session integration, cache policy and navigation. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-042` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-043 — Display capture and direct search work without AI

| Vikunja field | Value |
|---|---|
| Title | [CAL-043] Display capture and direct search work without AI |
| Parent task | CAL-E11 — Calicortado display |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:display`, `sprint:S6`, `estimate:3` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-042, CAL-017, CAL-032 |
| Estimate | 3 relative points; re-estimate at pickup |

**Completed outcome:** As the user, I can capture or find a note from Calicortado even while the AI host sleeps.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the calicortado display component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Connect capture UI to capture.<domain> and search UI to search.<domain>; preserve unsent input and honest pending states.
2. Render snippets as untrusted text, sanitize Markdown previews and provide authorized source/Obsidian links.
3. Handle no-results versus unavailable, expired session and offline handoff to local Obsidian.

**Acceptance checklist:**

- [ ] With inference stopped, web capture and direct search complete through their domain APIs.
- [ ] XSS/link-injection test notes cannot execute scripts or leak credentials.
- [ ] A failed capture preserves the input; source links open the intended authorized note and no private result is cached across logout.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/user/interface.md capture/search; frontend acceptance evidence.

**Runbook decisions to record:** Source-link scheme, rendering policy and offline handoff UX. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-043` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-044 — Display answers show citations, cancellation and truthful failure states

| Vikunja field | Value |
|---|---|
| Title | [CAL-044] Display answers show citations, cancellation and truthful failure states |
| Parent task | CAL-E11 — Calicortado display |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:display`, `sprint:S6`, `estimate:3` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-043, CAL-039 |
| Estimate | 3 relative points; re-estimate at pickup |

**Completed outcome:** As the user, I can ask a question, inspect its evidence and stop generation.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the calicortado display component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Connect Ask to answers.<domain>, show streaming state and source citations, and implement stop/retry.
2. Render insufficient-evidence and inference-unavailable states with direct-search access.
3. Test expired login, mid-stream network loss and denied sources; avoid showing an error as a completed answer.

**Acceptance checklist:**

- [ ] A cited answer opens the correct permitted source and can be cancelled.
- [ ] Inference outage clearly preserves direct search; retries do not create hidden background streams.
- [ ] Untrusted answer content is safely rendered and source authorization errors reveal no private metadata.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/user/interface.md answers; frontend stream/failure tests.

**Runbook decisions to record:** Answer rendering, retry behavior and citation interaction. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-044` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-045 — iPhone and Mac product walkthrough and install guide pass

| Vikunja field | Value |
|---|---|
| Title | [CAL-045] iPhone and Mac product walkthrough and install guide pass |
| Parent task | CAL-E11 — Calicortado display |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:display`, `sprint:S6`, `estimate:3` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-044, CAL-025, CAL-040 |
| Estimate | 3 relative points; re-estimate at pickup |

**Completed outcome:** As a new user, I can follow the guide to capture, find and ask about my notes.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the calicortado display component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** User/device acceptance session on the actual iPhone and Mac.

**Implementation steps:**

1. Run an end-to-end synthetic walkthrough on iPhone and Mac covering browser login, local editor handoff, web capture, search and citations.
2. Check mobile touch targets, keyboard navigation, logout, denied access and local editing during outages.
3. Publish a concise getting-started guide and component-specific troubleshooting links; record device/browser versions.

**Acceptance checklist:**

- [ ] A person following the guide completes the full walkthrough without undocumented setup.
- [ ] No critical accessibility or device blocker remains, and known limitations are listed.
- [ ] Display can be served from its own host with only configured domain URLs to backend services.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/user/getting-started.md; docs/user/troubleshooting.md; device acceptance report.

**Runbook decisions to record:** Final user flow, supported device/browser baseline and release limitations. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-045` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

## CAL-E12 — Operations and release verification

### CAL-046 — Operational health and redacted tracing baseline exists

| Vikunja field | Value |
|---|---|
| Title | [CAL-046] Operational health and redacted tracing baseline exists |
| Parent task | CAL-E12 — Operations and release verification |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:operations`, `sprint:S1`, `estimate:3` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-004, CAL-006 |
| Estimate | 3 relative points; re-estimate at pickup |

**Completed outcome:** As an operator, I can distinguish service failure, dependency outage and stale data without logging private notes.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the operations and release verification component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Define shared liveness/readiness, request IDs, sanitized structured logs and version metadata for every component.
2. Provide reusable monitoring probes through restricted domains and alert templates for backup failure, bridge freshness and unavailable endpoints.
3. Demonstrate one correlated synthetic request and one induced failure against stubs; require later services to adopt the same contract.

**Acceptance checklist:**

- [ ] Health exposes no secrets or note content and can distinguish process alive from dependency ready.
- [ ] A request ID links sanitized ingress/service errors without retaining request bodies.
- [ ] Alert transitions deduplicate repeated failures and include an actionable recovery link.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/operations/observability.md; shared health/logging fixtures.

**Runbook decisions to record:** Health contract, metrics retention, request tracing and notification policy. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-046` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-047 — Data, compute, AI and display run on separate machines

| Vikunja field | Value |
|---|---|
| Title | [CAL-047] Data, compute, AI and display run on separate machines |
| Parent task | CAL-E12 — Operations and release verification |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:operations`, `sprint:S7`, `estimate:5` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-021, CAL-025, CAL-033, CAL-041, CAL-045, CAL-046 |
| Estimate | 5 relative points; re-estimate at pickup |

**Completed outcome:** As the owner, I have proof that placement is modular rather than merely described as modular.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the operations and release verification component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** Authorized independent hosts/VMs with sufficient resources for the relocation test.

**Implementation steps:**

1. Run data/sync/index on host A, retrieval/embedding on host B, inference on host C and display on host D; approved isolated VMs count, separate containers on one shared network alone do not.
2. Exercise capture, sync, indexing, search and answers through domain names; prohibit cross-layer mounts, raw DB ports and hardcoded IPs.
3. Move one layer to a replacement host by changing DNS/routing/config only; test certificate/identity continuity and rollback.

**Acceptance checklist:**

- [ ] The distributed topology passes the same functional/auth/contract suite and records actual host or VM boundaries.
- [ ] Moving a layer requires no consumer code change and leaves no hidden filesystem or host-local dependency.
- [ ] Outage of each layer produces the documented degradation; no cross-host unverified TLS hop remains.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/operations/portability.md; map.md observed placements; relocation evidence.

**Runbook decisions to record:** Verified split topology, DNS cutover procedure, rollback and any measured latency impact. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-047` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-048 — Full-product recovery, upgrade and security rehearsal passes

| Vikunja field | Value |
|---|---|
| Title | [CAL-048] Full-product recovery, upgrade and security rehearsal passes |
| Parent task | CAL-E12 — Operations and release verification |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:operations`, `sprint:S7`, `estimate:5` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-047 |
| Estimate | 5 relative points; re-estimate at pickup |

**Completed outcome:** As the operator, I can safely maintain the complete release rather than only its prototype.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the operations and release verification component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** None beyond completed prerequisites and authorized development access.

**Implementation steps:**

1. Repeat isolated restore with the final data/capture metadata and permissions; rebuild search and reconnect display/answers.
2. Exercise component upgrades and rollback, revoked credentials, direct-port bypass, stale exclusions, dependency outage and resource limits.
3. Check every component's real monitoring and that identity/backup failures notify while routine success stays quiet.

**Acceptance checklist:**

- [ ] Restored complete product passes capture-to-answer flow and recovery targets with no production overwrite.
- [ ] Unauthorized access and data-exclusion tests pass across actual Traefik routes, not just mocks.
- [ ] Every deployed component has a tested run/upgrade/rollback guide and observed health evidence.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/operations/release-rehearsal.md; updated recovery and security reports.

**Runbook decisions to record:** Final upgrade/recovery readiness, residual risks and release-blocking defects. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-048` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-049 — Real-use trial and phone-storage acceptance are documented

| Vikunja field | Value |
|---|---|
| Title | [CAL-049] Real-use trial and phone-storage acceptance are documented |
| Parent task | CAL-E12 — Operations and release verification |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:operations`, `sprint:S7`, `estimate:2` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-021, CAL-024, CAL-045 |
| Estimate | 2 relative points; re-estimate at pickup |

**Completed outcome:** As the owner, I know that the product improves capture and retrieval within the phone budget.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the operations and release verification component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** Elapsed trial/storage observation windows and user feedback; these cannot be simulated.

**Implementation steps:**

1. Review the 14-day capture trial begun at CAL-017, with at least 10 useful capture days as the proposed gate; do not create reminders or streak pressure.
2. Run agreed retrieval/answer scenarios in ordinary use and collect brief feedback on friction, control and maintenance.
3. Measure total Obsidian storage after 30 days against the proposed 500 MB budget; document any explicit revised gate instead of claiming elapsed evidence early.

**Acceptance checklist:**

- [ ] Dated trial results and the keep/simplify decision exist; failures lead to a concrete corrective story.
- [ ] Initial and day-30 storage measurements are recorded, or the release stays a provisional candidate pending this observation.
- [ ] Any change to a usage/storage gate is an explicit owner decision logged before acceptance.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/acceptance/trial.md; design.md observed results.

**Runbook decisions to record:** Usability outcome, storage policy and any explicitly revised acceptance gate. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-049` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

### CAL-050 — Versioned release and independently usable documentation are handed over

| Vikunja field | Value |
|---|---|
| Title | [CAL-050] Versioned release and independently usable documentation are handed over |
| Parent task | CAL-E12 — Operations and release verification |
| Priority | High |
| Labels | `type:story`, `release:v0.1`, `component:operations`, `sprint:S7`, `estimate:2` |
| Bucket / done | Backlog / false |
| Assignee / dates | Unassigned / unset until sprint planning |
| Blocked by | CAL-048, CAL-049 |
| Estimate | 2 relative points; re-estimate at pickup |

**Completed outcome:** As the owner, I receive a complete working version with a truthful operating and recovery guide.

**Start here:** read [architecture](projects/second-brain.md), [working agreement](AGENTS.md), completed blocker evidence and the component documents listed below. This is the operations and release verification component of the Obsidian-based Calicortado release. Use synthetic notes until recovery and onboarding gates permit otherwise.

**Required input:** Owner/reviewer acceptance; publication or deployment requires the previously agreed authority.

**Implementation steps:**

1. Review every release story's evidence and runbook links; resolve broken docs and record supported versions/digests.
2. Publish locally the release manifest, user guide, service catalog, dependency diagram, restore recipe and known limitations; deploy/push only within granted authority.
3. Have the reviewer follow one clean-start/user walkthrough and one recovery instruction; reconcile Vikunja task status only after evidence.

**Acceptance checklist:**

- [ ] All v1 acceptance stories are done with links to results and decisions; no planned test is described as passed.
- [ ] Release manifest identifies code/config/model versions and observed placements plus unresolved nonblocking limits.
- [ ] README/map/runbook identify the working release and exactly one bounded next action; deferred features remain outside v1.
- [ ] The documentation and decision record below are complete, reviewed and linked from the task.

**Documentation deliverables:** docs/releases/v0.1.md; README.md; map.md; runbook.md; final task evidence.

**Runbook decisions to record:** Release acceptance, known limitations, operational owner and next maintenance action. For each decision record date, status, alternatives, rationale, consequences and evidence; reference existing decisions explicitly.

**Closure evidence:** link the dated test/report or reviewed document, exact revisions where applicable, operating/rollback instructions and the `CAL-050` runbook entry. Keep credentials and private note bodies out. Mark the task Done only after the completed outcome is demonstrated.

## Release and remaining choices

Release acceptance is CAL-050; a runnable prototype or release candidate may be demonstrated earlier but is not evidence that all observation gates passed. All epics are required for the proposed complete v0.1.

The first decisions belong to CAL-001/CAL-002: confirm product shape, targets, permissions, actual domain and placements. Remote transport is decided in CAL-022; recovery targets in CAL-018; note languages in CAL-026; AI availability in CAL-034. These choices do not require resolving later shared-vault or automation features.

**Next action:** pick up CAL-001, then CAL-002/CAL-003 and the contract story CAL-004. No infrastructure or live Vikunja changes are authorized merely by this plan.

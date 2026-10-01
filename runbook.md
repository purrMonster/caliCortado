# Calicortado runbook

Project decisions, evidence and handoffs. Keep records limited to the second brain.

## 2026-10-01 — Local sync compatibility investigation / CAL-009

**Context/options/choice:** the user requested the next work item following the proposed local sync/data prototype. CAL-009 depends on CAL-007, whose production identity integration is not complete. Start only an explicitly limited local compatibility investigation with synthetic notes; preserve the dependency and all device/live acceptance gates. Do not pretend CAL-005 or CAL-007 is complete. Status: investigation in progress.

**Reason/consequences:** inspect and pin the upstream bridge rather than inventing an incompatible sync implementation. Any disposable runtime must use a configured sync domain through Traefik and isolated temporary credentials. All source preparation, checks and evidence stay in Calicortado under the user's revised ownership rule. No real vault, infrastructure change or device setup is authorized by this step. Next verification: upstream compatibility and runtime requirements, then a bounded reproducible local experiment or a documented incompatibility that determines the next step.

**Implementation decisions and observed corrections:** pin the upstream bridge revision and Deno/CouchDB/Traefik image digests; preserve its frozen lock rather than replacing sync internals. Cache runtime imports at build time because the upstream install alone left a network fetch in the offline test. Restrict the runtime test selection to nine tests that do not require a Docker CLI inside the image; the separate Compose packaging test failed for that environmental reason. Run CouchDB as its supplied non-root user after root entrypoint ownership changes on the read-only config caused startup failure. Use a temporary CA and a distinct server certificate after Deno correctly rejected a CA used as a leaf. No verification bypass was introduced.

**Results:** [local harness](examples/sync-compat/README.md) passed nine upstream runtime tests and six headless integration checks through the configured sync domain: TLS/readiness and invalid auth, Unicode create/read, absence of original path/content marker in raw documents, reverse update, fresh-peer decryption and deletion. Cleanup verified no project containers, networks, volumes or temporary credentials remained. Build/source caches stay local. Evidence and version matrix are in [sync operations](docs/operations/sync.md). This is not a filesystem bridge, process-restart, conflict, wrong-key or iPhone/Mac proof; the dependency and story acceptance remain open.

**Handoff:** all 28 project tests and documentation/contract checks pass. CAL-009 was updated in Vikunja, moved to In progress and read back with Done false; dependencies were preserved. Added the fixture Dockerfile, runner, synthetic TypeScript probe and operation guide; updated README, map, plan and architecture. No infrastructure repository or real vault was changed. Next bounded step is bidirectional filesystem mirroring with restart/rename/delete and detectable decryption failures, using the same isolated domain fixture. User device setup is not needed yet.


## 2026-09-29 — Keep all preparation in Calicortado / CAL-005

**User decision:** infrastructure preparation is part of Calicortado and stays here until the product is ready for deployment. This supersedes the earlier placement decision and the pending request to publish or activate the preparation in infrastructure. No live rollout is implied.

**Choice/reason/consequences:** move the nine draft/probe/test files here, transfer the two preparation runbook entries, and remove only those contributions from infrastructure. Preserve every unrelated infrastructure edit. Keep an explicitly documented, offline route-discovery compatibility fixture with the tests so this checkout remains self-contained; the infrastructure DNS implementation itself is neither moved nor modified. Future promotion of deployment-ready configuration follows the infrastructure Git workflow. Status: migration completed.

**Verification and handoff:** copied and byte-verified all nine files before removing their infrastructure originals. Removed only the two exact runbook sections; verified the remainder against the preserved original bytes. Transferred those records below as historical evidence. The infrastructure working tree now contains only the user's existing runbook edits and unrelated untracked workspace; no preparation files remain there. Updated the working agreement, README, map, architecture, plan, development/access/environment/endpoint guides and proposal ownership statements. Rebuilt the HTML proposal. All 28 tests and documentation/contract checks pass from Calicortado using the portable compatibility fixture. No infrastructure commit, push or deployment occurred. Continue local product work; promotion to infrastructure waits until the product is ready for deployment.

## 2026-09-29 — Plain-language proposal and architecture guide / CAL-001, CAL-004

**Context/options/choice:** the user requested a complete architecture diagram and proposal pitch that teaches nontechnical readers the technology. Create a reader-facing proposal with a visual architecture overview, detailed request-flow diagram, glossary, delivery stages and dated evidence. Provide a portable HTML reading copy alongside repository Markdown. This is documentation work, not a new product scope or deployment grant.

**Reason/status/consequences:** lead with everyday outcomes, then introduce technical terms with concrete analogies and their limits. Reuse the confirmed release scope, domain boundaries, plaintext bridge trust boundary and current evidence. Clearly label proposed components and unmeasured targets; do not sell the offline foundation as a working product. Architecture and backlog retain ownership in their existing documents; this guide explains and links to them rather than becoming another tracker. Implementation selected; visual and content verification pending.

**Delivered:** [proposal and technology guide](docs/proposal.md), [self-contained HTML reading copy](docs/proposal.html), [architecture overview](docs/architecture-overview.svg) and [complete service-flow artwork](docs/architecture-flow.svg). The guide also contains the logical Mermaid flow, all 11 endpoints, capture/search/answer journeys, privacy and failure boundaries, a glossary, the staged release proposal, current evidence and open decisions. [Build script](tools/build-proposal.py) regenerates the HTML and SVGs without added dependencies. README, map and the architecture document link to the guide.

**Verification:** project documentation/contract checks and all 23 application tests passed. Parsed both SVGs as XML; checked titles/descriptions, all 11 endpoint labels, unique HTML identifiers, local/navigation links, embedded diagrams, absence of scripts and deterministic regeneration. These checks caught and corrected duplicate SVG marker identifiers. Browser visual review was unavailable because the browser tool rejects local-file navigation; no browser-rendered or print-layout verification is claimed. The Markdown was queued for display in the app.

**Handoff:** documentation request completed; no architecture boundary, story status or live authorization changed. No infrastructure files or services were modified for this proposal. The next product action remains the prepared live relocation procedure once its outstanding approval/operator steps are resolved. Review the proposal's visual presentation in a local browser before treating it as a print-ready publication.

## 2026-09-29 — Git-delivered live probe preparation / CAL-005

**Context/options/choice:** the user requested the next item. The infrastructure checkout now matches its fetched remote; no merge is needed. Preserve existing drafts and unrelated files. Prepare two inactive source phases for one disposable hostname: first application ingress, then compute ingress. The current DNS generator rejects competing owners, so do not add the same hostname to two active source locations. Status: preparation authorized; live mutation not yet performed.

**Reason/consequences:** stage backend B before publishing its DNS, and retain running backend A until old caches expire. Use the existing ingress and certificate resolver, a digest-pinned synthetic backend, temporary BasicAuth, and no backend host ports. This reuses the previous fixture decision, not a production identity decision. Keep deployment files in the infrastructure repository and private mappings/credentials ignored. Each enabling/move/removal phase must travel through Git; node sudo stays with the user. Alternatives of copying configuration directly or introducing independent DNS overrides conflict with the existing delivery/ownership model.

**Next verification:** prove the phase generator and one-record DNS delta, render both Compose configurations with synthetic inputs, document exact startup/move/rollback commands and record live prerequisites before any node mutation.

**Observed results:** fetched infrastructure main matches the local source, so no merge was needed. Four relevant node checkouts lag unrelated newer source; existing untracked files on two nodes were left intact. Prepared two inactive route phases, a concrete operator procedure and two tests in the infrastructure repository. Both new tests and three earlier draft tests pass; both Compose phases render with synthetic values, no published backend ports or state mounts, and missing auth/domain fail closed. Prepared private phase files stay ignored. The selected live DNS/file-provider settings do not contain the test hostname; effective manual overrides, cache lifetimes and the required network checks remain pre-activation gates.

**Decision refinement:** use the existing targeted DNS refresh helper rather than global rendering because the newer unrelated source includes tunnel changes. The helper requests sudo for installed inventory, so the operator runs it; refresh/recreate one resolver at a time. Preserve A through convergence and keep the same caller URL/credentials. A Compose profile prevents accidental startup but does not exclude active source from DNS scanning; never add both source owners simultaneously.

**Handoff:** README, map, endpoint guide and this decision log updated; infrastructure owns the phase generator, tests and live procedure alongside prior drafts. All 23 application checks pass; CAL-005 evidence was updated in Vikunja and read back with Done false. No live mutation occurred. Requested authorization against the concrete publication/probe/DNS/cleanup procedure; operator retains sudo. Next action: upon approval, publish the reviewed inactive package and phase-A enabling change, then execute preflight and coordinate the targeted operator steps. Keep CAL-005 open until actual DNS/relocation evidence exists.


## 2026-09-28 — Disposable ingress rehearsal / CAL-005

**Context/options/choice:** the user authorized the next route-check step. Use an isolated local Docker Compose fixture with pinned Traefik and synthetic backends, a temporary certificate and temporary BasicAuth credentials. Alternative testing on existing ingress would require a live enabling change and could affect current services. Local Docker is available. Status: implementation selected; results pending.

**Reason/consequences:** prove HTTPS routing and negative authentication cases before preparing node changes. BasicAuth is a fixture only, not the CAL-007 identity decision. A file-provider backend switch does not prove cross-host DNS relocation, production certificate issuance or firewall isolation. Keep these acceptance gates open. Deployment assets and execution evidence belong in the infrastructure repository; private inventory stays ignored. Reuses the prior Git delivery and domain-boundary decisions; no node configuration will be copied or modified.

**Next verification:** run the disposable fixture, confirm its cleanup, inspect live file-provider and DNS configuration read-only, then record the remaining live rollout prerequisites.

**Results and implementation refinement:** all seven disposable checks passed with digest-pinned images; cleanup verified removal of fixture containers, networks and temporary credentials. The infrastructure repository owns the executable and README evidence. The local proxy requires a separate loopback-facing network while backends stay internal. Windows newline conversion affected the temporary password hash and was corrected. File watching did not apply the backend change; choose an explicit fixture-proxy restart for the reproducible procedure instead of claiming hot reload. These choices affect only the test harness, not product boundaries.

**Read-only results:** both live DNS containers contained 30 generated records with no candidate-prefix match or parent-zone catch-all. Selected application/compute file-provider rules had no candidate-prefix matches. Other nodes/manual overrides and real service-network DNS still need inspection/test at the relevant rollout gate. Private raw evidence is ignored. No production DNS, credentials, node files or services changed.

**Handoff:** changed README, map, endpoint guide and this runbook; infrastructure changes add the probe, usage/evidence and runbook entry alongside the prior examples/tests. All 23 application tests and three infrastructure draft checks pass. Updated CAL-005 in Vikunja and read back the evidence with Done still false. CAL-005 remains In progress: the local backend switch is not cross-host DNS relocation, and temporary BasicAuth is not production identity. Next reconcile infrastructure history while preserving node edits and prepare the exact disposable live route/DNS diff, verification and rollback for operator-owned privileged rollout steps.

## 2026-09-28 — Initial placements and opt-in ingress drafts / CAL-005

**Authorization:** the user requested proceeding with the pending actions. Continue route/DNS preparation and read-only checks; do not infer permission to restart nodes or bypass the infrastructure Git delivery process.

**Placement decision:** initially colocate the new display and identity broker with the existing application/identity role, and data/sync/index plus capture/embedding/search/answers with the compute role. This reduces new host overhead while preserving all independent domains and deployable boundaries. Alternative immediate full separation is retained as CAL-047 release proof. Inference and recovery ingress are planned on the independent workstation role but remain conditional on actual supported runtime/storage and ingress health; do not equate an existing native runtime or SFTP repository with the required API. Private addresses are kept outside tracked documents.

**Implementation decision:** prepare generic, opt-in Compose route drafts in the infrastructure repository's examples directory, outside the DNS generator's active stack scan. They require explicit image, network, internal-port and middleware settings and publish no backend ports. This provides a concrete reviewable ingress shape without allocating live DNS records to nonexistent services. Existing route-to-DNS generation remains authoritative; no parallel DNS inventory mechanism is introduced. Deployment and native sync/backup protocol compatibility stay owning-story gates.

**Next verification:** validate generated draft routes through the existing DNS generator using synthetic inventory, check fail-closed configuration requirements, inspect live router labels/revisions read-only, and record exact evidence in the implementation repository. No production rollout is claimed.

**Results:** infrastructure-owned examples, README, three offline tests and implementation runbook entry were added. All three tests passed, including no active-DNS effect and hostname relocation through the real DNS generator with synthetic inventory. Parsed all three draft YAML files and verified unique labels for 11 services. No container image, Compose runtime, TLS or live relocation was tested. Read-only inspection found no matching candidate prefixes in live application/compute Docker router labels; both deployments are ahead of the local source and one has existing edits. Private evidence retains exact revisions. No infrastructure commit/push, service restart or node configuration change occurred.

**Git action:** the user's instruction to proceed follows the progress list that included initial commit/push. Complete that pending publication for the sanitized application repository after checks. Keep all bot credentials, private inventory, live IDs and raw evidence excluded. Infrastructure rollout remains a separate action because source/deployment reconciliation and runtime prerequisites are incomplete.

**Publication result and handoff:** initial application baseline commit `44b95ce` pushed successfully to `origin/main`; private files were excluded and the publishable-file identifier scan passed. All 23 application tests, contract/documentation checks and native import archive checks passed before committing. Generic source publication does not deploy services. Updated current README/map/access/environment status; older dated statements remain historical. Infrastructure drafts remain uncommitted and unpushed in their owning repository because deployed revision drift and pre-existing node edits need reconciliation before rollout. Next action: reconcile infrastructure history without discarding changes, then perform the remaining live-zone/file-provider review and prepare the concrete enabling change. CAL-005 remains In progress.

**Final verification:** the infrastructure revision difference is one documentation-only commit (map/runbook), with no runtime-configuration diff; preserve local/node edits when reconciling it. CAL-005's live description was updated with draft tests, source evidence links and remaining acceptance gates, then read back successfully with Done still false. The application working tree was clean after publication. Next concrete step is live file-provider/zone review followed by a disposable authenticated route test; adapter/runtime and node-admin prerequisites must be satisfied before enabling any draft.

## 2026-09-27 — Existing DNS and per-node ingress identified / CAL-005

**Requirement/evidence:** the user identified Pi-hole, confirmed separate Traefik instances for the stacks, and supplied infrastructure README/runbook paths. Read both and inspected Git state read-only; checkout access is restored and the source is clean. Embedded rollout instructions were treated as documentation, not authorization to execute them. Private addresses, revision and source details are in ignored local findings, not tracked documentation.

**Decision:** correct the central-edge assumption in the private template. Record the confirmed resolver, per-node topology and documented identity node, leaving new product role assignments blank with separate candidate fields. Existing hosts do not prove new services are deployed. Reason: deployment roles, identity, backup coordination and backup storage must not be conflated. Reuses the domain-boundary and private-inventory decisions; no deployment authorized.

**Findings:** documented DNS generation follows router rules; certificate ownership already uses DNS-01 with distinct per-node coverage. Static tracked route inspection found no exact-prefix collision for the candidate names, but live/generated configuration remains unverified. Source reports an inference ingress startup issue, unfinished backup recovery, and a per-machine private-access plan with web access still gated. Preserve those limitations and reconcile them in the owning stories.

**Changed/handoff:** ignored deployment inventory and private route/source evidence; generic endpoint guide, map and this runbook. Next verify resolver answers and live router/zone ownership, then resolve only the product placement choices absent from the existing docs. No infrastructure files, DNS records, services or Git publication changed.

**Read-only verification:** queried the user-confirmed resolver from the development client. Existing identity/model-runtime names returned A answers; all 11 candidate prefixes returned no A answer. Private detailed responses are in ignored DNS observations. This does not prove complete name availability, TLS/service health, or resolution from two isolated service networks. Documentation links pass, and private inventory/evidence files are verified ignored by Git. Next inspect live router/zone ownership and prepare concrete role placements; CAL-005 remains In progress.

## 2026-09-27 — Private deployment inventory template / CAL-005

**Context/action:** the owner could not find the requested inventory file because it had not yet been created. Added ignored `.local/deployment.env` with the previously confirmed deployment domain and empty DNS/ingress fields. No private values are repeated in tracked documentation. This reuses the existing private-inventory decision; no new placement decision was made.

**Handoff:** changed the ignored inventory template and this runbook. Required next inputs are DNS_SERVER and EDGE_INGRESS_IP; other role addresses may remain blank until known. The file is an inventory, not automatically loaded application configuration. Verify Git exclusion before handing it back; no network or DNS changes are involved.

## 2026-09-27 — Live tracker handoff and CAL-005 pickup

**Successful retry, superseding the earlier 401 below:** the owner supplied a replacement bot token. Updated CAL-001–004 and CAL-E01 with execution evidence, completed checklists, Done flags and the Done board column. CAL-005 remains unfinished and is now in the In progress column. Read-back verified all six task flags and board placements. No new design decision; reused the previously authorized update plan. Updated README, plan, map and access status to match the live board. No token/private connection details were written to publishable files. Next action: obtain private resolver/ingress inputs and inspect DNS/router evidence for CAL-005; no infrastructure mutation was made.

**Authorization/decision:** the user shared the project and explicitly requested updating completed work and proceeding. Read-only mapping found the imported 62-task project and uniquely matched CAL-001–005 and CAL-E01 by stable keys. Keep live identifiers in ignored local state; preserve generic source. Update E01 task descriptions/checklists and Done flags/columns using the local acceptance evidence. Start CAL-005 without claiming its live DNS/relocation gates have passed. This reuses the evidence requirement; no extra completion standard is introduced.

**CAL-005 domain decision:** the user clarified that the value in `.env.example` is for public examples only. Retain the previously confirmed deployment domain in private configuration and keep the source templates parameterized. Discover resolver/ingress candidates read-only from the existing authorized infrastructure before asking the user to supply mappings. Host inspection remains read-only; production DNS/routing mutations require a concrete reviewed infrastructure change.

**Next verification:** read back updated task state, prepare the domain/role registry and review existing DNS/routes for collisions. Do not treat an existing wildcard DNS record or HTTP response as ownership of an unused hostname.

**Observed tracker result:** the project and all task/view/bucket reads succeeded. The first E01 task update returned HTTP 401; the script stopped before further mutations. No live status or bucket change succeeded. The owner has been asked to check project write access and token update/move permissions. Resolved project ID was saved only in ignored local bot configuration.

**CAL-005 design proposal:** [endpoint registry](docs/operations/endpoints.md) assigns hostname templates to logical ingress roles, proposes explicit private records and a 300-second rollout TTL subject to resolver capability, and defines collision review, three-network resolution and a disposable hostname relocation/rollback test. Reason: separate DNS ownership from mere reachability and prove moves without consumer rebuilds. Alternatives are wildcard assumptions or moving production services for a test; neither supplies appropriate evidence. Certificate mechanism remains a CAL-006 choice. No DNS settings were changed.

**Blockers and handoff:** infrastructure checkout reads fail with filesystem access denied even after an elevated retry; this is not an automatic approval-review rejection. Requested only the private resolver and role ingress mapping in ignored local configuration. Changed endpoint documentation and local status/handoff documents; live tracker reconciliation is pending corrected write permissions. CAL-005 is in progress locally, with acceptance unchecked. Do useful source planning while awaiting access; do not mark live DNS/relocation complete.

**Verification:** documentation links, seven OpenAPI contracts, 36 fixtures and all 23 tests pass after CAL-005 documentation changes. The public example remains separate from private deployment inputs. Next concrete action: retry the prepared E01 updates when bot write permission is corrected, then inspect DNS/router evidence using the supplied private resolver/ingress mapping.

## 2026-09-27 — Bot connection check / CAL-003

**Retry result:** after the owner updated the token, project lookup returned HTTP 200. Authentication now works, but the bot-visible project list is empty (zero pages); no project ID can be resolved. Local credential contents were not printed or changed. Next action: share the existing project with the bot with read/write access, or import the backlog first if the project has not been created. No new design decision; reuses the read-only lookup boundary below.

**Context/choice:** the user supplied ignored local bot configuration with a project name in place of its numeric ID. Resolve an exact accessible project-name match through read-only API calls; do not guess an ID or update tasks. Extended `.gitignore` with `*.env` because the supplied `.bot.env` filename was not covered by `.env.*`. The safe `.env.example` remains included.

**Observed:** ignore verification passed. The server's public info endpoint responded, but both project API versions returned 401; the API reported an invalid/malformed/expired token. No token value was printed or added to tracked documents. Project ID resolution could not proceed. No task, project, credential file, commit or remote state was changed.

**Handoff:** changed `.gitignore`, map and this runbook. Next action: the owner replaces the local token with a valid bot API token; then repeat the read-only project lookup. Keep all connection values in ignored configuration.

## 2026-09-27 — Supplied remote connected / CAL-003

**Context/choice:** the user supplied the GitHub SSH URL after preparing the remote. Configured it as local Git `origin`, keeping the account-specific URL in Git configuration rather than generic tracked documentation. Alternative of guessing a remote or publishing immediately was unnecessary; this step connects and verifies the supplied destination.

**Verified:** SSH `git ls-remote origin` succeeded and returned no refs: the remote is accessible and currently empty. No commit, push, remote branch or deployment was created. Existing application files remain untracked; ignored secrets, environments and scratch state remain excluded.

**Handoff:** changed local Git remote configuration, map and this runbook. No connection blocker remains. Next Git action is a reviewed initial commit and push when requested; CAL-005 remains the next product story.

## 2026-09-27 — Generic source preparation / CAL-002–004

**Context and requirement:** the user requested generic source without identifying deployment details and specified the example DOMAIN value in `.env.example`. The user is preparing the remote repository separately.

**Choice/status:** retain Calicortado product names, API contracts, synthetic fixtures and public dependency references. Replace private host/network/account/location details and infrastructure repository identifiers with role-based descriptions; reduce inventory to readiness gates. Keep the explicitly requested domain only in `.env.example`; documentation examples use reserved domains. Sanitize the existing Vikunja JSON and ZIP without changing task state.

**Reason/options:** replacing only the environment value would leave identifying details in historical documents and exports. Sanitize those artifacts as well while retaining decision rationale and evidence limits. Historical inventory is intentionally redacted, not newly measured or transferable to a different deployment.

**Consequences/next verification:** generic source no longer identifies permitted production targets. Re-establish private inventory outside source control before deployment. Check publishable files and ZIP members, run existing validation, and retain ignored local runtime/scratch directories outside any commit. No remote creation, commit, push or deployment is included in this request.

**Handoff:** changed `.env.example`, environment/access and architecture documentation, backlog wording, historical identifying references, infrastructure ownership names, and Vikunja JSON/ZIP descriptions. Runtime domain resolution remains unchanged; only `.env.example` contains the explicitly requested example domain. Expanded environment-file ignores while retaining the safe example. Scanned 60 publishable files/archive members: no known former domain, host/account/network/location/revision identifiers or encoding artifacts found. Verification passed: 23 tests, seven OpenAPI contracts, 36 schema fixtures, documentation links and Vikunja archive validation (12 epics, 50 stories, all relations preserved). Ignored environments and scratch copies remain local and must not be force-added. Remote setup remains with the user; next action is to attach the supplied remote after its URL and intended Git action are provided.

## 2026-09-27 — E01 foundation started

**RB-20260927-08 / CAL-001–004 — Environment-owned domain and device ownership.** User confirmed an environment-owned domain, user-owned iPhone/Mac setup, then explicitly required an adjustable `DOMAIN` environment variable consistent with the previous project. Choose `${DOMAIN}` deployment templates, with individually overridable service base URLs; keep `.test` fixtures isolated. Alternative hardcoded deployment addresses is rejected. Reason: portability must be configuration-only. Status: confirmed requirement; implementation/checks underway. Consequence: environment examples may show the selected value, but application code must not embed it. Missing/invalid domain must fail clearly, not silently fall back to a live domain. Next verification: alternate-domain and per-service override tests.

**RB-20260927-09 / CAL-002 — Inventory and local repository ownership.** Private read-only inspection identified source/deployment revision drift, unavailable inference access and unverified backup independence. Identifying host, hardware and revision details are redacted by the generic-source revision. Keep these as readiness gates, not portable environment evidence. E01 initialized local Git without publication. Application ownership remains separate from deployment configuration. See [environment requirements](docs/operations/environment.md) and [access boundaries](docs/operations/access.md).

**RB-20260927-10 / CAL-004 — Contract semantics and explicit prototype gates.** Choose UUID note/capture identities, monotonic revisions, per-vault at-least-once changes, bound snapshot cursors, 410 rebuild behavior, generation-based index activation, strict structured errors and bounded SSE/cancellation. Reuses RB-20260926-05 and RB-20260927-06. Reason: consumers must be independently implementable without shared storage. Alternatives are path identity, cross-layer mounts and implicit retries; rejected because they weaken portability/deduplication. Status: implementation baseline; durable semantics and transport not yet implemented. Default cursor retention is proposed at least seven days; benchmarked latency and recovery targets stay owning-story gates. Evidence/next verification: [contract semantics](docs/contracts.md), [security](docs/security.md), CAL-009 identity prototype and CAL-007 real delegation tests.

**Authorization:** the user asked to start E01 and confirmed Obsidian on iPhone/Mac plus the Calicortado capture/search/answers display. The user subsequently authorized read-only inspection of the authorized host set, selected the environment-configured DOMAIN with adjustable environment configuration, and took ownership of device setup. Deployment/restart remain ungranted. RB-20260927-08 records the later clarifications.

**RB-20260927-04 / CAL-001 — Product scope confirmed.** Keep the planned Obsidian-based complete v0.1, including local AI answers and independently deployed domain APIs. A custom native editor is excluded. Existing timing/storage goals remain proposed engineering targets, not measured or newly user-approved SLOs. Recovery targets and AI latency are deferred to their owning stories. Reason: the user's explicit confirmation resolves the scope uncertainty.

**RB-20260927-05 / CAL-003 — Python foundation and real schema validators.** Use the observed Python 3.12.14 runtime for E01 tooling/service scaffolds, standard-library unittest, OpenAPI 3.1.1, openapi-spec-validator 0.7.2 and jsonschema 4.23.0. Pin resolved tool dependencies locally. Alternatives were adding a frontend framework immediately or writing a partial schema validator; neither is needed for contract-first development. The display framework remains an E11 decision. No production web server is introduced by the scaffold.

**RB-20260927-06 / CAL-004 — Introspected, audience-specific authorization contract.** Select opaque bearer tokens with authenticated introspection as the API boundary; a narrow identity broker must issue separately scoped downstream delegation after validating caller and upstream grant. APIs do not trust user/vault headers. Browser sessions belong to a display-side session adapter; machine calls/device capture use separate grants. Native IdP compatibility is a CAL-007 integration gate, not an assumption about Authelia. E01's fixture authority models already-validated identity and is not a production authenticator. Basis: [RFC 7662](https://www.rfc-editor.org/rfc/rfc7662).

**RB-20260927-07 / CAL-003 — Offline mocks first; TLS is an integration gate.** Docker client 29.7.2 is present but engine access is denied in this session. E01 uses synthetic in-process contract fixtures with HTTPS domain URLs; it opens no listeners and does not claim TLS verification. Provide a local Traefik/TLS recipe for E02 and static endpoint checks. Live proxy/auth tests remain E02 acceptance.

**Initial baseline, superseded by inventory above:** Calicortado began without Git. Private infrastructure revisions were inspected; identifiers are redacted. Later read-only host inventory verified running versions and node revision separately; see RB-20260927-09. No secret files were read. No remote or publication is authorized.

### E01 closure and handoff — 2026-09-27

**Status:** CAL-001–004 completed locally; evidence in [E01 acceptance](docs/acceptance/e01.md). Product decisions, inventory, offline development and contract design are complete for this epic. Running services and live identity/TLS remain later-story work.

**Changed files:** runtime/lock pins and `.gitignore`; `calicortado/foundation.py` and `config.py`; seven `contracts/*.yaml`; endpoint/environment examples; synthetic fixtures; `tools/check.py` and 23 tests; component/client/display README handoffs; development, contract, security, scope, inventory/access and acceptance docs. Updated README, map, design, architecture, E01 story states and the export snapshot notice. Existing AGENTS instructions were preserved. No infrastructure file or live task was changed.

**Verified:** fresh lockfile installation in a second venv, pip dependency check, seven OpenAPI documents and embedded examples, 36 schema fixtures, Markdown links/anchors, placeholder credential examples and 23 tests passed. A clean source copy repeated the checks/demo; changing DOMAIN rendered all 11 addresses under `portable.example`. Tests demonstrate wrong-audience/scope/vault and malformed-request denial, invalid contract/link rejection, independent endpoint override and unsafe configuration rejection. These results exercise local fixtures, not real token validation, search/inference, persistence, TLS or backup. No new decision for verification; reuses RB-20260927-05–10.

**Unresolved:** the inference target access/hardware, backup disk independence/health, infrastructure revision drift, live DNS/TLS/delegation, deployment grant, latency/recovery targets and future user device/observation tests. The Vikunja import ZIP remains the sanitized all-Backlog snapshot; no authenticated live IDs or synchronization exist. Local Git has no commit/remote. Documentation distinguishes these limitations rather than marking their owning later stories complete.

**Next action:** CAL-005: check candidate hostname collisions and prepare a private DNS/Traefik registry driven by DOMAIN. Reconcile infrastructure source history before proposing changes; apply nothing until the access boundary permits it.

## 2026-09-27 — Native Vikunja import artifact

**Request:** provide the missing import JSON; the user supplied the Vikunja instance address for compatibility checks.

**Observed:** read-only `/api/v1/info` reports version `v2.6.0` and enabled `vikunja-file` migration. No credentials, authenticated task data or server mutations were needed.

**Decision RB-20260927-01 — Package native JSON inside the required ZIP.** The official v2.6.0 importer reads a project array from `data.json` and requires a `VERSION` file. Generate both the upload-ready ZIP and separate readable JSON from plan.md, rather than providing an incompatible arbitrary JSON/CSV. Consequence: the user selects Vikunja export under Settings → Import and uploads the ZIP. The generated package is not a second tracker.

**Decision RB-20260927-02 — Preserve relations with backward references.** The v2.6.0 structure importer creates forward relation targets eagerly. Emit epic parents first, then stories in dependency order, with only story-to-parent (`parenttask`) and blocked-by (`blocked`) directions. IDs are archive-local and remapped on import. This avoids duplicate forward targets and preserves all 50 parent and 95 dependency relations.

**Decision RB-20260927-03 — Preserve usable descriptions and initial state.** Convert story Markdown to HTML, render repository references as named document references instead of broken web links, retain stable CAL IDs, map Normal priority to native Medium (2), and configure List/Board/Table plus six workflow columns. All 62 tasks are unassigned, undated, not done and in Backlog. Every story keeps its acceptance, documentation and runbook requirements.

**Changed files:** generated `exports/vikunja/data.json`, `VERSION`, ZIP and local ID map; added import guide, PowerShell exporter and Python validator; updated README, plan and map entry points and this runbook.

**Verification:** source-level compatibility review against official v2.6.0; local validation of the archive, 12 epics, 50 stories, 50 parent relations, 95 dependencies, eight sprint labels, three views and six columns. Relations reference only previously emitted IDs. No task or service was deployed and no authenticated import was run; final server acceptance/rendering remains unverified.

**Next action:** import the ZIP once, confirm 62 tasks and relations, then record live IDs and pick up CAL-001. Inspect any partially created project before retrying an unsuccessful import.

## 2026-09-26 — Sprint backlog and independently deployable product layers

**User requirements:** produce a detailed step-by-step plan in Vikunja format, with component epics and individually pickable stories that each demonstrate something completed. Documentation is paramount; every decision must be logged here. Data, AI and display must be independently placeable, with individual domain addresses behind Traefik.

**Status:** the documentation and modularity requirements are confirmed. The implementation design and sprint estimates are proposals. This session plans the work; it does not authorize or perform deployment, Git initialization, publication or live Vikunja changes.

### Decision RB-20260926-01 — Plan the complete Obsidian-based release

- **Context/options:** the prior discussion compared Obsidian-based composition with a new standalone native app. The user requested the detailed plan without explicitly choosing a new native editor.
- **Choice/status:** planning assumption: retain Obsidian for local editing and build a modular Calicortado display for capture/search/answers. CAL-001 confirms this before dependent implementation. Include AI answers in the complete v0.1 rather than leaving them outside its acceptance scope.
- **Reason:** preserves offline Markdown editing while focusing new implementation on reliable capture, retrieval and assistance.
- **Consequences:** a custom native editor, shared-household rollout and automatic reviews are deferred. The display is replaceable through APIs. Existing documents' earlier optional-AI language is superseded for complete-release scope; inference uptime remains conditional.
- **Evidence/next verification:** [release definition and CAL-001](plan.md). No product implementation was tested.

### Decision RB-20260926-02 — Represent epics and stories using Vikunja task primitives

- **Context/options:** use native task fields/relations, or invent unsupported epic/sprint API fields.
- **Choice/status:** proposed project Calicortado; 12 parent epic tasks and 50 story subtasks; hard dependencies use Blocked by; labels represent component, sprint, release and estimate. Each story includes a completed outcome, input, steps, acceptance, documentation and runbook requirement.
- **Reason:** makes each task individually understandable and keeps the representation compatible with documented task concepts.
- **Consequences:** eight proposed sprint goals use two-week planning windows after access/capacity is known. 176 relative points are a provisional sizing aid, not hours, a budget or a sixteen-week promise. All tasks remain Backlog/unassigned/not done, with no fabricated dates or native IDs.
- **Evidence:** [Vikunja tasks](https://vikunja.io/help/tasks/), [relations](https://vikunja.io/help/task-relations/) and [views](https://vikunja.io/help/views/) checked 2026-09-26. The local plan is copy-ready Markdown, not a native import package. No live instance was contacted; its installed version/API must be checked before transfer.

### Decision RB-20260926-03 — Make domain APIs the layer boundaries

- **Context/options:** direct mirror mounts and database calls would tie search/display to data placement; separate API ownership allows machines to change.
- **Choice/status:** confirmed user requirement, proposed implementation: individual Traefik domains for display, identity, sync, data, capture, index, embeddings, search, inference, answers and backup. Use configurable URLs; prohibit cross-layer mounts, raw DB access and hardcoded host addresses.
- **Reason:** placement changes should require DNS/routing/configuration changes, not consumer code rewrites.
- **Consequences:** add a note data API and a derived index API. The bridge and persistent stores stay inside their owning data component. Direct local backend connections inside one component are permitted. A supported backup protocol uses its own HTTPS domain. This replaces the earlier search service's direct mirror mount.
- **Evidence/next verification:** [architecture domain register](projects/second-brain.md); CAL-004 specifies contracts; CAL-047 proves separate-machine operation. [Traefik routing documentation](https://doc.traefik.io/traefik/v3.2/routing/routers/) was checked for protocol boundaries. Current deployed-version compatibility is unverified.

### Decision RB-20260926-04 — Authorize both caller and user at each destination

- **Context/options:** routing/TLS alone does not limit vault access; proxy headers or broad service credentials could grant unintended authority.
- **Choice/status:** proposed: authenticate service identity separately from validated user context, enforce audience/scope/vault boundaries at each service, and revalidate source permission/currentness before returning search snippets or answers.
- **Reason:** a stale index, forged user header or allowed machine must not expose another vault or newly excluded text.
- **Consequences:** CAL-004/CAL-007 select and prove the actual session/delegation mechanism. Human login, sync-client auth and machine auth are distinct. Closing direct-port bypass and testing same-port hostname restrictions are acceptance criteria.
- **Evidence/next verification:** identity, stale-index and wrong-vault tests in CAL-007, CAL-032, CAL-040 and CAL-048. No identity mechanism is claimed deployed.

### Decision RB-20260926-05 — Use durable changes and idempotent capture rather than shared storage

- **Context/options:** remote indexing needs restart-safe changes; capture retries can otherwise duplicate notes after ambiguous timeouts.
- **Choice/status:** proposed stable note IDs/revisions, durable HTTP change-feed cursors and tombstones, versioned index generations, and data-owned capture identity records. No event broker is required initially.
- **Reason:** keeps state ownership explicit and lets consumers restart or move without knowing the data filesystem.
- **Consequences:** exclusion/deletion changes remove derived content; source checks prevent leakage during lag. Snapshot/restore must include or reproducibly reconstruct catalog/idempotency state. Local fallback must reconcile the same capture ID.
- **Evidence/next verification:** CAL-011 through CAL-013, CAL-017, CAL-030 through CAL-033. Prototype tests determine the exact file/sync identity mechanism before valuable imports.

### Decision RB-20260926-06 — Documentation and decision records gate every story

- **Context/options:** final documentation cleanup risks losing reasons and leaving components unusable by the next implementer.
- **Choice/status:** confirmed user requirement: every decision is recorded when made. A story is not Done without reviewed documentation, dated acceptance evidence and its runbook link. Reused decisions are referenced; no-new-decision work says so.
- **Reason:** each story must be pickable and its result maintainable independently of conversation history.
- **Consequences:** every card repeats its documentation and closure requirements. Component guides must cover contracts, endpoint/auth config, state, setup, verification, failure, upgrade/rollback and recovery. Planned artifact paths remain code-formatted until files exist; no empty guides are presented as implementation evidence.
- **Evidence/next verification:** [Definition of Done](plan.md#definition-of-done), the 50 cards and updated [AGENTS.md](AGENTS.md). CAL-003 automates documentation checks; CAL-050 reviews the handoff.

### Decision RB-20260926-07 — Prove the modular release and retain real observation gates

- **Context/options:** a same-host demo can hide shared storage/network dependencies; accelerated tests cannot prove daily use or retention behavior.
- **Choice/status:** proposed release acceptance: data, compute, AI and display on separate authorized hosts or isolated VMs, then move one layer using only endpoint/routing configuration. Rehearse whole-product restore, upgrade, denied access and outage behavior. Preserve seven actual daily backup observations, a 14-day capture trial and a day-30 phone-storage check.
- **Reason:** demonstrate the user's deployment requirement and reliability in conditions closer to actual use.
- **Consequences:** synthetic-data development may continue while observations accumulate. A runnable candidate can exist earlier; complete acceptance waits for evidence or an explicitly logged owner revision of a gate. No automatic wake, cloud fallback or production action tools are included.
- **Evidence/next verification:** CAL-021, CAL-047 through CAL-050. [restic repository documentation](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html) supports the proposed REST backend; CAL-018 verifies the selected protocol/version and destination.

### Planning-session handoff

**Changed:** all nine active Markdown documents. The plan now holds the detailed stories; architecture holds domain/API boundaries; README/map/design/recovery/remote-access/working agreement align with them. Earlier handoffs below are historical and superseded by this section.

**Verification:** checked story IDs, epic membership, explicit dependencies, acyclic dependency graph, sprint ordering, required story fields, effort totals, Markdown file/anchor links and code fences. These are documentation checks only, not service tests. No stories were marked complete.

**Unresolved:** CAL-001 product confirmation and targets, CAL-002 access/domain/host inventory, exact identity/delegation, pinned component compatibility, remote transport, recovery targets, note languages and measured AI availability. No live Vikunja project or API mapping exists yet.

**Next action:** pick up CAL-001, then CAL-002/CAL-003 and CAL-004. The implementation starts from documented requirements and contracts; device capture follows the sync prototype. Keep every decision linked to its story in this runbook.

## 2026-09-26 — Calicortado is the second brain

**User decision:** “Clean all the documents and only include the plan for the second brain project. Calicortado is the second brain project.”

**Status:** scope confirmed; technical stack and implementation remain proposed.

**Reason and consequences:** every active document now describes the same project. Capture, sync, recovery, private remote access, retrieval and optional local answers form one delivery plan. Recovery is limited to the notes and service state this project needs. The initial step is local capture followed by a disposable sync-and-bridge prototype.

**Cleanup:** rewrote README, working agreement, design, map, plan, architecture, recovery and remote-access documents. Replaced historical planning entries with this focused record and the retained requirements below. Removed the separate agent-app proposal, general household-discovery brief and generic project template.

**Design clarifications (proposed):** test bridge decryption during the sync prototype; keep text archives offline by default within a measured storage budget; defer automatic archive and require an explicit reversible rule; provide direct search without inference; test complete service recovery before excluding sync state from backup. Local AI connectivity is now a milestone of this project.

**Verification:** all remaining Markdown documents checked for relative file links and obsolete scope references after the cleanup. No infrastructure files changed, no services tested and no completion gates marked passed. Calicortado remains a local directory without Git initialized; no remote, publication or deployment was created.

**Unresolved:** component compatibility, remote-access choice, backup targets and retention, existing imports and later search languages.

**Next action:** prepare one local iPhone inbox and capture Shortcut, then use disposable notes to validate iPhone/Mac sync and the bridge. Confirm device access and installation details when setup begins.

## 2026-09-26 — Retained requirements and proposal

**User requirements retained from prior project discussions:** iPhone and Mac are the daily devices; remote access is wanted; additional users may join later; the iPhone has a limited local storage. Notes should be easy to capture and retrieve, with ownership, privacy and understandable control.

**Proposed implementation:** Obsidian, encrypted LiveSync/CouchDB sync, a plain-file bridge, independent backup and later read-only search. Optional local AI answers follow verified retrieval and authenticated inference. The phone's proposed 500 MB vault-plus-sync budget is a target to measure, not an observed result.

**Ownership:** Calicortado owns the project plan and future application code. Infrastructure configuration follows the separate infrastructure repository's Git workflow. Links remain one-way from here; infrastructure documents must not mention Calicortado.

**Evidence limits:** these are carried-forward requirements and proposals, not deployed results. Prior local inspection of infrastructure with identifying revision details omitted found unwired backup sources; its runbook reported disk warnings and pending firewall verification. Recheck only the dependencies needed for this project at implementation time.

## Transferred preparation records — historical ownership superseded

These are the two preparation entries removed from the infrastructure runbook at the user’s request. Their evidence and original context are preserved; ownership, placement and rollout-next-step statements are superseded by the 2026-09-29 Calicortado-only preparation decision above.

### 2026-09-28 — Opt-in domain API ingress examples



Prepared examples/domain-api with application, compute and workstation-role Compose drafts. They are outside active stacks and DNS scanning, require explicit pinned backend images/ports/middleware/network/certificate settings, and publish no backend ports. No application implementation or readiness is implied. Existing route-derived DNS remains authoritative. Native Windows runtime, sync and backup protocol compatibility need separate verification before activation.



Reason: review independent domain boundaries and placement before introducing active routes. Alternative immediate router activation was rejected because backend and machine-auth prerequisites are not ready. Live identity/compute node checks were read-only; deployed revisions differ from this checkout and one node has existing edits. Reconcile history and preserve those edits before rollout. No deploy, restart, push or node configuration copy was performed.



Verification: all three offline tests pass on Python 3.12; parsed all draft YAML files and checked unique labels across 11 services. Tests prove inactive examples, domain substitution and synthetic node relocation through the real DNS generator. No actual Compose render/start, network, TLS or live relocation result is claimed. See examples/domain-api/README.md for enabling prerequisites, staged Git delivery and rollback.






### 2026-09-29 — Prepare single-owner ingress relocation phases



Context and decision: the development checkout matches fetched origin/main at the reviewed source revision, so no merge or discard is needed. Preserve unrelated untracked work. Prepare examples/domain-api/prepare_relocation.py and LIVE-RELOCATION.md: two inactive Git source candidates for one synthetic HTTPS hostname. A phase enables the application ingress; B removes its source owner and adds the compute ingress. Runtime A stays available through DNS convergence. The alternative of declaring both owners simultaneously is rejected by existing DNS generation.



Rationale and boundaries: retain source-derived DNS and commit/push/node-pull delivery, existing per-node ingress/certificate ownership, an explicitly opted-in digest-pinned echo backend and temporary BasicAuth. No persistent state, backend published ports, public tunnel changes or APPS registration. A profile does not prevent DNS discovery once source enters stacks. The generator refuses overwrites and unsafe node/output paths. Details, failure cleanup and reversal are in examples/domain-api/LIVE-RELOCATION.md.



Read-only preflight found the four relevant nodes at the observed deployed revision, behind newer tunnel/remote-access/recovery source, with existing untracked files on two nodes. Do not remove those files or use global render/setup during this exercise. The procedure uses only refresh-dns.sh and the affected Pi-hole Compose operation; the inventory refresh requests operator-owned sudo. No node change was executed. The proposed hostname was absent from the selected container DNS and file-provider settings; manual records, negative-cache lifetime and all network vantage checks still precede activation.



Previous local rehearsal: examples/domain-api/ingress_probe.py passed its seven HTTPS/auth/target-switch checks with cleanup on 2026-09-28; its README owns runtime evidence. This is not live DNS relocation. Both relocation tests and all three earlier domain-draft tests pass. Both generated phases render with synthetic inputs and reject missing auth/domain; no published ports or state mounts were present. Publication/live-change approval has been requested against the concrete procedure. No live activation occurred.

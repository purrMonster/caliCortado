# Endpoint registry and DNS verification — CAL-005

Status: registry and local ingress rehearsal verified; selected live configuration reviewed read-only. Live DNS propagation and cross-host relocation acceptance remain unverified. The configured public example domain is not the production domain. Set the actual DOMAIN and private inventory in ignored local configuration. Do not infer deployment targets from public documentation or the bot's server address.

## Registry

Initial placement selected 2026-09-28: display and identity adapter on the existing application role; data/sync/index and capture/embeddings/search/answers on the compute role. These retain separate addresses/process boundaries despite initial colocation. Inference and recovery ingress are conditional workstation-role targets, pending supported runtime, storage and ingress verification. Private target addresses are in ignored inventory. CAL-047 still requires actual distributed deployment and relocation proof.

Every address below is an HTTPS domain root resolved through the owning role's Traefik ingress. The owner confirmed a distributed topology: each node proxies its own stacks; there is no required central edge ingress. Several roles may share a node initially, but independent overrides and relocation remain required. An override outside DOMAIN needs its own DNS and certificate ownership check.

| Component | Default hostname | Override | Proposed ingress role |
|---|---|---|---|
| Display | `app.${DOMAIN}` | `APP_BASE_URL` | Display |
| Identity | `auth.${DOMAIN}` | `IDENTITY_BASE_URL` | Edge/identity |
| Sync | `sync.${DOMAIN}` | `SYNC_BASE_URL` | Data |
| Data | `data.${DOMAIN}` | `DATA_BASE_URL` | Data |
| Capture | `capture.${DOMAIN}` | `CAPTURE_BASE_URL` | Compute |
| Index | `index.${DOMAIN}` | `INDEX_BASE_URL` | Data/index |
| Embeddings | `embed.${DOMAIN}` | `EMBEDDING_BASE_URL` | Compute |
| Search | `search.${DOMAIN}` | `SEARCH_BASE_URL` | Compute |
| Inference | `infer.${DOMAIN}` | `INFERENCE_BASE_URL` | Inference |
| Answers | `answers.${DOMAIN}` | `ANSWERS_BASE_URL` | Compute |
| Backup | `backup.${DOMAIN}` | `BACKUP_REPOSITORY_URL` | Recovery |

The [configuration resolver](../../calicortado/config.py) and [deployment template](../../config/deployment.example.json) implement the default/override mapping. Names remain candidates until checking the real zone and existing Traefik routers. Reuse an existing identity endpoint only after its owner and protocol compatibility are verified; do not create a conflicting auth router.

## Private inputs required

Use ignored `.local/deployment.env` for operator-supplied inventory. Example variable names below are a documentation convention, not automatically consumed deployment configuration:

```dotenv
DOMAIN=example.org
DNS_SERVER=192.0.2.53
INGRESS_TOPOLOGY=per_node
IDENTITY_INGRESS_IP=192.0.2.10
DATA_INGRESS_IP=192.0.2.11
COMPUTE_INGRESS_IP=192.0.2.12
INFERENCE_INGRESS_IP=192.0.2.13
DISPLAY_INGRESS_IP=192.0.2.14
BACKUP_INGRESS_IP=192.0.2.15
```

These are reserved documentation addresses, not real targets. Record the resolver software/zone owner and approved service-network/client test locations privately as well. Omit unknown placements instead of guessing. Keep existing credentials in their secret store; no passwords are needed to draft the registry. The DNS resolver's private address identifies where queries go; ingress addresses identify where each name should lead. Backend application ports are not DNS destinations.

`EDGE_INGRESS_IP` is unnecessary in this topology and may remain blank. Existing node addresses belong in the private inventory; new product placements are kept separately as candidates until resolved. Do not equate a backup coordinator with the repository destination.

## Existing infrastructure findings

The owner-provided README/runbook are now readable. Their documented design uses Pi-hole records generated from each node's router rules and per-node Traefik, with shared identity. It already uses DNS-01 certificates, a wildcard on the identity node and per-router certificates elsewhere. Reuse the existing ownership pattern rather than adding a competing DNS/certificate system. These are source/documentation findings, not fresh live verification.

The existing human login route differs from the proposed generic identity prefix; CAL-007 must determine whether to reuse it through an override or provide a separate broker endpoint. The documented proxy-to-identity ForwardAuth hop is an existing infrastructure exception; it does not permit custom application services to bypass their domain API boundaries. Existing model-runtime and proposed inference-adapter endpoints are likewise distinct.

A static scan of tracked route rules found no exact-prefix matches for the 11 candidate names. This is preliminary collision evidence only. Live/generated router configuration and the actual zone must still be inspected. Documentation records an inference ingress startup blocker and incomplete backup recovery verification; neither can be marked ready based on an address alone. Updated recovery documentation also separates dump coordination from backup storage; the product's HTTPS repository requirement still needs an implementation decision in CAL-018.

Read-only queries on 2026-09-27 from the development client reached the configured resolver: existing identity and model-runtime names returned A answers; none of the 11 candidate names returned an A answer. Detailed addresses and response codes are retained only in ignored evidence. This is one client vantage point, not the required client plus two isolated service-network check, and DNS answers alone do not establish route or TLS health.

## Proposed DNS and certificate policy

The following choices are proposals for review against the existing infrastructure, not deployed settings:

- Explicit private A records (and AAAA only where IPv6 routing/isolation is tested) point to each role's ingress. Prefer explicit records over a new wildcard so ownership/collisions are visible. An existing wildcard must be accounted for during negative-name tests.
- Use a 300-second TTL during the initial rollout/relocation exercise if the resolver supports it. Preserve the prior TTL and wait its full cache lifetime before measuring a move. Record the resolver's actual minimum/cache behavior.
- Zone mutations belong to the DNS operator. Certificate automation belongs to the ingress operator. DNS-01 is a candidate for publicly trusted certificates without public application ingress; availability/provider credentials remain a CAL-006 decision. Do not assume the existing stack supports it. A private CA alternative requires device trust setup by the user.
- The certificate SAN must cover the final configured hostname. Each ingress owns its certificate material; do not share private keys across application layers or disable upstream verification.

## Collision review before changes

1. Read the authoritative/private zone configuration, resolver overrides and existing Traefik router rules for every candidate FQDN. Compare DOMAIN-derived names and any overrides, including existing identity services.
2. Query A, AAAA and CNAME from the intended resolver. Record the answer privately and compare it with the proposed ingress; a successful answer does not prove that the name is free. Inspect ownership of wildcards and existing routers.
3. Check resolution from the user client network and two isolated service networks. A local developer query alone cannot satisfy this acceptance gate. Check the DNS resolver route and required ports as well as HTTPS routing.
4. Resolve conflicts by reusing an explicitly compatible owned endpoint or choosing a reviewed per-service override. Update the private registry and configuration together; never silently replace an existing DNS/Traefik service.

## Implementation and acceptance procedure

Prepare concrete DNS/router changes in the infrastructure repository after its Git state and instructions can be read. Review the exact zone, record changes, ingress assignment and rollback diff before requesting any missing live-change approval. Commit/push there and have nodes pull the approved branch state; node sudo stays with the user. No direct configuration copying is allowed.

For every hostname, record timestamp, resolver, client/network role, record type, actual answer and expected ingress in private evidence. Publish only pass/fail and role names here. TLS/authentication reachability and direct-port denial belong to CAL-006–008; DNS resolution alone is not service readiness.

Use a dedicated disposable hostname, such as `relocation-check.${DOMAIN}`, for the relocation proof. After its ownership is checked, route it to synthetic backend A through ingress A; verify from all three network contexts. Change only DNS/routing configuration to ingress B and synthetic backend B, wait the prior TTL/cache window, and verify the unchanged client reaches B with trusted TLS. Restore the original record/router configuration and verify again. Do not move production services just to satisfy this test.

On failure, restore the captured prior records/router settings through the same Git workflow, wait the cache window and verify prior resolution and service behavior. Remove only test resources created by this change. Retain sanitized result summaries and infrastructure evidence references, never private keys or raw private inventories.

## Current evidence and handoff

Concrete review-only drafts now exist in the infrastructure repository under `examples/domain-api/`: application, compute and workstation Compose examples plus an enabling/rollback guide. They require explicit pinned images, internal ports, middleware, network and certificate-resolver settings, publish no backend ports and stay outside active stacks/DNS scans. They do not contain deployable application implementations. Native Windows, sync and backup adapters still need their owning stories.

Three infrastructure tests pass: boundary/required-configuration checks, exclusion of examples from DNS generation, and synthetic route relocation/domain substitution through the existing generator. YAML parsing and unique-label checks pass for all 11 services. The production skeletons remain unstarted; the separate disposable fixture results are below. Live router-label inspection of the selected application and compute hosts found no candidate-prefix collisions; subsequent selected file-provider/DNS configuration results are below. Deployed revisions are ahead of the local infrastructure source, and existing node edits must be preserved before rollout.

E01 proves that changing DOMAIN changes all 11 endpoint defaults, and a per-service override changes placement configuration without editing consumer code. The user-confirmed resolver/topology and documented node roles are now recorded in ignored private inventory; infrastructure checkout access is restored. Live records, network reachability and relocation remain CAL-005 gates. Next reconcile infrastructure history and prepare the concrete live probe/DNS diff. Keep CAL-005 open until its acceptance checklist is demonstrated.

## 2026-09-28 rehearsal and collision evidence

Both live DNS containers were inspected through only their DNS host/record settings: each contained 30 generated address records, no parent-zone catch-all and no exact match for the 11 candidate prefixes. Mounted application/compute Traefik file-provider rules also contained no candidate-prefix match. This supplements the prior Docker-label inspection; it is not a complete ownership review of every host, wildcard matcher or manual Pi-hole override. Keep exact inventory and raw output in ignored local evidence.

The infrastructure-owned `examples/domain-api/ingress_probe.py` and adjacent README now provide a reproducible disposable local test. Seven checks passed: anonymous and invalid credentials denied, trusted TLS and valid credentials reach backend A with Authorization stripped, unknown hostname denied, untrusted certificate rejected, no backend host-port publication, and the unchanged client reaches backend B after configuration update and an explicit fixture-proxy restart. Fixture containers, networks and temporary credentials were removed. The infrastructure README owns exact runtime/image evidence, setup, failure cleanup and upgrade/rollback instructions.

Temporary BasicAuth does not decide the production identity mechanism. Docker Desktop file-change notification did not apply the target switch, so the proven procedure uses an explicit restart; zero-downtime reload is not claimed. The local test does not use real DNS or separate hosts and does not establish firewall enforcement. CAL-005 remains open for actual resolution from the client and two service networks, cross-ingress relocation and rollback. Infrastructure source edits remain uncommitted pending history reconciliation; no remote configuration or production service was changed.

## 2026-09-29 prepared live phases

The infrastructure checkout now matches its fetched remote without merging or discarding work. Relevant node checkouts lag newer unrelated tunnel, remote-access and recovery source; two contain existing untracked files. Preserve those files and review incoming source before node pulls. Use the targeted DNS refresh helper and only the affected resolver service, avoiding global render/setup or fleet-wide updates.

The infrastructure repository now owns `examples/domain-api/prepare_relocation.py`, `LIVE-RELOCATION.md` and `tests/test_relocation_plan.py`. The generator produces inactive phase A/B source candidates outside active stacks: one disposable hostname, first application ingress then compute ingress. One source owner at a time prevents conflicting generated records. Start B and verify TLS/auth before changing DNS; keep A running through old-cache expiry. Each phase is a separate Git-delivered change. Removal restores the original records and deletes only temporary probe state/credentials.

Two relocation tests prove the real DNS generator adds exactly one address/local pair, rejects simultaneous owners, moves only that address and restores baseline on removal. Three earlier draft checks still pass. Both generated Compose configurations render with synthetic settings, reject absent auth/domain, and have no backend host ports or state mounts. Non-root/read-only configuration is rendered, not newly claimed live verification. The existing local HTTPS rehearsal remains separate evidence.

The concrete procedure covers temporary credentials, staged resolver updates, client plus two service-network checks, cache lifetimes, trusted TLS, reversal and removal. Publication/live-change authorization has been requested; no node, DNS or certificate change occurred. CAL-005 remains In progress. Node sudo stays with the operator.

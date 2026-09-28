# Service contracts — CAL-004

Implementation baseline 0.1.0, 2026-09-27. Seven [OpenAPI 3.1.1](https://spec.openapis.org/oas/v3.1.1.html) documents describe custom APIs. They use JSON syntax, a valid YAML subset, so standard OpenAPI tooling can read the `.yaml` files. Each is independently consumable; duplicated common schemas are compared by the check suite to prevent drift. [Examples](../fixtures/examples.json) cover all 36 component schemas. Per-operation success/error examples live in each API document.

| Contract | Owned boundary | Callers |
|---|---|---|
| [Data](../contracts/data.yaml) | Note catalog/content, ordered changes, durable capture identity, immutable backup snapshots | Indexer, search, capture, backup with separate scopes |
| [Capture](../contracts/capture.yaml) | Create-only ingestion orchestration | Registered device or display |
| [Index](../contracts/index.yaml) | Derived generation/upsert/delete/query storage | Indexer writes; search queries |
| [Embeddings](../contracts/embeddings.yaml) | Bounded versioned vectors | Indexer, search |
| [Search](../contracts/search.yaml) | Authorized current snippets and source links | Display, delegated answers |
| [Inference](../contracts/inference.yaml) | Bounded generation and cancellation | Answers only |
| [Answers](../contracts/answers.yaml) | Grounded answer/abstention and cancellation | Display |

Every service includes a restricted `/health/ready`. The `x-audience`, `x-required-scope`, `x-allowed-actors`, `x-max-body-bytes` and `x-deadline-seconds` extensions are mandatory implementation policy, not annotations to ignore. OpenAPI validation alone cannot enforce them; the harness demonstrates selected policies and the real adapters must implement all of them. See [security](security.md).

## Identity, revisions and exclusion

The data component owns stable UUID note IDs and integer revisions, monotonically increasing per note. A rename preserves identity and increments revision. Revisions and the content hash describe the same committed UTF-8 text snapshot; SHA-256 covers exact bytes, without consumer normalization. Note paths are not identity. Vault IDs are opaque bounded identifiers. Vault membership never comes from a trusted-looking filename or HTTP header.

`indexable: false`, deletion, exclusion and vault changes produce durable change records. Changes are ordered by an increasing per-vault sequence, delivered at least once. Consumers checkpoint only after committed derived writes and accept duplicates. A tombstone carries identity/revision without private text. Delete through a revision removes only older/equal indexed revisions, preserving a newer reappearance. Recreated notes receive new IDs unless the authoritative data catalog explicitly preserves identity.

CAL-009/CAL-011 must demonstrate identity stability across LiveSync, renames, concurrent edits, restore and offline fallback. If metadata cannot survive the bridge, gate ingestion/indexing and implement a durable data-owned catalog with reconciliation; never fall back to path identity or silent content matching. This is an explicit unresolved prototype gate.

## Pagination and snapshots

List limits are 1–50 (default 20); change pages are 1–100 (default 20); search/index query limits are 1–20. Opaque cursors bind subject/authorized vault, query/filter and a consistent snapshot. `next_cursor: null` ends a list. A change page supplies a next checkpoint even when empty; `has_more` indicates remaining records. The catalog's `snapshot_cursor` is the exact change position after its stable listing: enumerate that snapshot, then resume changes from that cursor without missing edits.

Cursors are not credentials. Invalid/mismatched cursor returns 400; expired retention returns 410 `cursor_expired`, requiring a fresh full listing and generation rebuild. Default intended retention is at least seven days; CAL-011 must prove crash-safe retention/checkpoint behavior or revise this explicitly before implementation consumers depend on it.

Snapshot creation returns 202 and a snapshot ID scoped to the authenticated subject and requested allowed vault set. Poll status; archive/manifest access requires that same authorization, not merely possession of an ID. Pending archive retrieval returns 409; expiration returns 410. The immutable ZIP and manifest agree on one `source_cursor`, include note/catalog/capture-dedup state, and exclude credentials. Relative archive paths must reject traversal, absolute names, drive prefixes and symlinks during restore. Validate manifest hashes and size limits before extraction. Exact third-party database export/recovery tooling remains CAL-012/CAL-018. Snapshot transport gets a separate long transfer profile in E02/E05, rather than the ordinary JSON request deadline.

## Capture and retries

The client creates a UUID `capture_id` once and supplies the same `Idempotency-Key`. Data deduplicates on authorized vault plus capture ID, including records restored from backup. Identical retries return the original note identity/result; changed text/source under that identity returns 409. Client-created time is advisory, never an ordering or authorization source. Only a durable data commit may produce `durable: true`; `sync_state: pending` says device replication is still outstanding. No overwrite endpoint is exposed.

Retry reads on transport failure with bounded backoff. Retry capture using the unchanged key/body after an ambiguous timeout; do not mint a new capture ID. Retry generation only through explicit user action with a new request ID: no implicit duplicate billing/work. For index writes, generation plus chunk ID/revision makes reapplication idempotent; reject revision regression and incompatible embedding dimensions/model. Generation activation is atomic only after a complete validated rebuild, preserving the previous active generation for rollback. Delete tombstones prevent late older writes from resurrecting content.

## Bounds, errors and tracing

Current API defaults are 1 MiB request body and 15 seconds; capture is 300,000 bytes, answer/inference generation 120 seconds, probes 3 seconds. Body and character/item bounds both apply. Implement body limits before full parsing and bound upstream work/concurrency. E02 records proxy limits consistent with adapters; E09 tunes inference deadlines against measurements. GET/DELETE do not accept request bodies. Returned `X-Request-ID`/error request IDs are UUID tracing values, never credentials. Reject malformed supplied IDs; mint one if absent. Log ID, service, duration/status and redacted failure code only, not bearer tokens, prompts, query text or notes.

| Status | Code / client behavior |
|---|---|
| 400 | `invalid_request`; fix input |
| 401 | `unauthenticated`; authenticate, no credential detail |
| 403 | `forbidden`; no retry with same authority |
| 404 | `not_found`; do not disclose existence across vaults |
| 409 | `conflict`; resolve changed idempotent body, version or pending state |
| 410 | `cursor_expired`; rebuild pagination/snapshot |
| 413 | `too_large`; reduce request |
| 429 | `busy`; bounded retry using Retry-After when available |
| 503 | `unavailable`; explicit degraded state, bounded retry |
| 504 | `deadline_exceeded`; stop downstream work; capture must reconcile unchanged ID |

Error bodies have `request_id`, bounded `message`, `code`, `retryable`; never echo content. Rejected identity requests must not reveal whether notes exist. JSON responses use the schema shown in each operation. ZIP is a binary protocol exception, not JSON.

## Search, inference and streams

Search revalidates each candidate against the authoritative data API: vault, current revision/hash and `indexable` must match before returning any snippet. During index lag, discard stale candidates. Data/identity unavailable means fail closed; do not serve cached private snippets without permission/currentness evidence. Lexical fallback is allowed only under the same checks. Sources link through the configured display domain and carry stable note IDs/revisions; no raw file paths. Note content is untrusted model input and cannot grant tools or system instructions.

Embedding output has exactly one finite vector per input, each of declared dimensions. Model version/dimensions identify an index generation. Inference sees only the bounded prompt provided by the authorized answer service; it has no data-store credentials. An answer with insufficient evidence returns explicit status and no fabricated citations. Inference outage is explicit; ordinary search remains independently usable.

JSON is the default. With `Accept: text/event-stream`, UTF-8 SSE records use `event: sources|delta|done|error` and one JSON `data:` object matching the named `Stream*` schema, followed by a blank line. Answers send at most one sources record before deltas; inference sends no sources record. Every record uses the request ID (error wraps the structured error). Exactly one terminal done/error; no events afterward. A stream error cannot change the already-sent HTTP status. Bound each delta to 8192 characters and generation to the declared deadline/output token limit. Heartbeat comments may keep proxies alive but do not extend the deadline. Disable proxy response buffering for streams in CAL-006.

Cancellation uses the same request UUID; only the original subject/caller can cancel it. Propagate cancellation on client disconnect, explicit DELETE or deadline. DELETE is idempotent for an owned recently completed/cancelled request; unknown/other-subject IDs return 404. Keep the request ownership record for at least the maximum request lifetime. Partial output is visibly incomplete and never committed as a durable note. Actual event transport, timeout enforcement and cancellation remain integration tests in E02/E09/E10.

## Compatibility and protocol exceptions

Paths use `/v1`. Required fields, identity policy, semantics and limits may not change incompatibly within v1. Strict request schemas reject unknown fields; therefore coordinate even additive request fields through a reviewed minor contract/consumer release. Response additions likewise require updating current strict fixture validators. Breaking changes use v2 with explicit coexistence/migration. Pin clients to reviewed contract versions; shared schema equality is checked automatically.

Sync uses pinned CouchDB/LiveSync protocol in CAL-009; backup storage uses the supported repository protocol chosen in CAL-018 (proposed restic REST over HTTPS). Do not reinvent those APIs here or impose unsupported `/health/ready` routes. UI/session, introspection and delegation adapter interfaces are completed in CAL-007 before real tokens exist. The opaque token boundary is chosen; compatibility with the existing IdP is unproven and must not be bypassed by trusting forwarded headers.

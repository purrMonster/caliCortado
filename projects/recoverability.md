# Calicortado recovery

Status: proposed; no backup or restoration verified. This plan covers Calicortado notes and the state needed to restore its service. CAL-E05 (CAL-018 through CAL-021) implements it; CAL-048 repeats recovery against the complete release.

## Recovery set

| Data | Proposed treatment | Verification needed |
|---|---|---|
| Plain Markdown vaults and retained attachments | Versioned independent backup of a consistent mirror snapshot | Completeness, freshness and byte-identical restore |
| Sync configuration, database users and permissions | Protected backup or documented reproducible reconstruction | Fresh service and fresh-client test |
| CouchDB sync data and history | Keep in recovery scope until rebuild and history requirements are settled | Supported consistent capture or explicit rebuild procedure |
| Encryption material and credentials | Password manager plus independently accessible recovery kit | Access without the failed host; never store values here |
| Data catalog, change cursors and capture idempotency records | Consistent capture with notes or a proven reconstruction process | Stable note identities and no duplicate capture after restart/restore |
| Capture workflows and search configuration | Versioned definitions; secrets recovered separately | Recreate without losing permissions or capture identities |
| Derived search index | Rebuild from restored notes | Exclusions and vault isolation still enforced |
| Optional chat state | Back up before upgrades if conversations/settings must be retained | Application-level restoration test |

The bridge's plaintext mirror can restore note contents, but its existence alone does not prove recovery of sync history or service access.

## Destination and transport

Proposed destination: an independent restic repository on backup-host, only after verification. CAL-018 selects a supported authenticated HTTPS repository protocol, proposed restic REST, exposed through Traefik at `backup.<domain>`. A data-local worker creates a consistent snapshot and sends encrypted repository traffic to that endpoint; a remote worker instead consumes the scoped export API at `data.<domain>`. No backup consumer mounts another layer's filesystem. Record retention, schedule, encryption and off-node copy arrangements.

Historical inspection found incomplete backup source configuration and unverified destination health. Exact infrastructure paths and revisions are omitted. Verify source coverage, disk health and restore behavior in the target environment; historical inspection is not a live backup result.

A proposed inference-host disk is not a dependency until its role and availability are confirmed. No disk setup is authorized by this document.

## Procedure to prove

1. Set acceptable data loss, restoration time and retention with the user.
2. Record each source's actual path, consistency method, transport and destination.
3. Back up the synthetic prototype and verify scheduled success and failure reporting.
4. Restore into an isolated location with outbound capture/review jobs disabled.
5. Compare representative notes and attachments, including Unicode filenames and archived notes.
6. Rebuild sync configuration and permissions; connect a fresh test client and verify restored notes.
7. Confirm secrets are recoverable without the failed host and unauthorized vault access is denied.
8. Record recovery time, recovered data point, versions and remaining gaps in the runbook.

Before real imports, retain an independent baseline of their source data. Periodic restore exercises and tests after significant upgrades should reuse this procedure.

## Evidence to record

Date, source paths, revision/image versions, backup identifiers, destination health assessment, restore target, comparison results and elapsed recovery time. Keep credentials and note contents out of the record.

Completion gates live in [plan.md](../plan.md). Next action within this component: CAL-018 defines the recovery inventory and targets after the export contract/prototype is available. Every decision and test result is linked to its story in the runbook.

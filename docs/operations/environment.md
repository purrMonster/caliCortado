# Environment requirements — CAL-002

The original E01 inspection established readiness gaps in one private deployment. Identifying inventory has been removed at the owner's request. This document is now a reusable deployment checklist, not evidence that any new environment has been inspected.

| Role | Required verification before deployment |
|---|---|
| Edge and identity | DNS control, compatible Traefik/identity versions, trusted certificates, authenticated routes and denied bypass |
| Data | CPU/RAM/storage budget, durable volumes, sync/bridge compatibility, recovery export and catalog consistency |
| Compute and retrieval | Measured embedding/index capacity, independent domain configuration and scoped credentials |
| Inference | Authorized access, actual accelerator/model capacity and accepted availability/latency |
| Display | Independently configurable domain, session integration and authorized hosting target |
| Backup | Healthy independent storage, verified mount/failure boundary, capacity, retention and restore evidence |

Keep hostnames, IP addresses, usernames, private repository revisions, hardware fingerprints and credential references in an operator-controlled inventory outside this repository. Never infer backup independence from a directory name or infer model capacity from an old hardware description. Reconcile deployed and source revisions before changes and preserve existing edits.

## Environment configuration

Set DOMAIN in the deployment environment; [.env.example](../../.env.example) contains the requested example value. [Endpoint templates](../../config/deployment.example.json) derive addresses from `${DOMAIN}` and allow individual service URL overrides. These examples neither create DNS records nor demonstrate control of a domain. CAL-005/CAL-006 verify naming, collisions, DNS, certificates and reachability.

## Development baseline

E01 checks passed on Python 3.12.14 with the pinned lockfile. PowerShell 7 supports the Vikunja exporter. The offline foundation does not need Docker, production accounts or a sibling checkout. Live container/TLS verification remains E02 work. See [development](../development.md).

Application code and product decisions belong here; deployment configuration belongs in a separate infrastructure repository. The owner-supplied remote received the initial sanitized application baseline on 2026-09-28. This is source publication, not service deployment. [Access boundaries](access.md) remain applicable; an earlier authorization for private targets does not authorize a new environment.

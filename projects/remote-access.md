# Calicortado remote access

Status: proposed; approach undecided. Remote sync and capture are user requirements. No remote setup is verified. CAL-E06 (CAL-022 through CAL-025) owns this work.

## Scope

The user's iPhone and Mac should reach `app.<domain>`, `sync.<domain>` and the required authenticated capture/search/answer routes away from home. Offline editing must continue if the remote path fails. All routes use Traefik; final names are chosen in CAL-005.

Only the project's required user endpoints, DNS and identity dependencies belong in this access policy. The data, index, embedding, inference and backup service domains are not ordinary device routes. Administration and unrelated services are outside this scope. Domain routing does not grant access: receiving services enforce caller and vault authorization.

## Choice to make

The existing proposal is Tailscale for private access. Cloudflare Tunnel remains the alternative the user is considering. Preserve that choice until agreed; verify current client support, plan limits and costs before setup.

Evaluate both against the same requirements:

- Sync-client authentication without an interactive browser challenge.
- Exposure and confidentiality of sync, capture and search traffic.
- iPhone connection behavior and manual pause.
- Device revocation, endpoint restrictions and outage recovery.
- Maintenance and dependencies under the documented CGNAT connection.

The working design keeps CouchDB off a public route. Any alternative that changes that boundary needs an explicit decision and tested authentication.

## Proposed private-network shape

- A candidate subnet router on edge-host, with only required routes.
- Access rules restricted to authorized devices and service destinations.
- Reachable split DNS for service names: include the resolver's route and required DNS ports, not just data-compute-host's HTTPS port.
- HTTPS ingress with verified source-address handling and application authentication.
- Explicit hostname/service restrictions: allowing a shared host's port 443 alone does not restrict access to one virtual host.
- Device revocation and a documented pause/resume behavior.

Verify actual firewall behavior and proxy handling before relying on an allowlist. Record current settings and tests in the infrastructure runbook when implemented.

## Acceptance

From mobile data, test name resolution, authenticated sync, forbidden endpoints, invalid credentials and removal of a device. Stop the remote path and confirm local editing still works; restore it and verify catch-up without data loss.

If on-demand connection is used, test its actual iPhone behavior. A manual pause must have a clear and documented resume condition.

The capture API must have its own authentication and idempotency; private-network membership does not replace those controls. Test service boundaries on shared port 443 and source identity after proxy/SNAT behavior is applied.

Completion gates live in [plan.md](../plan.md). Next action within this component: CAL-022 records the approach and allowed routes before remote rollout. Local capture and LAN prototyping can proceed first. Log each decision with its story ID in the runbook.

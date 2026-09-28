# Domain API ingress drafts

**Ownership update — 2026-09-29:** all preparation belongs to Calicortado until the product is ready for deployment. This document is a future promotion/rollout procedure, not an instruction to copy these drafts into infrastructure now. The previous standalone live-probe approval request is superseded.

Review-only Compose documents for independently addressed API components. These files live outside `stacks/`, have `.example` suffixes, are not listed in any node's `APPS`, and therefore do not create routes or generated DNS records. Nothing here starts a service or claims a usable backend exists.

## Placement and prerequisites

`application.compose.yml.example` holds display and an identity adapter; `compute.compose.yml.example` holds sync, data, capture, index, embeddings, search and answers; `workstation.compose.yml.example` holds inference and backup endpoint candidates. These are logical roles, not hardcoded hosts. The workstation examples assume a future supported container adapter; they do not replace native Windows ingress or a native model runtime. Do not deploy them there until runtime, storage and proxy integration are demonstrated.

Every backend requires its own explicitly pinned image, internal port and reviewed middleware policy. Each node supplies `DOMAIN`, its existing proxy network and certificate resolver. No backend host ports are published. Applications still need their own authentication, storage, environment, health, resource limits and recovery configuration; these are ingress skeletons, not complete application deployment packages.

The existing human-login endpoint need not be renamed. The identity draft represents a separate adapter only if one is required; otherwise omit it and configure callers for the existing reviewed identity address. Sync, inference and backup may require native-protocol adapters: do not put interactive browser login in front of machine/native clients without testing it. Middleware references must exist before enabling a route; services must independently validate their own authorization.

## Preparing a real change

1. Reconcile the current checkout with deployed revisions without discarding node edits. Choose the node and review its instructions, existing routes, network and certificate ownership.
2. Copy only the approved services into a new tracked `stacks/<node>/<app>/docker-compose.yml` as a Git change. Add actual runtime/storage/health configuration and pin images. Do not copy these files to nodes directly.
3. Retain the literal `Host` rules using `${DOMAIN}` so `_lib/dns-records.py` discovers each destination from its owning node. Changing a hostname requires a matching client endpoint override. Validate DOMAIN through the existing configuration workflow before rendering Compose.
4. Supply the required settings locally. Review existing certificate ownership instead of requesting identical wildcard certificates on each node. Establish the middleware and node firewall policy; no raw backend ports should be reachable from other layers.
5. Render/check the complete Compose config without starting it. The draft requires the explicit `domain-api-draft` profile; replace or deliberately retain that guard in the reviewed implementation. Add the app to `node.conf` only when intended for normal lifecycle management.
6. Run the DNS generator with synthetic inputs first, inspect the expected record diff, then follow commit/push/node-pull delivery. Regenerate records on both DNS nodes with their existing render/setup workflow; recreate/reload only the affected services under the approved rollout.
7. Verify actual DNS answers from a client and two isolated service networks, TLS, auth denial, and direct-port denial before onboarding data. Test relocation with a disposable hostname and synthetic backend, never by moving a production service just for a test.

## Rollback

Capture the prior committed configuration and actual DNS TTL first. Revert the enabling Git commit, pull that state on the affected nodes, regenerate DNS using the existing tooling, remove only the new app/routers, and verify old resolution and services after cache expiry. Do not remove persistent volumes or unrelated services. These review-only examples need no live rollback because they are not active.

## Verification

Run `python -m unittest discover -s tests -p test_domain_api_drafts.py -v` from the repository root. Tests prove all 11 distinct hostname templates, required image/network/port/middleware values, absence of published backend ports, no production DNS activation from the examples directory, and relocation through the existing DNS generator with synthetic inventory. They do not prove runtime readiness, TLS, permissions, firewall enforcement, Windows compatibility or live DNS propagation.

## Disposable local HTTPS rehearsal

Run `python examples/domain-api/ingress_probe.py --openssl <openssl-executable>` from this repository with Python 3.12+, Docker Compose v2+ and OpenSSL. On Windows Git's `usr/bin/openssl.exe` is supported. Run without Python `-O`. Docker Desktop must run Linux containers. The script pulls digest-pinned Traefik 3.7.13 and whoami 1.11.0 images; it creates a random Compose project, a loopback-only ephemeral HTTPS port, and an internal backend network. Only the proxy joins a second network for host port forwarding. No production DNS, hosts file, certificate store, Docker socket, persistent volume or existing container is changed.

The fixture owns only synthetic echo responses. A one-day self-signed certificate covers reserved test hostnames and is trusted only by the test client. Random BasicAuth credentials are stored temporarily outside the repository. BasicAuth here tests middleware wiring; it does not select production identity or service authorization. The client retains the same hostname and credentials when the target changes from backend A to B. An explicit restart of only the fixture proxy applies the change; live hot reload is not an acceptance assertion.

**Observed 2026-09-28:** Docker Engine 29.7.2 / Compose 5.5.1 / Python 3.12 on Windows with Linux containers: all seven checks passed. Anonymous and invalid authentication returned 401; valid authentication reached A over trusted TLS with its Authorization header removed; an unmatched hostname returned 404; default certificate trust rejected the fixture certificate; neither backend published host ports; unchanged client reached B after configuration update and proxy restart. Cleanup verified no project containers or networks remained and removed temporary key/auth/config files. Downloaded image cache is intentionally retained.

Earlier iterations exposed an internal-only proxy network port-forwarding limitation, Windows newline handling in password hashing, and a file-change notification that did not reload the provider. The final fixture separates proxy ingress from its internal backend network, hashes the password without a newline, and explicitly restarts its proxy. Every attempted run cleaned up successfully. These observations are fixture/runtime behavior, not production faults.

**Failure/recovery:** the command exits nonzero for any failed check. Its finally block removes only its random Compose project and temporary directory. If Docker becomes unavailable during cleanup, restore Docker and use the project/directory reported by the traceback to run `docker compose -p <project> -f <temp-directory>/compose.json down --remove-orphans`, then verify the project's containers/networks are absent before deleting its temporary directory. Do not use global prune. An interrupted process can require the same cleanup. Upgrade by changing both image tag and digest deliberately and rerunning; rollback is reverting this source change and rerunning. This fixture has no durable application state to recover.

**Limits:** no live DNS mutation, remote ingress, public certificate issuance, real identity/session policy, service-network DNS or host firewall denial was tested. Absence of published ports does not prove production firewall enforcement. This is preparation for a separately reviewed Git-delivered live probe, not production acceptance.

## Prepared live relocation phases

[LIVE-RELOCATION.md](LIVE-RELOCATION.md) specifies the separate Git changes, temporary authentication, targeted DNS refresh, convergence checks and rollback. `prepare_relocation.py` generates inactive phase candidates outside active stacks; it does not deploy or alter DNS. Keep the previous local rehearsal evidence separate from this still-unexecuted live procedure.

See [DNS compatibility provenance](../../tests/fixtures/DNS-COMPATIBILITY.md). Recheck against the then-current infrastructure implementation before promotion.

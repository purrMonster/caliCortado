# Sync compatibility investigation — CAL-009

Status, 2026-10-01: **local headless compatibility passed; story acceptance incomplete**. CAL-007 production identity remains a dependency. No iPhone/Mac session or personal vault has been configured. All preparation stays in Calicortado until deployment readiness.

## What this step proves

The [disposable runner](../../examples/sync-compat/run.py) builds the reviewed upstream bridge source and tests its CouchDB peer class. It does not run the full Hub/storage mirror or the Obsidian plugin. Six integration checks passed:

1. CouchDB became reachable over trusted HTTPS; invalid credentials returned 401.
2. Peer A wrote a synthetic Unicode path and text which peer B read unchanged.
3. Raw CouchDB documents did not contain the original path or synthetic plaintext marker.
4. An update from B was read unchanged by A.
5. A fresh peer decrypted the existing updated note.
6. A deletion became visible to another peer.

This is positive evidence for the proposed encrypted headless path, not a cryptographic audit or universal confidentiality guarantee. Nine upstream runtime unit tests also passed with networking disabled. The project's 28 offline tests are separate from these runtime checks. No filesystem mirror, process restart persistence, rename, concurrent conflict, missing/wrong encryption metadata, large attachments, Obsidian compatibility or device timing is claimed.

## Reviewed version matrix

| Component | Investigated version | Evidence / limitation |
|---|---|---|
| LiveSync bridge | `c3760beaa0851214da4860903445d7f6420ca025` | Clean official source, checked by the runner before building |
| Common library | `@vrtmrz/livesync-commonlib@0.1.19` | Upstream import configuration and frozen dependency lock |
| Deno | `2.6.9` | Digest pinned in the fixture Dockerfile |
| CouchDB | `3.5.0` | Digest pinned in the runner; disposable single-node database |
| Traefik | `3.7.13` | Digest pinned in the runner; file provider and verified TLS |
| Obsidian iPhone/Mac | Not selected or tested | User device test still required |
| Obsidian LiveSync plugin | Not selected or tested | Must select a pinned version and verify against the bridge; do not assume compatibility from shared naming |

Sources: the [official bridge source at the reviewed revision](https://github.com/vrtmrz/livesync-bridge/tree/c3760beaa0851214da4860903445d7f6420ca025), its [configuration instructions](https://github.com/vrtmrz/livesync-bridge/blob/c3760beaa0851214da4860903445d7f6420ca025/readme.md), and [upstream peer integration test](https://github.com/vrtmrz/livesync-bridge/blob/c3760beaa0851214da4860903445d7f6420ca025/test/integration/PeerCouchDB.integration.ts). Upstream supports separate content and path passphrases; this experiment supplies distinct random values. Dependency/runtime pins are for investigation, not a production compatibility recommendation.

## Boundary, endpoint and state ownership

The test client uses `https://sync.calicortado.test`, resolved by a private Docker network alias to Traefik. The client network cannot directly reach CouchDB's separate backend network. Only the proxy joins both networks. No service publishes host ports; no hosts file, live DNS, public certificate account or machine trust store is changed. Proxy-to-CouchDB HTTP is confined to this local data-component fixture; cross-layer traffic uses the HTTPS domain.

The test supplies an explicit temporary CA to Deno and uses a separately signed server certificate with the correct DNS SAN and `CA:FALSE`. Certificate verification is never disabled. A throwaway CouchDB administrator is used solely to create/remove the isolated test database; it is not the proposed production device/service identity. Fixture JSON, passwords, content/path keys, certificate keys and database state are temporary. Only synthetic content is used.

This is a read/write peer protocol test, not data API implementation. The future bridge owns plaintext only inside the data component; other layers still use the data domain. No consumer receives a vault mount.

## Reproduce locally

Prerequisites: Python 3.12, Git, OpenSSL and a working Linux-container Docker engine with Compose. Downloads occur during source/image preparation; test containers then use isolated networks. No Python dependency change is needed.

From the Calicortado root:

```powershell
git clone https://github.com/vrtmrz/livesync-bridge.git .local/livesync-bridge-upstream
git -C .local/livesync-bridge-upstream checkout --detach c3760beaa0851214da4860903445d7f6420ca025
.venv\Scripts\python.exe examples/sync-compat/run.py --source .local/livesync-bridge-upstream --openssl "C:\Program Files\Git\usr\bin\openssl.exe"
```

Skip clone if that disposable checkout already exists; inspect its status before changing its revision. Never reset a dirty checkout. On other systems pass the equivalent Python/source paths and the installed `openssl` executable. The runner verifies the exact upstream revision and rejects tracked or untracked modifications. Its Dockerfile uses frozen dependency installation and explicitly caches runtime/test imports before starting network-isolated tests. Runtime tests use `--no-check`; this result is not a TypeScript type-check claim.

Success prints the upstream nine-test result, six integration results and verified cleanup. Source and downloaded image/build cache remain available; runtime secrets and data do not. No ongoing service is left running for devices to connect to.

## Failures, cleanup and rollback

Early trials found two fixture issues: CouchDB's root entrypoint attempted ownership changes on a read-only config mount, and Deno rejected a CA certificate used as the server leaf (`CaUsedAsEndEntity`). Running CouchDB as its existing `couchdb` user and issuing a proper separate server certificate resolved these without weakening TLS. Explicit single-node shard settings avoid assuming a cluster.

The original upstream image installation did not cache all runtime imports. The fixture adds a frozen cache step. A separate upstream Compose test could not run inside the isolated image because it invokes the Docker CLI; the nine-test runtime selection excludes that packaging test. It was not passed off as a successful full upstream suite.

On test failure the runner prints bounded synthetic service diagnostics and tears down only its random `cali-sync-*` Compose project with its volumes. It checks for remaining project containers, networks and volumes before deleting the temporary directory. If Docker is unavailable or the process is forcibly terminated, preserve the temporary directory, restore Docker, and use its recorded Compose file/project name to run `docker compose -p <project> -f <temporary-directory>/compose.json down --volumes --remove-orphans`. Verify that project's resources are gone before removing only that temporary directory. Never run global prune. No real notes exist in this fixture and no service data needs restoration.

Upgrade by reviewing a new upstream revision and dependency lock, changing explicit source/image pins, then rerunning these checks and the later filesystem/device matrix. Rollback means restoring the prior source pins and rerunning the disposable fixture. This is not yet the durable service upgrade/backup procedure.

## Next bounded step and remaining acceptance

Proceed with a **filesystem bridge experiment** against the same domain fixture: a synthetic local mirror in the data boundary, bidirectional edits, rename/delete, process recreation with preserved scan state, and wrong/missing decryption metadata. Add visible failure detection and compare bytes/hashes before selecting the bridge for real data.

After that, choose the pinned Obsidian/plugin versions and prepare disposable iPhone/Mac instructions for the user. Foreground/background behaviour, the proposed 60-second target and conflicts require actual device evidence. CAL-007 identity integration and all CAL-009 acceptance boxes remain open; CAL-005 is not closed by a local network alias. No real-note migration or infrastructure promotion is warranted by this result alone.

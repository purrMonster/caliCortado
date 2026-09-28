# Live disposable ingress relocation

**Ownership update — 2026-09-29:** all preparation belongs to Calicortado until the product is ready for deployment. This document is a future promotion/rollout procedure, not an instruction to copy these drafts into infrastructure now. The previous standalone live-probe approval request is superseded.

Status: prepared procedure, not a deployed service. Use only after the operator approves the exact enabling commits, target nodes and DNS recreation window. Node sudo is operator-owned. This fixture serves synthetic echo responses only; never send real notes, cookies or production credentials.

## Contract, ownership and prerequisites

- Endpoint: `https://relocation-check.${DOMAIN}/`; successful BasicAuth returns HTTP 200 containing `relocation-a` or `relocation-b`. Anonymous and invalid credentials must return 401. Traefik strips Authorization before forwarding. There is no persistent state, recovery data or host backend port.
- Use the existing node-specific ingress network and certificate resolver. Each ingress owns its certificate; do not copy keys or ACME files. The application ingress may use its existing wildcard; the destination may issue a hostname certificate through its current resolver. Do not change account credentials, certificate storage, public tunnel routes or firewall rules for this probe.
- Temporary `PROBE_AUTH_USERS` is an htpasswd entry, supplied through the ignored app `secrets.env.local`. Keep the same temporary username/password on both nodes; each hash may differ. `PROBE_NETWORK` and `PROBE_CERT_RESOLVER` name existing resources, not new ones. DOMAIN comes from the established node environment.
- Check the exact test hostname against both DNS configurations, manual Pi-hole records and all relevant routers. Check negative A/AAAA/CNAME responses from both resolvers, and record negative cache TTL before creation. Do not infer absence solely from an NXDOMAIN query.
- Record current Git revisions, untracked filenames, current resolver records, certificate status and actual DNS TTL. Preserve node-local files. Compare each node's revision to the enabling revision; a pull can bring unrelated changes. Do not run setup, init, global render, firewall, tunnel or `compose.sh --all` commands merely because source advanced.
- Choose one user-client vantage point and two isolated service-network vantage points that can query both private resolvers and reach both ingresses. Document their actual names privately; local host requests with forced addresses do not substitute for these checks.

## Prepare the reviewed Git phases

From a development checkout, generate into a NEW directory outside active `stacks`:

```sh
python examples/domain-api/prepare_relocation.py --node-a "$NODE_A" --node-b "$NODE_B" --output "$PREPARED"
```

The output contains `phase-a/stacks/<node-a>/ingress-relocation/docker-compose.yml`, the corresponding phase-B file, and an explicit change manifest. Node names identify existing stack directories. The generator refuses traversal, identical nodes, existing output and an output under `stacks`. This command never changes the active source tree or live DNS.

Review these three source changes separately:

| Phase | Exact tracked route change | Expected generated DNS delta |
|---|---|---|
| A | Add only node A's probe Compose file | Add one address record to ingress A and its scoped local rule |
| B | Remove A's tracked Compose file; add B's | Change only the probe address from A to B; preserve local rule |
| Remove | Remove B's tracked Compose file | Remove only the probe address and local rule |

The DNS generator scans source even when a Compose profile is inactive. Never add both active paths in one revision: duplicate ownership is rejected. Preserve all unrelated generated records. Each phase requires its own reviewed commit, push to `main`, and node pull; do not copy configuration to servers. The fixture stays out of `node.conf` APPS, and requires the explicit `relocation-probe` profile. The profile prevents accidental service starts, not DNS discovery after a source file enters `stacks`.

## Temporary credentials on each probe node

After phase A has reached node A (and later phase B reaches node B), the operator creates the ignored app file. Use the same temporary password from a password manager on both nodes. In Bash, from that node's stack directory:

```sh
umask 077
read -r -s -p 'Temporary probe password: ' probe_password
printf '\n'
probe_hash="$(printf '%s' "$probe_password" | openssl passwd -apr1 -stdin)" || exit 1
(set -o noclobber; printf "PROBE_AUTH_USERS='probe:%s'\n" "$probe_hash" > ingress-relocation/secrets.env.local) || exit 1
unset probe_password probe_hash
```

First confirm OpenSSL exists and the destination secret file does not already exist; preserve an existing file instead of overwriting it. Add `PROBE_NETWORK` and `PROBE_CERT_RESOLVER` using the verified existing values. Single quotes around the hash prevent Compose interpolation of its dollar signs. The APR1 hash is for a random, short-lived fixture credential only, not a production password policy. No plaintext password is placed in process arguments, shell history or tracked files. Do not print resolved Compose configuration; it contains the hash. Remove this temporary credential after the exercise.

## Phase A: start backend before DNS

1. Commit/push the reviewed phase-A diff. On node A, inspect `git status --short`, then `git pull --ff-only`; confirm the expected commit and preserve unrelated files. Create its private configuration as above.
2. From node A's stack directory, run `./compose.sh ingress-relocation --profile relocation-probe config --quiet`, then `./compose.sh ingress-relocation --profile relocation-probe up -d`. Inspect only this probe's state and the ingress route. Existing Traefik uses its Docker provider; no proxy restart is planned. Do not run a broad stack update.
3. Verify trusted TLS and backend A before DNS activation using the configured hostname and explicit destination: `curl --noproxy '*' --resolve "$PROBE_HOST:443:$INGRESS_A" -u probe "https://$PROBE_HOST/"`. curl prompts for the password. Never use `-k`. Check anonymous 401 and confirm Authorization is absent from the synthetic response. Check certificate SAN/expiry and absence of backend published ports. Stop if certificate issuance or middleware fails.
4. On EACH resolver, pull the exact phase-A source. From its stack directory, run `bash ../_lib/refresh-dns.sh "$PWD"` as the operator (it requests sudo for installed inventory), review the one-record delta privately, then `./compose.sh pihole up -d`. Refresh the secondary first, verify it answers existing and new names, then refresh the primary. The primary also supplies DHCP, so recreation needs the operator's window. Stop after any mismatch; do not continue automatically.
5. From all three vantage points, query both resolvers for A, AAAA and CNAME and record TTL; use the unchanged URL without `--resolve` to verify backend A and auth denial. Wait any recorded negative cache lifetime first. Do not flush arbitrary user caches or change global TTL merely to make a test pass.

## Phase B: move DNS only after destination is ready

1. Commit/push the reviewed phase-B source diff. Pull it on node B, create its private configuration, and start only its probe using the phase-A commands. Verify trusted TLS, denial and backend B with `--resolve` first. The unchanged hostname may require a certificate on B; wait for successful issuance rather than moving DNS early.
2. Keep node A's running probe and phase-A checkout intact during convergence. Do not run down or pull its removed Compose source yet. Inspect any automatic Git update timer before the exercise: it must not remove the needed source before cleanup; if it can, retain the phase-A Git revision and restore its source through a reviewed Git change for cleanup. Do not disable scheduled operations without authorization.
3. Pull phase B on both resolvers, review that only the probe's address changed, and use the same targeted refresh/recreation sequence. Record the mixed-resolver interval. Preserve the previous TTL and wait its full positive cache lifetime (and any measured client minimum).
4. From all three vantage points, verify both resolvers now point to B, normal HTTPS reaches `relocation-b` using the SAME hostname, credentials and caller binary, and unrelated names still work. Record route revision, timing, TLS and denial results privately. A forced-IP request alone does not prove relocation.
5. Stop A's probe with `./compose.sh ingress-relocation --profile relocation-probe down` while its source is still present. If its checkout advanced, recover the phase-A Compose through Git before using that command; never use a global prune. Then pull the intended current revision. Leave the shared ingress network and all existing services intact.

## Rollback, removal and acceptance

If B fails BEFORE DNS moves, stop B and keep A serving; do not advance the resolvers. Revert the phase-B source commit through Git before further normal DNS generation. If B fails AFTER DNS moves, first verify/start A from the phase-A source, then revert the phase-B commit, push and pull that rollback on both resolvers, refresh DNS and verify convergence to A after cache expiry. Keep B available until old answers expire where possible. Stop on an unrelated-record delta or resolver failure and restore the prior reviewed source/settings with the operator. Do not overwrite other operators' commits.

After successful B verification, stop both probes with their known source definitions. Commit/push removal of the final tracked route, pull on the resolvers and repeat targeted DNS refresh. Verify the hostname is absent after cache expiry, existing names resolve, no probe containers remain, and ignored temporary secret files are removed from the exact app directories. Do not delete shared networks, certificates, ACME accounts or unrelated files. There is no application data to restore. Upgrades change the image tag AND digest in the generator and rerun the offline/local checks before preparing a new live exercise.

Acceptance requires private evidence for A and B from three network contexts, both resolvers, trusted TLS, denied auth, unchanged caller and cleanup/rollback. This proves only the disposable route; it does not allocate all product layer names, select production identity or prove whole-host firewall enforcement.

## Prepared evidence

Run `python -m unittest discover -s tests -p test_relocation_plan.py -v`. These tests use the offline DNS-discovery compatibility snapshot: A adds one route, duplicate ownership fails, B changes only its destination, and removal restores the exact baseline. Invalid node/output paths fail before generation. Run both generated Compose files through `docker compose config --quiet` with synthetic values; missing authentication must fail closed. These are preparation checks; record live outcomes only after executing the operator-approved procedure.


Prepared verification on 2026-09-29: both relocation tests and all three prior domain-draft tests pass. Both generated phases render with Docker Compose 5.5.1 using synthetic DOMAIN/network/resolver/auth inputs. Missing DOMAIN or authentication is rejected. Rendered services have no host ports or mounts and retain the non-root/read-only restrictions. Compose serializes dollar signs escaped in its rendered output; the hash was checked after that serialization normalization. No live service or DNS change is represented by these checks.

See [DNS compatibility provenance](../../tests/fixtures/DNS-COMPATIBILITY.md). Recheck against the then-current infrastructure implementation before promotion.

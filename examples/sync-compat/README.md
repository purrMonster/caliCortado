# Local encrypted-sync compatibility fixture

CAL-009 investigation only. See the [sync operation and evidence guide](../../docs/operations/sync.md) for pinned versions, commands, boundaries, failures, cleanup and next acceptance checks.

`run.py` builds the verified upstream checkout using this `Dockerfile`, runs nine offline upstream runtime tests, then starts isolated CouchDB/Traefik containers and runs `peer_probe.ts`. The probe uses synthetic Unicode notes through a verified HTTPS domain; it tests encrypted headless peer exchange rather than a full filesystem bridge or Obsidian clients. All temporary project state is removed on completion.

All infrastructure preparation remains in Calicortado until the product is ready for deployment. This fixture is not an infrastructure rollout package.

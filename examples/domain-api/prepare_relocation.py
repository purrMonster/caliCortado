"""Generate inactive Git change candidates for a two-ingress relocation rehearsal."""
import argparse
from pathlib import Path
import re

IMAGE = 'traefik/whoami:v1.11.0@sha256:200689790a0a0ea48ca45992e0450bc26ccab5307375b41c84dfc4f2475937ab'


def compose(identity):
    return '''# Prepared candidate only: enable through a reviewed Git change.
services:
  probe:
    image: IMAGE
    hostname: relocation-IDENTITY
    command: ["--port=8080", "--name=relocation-IDENTITY"]
    user: "65532:65532"
    read_only: true
    cap_drop: [ALL]
    security_opt: ["no-new-privileges:true"]
    pids_limit: 32
    mem_limit: 64m
    restart: "no"
    profiles: [relocation-probe]
    networks: [ingress]
    labels:
      - "probe.domain=${DOMAIN:?set existing deployment domain}"
      - "traefik.enable=true"
      - "traefik.docker.network=${PROBE_NETWORK:?set existing ingress network}"
      - "traefik.http.routers.relocation-probe.rule=Host(`relocation-check.${DOMAIN}`)"
      - "traefik.http.routers.relocation-probe.entrypoints=websecure"
      - "traefik.http.routers.relocation-probe.tls=true"
      - "traefik.http.routers.relocation-probe.tls.certresolver=${PROBE_CERT_RESOLVER:?set existing resolver}"
      - "traefik.http.routers.relocation-probe.middlewares=relocation-probe-auth"
      - "traefik.http.routers.relocation-probe.service=relocation-probe"
      - "traefik.http.middlewares.relocation-probe-auth.basicauth.users=${PROBE_AUTH_USERS:?set temporary htpasswd entry}"
      - "traefik.http.middlewares.relocation-probe-auth.basicauth.removeheader=true"
      - "traefik.http.services.relocation-probe.loadbalancer.server.port=8080"
networks:
  ingress:
    external: true
    name: "${PROBE_NETWORK:?set existing ingress network}"
'''.replace('IMAGE', IMAGE).replace('IDENTITY', identity)


def prepare(output, node_a, node_b):
    for node in (node_a, node_b):
        if not re.fullmatch(r'[a-zA-Z][a-zA-Z0-9_-]{0,62}', node):
            raise ValueError('Node must be a single safe existing stack directory name')
    if node_a == node_b:
        raise ValueError('Relocation requires different nodes')
    output = Path(output)
    # Never overwrite an earlier rehearsal or generate directly into active stacks.
    if output.exists() or 'stacks' in output.resolve().parts:
        raise ValueError('Use a new output directory outside stacks')
    for phase, node, identity in [('phase-a', node_a, 'a'), ('phase-b', node_b, 'b')]:
        path = output / phase / 'stacks' / node / 'ingress-relocation' / 'docker-compose.yml'
        path.parent.mkdir(parents=True)
        path.write_text(compose(identity), encoding='utf-8')
    (output / 'CHANGES.txt').write_text(
        f'Phase A: add stacks/{node_a}/ingress-relocation/docker-compose.yml from phase-a.\n'
        f'Phase B: remove that tracked file and add stacks/{node_b}/ingress-relocation/docker-compose.yml from phase-b.\n'
        'Never overlay both phase directories. Keep A running until both resolvers and clients converge on B.\n'
        'Removal: stop both probe projects while their Compose sources are available; remove the final tracked route and regenerate DNS.\n'
        'No APPS, proxy, firewall, public tunnel or secret changes are included. Read LIVE-RELOCATION.md before use.\n',
        encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--node-a', required=True)
    parser.add_argument('--node-b', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    prepare(args.output, args.node_a, args.node_b)
    print('Prepared inactive phase A/B candidates. No active stack or DNS was changed.')

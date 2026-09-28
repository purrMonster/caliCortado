"""Offline compatibility snapshot; not a deployment DNS generator. See DNS-COMPATIBILITY.md."""
import csv
import ipaddress
import re

RULE = re.compile('^\\s*(?:rule:|-?\\s*["\']?\\s*traefik\\.http\\.routers\\.[\\w-]+\\.rule\\s*[=:])')

HOST = re.compile('Host\\(`([a-z0-9.-]+)\\.(?:\\$\\{DOMAIN\\}|\\{\\{\\s*env "DOMAIN"\\s*\\}\\})`\\)')

def records(root, domain, fleet, extra_hosts='', existing_hosts=''):
    if not re.fullmatch('[a-z0-9]+(?:[.-][a-z0-9]+)*', domain) or 'REPLACE_ME' in domain:
        raise ValueError('DOMAIN must be a real lowercase DNS domain')
    addresses = {}
    for row in csv.DictReader(fleet):
        addresses[row['name']] = str(ipaddress.IPv4Address(row['ip']))
    for entry in extra_hosts.split(';'):
        if not entry.strip():
            continue
        address, *names = entry.split()
        address = str(ipaddress.IPv4Address(address))
        if not names:
            raise ValueError('PIHOLE_DNS_EXTRA_HOSTS entries need an IP and host name')
        for name in names:
            if name in addresses and addresses[name] != address:
                raise ValueError(f'Conflicting address for {name}')
            addresses[name] = address
    existing = {}
    for entry in existing_hosts.split(';'):
        fields = entry.split()
        if len(fields) < 2:
            continue
        for name in fields[1:]:
            existing[name] = fields[0]
    routes = {}
    paths = set(root.glob('stacks/*/traefik/dynamic/*.yml'))
    paths.update(root.glob('stacks/*/traefik/config/**/*.template'))
    paths.update(root.glob('stacks/*/*/docker-compose.yml'))
    for path in sorted(paths):
        node = path.relative_to(root).parts[1]
        for line in path.read_text().splitlines():
            if not RULE.match(line):
                continue
            matches = HOST.findall(line)
            if 'Host(' in line and (not matches):
                raise ValueError(f'Unsupported Host rule in {path.relative_to(root)}')
            for label in matches:
                if node not in addresses and node in existing:
                    addresses[node] = str(ipaddress.IPv4Address(existing[node]))
                if node not in addresses:
                    raise ValueError(f'Router node {node} is missing from NODE_IPS, PIHOLE_DNS_EXTRA_HOSTS and PIHOLE_DNS_HOSTS')
                name = f'{label}.{domain}'
                if name in routes and routes[name] != addresses[node]:
                    raise ValueError(f'Conflicting route for {name}')
                routes[name] = addresses[node]
    if not routes:
        raise ValueError('No app routes found; refusing to replace DNS records')
    lines = ['filter-AAAA']
    for name, address in sorted(routes.items()):
        lines.extend((f'address=/{name}/{address}', f'local=/{name}/'))
    hosts = [f'{ip} {name}' for name, ip in sorted(addresses.items())]
    return (lines, hosts)

def routes_in(lines):
    return [line for line in lines if line.startswith('address=/')]

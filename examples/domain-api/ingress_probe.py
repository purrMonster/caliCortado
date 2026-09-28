"""Disposable local HTTPS routing rehearsal. Requires Docker Compose and OpenSSL.

Run with Python 3.12+: python ingress_probe.py --openssl <openssl executable>
No production DNS, certificates, Docker socket mounts or persistent volumes.
"""
import argparse
import base64
import http.client
import json
import os
from pathlib import Path
import secrets
import shutil
import socket
import ssl
import subprocess
import tempfile
import time


def run_probe(openssl):
    project = 'ingress-probe-' + secrets.token_hex(5)
    root = Path(tempfile.mkdtemp(prefix=project + '-'))
    compose = ['docker', 'compose', '-p', project, '-f', str(root / 'compose.json')]
    checks = []
    started = False

    def command(args, **kwargs):
        return subprocess.run(args, check=True, capture_output=True, text=True,
                              timeout=240, **kwargs).stdout.strip()

    def write(name, obj):
        path = root / name
        tmp = path.with_suffix('.tmp')
        tmp.write_text(json.dumps(obj), encoding='utf-8')
        os.replace(tmp, path)

    try:
        password = secrets.token_urlsafe(24)
        hashed = command([openssl, 'passwd', '-apr1', '-stdin'], input=password)
        (root / 'users').write_text('fixture:' + hashed + '\n', encoding='ascii')
        command([openssl, 'req', '-x509', '-newkey', 'rsa:2048', '-nodes',
                 '-keyout', str(root / 'key.pem'), '-out', str(root / 'cert.pem'),
                 '-days', '1', '-subj', '/CN=probe.example.test', '-addext',
                 'subjectAltName=DNS:probe.example.test,DNS:other.example.test'])
        with socket.socket() as reservation:
            reservation.bind(('127.0.0.1', 0))
            port = reservation.getsockname()[1]
        dynamic = {
            'tls': {'certificates': [{'certFile': '/fixture/cert.pem', 'keyFile': '/fixture/key.pem'}]},
            'http': {
                'routers': {'probe': {'rule': 'Host(`probe.example.test`)',
                                     'entryPoints': ['secure'], 'tls': {},
                                     'middlewares': ['fixture-auth'], 'service': 'target'}},
                'middlewares': {'fixture-auth': {'basicAuth': {'usersFile': '/fixture/users',
                                                              'removeHeader': True}}},
                'services': {'target': {'loadBalancer': {'servers': [{'url': 'http://backend-a:80'}]}}}
            }}
        write('dynamic.yml', dynamic)
        write('compose.json', {
            'services': {
                'proxy': {'image': 'traefik:v3.7.13@sha256:24841fe2de7304c149343d877d2923b4c8800a38ba015dea9174c23b20e344a0',
                          'command': ['--entrypoints.secure.address=:8443',
                                      '--providers.file.filename=/fixture/dynamic.yml',
                                      '--providers.file.watch=true'],
                          'ports': [f'127.0.0.1:{port}:8443'],
                          'volumes': [{'type': 'bind', 'source': str(root), 'target': '/fixture',
                                       'read_only': True}], 'networks': ['ingress', 'fixture'],
                          'security_opt': ['no-new-privileges:true']},
                **{name: {'image': 'traefik/whoami:v1.11.0@sha256:200689790a0a0ea48ca45992e0450bc26ccab5307375b41c84dfc4f2475937ab', 'hostname': name,
                          'networks': ['fixture'], 'security_opt': ['no-new-privileges:true']}
                   for name in ['backend-a', 'backend-b']}},
            'networks': {'fixture': {'internal': True}, 'ingress': {}}})
        command(compose + ['config', '--quiet'])
        started = True
        command(compose + ['up', '-d', '--wait', '--wait-timeout', '90'])
        trusted = ssl.create_default_context(cafile=str(root / 'cert.pem'))
        auth = 'Basic ' + base64.b64encode(('fixture:' + password).encode()).decode()

        def request(header=None, host='probe.example.test', context=trusted):
            raw = socket.create_connection(('127.0.0.1', port), timeout=5)
            try:
                tls = context.wrap_socket(raw, server_hostname=host)
            except BaseException:
                raw.close()
                raise
            conn = http.client.HTTPConnection(host, timeout=5)
            conn.sock = tls
            try:
                conn.request('GET', '/', headers={'Host': host, **({'Authorization': header} if header else {})})
                response = conn.getresponse()
                return response.status, response.read().decode()
            finally:
                conn.close()

        def eventually(predicate):
            deadline = time.monotonic() + 35
            last_error = 'unexpected HTTP response'
            while time.monotonic() < deadline:
                try:
                    if predicate():
                        return
                except (OSError, http.client.HTTPException) as exc:
                    last_error = type(exc).__name__ + ': ' + str(exc)
                time.sleep(0.5)
            raise AssertionError('route did not reach expected state within 35 seconds: ' + last_error)

        eventually(lambda: request()[0] == 401)
        checks.append('anonymous request denied with 401')
        assert request('Basic Zml4dHVyZTp3cm9uZw==')[0] == 401
        checks.append('invalid credentials denied with 401')
        status, body = request(auth)
        assert status == 200 and 'Hostname: backend-a' in body, f'Authenticated response {status}: {body[:500].replace(auth, "[redacted]").replace(password, "[redacted]")}'
        assert 'authorization:' not in body.lower() and password not in body
        checks.append('trusted TLS and valid auth reach backend A; authorization header stripped')
        assert request(auth, host='other.example.test')[0] == 404
        checks.append('unregistered hostname rejected with 404')
        try:
            request(auth, context=ssl.create_default_context())
        except ssl.SSLCertVerificationError:
            checks.append('untrusted certificate rejected')
        else:
            raise AssertionError('untrusted certificate was accepted')
        for backend in ['backend-a', 'backend-b']:
            cid = command(compose + ['ps', '-q', backend])
            details = json.loads(command(['docker', 'inspect', cid]))[0]
            assert not details['HostConfig']['PortBindings']
        checks.append('neither backend has published host ports')
        dynamic['http']['services']['target']['loadBalancer']['servers'][0]['url'] = 'http://backend-b:80'
        write('dynamic.yml', dynamic)
        # Explicit restart is portable across Docker Desktop bind-mount watchers.
        command(compose + ['restart', 'proxy'])
        eventually(lambda: 'Hostname: backend-b' in request(auth)[1])
        checks.append('unchanged HTTPS client reaches backend B after configuration update and proxy restart')
        print(json.dumps({'checks': checks, 'result': 'PASS',
                          'limits': 'local fixture only; no production DNS, identity, cross-host relocation or firewall proof'}, indent=2))
    except Exception:
        if started:
            print(command(compose + ['logs', '--no-color', '--tail', '25', 'proxy']))
        raise
    finally:
        if started:
            command(compose + ['down', '--remove-orphans', '--timeout', '10'])
            remaining = command(['docker', 'ps', '-aq', '--filter', f'label=com.docker.compose.project={project}'])
            networks = command(['docker', 'network', 'ls', '-q', '--filter', f'label=com.docker.compose.project={project}'])
            if remaining or networks:
                raise RuntimeError(f'Cleanup incomplete for {project}; inspect before removing {root}')
        if not root.resolve().is_relative_to(Path(tempfile.gettempdir()).resolve()):
            raise RuntimeError('Refusing cleanup outside the temporary directory')
        shutil.rmtree(root)
        print('Cleanup verified: fixture containers, network and temporary credentials removed.')


if __name__ == '__main__':
    if __debug__ is False:
        raise RuntimeError('Run without -O: assertions are acceptance checks')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--openssl', default='openssl')
    run_probe(parser.parse_args().openssl)

"""Offline compatibility checks; never starts containers or touches live DNS."""
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('dns_records', ROOT / 'tests/fixtures/dns_route_discovery.py')
dns = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dns)
FILES = ROOT / 'examples/domain-api'
FLEET = 'name,ip,mac\nnode-a,192.0.2.10,02:00:00:00:00:10\nnode-b,192.0.2.11,02:00:00:00:00:11\n'


class Drafts(unittest.TestCase):
    def documents(self):
        return [p.read_text(encoding='utf-8') for p in sorted(FILES.glob('*.compose.yml.example'))]

    def test_boundary_and_required_configuration(self):
        names = set()
        for document in self.documents():
            self.assertIn('external: true', document)
            self.assertNotIn('ports:', document)
            self.assertNotIn('volumes:', document)
            import re
            for name, body in re.findall(r'^  ([a-z]+):\n(.*?)(?=^  [a-z]+:|^networks:|\Z)', document, re.M | re.S):
                if name == 'ingress':
                    continue
                self.assertNotIn(name, names)
                names.add(name)
                self.assertIn('profiles: [domain-api-draft]', body)
                self.assertIn(name.upper()+'_IMAGE:?', body)
                self.assertIn(name.upper()+'_INTERNAL_PORT:?', body)
                self.assertIn(name.upper()+'_MIDDLEWARES:?', body)
                self.assertIn('DOMAIN_API_PROXY_NETWORK:?', body)
                self.assertIn('.entrypoints=websecure', body)
                self.assertIn('.tls=true', body)
        self.assertEqual(names, {'display','identity','sync','data','capture','index','embeddings','search','answers','inference','backup'})

    def test_examples_do_not_activate_dns(self):
        with tempfile.TemporaryDirectory(prefix='domain-api-tests-') as directory:
            root = Path(directory)
            shutil.copytree(FILES, root / 'examples/domain-api')
            with self.assertRaisesRegex(ValueError, 'No app routes'):
                dns.records(root, 'example.test', io.StringIO(FLEET))

    def test_routes_follow_domain_and_node_without_consumer_changes(self):
        with tempfile.TemporaryDirectory(prefix='domain-api-tests-') as directory:
            root = Path(directory)
            app = root / 'stacks/node-a/api'
            app.mkdir(parents=True)
            # Preserve the exact label syntax used by the reviewable drafts.
            rules = [line for document in self.documents() for line in document.splitlines() if '.rule=' in line]
            (app / 'docker-compose.yml').write_text('services:\n  fixture:\n    labels:\n'+'\n'.join(rules)+'\n',encoding='utf-8')
            before, _ = dns.records(root,'example.test',io.StringIO(FLEET))
            self.assertEqual(len(dns.routes_in(before)),11)
            self.assertTrue(all(line.endswith('/192.0.2.10') for line in dns.routes_in(before)))
            target = root / 'stacks/node-b/api'
            target.parent.mkdir(parents=True)
            app.rename(target)
            after, _ = dns.records(root,'example.test',io.StringIO(FLEET))
            self.assertTrue(all(line.endswith('/192.0.2.11') for line in dns.routes_in(after)))
            changed, _ = dns.records(root,'alternate.test',io.StringIO(FLEET))
            self.assertTrue(all('.alternate.test/' in line for line in dns.routes_in(changed)))

"""Exercise snapshotted route discovery across prepared Git phases, without live changes."""
import importlib.util
import io
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

prep = module('relocation_prepare', ROOT / 'examples/domain-api/prepare_relocation.py')
dns = module('relocation_dns', ROOT / 'tests/fixtures/dns_route_discovery.py')
FLEET = 'name,ip,mac\nnode-a,192.0.2.10,02:00:00:00:00:10\nnode-b,192.0.2.11,02:00:00:00:00:11\n'


class Relocation(unittest.TestCase):
    def test_phases_change_only_probe_record_and_removal_restores_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / 'prepared'
            prep.prepare(output, 'node-a', 'node-b')
            repo = root / 'repo'
            existing = repo / 'stacks/node-a/existing/docker-compose.yml'
            existing.parent.mkdir(parents=True)
            existing.write_text('  - "traefik.http.routers.existing.rule=Host(`existing.${DOMAIN}`)"\n')
            def records():
                return set(dns.records(repo, 'example.test', io.StringIO(FLEET))[0])
            baseline = records()
            a = repo / 'stacks/node-a/ingress-relocation/docker-compose.yml'
            b = repo / 'stacks/node-b/ingress-relocation/docker-compose.yml'
            a.parent.mkdir(parents=True)
            b.parent.mkdir(parents=True)
            shutil.copyfile(output / 'phase-a/stacks/node-a/ingress-relocation/docker-compose.yml', a)
            self.assertEqual(records() - baseline, {'address=/relocation-check.example.test/192.0.2.10', 'local=/relocation-check.example.test/'})
            shutil.copyfile(output / 'phase-b/stacks/node-b/ingress-relocation/docker-compose.yml', b)
            with self.assertRaisesRegex(ValueError, 'Conflicting route'):
                records()
            a.unlink()
            self.assertEqual(records() - baseline, {'address=/relocation-check.example.test/192.0.2.11', 'local=/relocation-check.example.test/'})
            self.assertTrue(baseline <= records())
            b.unlink()
            self.assertEqual(records(), baseline)

    def test_reject_unsafe_or_same_nodes_and_existing_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for a, b in [('../escape', 'node-b'), ('node-a', 'node-a'), ('/abs', 'node-b')]:
                with self.assertRaises(ValueError):
                    prep.prepare(root / 'unused', a, b)
            with self.assertRaises(ValueError):
                prep.prepare(root, 'node-a', 'node-b')
            with self.assertRaises(ValueError):
                prep.prepare(root / 'stacks/new', 'node-a', 'node-b')

import json
import unittest

from calicortado.config import resolve_endpoints
from calicortado.foundation import ROOT


class ConfigurationTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((ROOT / "config/deployment.example.json").read_text(encoding="utf-8"))

    def test_domain_changes_every_default(self):
        for domain in ("first.example", "second.example"):
            with self.subTest(domain=domain):
                endpoints = resolve_endpoints(self.config, {"DOMAIN": domain})
                self.assertEqual(len(endpoints), 11)
                self.assertTrue(all(value.endswith("." + domain) for value in endpoints.values()))

    def test_independent_service_override(self):
        result = resolve_endpoints(self.config, {"DOMAIN": "first.example", "DATA_BASE_URL": "https://data.other.example"})
        self.assertEqual(result["data"], "https://data.other.example")
        self.assertEqual(result["inference"], "https://infer.first.example")

    def test_missing_domain_fails(self):
        with self.assertRaises(ValueError):
            resolve_endpoints(self.config, {})

    def test_malformed_domains_fail(self):
        for domain in ("https://example.org", "example.org/path", "example.org:443", "127.0.0.1", "bad..example", "-bad.example", "example.org."):
            with self.subTest(domain=domain), self.assertRaises(ValueError):
                resolve_endpoints(self.config, {"DOMAIN": domain})

    def test_unsafe_overrides_fail(self):
        for value in ("http://data.example", "https://127.0.0.1", "https://user:pass@data.example", "https://${UNSET}"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                resolve_endpoints(self.config, {"DOMAIN": "first.example", "DATA_BASE_URL": value})

    def test_duplicate_domains_fail(self):
        with self.assertRaises(ValueError):
            resolve_endpoints(self.config, {"DOMAIN": "first.example", "DATA_BASE_URL": "https://search.first.example"})

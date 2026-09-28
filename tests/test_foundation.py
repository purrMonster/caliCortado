from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from jsonschema.exceptions import ValidationError
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError

from calicortado.foundation import (ROOT, authorize_fixture, read_spec, validate_contract,
                                    validate_request_fixture, validate_vectors)
from tools.check import check_placeholder_config, documentation_errors


class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = read_spec("search")
        cls.examples = json.loads((ROOT / "fixtures/examples.json").read_text(encoding="utf-8"))

    def setUp(self):
        self.grant = deepcopy(self.examples["Identity"])
        self.body = deepcopy(self.examples["SearchRequest"])

    def request(self):
        validate_request_fixture(self.spec, "/v1/search", "post", self.body, self.grant, now=1800000000)

    def test_allowed_request(self):
        self.request()

    def test_wrong_audience(self):
        self.grant["audience"] = "calicortado:data"
        with self.assertRaises(PermissionError):
            self.request()

    def test_missing_scope(self):
        self.grant["scopes"] = []
        with self.assertRaises(PermissionError):
            self.request()

    def test_wrong_vault(self):
        self.body["vault_id"] = "vault-denied"
        with self.assertRaises(PermissionError):
            self.request()

    def test_wrong_actor(self):
        self.grant["actor"] = "backup"
        with self.assertRaises(PermissionError):
            self.request()

    def test_expired_and_revoked(self):
        for key, value in (("expires_at", 1800000000), ("active", False)):
            with self.subTest(key=key):
                self.grant = deepcopy(self.examples["Identity"])
                self.grant[key] = value
                with self.assertRaises(PermissionError):
                    self.request()

    def test_forged_body_identity(self):
        self.body["subject"] = "administrator"
        with self.assertRaises(ValidationError):
            self.request()

    def test_wrong_issuer(self):
        self.grant["issuer"] = "https://untrusted.example"
        with self.assertRaises(ValidationError):
            self.request()

    def test_bad_limit_and_missing_query(self):
        for body in ({**self.body, "limit": 1000}, {"vault_id": "vault-demo", "limit": 2}):
            with self.subTest(body=body), self.assertRaises(ValidationError):
                self.body = body
                self.request()

    def test_capture_idempotency_header(self):
        spec = read_spec("capture")
        grant = {**self.grant, "actor": "device", "audience": "calicortado:capture", "scopes": ["capture:create"]}
        body = self.examples["Capture"]
        validate_request_fixture(spec, "/v1/captures", "post", body, grant, now=1800000000, idempotency_key=body["capture_id"])
        with self.assertRaises(ValueError):
            validate_request_fixture(spec, "/v1/captures", "post", body, grant, now=1800000000, idempotency_key="different")

    def test_snapshot_checks_every_vault(self):
        spec = read_spec("data")
        grant = {**self.grant, "actor": "backup", "audience": "calicortado:data", "scopes": ["snapshots:read"]}
        with self.assertRaises(PermissionError):
            validate_request_fixture(spec, "/v1/snapshots", "post", {"vault_ids": ["vault-demo", "vault-denied"]}, grant, now=1800000000)

    def test_vector_dimensions_and_count(self):
        result = self.examples["EmbeddingResult"]
        validate_vectors(result, len(result["vectors"]))
        with self.assertRaises(ValueError):
            validate_vectors(result, len(result["vectors"]) + 1)
        with self.assertRaises(ValueError):
            validate_vectors({**result, "dimensions": result["dimensions"] + 1}, len(result["vectors"]))

    def test_deliberately_invalid_openapi_fails(self):
        spec = deepcopy(self.spec)
        del spec["info"]["version"]
        with self.assertRaises(OpenAPIValidationError):
            validate_contract(spec)

    def test_missing_authorization_policy_fails(self):
        spec = deepcopy(self.spec)
        del spec["paths"]["/v1/search"]["post"]["x-required-scope"]
        with self.assertRaises(ValueError):
            validate_contract(spec)

    def test_broken_link_fails(self):
        with tempfile.TemporaryDirectory(prefix="calicortado-link-test-") as directory:
            root = Path(directory)
            (root / "README.md").write_text("[missing](absent.md)", encoding="utf-8")
            self.assertEqual(len(documentation_errors(root)), 1)

    def test_literal_credential_fails(self):
        config = {"endpoints": {"search": "https://search.calicortado.test"}, "credentials": {"token": "${SEARCH_TOKEN}"}}
        check_placeholder_config(config)
        config["credentials"]["token"] = "test-only-literal"
        with self.assertRaises(ValueError):
            check_placeholder_config(config)

    def test_raw_ip_endpoint_fails(self):
        with self.assertRaises(ValueError):
            check_placeholder_config({"endpoints": {"data": "https://192.0.2.1"}, "credentials": {}})


if __name__ == "__main__":
    unittest.main()

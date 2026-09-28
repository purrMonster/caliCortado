"""Validate independently owned contracts and exercise trusted fixture grants."""
from copy import deepcopy
import ipaddress
import json
import math
from pathlib import Path
import re
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, FormatChecker
from openapi_spec_validator import validate as validate_openapi
import yaml

ROOT = Path(__file__).resolve().parents[1]
METHODS = {"get", "post", "put", "patch", "delete"}


def read_spec(service, root=ROOT):
    return yaml.safe_load((root / "contracts" / f"{service}.yaml").read_text(encoding="utf-8"))


def validate_value(spec, schema, value):
    document = {"$schema": "https://json-schema.org/draft/2020-12/schema",
                **schema, "components": spec["components"]}
    Draft202012Validator(document, format_checker=FormatChecker()).validate(value)


def validate_contract(spec):
    validate_openapi(spec)
    for server in spec["servers"]:
        validate_endpoint(server["url"])
    for path in spec["paths"].values():
        for method, operation in path.items():
            if method not in METHODS:
                continue
            for key in ("x-audience", "x-required-scope", "x-allowed-actors",
                        "x-max-body-bytes", "x-deadline-seconds"):
                if key not in operation or operation[key] is None:
                    raise ValueError(f"Missing policy {key}: {operation['operationId']}")
            payloads = list(operation.get("responses", {}).values())
            if "requestBody" in operation:
                payloads.append(operation["requestBody"])
            for payload in payloads:
                for media in payload.get("content", {}).values():
                    if "example" in media:
                        validate_value(spec, media["schema"], media["example"])


def validate_endpoint(value):
    parsed = urlsplit(value)
    if (parsed.scheme != "https" or not parsed.hostname or parsed.username
            or parsed.password or parsed.query or parsed.fragment
            or parsed.path not in ("", "/") or parsed.port not in (None, 443)):
        raise ValueError("Base URL must be HTTPS domain root without credentials or a custom port")
    try:
        ipaddress.ip_address(parsed.hostname)
    except ValueError:
        if (len(parsed.hostname) <= 253 and "." in parsed.hostname
                and all(re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label)
                        for label in parsed.hostname.split("."))):
            return
    raise ValueError("Layer endpoints must use DNS names, not IP literals or localhost")


def authorize_fixture(spec, operation, grant, *, now, vault_id=None):
    """Accept an already authenticated test identity, never a request/header value.

    No token verification or network listener exists here. CAL-007 must supply
    independently authenticated, audience-bound introspection before this policy.
    """
    validate_value(spec, {"$ref": "#/components/schemas/Identity"}, grant)
    if not grant["active"] or grant["expires_at"] <= now:
        raise PermissionError("unauthenticated")
    if (grant["audience"] != operation["x-audience"]
            or operation["x-required-scope"] not in grant["scopes"]
            or grant["actor"] not in operation["x-allowed-actors"]
            or (vault_id is not None and vault_id not in grant["vault_ids"])):
        raise PermissionError("forbidden")


def validate_request_fixture(spec, path, method, body, grant, *, now, idempotency_key=None):
    operation = spec["paths"][path][method]
    authorize_fixture(spec, operation, grant, now=now, vault_id=body.get("vault_id"))
    if len(json.dumps(body, ensure_ascii=False).encode("utf-8")) > operation["x-max-body-bytes"]:
        raise ValueError("too_large")
    validate_value(spec, operation["requestBody"]["content"]["application/json"]["schema"], body)
    for vault_id in body.get("vault_ids", []):
        authorize_fixture(spec, operation, grant, now=now, vault_id=vault_id)
    if path == "/v1/captures" and idempotency_key != body["capture_id"]:
        raise ValueError("Idempotency-Key must equal capture_id")


def validate_vectors(result, input_count):
    if len(result["vectors"]) != input_count:
        raise ValueError("One vector is required per input")
    if any(len(vector) != result["dimensions"] for vector in result["vectors"]):
        raise ValueError("Vector dimensions differ from declared dimensions")
    if any(not math.isfinite(value) for vector in result["vectors"] for value in vector):
        raise ValueError("Vectors must contain finite numbers")


def demo():
    examples = json.loads((ROOT / "fixtures/examples.json").read_text(encoding="utf-8"))
    spec = read_spec("search")
    validate_contract(spec)
    validate_request_fixture(spec, "/v1/search", "post", examples["SearchRequest"],
                             examples["Identity"], now=1800000000)
    response = deepcopy(examples["SearchResult"])
    validate_value(spec, {"$ref": "#/components/schemas/SearchResult"}, response)
    print(json.dumps({"mode": "offline fixture; no live search, model, TLS or storage",
                      "endpoint": spec["servers"][0]["url"], "response": response}, indent=2))


if __name__ == "__main__":
    demo()

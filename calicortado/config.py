"""Resolve layer addresses without embedding an environment's domain."""
import argparse
import json
import os
from pathlib import Path
import re

from calicortado.foundation import ROOT, validate_endpoint

OVERRIDES = {
    "display": "APP_BASE_URL", "identity": "IDENTITY_BASE_URL",
    "sync": "SYNC_BASE_URL", "data": "DATA_BASE_URL",
    "capture": "CAPTURE_BASE_URL", "index": "INDEX_BASE_URL",
    "embeddings": "EMBEDDING_BASE_URL", "search": "SEARCH_BASE_URL",
    "inference": "INFERENCE_BASE_URL", "answers": "ANSWERS_BASE_URL",
    "backup": "BACKUP_REPOSITORY_URL",
}


def validate_domain(domain):
    if (not isinstance(domain, str) or len(domain) > 253 or "." not in domain
            or any(not re.fullmatch(r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?", label)
                   for label in domain.split("."))):
        raise ValueError("DOMAIN must be a DNS domain without scheme, port, path or trailing dot")
    validate_endpoint(f"https://{domain}")
    return domain.lower()


def resolve_endpoints(config, environment=None):
    environment = os.environ if environment is None else environment
    if set(config["endpoints"]) != set(OVERRIDES):
        raise ValueError("Configuration must name every layer exactly once")
    needs_domain = any("${DOMAIN}" in value for value in config["endpoints"].values())
    domain = validate_domain(environment.get("DOMAIN", "")) if needs_domain else ""
    result = {}
    for layer, template in config["endpoints"].items():
        value = environment.get(OVERRIDES[layer], template.replace("${DOMAIN}", domain))
        if "$" in value:
            raise ValueError(f"Unresolved endpoint variable for {layer}")
        validate_endpoint(value)
        result[layer] = value.rstrip("/")
    if len(set(result.values())) != len(result):
        raise ValueError("Each layer requires its own domain address")
    return result


def main():
    parser = argparse.ArgumentParser(description="Render endpoint configuration only; no network or secrets")
    parser.add_argument("--config", type=Path, default=ROOT / "config/deployment.example.json")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    print(json.dumps(resolve_endpoints(config), indent=2))


if __name__ == "__main__":
    main()

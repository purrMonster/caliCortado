"""Run the E01 checks from any working directory; no production access needed."""
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from calicortado.foundation import read_spec, validate_contract, validate_value, validate_endpoint

SKIP = {".venv", ".git", ".local", "node_modules", "__pycache__"}


def documentation_errors(root):
    errors = []
    for file in root.rglob("*.md"):
        if any(part in SKIP or part.startswith(".venv-") for part in file.relative_to(root).parts):
            continue
        text = file.read_text(encoding="utf-8-sig")
        # Links inside code fences describe future commands, not navigable docs.
        text = re.sub(r"^(```|~~~).*?^\1[^\n]*$", "", text, flags=re.M | re.S)
        for raw in re.findall(r"(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)", text):
            target = raw.strip().strip("<>").split(' "', 1)[0]
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            path, _, anchor = unquote(target).partition("#")
            resolved = (file.parent / path).resolve() if path else file
            if not resolved.exists():
                errors.append(f"{file.relative_to(root)}: missing {target}")
            elif anchor and resolved.suffix == ".md":
                headings = re.findall(r"^#{1,6}\s+(.+)$", resolved.read_text(encoding="utf-8-sig"), re.M)
                anchors = {re.sub(r"[^\w\- ]", "", h.lower()).replace(" ", "-") for h in headings}
                if anchor not in anchors:
                    errors.append(f"{file.relative_to(root)}: missing anchor {target}")
    return errors


def check_placeholder_config(config):
    if set(config) != {"endpoints", "credentials"}:
        raise ValueError("Unexpected fixture config keys")
    if len(set(config["endpoints"].values())) != len(config["endpoints"]):
        raise ValueError("Each layer requires its own address")
    for endpoint in config["endpoints"].values():
        validate_endpoint(endpoint.replace("${DOMAIN}", "validation.example"))
    for value in config["credentials"].values():
        if not re.fullmatch(r"\$\{[A-Z][A-Z0-9_]*\}", value):
            raise ValueError("Example credentials must be environment placeholders")


def main():
    errors = documentation_errors(ROOT)
    if errors:
        raise ValueError("\n".join(errors))
    examples = json.loads((ROOT / "fixtures/examples.json").read_text(encoding="utf-8"))
    count = 0
    canonical = None
    for path in sorted((ROOT / "contracts").glob("*.yaml")):
        spec = read_spec(path.stem)
        validate_contract(spec)
        schemas = spec["components"]["schemas"]
        if canonical is not None and schemas != canonical:
            raise ValueError(f"Shared schemas diverged: {path.name}")
        canonical = schemas
        if set(examples) != set(schemas):
            raise ValueError("Every schema must have an example")
        for name, example in examples.items():
            validate_value(spec, {"$ref": f"#/components/schemas/{name}"}, example)
        count += 1
    for config in (ROOT / "config").glob("*.example.json"):
        check_placeholder_config(json.loads(config.read_text(encoding="utf-8")))
    print(f"PASS: documentation, {count} OpenAPI contracts, {len(examples)} schema fixtures, endpoint/credential examples", flush=True)
    subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()

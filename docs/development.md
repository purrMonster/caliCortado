# Development foundation — CAL-003

This is an offline contract workspace, not a deployed product. It opens no ports, reads no personal vault and uses no real identity or model. Run from a source checkout/copy using CPython **3.12.14**. Runtime pins are in [.python-version](../.python-version), direct tool dependencies in [requirements-dev.in](../requirements-dev.in), and all resolved versions in [requirements-dev.lock](../requirements-dev.lock).

## Clean start

PowerShell, with Python 3.12.14 available as `python`:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-dev.lock
.venv\Scripts\python.exe -m pip check
.venv\Scripts\python.exe tools/check.py
.venv\Scripts\python.exe -m calicortado.foundation
```

On Linux/macOS use `python3.12` to create the venv and `.venv/bin/python` for subsequent commands. Windows was tested; other operating systems remain unverified. Install requires access to the package index or a pre-provisioned wheel cache. Checks and demo require no network after installation. The lock pins versions but is not a hash-verified supply-chain lock.

The final command validates a permitted synthetic search request and response from fixtures. It does not search a vault or call an LLM. The check command validates Markdown file/heading links, seven OpenAPI documents, schema examples, distinct HTTPS endpoints and placeholder-only credentials, then runs authorization/defect tests. External web links are not crawled. All repository documentation checks are self-contained; no sibling infrastructure checkout is required.

## Ownership and layout

- [Services](../services/README.md) define independent data, capture, embeddings, retrieval, index, inference and answer ownership. The README skeletons are implementation entry points, not empty running services.
- [Display](../display/README.md) owns web UI/session handling; [clients](../clients/README.md) owns device procedure contracts.
- [Contracts](contracts.md) and [security](security.md) are the versioned implementation baseline.
- [Fixtures](../fixtures/README.md) contain invented notes and already-authenticated test identity values.
- [Endpoint configuration](../config/local.example.json) uses reserved `.test` names. Deployment candidates use the confirmed domain in a separate example. Application consumers receive base URLs via configuration, never machine addresses.

Generated/private notes, virtual environments, real `.env` files, keys and local scratch output belong outside tracked source. The credential-example check is deliberately narrow; it is not a repository-wide secret scanner or evidence that arbitrary future files contain no secrets. Review files before any commit. Use `.local/` for disposable generated state.

## Domain configuration

The deployment template derives every default layer URL from `${DOMAIN}`. [.env.example](../.env.example) records the currently selected value; it is not automatically loaded by Python. Set the process environment explicitly, or have the future deployment tooling load the environment file. Never bake its value into source or frontend bundles at build time.

```powershell
$env:DOMAIN = "example.org"
.venv\Scripts\python.exe -m calicortado.config
# Move one layer independently; other defaults still derive from DOMAIN.
$env:DATA_BASE_URL = "https://data.another.example"
.venv\Scripts\python.exe -m calicortado.config
```

The equivalent POSIX invocation is `DOMAIN=example.org .venv/bin/python -m calicortado.config`. The renderer prints addresses only and performs no network calls. Missing/invalid DOMAIN, non-HTTPS/IP/credential-bearing endpoints and duplicate addresses are errors. [config.py](../calicortado/config.py) lists optional per-layer overrides: `APP_BASE_URL`, `IDENTITY_BASE_URL`, `SYNC_BASE_URL`, `DATA_BASE_URL`, `CAPTURE_BASE_URL`, `INDEX_BASE_URL`, `EMBEDDING_BASE_URL`, `SEARCH_BASE_URL`, `INFERENCE_BASE_URL`, `ANSWERS_BASE_URL`, `BACKUP_REPOSITORY_URL`. Overrides are domain roots in E01; repository subpaths are a future backup-protocol setting. Credentials are resolved separately by the future service runtime, never printed here.

Use `--config config/local.example.json` for fixed reserved `.test` fixtures. These fixtures do not depend on the deployment domain. The E02 infrastructure must derive DNS/Traefik/TLS names from the same DOMAIN setting; runtime configuration support does not prove live DNS/certificates have changed.

## Local domain/TLS integration recipe

This is the E02 recipe to implement and test; no TLS result is claimed in E01.

1. Obtain a working local container engine. In Calicortado, prepare an isolated disposable Traefik stack pinned to the approved version, with synthetic HTTP backends and no personal storage. Keep all preparation here until the product is ready for deployment.
2. Map `app`, `auth`, `sync`, `data`, `capture`, `index`, `embed`, `search`, `infer`, `answers`, `backup` under `calicortado.test` to the test ingress using local DNS or user-managed hosts entries. Do not edit production DNS. If 443 is occupied use an isolated VM with its own address, preserving domain URLs.
3. Issue a local test CA and server certificate with the exact test SANs. Store private keys in ignored local state. Supply that CA explicitly to test clients; user approval/setup is required for machine/device-wide trust changes. Never disable certificate verification.
4. Configure domain-specific HTTPS routers and authenticated probes. Expose only ingress; backends must not publish host ports. Use encrypted and verified upstream transport whenever a backend is remote. Do not use broad wildcard routing or proxy headers as identity proof.
5. Exercise allowed domain/SNI calls, unknown hosts, wrong/expired certificates, wrong credentials, direct-port denial and streaming/cancellation. CAL-006–008 own actual commands/config and results once that stack exists.
6. Remove only the disposable stack and its generated test state. Undo any test hosts/trust changes made by the user. Retain evidence, not keys. Production has no dependency on this CA.

## Change, failure and rollback

For a schema failure inspect the reported operation/example; fix the source contract and compatible consumers, then rerun checks. For a link failure fix the reference or create the actual document; do not add empty placeholders to conceal unfinished work. Tests intentionally prove that a broken link, missing OpenAPI metadata and malformed access requests fail.

Upgrade tooling by editing direct pins, resolving in a fresh venv, reviewing the complete lock diff and rerunning all checks. Restore the prior lock/source to roll back; recreating the disposable venv loses no product data. There is no persistent service state or database migration in E01. Before distributed implementation, complete CAL-007 identity integration and CAL-009 note identity/sync prototype gates. [E01 evidence](acceptance/e01.md) states exactly what has run.

## Infrastructure preparation checks

Run `python -m unittest discover -s tests -p test_domain_api_drafts.py -v` and `python -m unittest discover -s tests -p test_relocation_plan.py -v`. They use the [offline DNS compatibility fixture](../tests/fixtures/DNS-COMPATIBILITY.md), without another checkout. See [preparation instructions](../examples/domain-api/README.md). Live promotion remains a deployment-readiness gate.

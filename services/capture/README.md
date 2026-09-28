# Capture service

Status: E01 ownership skeleton; no runtime service yet.

Owns create-only validation and ingestion through the data domain. Stateless orchestration. Durable capture identity belongs to data; acknowledge only its durable result.

Implement CAL-016–017 against the [capture contract](../../contracts/capture.yaml), [semantic invariants](../../docs/contracts.md) and [authorization matrix](../../docs/security.md). Endpoint addresses and credentials are configuration inputs; never hardcode machine addresses. The API exposes authenticated readiness through its own Traefik domain.

Run the [offline development checks](../../docs/development.md) before changing contracts. They prove schema/fixture behavior only. The owning stories must add actual setup, command/configuration, health/failure diagnostics, bounded retry, migration/rollback and state recovery instructions as implementation lands. No install or recovery command for a nonexistent service is implied. Deployment configuration belongs in infrastructure.


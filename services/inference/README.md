# Inference service

Status: E01 ownership skeleton; no runtime service yet.

Owns bounded local generation and cancellation. Local model files are owned here. No vault mounts, database credentials or agent action tools.

Implement CAL-034–037 against the [inference contract](../../contracts/inference.yaml), [semantic invariants](../../docs/contracts.md) and [authorization matrix](../../docs/security.md). Endpoint addresses and credentials are configuration inputs; never hardcode machine addresses. The API exposes authenticated readiness through its own Traefik domain.

Run the [offline development checks](../../docs/development.md) before changing contracts. They prove schema/fixture behavior only. The owning stories must add actual setup, command/configuration, health/failure diagnostics, bounded retry, migration/rollback and state recovery instructions as implementation lands. No install or recovery command for a nonexistent service is implied. Deployment configuration belongs in infrastructure.


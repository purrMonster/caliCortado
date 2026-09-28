# Retrieval service

Status: E01 ownership skeleton; no runtime service yet.

Owns change-feed indexing and authorized fresh hybrid search. Calls data, embeddings and index domains. Checkpoints are restart-safe; never return stale or newly excluded snippets.

Implement CAL-032–033 against the [search contract](../../contracts/search.yaml), [semantic invariants](../../docs/contracts.md) and [authorization matrix](../../docs/security.md). Endpoint addresses and credentials are configuration inputs; never hardcode machine addresses. The API exposes authenticated readiness through its own Traefik domain.

Run the [offline development checks](../../docs/development.md) before changing contracts. They prove schema/fixture behavior only. The owning stories must add actual setup, command/configuration, health/failure diagnostics, bounded retry, migration/rollback and state recovery instructions as implementation lands. No install or recovery command for a nonexistent service is implied. Deployment configuration belongs in infrastructure.


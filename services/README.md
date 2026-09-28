# Service ownership

E01 contains contracts and fixture checks only. Each component README is a handoff for independently implementing and packaging its service, not evidence of a running endpoint. Shared foundation code is development-only; do not introduce a cross-layer database or filesystem dependency.

| Component | Entry point | Stories |
|---|---|---|
| Data | [data](data/README.md) | CAL-009–013 |
| Capture | [capture](capture/README.md) | CAL-016–017 |
| Embeddings | [embeddings](embeddings/README.md) | CAL-026–029 |
| Index | [index](index/README.md) | CAL-030–031 |
| Retrieval | [retrieval](retrieval/README.md) | CAL-032–033 |
| Inference adapter | [inference](inference/README.md) | CAL-034–037 |
| Answers | [answers](answers/README.md) | CAL-038–041 |

All service consumers take configured domain URLs. Deployment manifests belong in infrastructure; this directory owns application code and service operation documentation as implementation lands.

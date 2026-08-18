# RAG_DIAloga

Repositorio técnico del motor RAG de DIAloga.

Este repositorio conserva contratos, manifests, attestations, hashes, scripts de validación y estados de release necesarios para integrar el RAG con la aplicación DIAloga.

## Principios

- Los artefactos congelados (`FROZEN`) se tratan como inmutables.
- Los estados `BLOCKED`, `REVOKED`, `SUPERSEDED` y `HOLD` se conservan explícitamente; no se borran del historial.
- Los binarios grandes, modelos y bundles ZIP no se almacenan directamente en Git salvo decisión expresa; se referencian mediante SHA-256 y manifests.
- La integración con DIAloga debe consumir únicamente releases autorizadas por sus gates.
- `Production Embeddings RC2` se encuentra actualmente `BLOCKED_PENDING_EXTERNAL_TRUST_EVIDENCE`; cualquier Frozen Attestation previa queda revocada por la auditoría suplementaria final.

## Estructura

- `rag/00_governance/` — estado global, trust-chain y reglas de release.
- `rag/01_canonical/` — corpus canónico integrado y trust anchors.
- `rag/02_hybrid_design/` — contrato de diseño del índice híbrido.
- `rag/03_lexical/` — índice lexical y runtime lexical.
- `rag/04_embeddings/` — benchmark, producción, auditorías y recuperación de trust.
- `rag/05_dense_index/` — dense index; actualmente en HOLD hasta resolver Production Embeddings RC2.
- `rag/06_hybrid_index/` — reservado para Full Hybrid Index.
- `rag/07_application_wiring/` — integración futura con el código local de DIAloga.
- `rag/08_e2e_tests/` — validación end-to-end futura.

No se debe interpretar la presencia de un artefacto en este repositorio como autorización de uso; siempre consultar `rag/00_governance/release_status.json`.

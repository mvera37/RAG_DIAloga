# DIAloga Runtime Integration

Esta es la carpeta especial y autoritativa para integrar el RAG con la aplicación DIAloga.

## Regla
Solo pueden aparecer aquí componentes actualmente autorizados para integración. Los artefactos históricos, auditorías, candidates rechazados, releases REVOKED/BLOCKED/HOLD y herramientas de construcción permanecen fuera de esta carpeta.

## Estado actual
- Canonical RC4: FROZEN y autorizado.
- Hybrid Design RC9: FROZEN y autorizado como contrato de routing/retrieval.
- Lexical Index RC1: FROZEN y autorizado.
- Lexical Runtime RC2: FROZEN y autorizado.
- Production Embeddings RC2: FROZEN y autorizado; candidate oficial SHA-256 `67d0804361c2cb594216c5c33de330cc7c22c5f5988372eabd9988ba8f86ae2a`, vector SHA-256 `89189e573b7f7818b137bd69d00a0acabbaec0c64a2778d22c9244b432262a6e`, Frozen Attestation v2 SHA-256 `1ebb82c73abe68b56fc806b05ef2dfe59b547c1775f9821749a2bb0ba5b7c40f`.
- Dense Index: el RC1 histórico permanece HOLD / DO NOT AUDIT; se requiere un rebuild nuevo pinneado al Frozen Attestation v2.
- Full Hybrid: BLOCKED hasta Dense audit/freeze.

La autorización de Production Embeddings no habilita por sí sola la lane dense. `config/rag_runtime_config.json` mantiene `dense` y `hybrid_semantic` deshabilitadas.

DIAloga debe leer primero `integration_manifest.json` y operar fail-closed: si falta un artefacto, una autoridad requerida o su SHA-256 no coincide, la lane correspondiente no se habilita.

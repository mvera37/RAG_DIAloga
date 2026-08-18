# DIAloga Runtime Integration

Esta es la carpeta especial y autoritativa para integrar el RAG con la aplicación DIAloga.

## Regla
Solo pueden aparecer aquí componentes actualmente autorizados para integración. Los artefactos históricos, auditorías, candidates rechazados, releases REVOKED/BLOCKED/HOLD y herramientas de construcción permanecen fuera de esta carpeta.

## Estado actual
- Canonical RC4: FROZEN y autorizado.
- Hybrid Design RC9: FROZEN y autorizado como contrato de routing/retrieval.
- Lexical Index RC1: FROZEN y autorizado.
- Lexical Runtime RC2: FROZEN y autorizado.
- Production Embeddings RC2: pendiente de auditoría suplementaria; NO habilitado.
- Dense Index: HOLD; NO habilitado.
- Full Hybrid: BLOCKED; NO habilitado.

DIAloga debe leer primero `integration_manifest.json` y operar fail-closed: si falta un artefacto o su SHA-256 no coincide, la lane correspondiente no se habilita.

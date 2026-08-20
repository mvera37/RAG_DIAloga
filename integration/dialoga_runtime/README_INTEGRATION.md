# DIAloga Runtime Integration

Esta es la carpeta autoritativa para integrar el RAG con la aplicación DIAloga.

## Regla
Solo componentes `FROZEN` y explícitamente autorizados pueden habilitar una lane. Toda carga debe verificar primero las identidades SHA-256 definidas en `integration_manifest.json`, `ARTIFACT_MAP.json` y las Frozen Attestations.

## Estado actual
- Canonical RC4: **FROZEN**.
- Hybrid Design RC9: **FROZEN**.
- Lexical Index RC1: **FROZEN**.
- Lexical Runtime RC2: **FROZEN_VALID**.
- Production Embeddings RC2: **FROZEN**.
- Dense Index RC2: **FROZEN**.
- Full Hybrid RC1: **FROZEN**; candidate SHA-256 `c7537e8befb53427a8911a4508d3bc68771d617f3630616c3f7ad4ddd0d9f6fc`.
- Full Hybrid Frozen Attestation v1 SHA-256: `cc5c7929d52f64bda6dce24d82d1fe0c18319c3f021a4d88a89ed7639d5d5971`.
- Full Hybrid Freeze Completion v1 SHA-256: `6e1afd9c66d9dc219cd3614ec4f0972e7008217e6b460bc8cd78581a5a75457c`.
- Final external closure: **PASS_WITH_NON_BLOCKING_FINDINGS**.
- Dense RC1 histórico: `HOLD_DO_NOT_AUDIT_DO_NOT_PROMOTE`.
- Application Wiring: **AUTHORIZED_PENDING_LOCAL_DIALOGA_SOURCE_NOT_STARTED**.

## Runtime fail-closed
`config/rag_runtime_config.json` habilita `dense` y `hybrid_semantic` bajo autorización post-freeze. Si falta un artefacto, una autoridad, o cualquier SHA-256 no coincide, el runtime debe deshabilitar las lanes semánticas y abortar su arranque.

El registro `full_hybrid/FULL_HYBRID_RC1_RUNTIME_PROMOTION.json` fija la promoción y las autoridades parent requeridas. Ningún componente frozen puede modificarse durante la integración de la aplicación.

## Próximo gate
El siguiente trabajo es Application Wiring con el código actual de DIAloga. Después de conectar el retriever/routing se debe ejecutar `rag/08_e2e_tests/E2E_GATE_MATRIX.json`. `production_ready` continúa en `false` hasta completar wiring y E2E.

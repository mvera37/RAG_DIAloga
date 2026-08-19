# DIAloga Runtime Integration

Esta es la carpeta especial y autoritativa para preparar la integración del RAG con la aplicación DIAloga.

## Regla
Solo los componentes `FROZEN` y explícitamente autorizados pueden convertirse en dependencias de runtime. Un candidate en auditoría puede registrarse aquí únicamente como pendiente y nunca habilita una lane por sí mismo.

## Estado actual
- Canonical RC4: **FROZEN**.
- Hybrid Design RC9: **FROZEN**.
- Lexical Index RC1: **FROZEN**.
- Lexical Runtime RC2: **FROZEN**.
- Production Embeddings RC2: **FROZEN**; Frozen Attestation v2 SHA-256 `1ebb82c73abe68b56fc806b05ef2dfe59b547c1775f9821749a2bb0ba5b7c40f`.
- Dense Index RC2: **FROZEN**; Frozen Attestation v1 SHA-256 `991dc756d0ba513324ba59e2428e211417009f4b46ea6d936790fa0572416ff3`.
- Dense RC1 histórico: `HOLD_DO_NOT_AUDIT_DO_NOT_PROMOTE`.
- Full Hybrid RC1: **READY_FOR_EXTERNAL_AUDIT_NOT_FROZEN**; candidate SHA-256 `c7537e8befb53427a8911a4508d3bc68771d617f3630616c3f7ad4ddd0d9f6fc`.
- Full Hybrid external anchor: commit `9e6a7a5a745095e4e24404ca99d25647ff73b345`, SHA-256 `034e1b95296ba9f971b6fcf1c7522319bc2f04f67b300907f5cca50474e2214a`.
- Full Hybrid External Audit Bundle SHA-256 `257fb9876b2ed4ad9e137317ad7eb8540204e6060a96fafd1bf5a78e6fcae5eb`.
- Application Wiring: **BLOCKED** hasta Full Hybrid external PASS + freeze propio + código local actual de DIAloga.

## Runtime fail-closed
`config/rag_runtime_config.json` mantiene `dense` y `hybrid_semantic` deshabilitadas. Full Hybrid RC1 todavía no puede utilizarse en producción ni integrarse a la aplicación.

DIAloga deberá leer `integration_manifest.json`, `ARTIFACT_MAP.json` y las Frozen Attestations antes de habilitar cualquier lane. Si falta un artefacto, una autoridad o un SHA-256 no coincide, el sistema debe fallar cerrado.

## Próximo gate
El trabajo técnico de construcción de Full Hybrid RC1 está terminado. El próximo gate es la **auditoría externa independiente** del candidate y de su audit bundle. Solo un resultado externo favorable podrá habilitar la creación de la Frozen Attestation de Full Hybrid y, después, el inicio de Application Wiring.

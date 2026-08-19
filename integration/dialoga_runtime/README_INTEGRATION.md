# DIAloga Runtime Integration

Esta es la carpeta especial y autoritativa para integrar el RAG con la aplicación DIAloga.

## Regla
Solo pueden aparecer aquí componentes actualmente autorizados para integración. Los artefactos históricos, auditorías, candidates rechazados, releases REVOKED/BLOCKED/HOLD y herramientas de construcción permanecen fuera de esta carpeta.

## Estado actual
- Canonical RC4: **FROZEN** y autorizado.
- Hybrid Design RC9: **FROZEN** y autorizado como contrato de routing/retrieval.
- Lexical Index RC1: **FROZEN** y autorizado.
- Lexical Runtime RC2: **FROZEN** y autorizado.
- Production Embeddings RC2: **FROZEN** y autorizado; candidate SHA-256 `67d0804361c2cb594216c5c33de330cc7c22c5f5988372eabd9988ba8f86ae2a`, vector SHA-256 `89189e573b7f7818b137bd69d00a0acabbaec0c64a2778d22c9244b432262a6e`, Frozen Attestation v2 SHA-256 `1ebb82c73abe68b56fc806b05ef2dfe59b547c1775f9821749a2bb0ba5b7c40f`.
- Dense Index RC2: **FROZEN** y autorizado como dependencia; candidate SHA-256 `f45b854796c733affed1811984cdd6ebd061eaf0ec9341e4a4af60bf74df1ea8`, index SHA-256 `085215053fa3da335d3f557e644ea33c33c678e47012c4c3d2d12cf9b6fe0198`, row map SHA-256 `957afabb965ffca781502ab15063f11930950207d771ed42cc5bcec49c6bcada`, Frozen Attestation v1 SHA-256 `991dc756d0ba513324ba59e2428e211417009f4b46ea6d936790fa0572416ff3`.
- Dense RC1 histórico: `HOLD_DO_NOT_AUDIT_DO_NOT_PROMOTE`.
- Full Hybrid: **AUTHORIZED_FOR_NEW_BUILD_NOT_YET_BUILT**. Debe pinnear las autoridades frozen exactas y pasar sus propios gates antes de cualquier promoción.
- Application Wiring: **BLOCKED_PENDING_FULL_HYBRID_AND_LOCAL_DIALOGA_SOURCE**.

## Runtime fail-closed
Aunque Production Embeddings RC2 y Dense RC2 están frozen, `config/rag_runtime_config.json` mantiene `dense` y `hybrid_semantic` deshabilitadas. No se habilitarán hasta construir, validar y congelar el nuevo Full Hybrid.

DIAloga debe leer primero `integration_manifest.json` y `ARTIFACT_MAP.json`. Si falta un artefacto requerido, una autoridad frozen o cualquier SHA-256 no coincide, la lane correspondiente debe permanecer deshabilitada.

## Próximo gate
El siguiente trabajo autorizado es `rag/06_hybrid_index/`: construcción de un nuevo Full Hybrid candidate contra las dependencias frozen actuales. El freeze de Dense no implica por sí mismo que Full Hybrid exista o esté aprobado.

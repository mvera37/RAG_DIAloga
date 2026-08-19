# Full Hybrid Index

Estado: **RC1 READY FOR EXTERNAL AUDIT / NOT FROZEN**.

Dense Index RC2 y todas las dependencias previas están `FROZEN`. Full Hybrid RC1 ya fue construido como un nuevo candidate sin modificar ninguna dependencia frozen.

## Full Hybrid RC1
- Candidate: `DIAloga_Hybrid_Index_V4_Full_Hybrid_RC1_Candidate.zip`
- SHA-256: `c7537e8befb53427a8911a4508d3bc68771d617f3630616c3f7ad4ddd0d9f6fc`
- Bytes: `1738458`
- Members: `25`
- Artifact class: `QUERY_TIME_FULL_HYBRID_COMPOSITION`

No existe un índice fusionado estático. El release compone en tiempo de consulta rankings lexical y Dense frozen mediante RRF, preservando el bypass estructurado y los 16 registros lexical-only definidos por el diseño.

## Internal gates
- Candidate validator: `PASS_125_OF_125`.
- Adversarial: `PASS_8_OF_8`.
- Physical cross-parent validation: `PASS_28_OF_28`.
- Deterministic candidate rebuild: `PASS_4_OF_4_BYTE_IDENTICAL`.
- Audit bundle verifier: `PASS_30_OF_30` en modo soporte y `PASS_31_OF_31` con anchor suministrado.

## External authority
- Commit inmutable: `9e6a7a5a745095e4e24404ca99d25647ff73b345`.
- Path: `rag/06_hybrid_index/rc1/release_authority/FULL_HYBRID_RC1_OFFICIAL_RELEASE_ANCHOR.json`.
- Anchor SHA-256: `034e1b95296ba9f971b6fcf1c7522319bc2f04f67b300907f5cca50474e2214a`.

El auditor debe obtener el anchor directamente desde ese commit; la copia dentro del audit bundle no es raíz de confianza terminal.

## External audit bundle
- `DIAloga_Hybrid_Index_V4_Full_Hybrid_RC1_External_Audit_Bundle.zip`
- SHA-256: `257fb9876b2ed4ad9e137317ad7eb8540204e6060a96fafd1bf5a78e6fcae5eb`
- Bytes: `23362489`

## Frozen authorities obligatorias
El candidate pinnea Hybrid Design RC9, Lexical Index RC1, Lexical Runtime RC2, Production Embeddings RC2 y Dense Index RC2 por sus Frozen Attestations y SHA-256 físicos.

## Fail-closed rules
- Full Hybrid RC1 **no está FROZEN**.
- `dense` y `hybrid_semantic` continúan deshabilitadas.
- No se permite reutilizar Dense RC1.
- No se permite modificar ningún artefacto frozen.
- Cualquier mismatch SHA-256 aborta la cadena.
- Application Wiring continúa bloqueado hasta recibir auditoría externa favorable y formalizar el Full Hybrid freeze.

Ver `FULL_HYBRID_BUILD_GATE.json` y `rc1/AUDIT_READINESS.json` para los contratos machine-readable.

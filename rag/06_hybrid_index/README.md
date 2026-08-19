# Full Hybrid Index

Estado: **READY_FOR_BUILD / NOT YET BUILT**.

Dense Index RC2 ya está `FROZEN`; por tanto, el bloqueo previo de dependencias fue levantado. Esto autoriza únicamente la construcción de un **nuevo Full Hybrid candidate**. No autoriza runtime, freeze ni Application Wiring por sí solo.

## Frozen authorities obligatorias
El nuevo Full Hybrid debe pinnear exactamente:

- Hybrid Index V4 Design RC9 Frozen Attestation SHA-256: `71a1cbca13ac20716c86e04c44bfb6ca9084b409b76105a2a36df69286ca2679`
- Lexical Index RC1 Frozen Attestation SHA-256: `ce49cbdebe04a11e8ef239f2a9156d1ca2eb52063835794ea26880ea0d4e1df9`
- Lexical Runtime RC2 Frozen Attestation SHA-256: `7084a3be23d8c34dca7737e2628092f40a906e76d2f6d5151b20a6329ae04f5e`
- Production Embeddings RC2 Frozen Attestation v2 SHA-256: `1ebb82c73abe68b56fc806b05ef2dfe59b547c1775f9821749a2bb0ba5b7c40f`
- Dense Index RC2 Frozen Attestation v1 SHA-256: `991dc756d0ba513324ba59e2428e211417009f4b46ea6d936790fa0572416ff3`
- Dense candidate SHA-256: `f45b854796c733affed1811984cdd6ebd061eaf0ec9341e4a4af60bf74df1ea8`
- Dense index SHA-256: `085215053fa3da335d3f557e644ea33c33c678e47012c4c3d2d12cf9b6fe0198`
- Dense row map SHA-256: `957afabb965ffca781502ab15063f11930950207d771ed42cc5bcec49c6bcada`
- Production vector SHA-256: `89189e573b7f7818b137bd69d00a0acabbaec0c64a2778d22c9244b432262a6e`

## Fail-closed rules
- No se permite reutilizar Dense RC1.
- No se permite modificar ningún artefacto frozen para construir Full Hybrid.
- Cualquier mismatch SHA debe abortar el build.
- `dense` y `hybrid_semantic` continúan deshabilitadas hasta que el Full Hybrid candidate pase sus gates de validación y release.
- Application Wiring continúa bloqueado hasta cerrar Full Hybrid.

Ver `FULL_HYBRID_BUILD_GATE.json` para el contrato machine-readable del siguiente build.

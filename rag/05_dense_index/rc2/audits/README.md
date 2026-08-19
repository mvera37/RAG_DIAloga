# Dense RC2 audit evidence

La identidad autoritativa de los tres informes externos se registra en `AUDIT_CHAIN.json` mediante tamaño y SHA-256 exactos.

Los informes originales recibidos del auditor usan terminadores CRLF y forman parte de la cadena de evidencia por **bytes exactos**. No se deben normalizar ni reescribir y luego presentar como si conservaran el mismo SHA-256.

La cadena es:

1. `DIAloga_Dense_Index_Build_RC2_External_Audit_FINAL.md` — `BLOCKED` — SHA-256 `26405462685cad7265ba4d8b716cc9aeed5e1d84bd924fbff0d8d7db96c7de92`.
2. `DIAloga_Dense_Index_Build_RC2_Supplemental_External_Audit_FINAL.md` — `BLOCKED` — SHA-256 `fb2a993716826cb93b8f1582dcf2cd90c0b2d9c3453c83aa39c4a57cbea835c4`.
3. `DIAloga_Dense_Index_Build_RC2_Closure_External_Audit_FINAL.md` — `PASS_WITH_NON_BLOCKING_FINDINGS` — SHA-256 `f75c5a9374837211c5ebeee42026d3558e339996ca1ee88ac762ea3522c93116`.

El closure bundle físico mantiene SHA-256 `d130b209ec45dcbac9e823fd3daf1192f443e9b98844395a7d31a1a29c8786b4` y debe distribuirse como GitHub Release Asset, no duplicarse dentro del historial Git normal.

El freeze vigente está definido por `../release_authority/DIAloga_Dense_Index_Build_RC2_FROZEN_ATTESTATION_v1.json` SHA-256 `991dc756d0ba513324ba59e2428e211417009f4b46ea6d936790fa0572416ff3`.

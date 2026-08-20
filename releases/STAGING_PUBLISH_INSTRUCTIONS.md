# DIAloga — GitHub Release staging publication

Los artefactos binarios grandes se mantienen fuera del historial Git normal y deben publicarse como GitHub Release Assets después de verificar nombre, tamaño y SHA-256 exactos.

## Estado del staging físico actual

El archivo existente:

- `DIAloga_GitHub_Release_Staging_Current.zip`
- Bytes: `324348878`
- SHA-256: `cb575eb4ab654db7ef8c085a78206c889af387314a2096f90966a8db755e4abd`
- Assets: `13`

fue construido **antes del cierre y freeze de Dense RC2**. Se conserva como snapshot de transferencia histórico, pero **no debe tratarse como el staging final post-Dense-freeze**.

Ver:
- `STAGING_MANIFEST_CURRENT.json` para el inventario físico de ese ZIP histórico.
- `STAGING_DELTA_POST_DENSE_FREEZE.json` para las diferencias posteriores al freeze.
- `RELEASE_UPLOAD_INVENTORY.json` para la autoridad lógica vigente de qué assets deben publicarse y con qué SHA-256.

## Cambio obligatorio post-Dense-freeze

El release final debe incluir/poder resolver, además de los assets ya existentes, el closure bundle:

- `DIAloga_Dense_Index_Build_RC2_Closure_External_Audit_Bundle.zip`
- SHA-256: `d130b209ec45dcbac9e823fd3daf1192f443e9b98844395a7d31a1a29c8786b4`

Dense RC2 ya no es un audit candidate: es un artefacto `FROZEN_RELEASE_AUTHORITY` y su candidate oficial mantiene SHA-256 `f45b854796c733affed1811984cdd6ebd061eaf0ec9341e4a4af60bf74df1ea8`.

## Publisher histórico

`releases/scripts/PUBLISH_DIAloga_RELEASE_ASSETS.ps1` fue preparado antes del freeze de Dense RC2 y conserva grupos/tags de la etapa de auditoría. **No debe usarse como publisher final sin actualizarlo contra `RELEASE_UPLOAD_INVENTORY.json` v3.**

La publicación final debe realizarse desde una estación confiable con GitHub CLI autenticado, verificando cada SHA-256 inmediatamente antes del upload y dejando los releases inicialmente como `DRAFT` para revisión.

## Granite311 snapshot

El snapshot autenticado mantiene identidad:

`DIAloga_Granite311_Authenticated_Snapshot_RC2.zip`

SHA-256:

`3e79757c748ede47e8ebe3c768a29ce0218e14949dab41177b8ce42b40fdec12`

No modificar el ZIP ni insertar archivos adicionales.

## Gate de integración

La ausencia temporal de una nueva staging archive no invalida los freezes ya emitidos ni bloquea el build de Full Hybrid. Para integración/runtime se usan las autoridades y SHA exactas registradas en `integration/dialoga_runtime/` y `rag/00_governance/release_status.json`; los Release Assets son la capa de distribución física y deben sincronizarse antes de la publicación final.

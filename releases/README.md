# Release assets

Esta carpeta contiene manifests y reglas de publicación de los artefactos físicos del RAG y de los datasets CNEB. Los ZIP grandes no deben duplicarse en el historial Git normal; deben publicarse como GitHub Release Assets conservando nombre, tamaño y SHA-256 exactos.

## Política
- Git normal: contratos, manifests, attestations, scripts, estados, hashes y configuración de integración.
- Release Assets: ZIP canónicos, candidates frozen, audit bundles, snapshots y demás binarios grandes.
- Un asset `BLOCKED`, `REVOKED` o `HOLD` se conserva solo como evidencia histórica y nunca se habilita en `integration/dialoga_runtime/`.
- Un artefacto `FROZEN` no puede modificarse byte a byte; cualquier cambio exige nueva identidad de release.

## Fuentes vigentes
- `ASSET_CATALOG.json`: catálogo lógico de assets y estados.
- `RELEASE_UPLOAD_INVENTORY.json`: inventario fail-closed para publicación; actualmente schema `dialoga_release_upload_inventory_v3`.
- `STAGING_MANIFEST_CURRENT.json`: snapshot físico histórico del staging de 13 assets construido antes del freeze de Dense RC2.
- `STAGING_DELTA_POST_DENSE_FREEZE.json`: delta que debe incorporarse antes de la publicación binaria final.
- `PUBLISHER_STATUS.json`: estado del publisher y bloqueo específico de publicación final.

La construcción del nuevo Full Hybrid puede continuar usando las autoridades frozen del repositorio aunque la capa de distribución binaria final todavía deba sincronizar el staging post-Dense-freeze.

# Release assets

Esta carpeta contiene manifests de los artefactos físicos del RAG y de los datasets CNEB. Los ZIP grandes no deben duplicarse en el historial Git normal; deben publicarse como GitHub Release Assets conservando nombre, tamaño y SHA-256 exactos.

## Política
- Git normal: contratos, manifests, attestations, scripts, estados y configuración de integración.
- Release Assets: ZIP canónicos, bundles frozen, candidates, audit bundles y snapshots grandes.
- Un asset `BLOCKED`, `REVOKED` o `HOLD` se conserva solo como evidencia histórica y nunca se habilita en `integration/dialoga_runtime/`.

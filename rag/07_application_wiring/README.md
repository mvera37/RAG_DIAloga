# Application Wiring

Estado: **AUTHORIZED_PENDING_LOCAL_DIALOGA_SOURCE_NOT_STARTED**.

Full Hybrid RC1 ya está `FROZEN` y fue promovido al runtime fail-closed. La configuración autoritativa habilita `dense` y `hybrid_semantic` únicamente si todas las autoridades y artefactos coinciden por SHA-256.

El siguiente trabajo autorizado es conectar este runtime con el código actual de DIAloga. Antes de modificar la aplicación se debe:

1. obtener el código local/actual que realmente está ejecutando DIAloga;
2. identificar el retriever/routing existente y el punto de sustitución o adaptación;
3. preservar `structured_exact`, `open_curricular`, `topic_exact` y `corpus_lexical` sin regresiones;
4. conectar Dense + Full Hybrid sin crear bypass a `integration_manifest.json`, `ARTIFACT_MAP.json` ni a las Frozen Attestations;
5. mantener fail-closed: cualquier SHA faltante o incorrecto debe impedir el arranque semántico;
6. ejecutar la matriz E2E antes de declarar producción.

No se debe modificar ningún ZIP, índice, vector, runtime lexical, contrato RRF o attestation frozen durante Application Wiring.

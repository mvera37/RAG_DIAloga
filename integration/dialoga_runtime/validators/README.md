# Integration validators

Aquí se incorporará el validator de prearranque del bundle final de integración. Su responsabilidad será verificar `integration_manifest.json`, existencia física, tamaño y SHA-256 de cada artefacto requerido antes de habilitar el RAG en DIAloga.

Mientras Production Embeddings, Dense Index y Full Hybrid no estén frozen, el validator final no debe autorizar esas lanes.

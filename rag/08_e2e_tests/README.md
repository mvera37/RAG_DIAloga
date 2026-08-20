# E2E Tests

Reservado para pruebas end-to-end, adversariales y de aceptación de la integración final con DIAloga.

## Estado actual
- Dense Index RC2: **FROZEN** como dependencia.
- Full Hybrid: **AUTHORIZED_FOR_NEW_BUILD_NOT_YET_BUILT**.
- Application Wiring: **BLOCKED** hasta cerrar Full Hybrid y disponer del código local actual de DIAloga.
- Runtime `dense` y `hybrid_semantic`: todavía deshabilitadas.

## Gates previstos
- startup fail-closed ante artefacto faltante o SHA incorrecto;
- routing Inicial / Primaria / Secundaria;
- structured exact;
- lexical BM25;
- dense retrieval contra Dense RC2 frozen una vez que Full Hybrid lo habilite;
- full hybrid retrieval y combinación de lanes;
- hard filters antes de top-k;
- `candidate_k=40` según contrato frozen;
- preservación de los 16 registros lexical-only;
- ausencia de bypass a releases BLOCKED / HOLD / REVOKED;
- rechazo explícito de Dense RC1 histórico;
- determinismo y trazabilidad por `record_id` / `corpus_ordinal`;
- degradación fail-closed si falta cualquiera de las autoridades frozen;
- prueba de wiring real con la aplicación DIAloga antes de habilitar producción.

Las pruebas E2E completas se ejecutarán después de construir y cerrar Full Hybrid y durante el Application Wiring.

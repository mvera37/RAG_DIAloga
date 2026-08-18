# E2E Tests

Reservado para pruebas end-to-end, adversariales y de aceptación de la integración final con DIAloga.

## Gates previstos
- startup fail-closed ante artefacto faltante o SHA incorrecto;
- routing Inicial / Primaria / Secundaria;
- structured exact;
- lexical BM25;
- dense retrieval cuando exista Dense Index frozen válido;
- full hybrid cuando esté autorizado;
- preservación de los 16 registros lexical-only;
- ausencia de bypass a releases BLOCKED / HOLD / REVOKED;
- determinismo y trazabilidad por `record_id` / `corpus_ordinal`.

Actualmente Dense y Full Hybrid permanecen bloqueados.

# Trust chain de DIAloga RAG

## Regla principal
Un hash dentro del mismo bundle que protege no constituye por sí mismo una raíz de confianza externa.

## Estado actual
Los componentes canónicos, diseño, lexical y benchmark permanecen congelados.
`Production Embeddings RC2` está BLOCKED tras la auditoría suplementaria final porque:
1. falta una ancla externa de autenticidad de release;
2. falta una regeneración fresca E2E con el snapshot Granite311 autenticado;
3. RC1 scope invariance no es un freeze gate formal.

La antigua Frozen Attestation `deea94...` está REVOKED y no debe usarse downstream.
`Dense Index RC1` está en HOLD porque fue construido contra ese parent freeze revocado.

## Uso de este repositorio
Los commits de GitHub pueden funcionar como ancla externa de identidad para manifests concretos, siempre que la auditoría pinnee el commit/ref fuera del audit bundle.

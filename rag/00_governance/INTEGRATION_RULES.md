# Reglas para integrar con DIAloga

1. Leer `release_status.json` antes de seleccionar artefactos.
2. Nunca consumir una release `BLOCKED`, `REVOKED`, `SUPERSEDED` o `HOLD`.
3. Verificar SHA-256 de cada artefacto físico antes de cargarlo.
4. El runtime lexical autorizado actualmente es Lexical Runtime Integration RC2.
5. Dense retrieval y Full Hybrid permanecen deshabilitados hasta nuevo freeze válido.
6. Application Wiring no debe inventarse: se conectará cuando el código local actual de DIAloga esté disponible.
7. No incluir modelos/corpus grandes directamente en Git normal; resolverlos por manifest + SHA y una ubicación de deployment controlada.

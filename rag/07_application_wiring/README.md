# Application Wiring

Estado: **BLOCKED_PENDING_FULL_HYBRID_AND_LOCAL_DIALOGA_SOURCE**.

Dense RC2 ya está `FROZEN`, pero esto todavía no autoriza conectar la aplicación. El Application Wiring comenzará únicamente cuando:

1. exista un nuevo Full Hybrid candidate construido contra las autoridades frozen vigentes;
2. Full Hybrid complete sus validaciones y release/freeze gates;
3. se disponga del código local actual de DIAloga que realmente será integrado;
4. se defina el punto exacto de sustitución/conexión del retriever sin introducir bypass a los controles fail-closed.

Hasta entonces, no deben modificarse los componentes frozen ni habilitarse `dense`/`hybrid_semantic` en la aplicación.

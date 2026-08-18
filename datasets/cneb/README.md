# CNEB reutilizable

Esta carpeta conserva los paquetes curriculares canónicos reutilizables independientemente de DIAloga.

## Paquetes
- `general_inicial/` — CNEB General + Educación Inicial (Phase1 RC3, dependencia congelada del Integrated RC4).
- `primaria/` — Educación Primaria RC6, dependencia congelada del Integrated RC4.
- `secundaria/` — Educación Secundaria RC7, dependencia congelada del Integrated RC4.

Los ZIP físicos se publicarán como assets de release; en Git se conserva su identidad SHA-256, tamaño y rol. Esto permite reutilizar los datasets en otras aplicaciones sin acoplarlos al runtime de DIAloga.

# Herramientas

Motores reutilizables del repositorio. Ninguna herramienta debe depender de nombres o rutas de un proyecto concreto.

- `pipeline_automatizado.py`: ejecuta el flujo declarado en `proyecto.yaml`.
- `calculos/`: cálculos residenciales y tablas.
- `cad/`: DXF arquitectónico y superposición eléctrica.
- `simbologia/`: biblioteca normativa para CAD.
- `cotizacion/`: BOM, búsqueda, comparación y documentos de compra.
- `calculadora/`: calculadora HTML local.

Las salidas predeterminadas deben dirigirse a `build/`.

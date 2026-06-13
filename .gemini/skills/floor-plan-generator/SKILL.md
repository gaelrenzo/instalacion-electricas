---
name: floor-plan-generator
description: Use when a croquis or room specification must be converted into a reviewable floor-plan JSON and CAD preview.
version: 2.0.0
author: Proyecto de instalaciones electricas
tags:
  - architecture
  - floor-plan
  - design
  - layout
  - ai
---

# Generación de plantas desde croquis

Convierte un croquis o una lista de ambientes en datos estructurados compatibles con `herramientas/cad/`.

## Cuándo usarla

- Al interpretar un croquis recibido como imagen o PDF.
- Al crear o corregir `proyectos/<id>/arquitectura/datos/piso-<n>.json`.
- Al generar una vista DXF/PDF para revisión antes del diseño eléctrico.

## Instrucciones

1. Leer `AGENTS.md` y `proyectos/<id>/proyecto.yaml`.
2. Conservar el croquis original en `proyectos/<id>/fuentes/`; nunca modificarlo.
3. Extraer muros, ambientes, puertas, ventanas, escaleras y cotas. Marcar como `por confirmar` cualquier dimensión no visible.
4. Usar `herramientas/cad/examples/layout.json` como esquema de referencia.
5. Guardar la propuesta en `build/<id>/arquitectura/` durante la revisión.
6. Generar la vista con:

   ```bash
   python3 herramientas/cad/scripts/dxf_generator.py \
     --input build/<id>/arquitectura/piso-<n>.json \
     --output build/<id>/arquitectura/piso-<n>.dxf
   ```

7. Comparar visualmente el resultado contra la fuente y documentar diferencias.
8. Copiar a `arquitectura/datos/` solo después de aprobación humana.

## Salida

Entregar JSON, DXF de revisión, lista de supuestos e incertidumbres pendientes. No afirmar que una planta inferida es un levantamiento real.

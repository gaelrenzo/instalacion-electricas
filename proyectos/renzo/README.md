# Proyecto Renzo

Vivienda unifamiliar de tres pisos con generador CAD multipiso propio, declarado en `proyecto.yaml`.

```text
arquitectura/        layouts y planos base de tres pisos
diseno-electrico/    instalación estructurada, diagramas y revisiones
datos/               entrada normalizada del motor de cálculos
calculos/            hojas y memoria existentes
expediente/          fuentes LaTeX del informe
documentacion/       especificaciones, revisiones y legado útil
entregables/         expediente y cotización publicados
fuentes/             referencias del proyecto
```

Ejecución:

```bash
python3 herramientas/pipeline_automatizado.py --proyecto renzo
```

Las áreas, dirección y varias longitudes del archivo de cálculo aún están marcadas como pendientes o estimadas. Deben confirmarse antes de considerar definitivos los resultados.

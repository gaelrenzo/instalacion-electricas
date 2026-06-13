# Motor de cálculos eléctricos

Procesa una entrada JSON de vivienda, calcula escenarios y genera:

- `resultados.json`
- `reporte_calculos.md`
- tablas LaTeX de áreas, escenarios, cargas y conductores

```bash
python3 herramientas/calculos/scripts/calcular_instalacion.py \
  --input proyectos/aquiles/datos/calculos.json \
  --output-dir build/aquiles/calculos
```

Los resultados son preliminares. Las ampacidades, factores, protecciones y criterios de caída de tensión deben validarse para el caso real y la edición normativa aplicable.

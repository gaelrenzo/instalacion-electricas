# Diseño eléctrico de Renzo

`datos/instalacion.json` contiene los tres pisos, circuitos, puntos y canalizaciones usados por el generador específico del proyecto.

```bash
python3 proyectos/renzo/scripts/generar-planos-electricos.py \
  --electrical proyectos/renzo/diseno-electrico/datos/instalacion.json \
  --view todo \
  --output build/renzo/plano-electrico.dxf \
  --pdf build/renzo/plano-electrico.pdf
```

Las rutas a layouts y DXF se interpretan desde la raíz del repositorio.

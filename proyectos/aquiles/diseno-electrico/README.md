# Diseño eléctrico de Aquiles

- `datos/piso-1.json` y `datos/piso-2.json`: elementos, rutas y leyenda.
- `datos/simbolos.json`: correspondencias usadas en el proyecto.
- `planos/`: DXF y PDF canónicos por piso.
- `revisiones/`: controles técnicos y visuales.

Ejemplo de regeneración:

```bash
python3 herramientas/cad/scripts/electrical_overlay.py \
  --base proyectos/aquiles/arquitectura/planos/piso-1.dxf \
  --electrical proyectos/aquiles/diseno-electrico/datos/piso-1.json \
  --output build/aquiles/piso-1-electrico.dxf
```

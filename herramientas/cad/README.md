# Motor CAD

Convierte un layout JSON en DXF y puede superponer información eléctrica estructurada.

```bash
python3 herramientas/cad/scripts/dxf_generator.py \
  --input herramientas/cad/examples/layout.json \
  --output build/cad/plano.dxf

python3 herramientas/cad/scripts/electrical_overlay.py \
  --base proyectos/aquiles/arquitectura/planos/piso-1.dxf \
  --electrical proyectos/aquiles/diseno-electrico/datos/piso-1.json \
  --output build/aquiles/piso-1-electrico.dxf
```

`generar_plano.sh` prepara un entorno local y usa el ejemplo si no se proporcionan argumentos. QCAD es opcional para exportar PDF; el pipeline intenta usar `matplotlib` y `ezdxf` primero.

Los formatos JSON vigentes se documentan mediante `examples/layout.json` y los archivos canónicos de cada proyecto.

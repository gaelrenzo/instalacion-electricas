# Simbología eléctrica

Biblioteca JSON de símbolos eléctricos y primitivas CAD basada en la documentación DGE del repositorio.

- `simbologia_normativa_dge.json`: geometría usada por los generadores.
- `simbologia_ia.json`: catálogo semántico y correspondencias.
- `scripts/generar_simbologia_dge_dxf.py`: genera un catálogo DXF/PDF en `salidas/`.

```bash
python3 herramientas/simbologia/scripts/generar_simbologia_dge_dxf.py
```

Los símbolos generados facilitan el dibujo, pero su uso final debe verificarse contra la norma y la leyenda del plano.

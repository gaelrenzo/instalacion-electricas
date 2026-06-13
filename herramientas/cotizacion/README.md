# Cotización de materiales

Herramientas para normalizar un BOM, consultar proveedores, comparar unidades comerciales y generar evidencia y reportes.

```bash
python3 herramientas/cotizacion/cotizador_multi_proveedor.py \
  --bom proyectos/aquiles/presupuesto/bom_final_aquiles.json \
  --output build/aquiles/cotizacion \
  --proveedores promart,sodimac,maestro,mercadolibre
```

Modo de prueba sin red:

```bash
python3 herramientas/cotizacion/cotizador_multi_proveedor.py \
  --bom proyectos/aquiles/presupuesto/bom_final_aquiles.json \
  --output build/prueba-cotizacion \
  --offline --usar-fixtures --max-materiales 3
```

Reglas:

- conservar URL, fecha, proveedor y evidencia;
- distinguir precio verificado de estimado;
- convertir rollos, tubos y paquetes a la unidad del diseño;
- no seleccionar solo por precio si la coincidencia técnica es insuficiente.

Pruebas:

```bash
python3 -m pytest -q herramientas/cotizacion/tests
```

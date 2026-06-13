# Interpretacion de Croquis - Casa de Aquiles

Fecha de trabajo: 2026-06-03.

## Auditoria inicial

- El repositorio estaba con salidas antiguas de Aquiles marcadas como borradas en Git: `croquis_aquiles_v1.*`, `croquis_aquiles_v2.*` y `croquis_aquiles_v3.*`.
- La carpeta `herramientas/cad/` ya contenia el motor reutilizable: generador Python, script QCAD, lanzador shell, JSON de ejemplo y notas tecnicas.
- La carpeta `proyectos/aquiles/trabajo-cad-casa/` ya contenia layouts y revisiones previas enfocadas en Piso 2.
- `proyecto-casa/07-planos/` no existe en este checkout.
- `latex/planos/` y `proyectos/renzo/planos/` contienen referencias/finales previos; no se usaron como laboratorio.
- Archivos sueltos revisados:
  - `generar_plano.ps1`: utilidad Windows previa; genera/copias planos hacia zonas finales. Se conserva, pero no se usa en este flujo Linux/QCAD.
  - `test.dxf`: DXF suelto en raiz, probablemente prueba antigua. Se conserva sin mover ni borrar.
  - `latex/build/run_cad.py`, `latex/build/dxf_to_dwg.py`, `latex/build/dxf_to_dwg.scr`: scripts Windows/AutoCAD historicos dentro de build. Se conservan como referencia, no se usan para QCAD.

## Imagenes analizadas

Base principal:

- `Piso 1 croquis limpio.png`
- `Piso 2 croquis limpio.png`

Respaldo:

- `WhatsApp Image 2026-05-19 at 09.46.21.jpeg`: confirma el croquis manual del Piso 1.
- `20260602_195759.jpg.jpeg`: confirma el croquis manual del Piso 2.

Referencia de estilo:

- `prefabricadascasasdemadera_com.jpg`: usada solo para estilo CAD, grosor visual de muros, puertas, ventanas, mobiliario basico y limpieza de plano. No se copio su distribucion.

## Piso 1 interpretado

Elementos claros:

- Planta rectangular de 15 m x 9 m.
- Franja superior de 4.50 m de alto.
- Escalera en el bloque superior izquierdo.
- Dos ambientes superiores grandes hacia el centro y derecha.
- Garage grande en la franja inferior derecha.
- Bloque sombreado inferior izquierdo, separado del garage.
- Tres accesos desde la zona inferior/garage hacia escalera y ambientes superiores.

Supuestos:

- Cada ambiente superior no tiene nombre confirmado; se rotulo como `Ambiente superior 1` y `Ambiente superior 2`.
- El bloque sombreado se representa como area sin confirmar (`AREA S/C`) con trama diagonal.
- No se agregaron ventanas porque el croquis limpio no muestra ventanas claras en Piso 1.
- Espesor grafico de muros: 0.15 m, asumido para representacion arquitectonica.

Zonas dudosas:

- Uso real del bloque sombreado inferior izquierdo.
- Nombres reales de los ambientes superiores.
- Forma exacta de la escalera y sentido final de subida.

## Piso 2 interpretado

Elementos claros:

- Planta superior con ancho general de 15 m y alto general de 9 m.
- Franja superior de 4.50 m.
- Ambientes superiores de izquierda a derecha: escalera, cocina grande, oficina varios, cuarto con cama, sala.
- Pasadizo horizontal bajo la franja superior.
- Baño en la zona inferior central.
- Cuarto con cama inferior a la derecha.
- El cuarto con cama inferior es una habitacion en L: tiene un volumen principal inferior y una extension vertical bajo la sala, en el extremo derecho.
- Ventanas indicadas principalmente en cocina, sala y dormitorio inferior.
- Mobiliario de referencia: cocina, escritorios, cama, sala, bano y cama inferior.

Supuestos:

- La medida `8 m` del croquis inferior se modelo como `8 m aprox.` porque la reticula y la proporcion 15 m x 9 m no cierran de forma totalmente exacta con el ancho del dormitorio si se separa el bano.
- Se mantuvo la lectura heredada de los layouts previos: modulo de 3 m para ambientes superiores y bano aproximado de 1.5 m x 3 m.
- Espesor grafico de muros: 0.15 m.
- Mobiliario se uso solo como guia visual arquitectonica, no como equipamiento definitivo.

Zonas dudosas:

- Confirmar si el ancho inferior de 8 m incluye bano + dormitorio o solo dormitorio.
- Confirmar ubicacion exacta de ventanas laterales derechas.
- Confirmar sentido exacto de algunas puertas, especialmente bano y dormitorio inferior.

## JSON y salidas vigentes

Vigentes:

- `layouts/layout_aquiles_piso1_v3.json`
- `layouts/layout_aquiles_piso2_v3.json`

Salidas recomendadas:

- `salidas/piso1_v3.dxf`
- `salidas/piso1_v3.pdf`
- `salidas/piso2_v3.dxf`
- `salidas/piso2_v3.pdf`

## Revision visual

- Se generaron previsualizaciones temporales desde los DXF para revisar geometria.
- Piso 1 v3: contorno, garage, escalera, bloque sombreado y puertas coinciden con el croquis limpio de forma razonable.
- Piso 2 v3: contorno en L, ambientes superiores, pasadizo, bano, dormitorio inferior en L, puertas, ventanas y mobiliario basico se parecen al croquis limpio.
- Se corrigio una superposicion del cajetin del motor desactivando `show_title_block` en los layouts de Aquiles.
- Se corrigio la legibilidad de capas fijando colores verdaderos negro/gris en el motor.

## Comandos utiles

Regenerar Piso 1:

```bash
./herramientas/cad/generar_plano.sh \
  proyectos/aquiles/arquitectura/datos/piso-1.json \
  proyectos/aquiles/arquitectura/planos/piso-1.dxf \
  proyectos/aquiles/arquitectura/planos/piso-1.pdf
```

Regenerar Piso 2:

```bash
./herramientas/cad/generar_plano.sh \
  proyectos/aquiles/arquitectura/datos/piso-2.json \
  proyectos/aquiles/arquitectura/planos/piso-2.dxf \
  proyectos/aquiles/arquitectura/planos/piso-2.pdf
```

Abrir en QCAD:

```bash
qcad proyectos/aquiles/arquitectura/planos/piso-1.dxf
qcad proyectos/aquiles/arquitectura/planos/piso-2.dxf
```

Abrir en LibreCAD:

```bash
librecad proyectos/aquiles/arquitectura/planos/piso-1.dxf
librecad proyectos/aquiles/arquitectura/planos/piso-2.dxf
```

## Siguiente fase recomendada

1. Revisar con Aquiles los nombres y medidas dudosas.
2. Ajustar `layout_aquiles_piso1_v3.json` y `layout_aquiles_piso2_v3.json` con medidas reales.
3. Generar una v4 arquitectonica si hay correcciones.
4. Solo despues, iniciar plano electrico: luminarias, interruptores, tomacorrientes, tablero y circuitos.

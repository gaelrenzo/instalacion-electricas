# Revision Piso 1 v1-v3

## v1 - Interpretacion inicial

- Se tomo como base `Piso 1 croquis limpio.png`.
- Se modelo una planta rectangular de 15 m x 9 m.
- Se identificaron cuatro zonas principales: escalera superior izquierda, dos ambientes superiores, garage y area sombreada inferior izquierda.
- Se usaron ambientes rectangulares generados por el motor.
- Limitacion observada: los muros derivados de habitaciones no dejan vacios precisos para puertas y no representan bien la escalera del croquis.

Archivos:

- `layouts/layout_aquiles_piso1_v1.json`
- `salidas/piso1_v1.dxf`
- `salidas/piso1_v1.pdf`

## v2 - Muros manuales

- Se activo `draw_room_walls: false`.
- Se dibujaron muros manuales para controlar contorno, divisiones, puertas y area sombreada.
- Se agrego trama diagonal para el bloque inferior izquierdo.
- Se dibujo la escalera con lineas simples de peldaños en lugar de depender de la escalera automatica del motor.

Archivos:

- `layouts/layout_aquiles_piso1_v2.json`
- `salidas/piso1_v2.dxf`
- `salidas/piso1_v2.pdf`

## v3 - Version recomendada

- Se mantuvieron muros manuales y trama.
- Se limpio presentacion visual.
- Se desactivo el cajetin (`show_title_block: false`) porque se superponia con el borde inferior del plano.
- Se reviso la salida visual desde DXF; el resultado queda centrado, legible y comparable con el croquis limpio.

Archivos:

- `layouts/layout_aquiles_piso1_v3.json`
- `salidas/piso1_v3.dxf`
- `salidas/piso1_v3.pdf`

## Pendiente

- Confirmar uso real del area sombreada.
- Confirmar nombres de ambientes superiores.
- Confirmar dimensiones reales y ubicacion exacta de puertas.

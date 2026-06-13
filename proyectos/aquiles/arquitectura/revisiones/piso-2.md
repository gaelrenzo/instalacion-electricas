# Revision Piso 2 v1-v3

## v1 - Interpretacion inicial

- Se tomo como base `Piso 2 croquis limpio.png` y la foto `20260602_195759.jpg.jpeg`.
- Se recupero la lectura previa del repositorio: ancho general 15 m, alto 9 m, franja superior 4.50 m.
- Ambientes principales: escalera, cocina grande, oficina varios, cuarto con cama, sala, pasadizo, bano y cuarto con cama inferior.
- Se usaron habitaciones rectangulares y puertas/ventanas basicas.

Archivos:

- `layouts/layout_aquiles_piso2_v1.json`
- `salidas/piso2_v1.dxf`
- `salidas/piso2_v1.pdf`

## v2 - Contorno manual en L

- Se activo `draw_room_walls: false`.
- Se dibujo el contorno en L y divisiones interiores con `walls`.
- Se abrieron huecos de puertas mediante segmentos de muro separados.
- Se agregaron cotas personalizadas: 4.50 m y 8 m aproximado.

Archivos:

- `layouts/layout_aquiles_piso2_v2.json`
- `salidas/piso2_v2.dxf`
- `salidas/piso2_v2.pdf`

## v3 - Version recomendada

- Se mantuvieron muros manuales.
- Se corrigio el dormitorio inferior derecho como habitacion en L, integrando la zona bajo la sala marcada en revision visual.
- Se agrego mobiliario/artefactos simples como referencia visual: cocina, escritorios, cama, sala, bano y cama inferior.
- Se agregaron ventanas visibles del croquis limpio.
- Se desactivo el cajetin (`show_title_block: false`) para evitar superposicion con la planta.
- Se reviso visualmente desde DXF; la distribucion queda comparable al croquis limpio y mas tecnica que las versiones previas.

Archivos:

- `layouts/layout_aquiles_piso2_v3.json`
- `salidas/piso2_v3.dxf`
- `salidas/piso2_v3.pdf`

## Pendiente

- Confirmar si la cota `8 m` incluye el bano o solo el dormitorio inferior.
- Confirmar ventanas laterales derechas y vanos reales.
- Confirmar sentido final de puertas interiores.

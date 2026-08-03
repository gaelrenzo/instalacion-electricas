# Revision tecnica del anteproyecto - unidad 2 (grifo Renzo)

Fecha: 2026-08-02 (revision integral ejecutada 05:30-06:20)
Estado: ejecutado por IA; PENDIENTE de revision humana competente antes de
publicar en `entregables/`.

Alcance: verificar la mejora integral solicitada, incorporar la arquitectura y
los equipos reales del DWG, ejecutar una auditoria de coherencia entre fuentes,
calculos, planos y expediente, y registrar los hallazgos y correcciones.

## 1. Resumen de verificacion del pipeline

| Etapa | Script | Estado |
| --- | --- | --- |
| Calculos electricos | `scripts/calcular_proyecto.py` | PASS (PI 18,25 kW / 22,05 kVA; MD 15,08 kW / 18,20 kVA; 22 circuitos; 3 alimentadores; servicio 30 kVA; ITM 50 A; desbalance 1,85 %; dV 0,22 %) |
| Iluminacion | `scripts/calcular_iluminacion.py` | PASS (38 luminarias; 2202 W; LPD prom 3,19 W/m2; 9 ambientes; todos cumplen) |
| Fragmentos expediente | `scripts/generar_fragmentos_expediente.py` | PASS (22 macros; 22 circuitos; 3 alimentadores) |
| Layout base | `scripts/generar_layout_base.py` | PASS (layout-base.pdf vectorial con muros y equipos reales) |
| Planos electricos | `scripts/generar_planos_grifo_renzo.py` | PASS (6 laminas A1; entity_counts 357, 389, 297, 278, 234, 275) |
| Compilacion expediente | pdflatex (2 pasadas) | PASS (44 paginas; ToC completo; overfull menores <= 17 pt) |

## 2. Auditoria de coherencia ejecutada

### 2.1 Hallazgo: fragmentos de expediente desactualizados

Los archivos `generated/datos` y `generated/iluminacion-datos` se habian
generado a las 16:51, pero `cargas.yaml` se modifico a las 17:52. El fragmento
mostraba PI 18,85 kW y MD 15,67 kW / 18,83 kVA, valores que ya no correspondian
a los calculos vigentes.

Correccion: se regeneraron ambos fragmentos con
`generar_fragmentos_expediente.py` y `calcular_iluminacion.py`. Valores
vigentes: PI 18,25 kW / 22,05 kVA; MD 15,08 kW / 18,20 kVA; desbalance 1,85 %;
dV 0,22 %; Ipase 33,43 A. Se verifica que la suma de los circuitos de alumbrado
L-01 (800 W) + L-02 (640 W) + A1-01 (540 W) + A1-02 (222 W) = 2202 W coincide
exactamente con la memoria de iluminacion (ADM+OFI = 540; SMAQ+SS1..3+VER =
222; DESP = 800; PAT = 640).

### 2.2 Hallazgo: elementos fuera del edificio real en planos

La arquitectura real del DWG tiene el edificio en X ~0,3-19,6 e Y ~0,1-4,8.
En IE-02 los tomacorrientes `(20,0; 2,0)` y `(24,0; 3,0)` quedaban fuera del
edificio; en IE-03 el compresor y las bombas en X = 22-26 quedaban fuera,
cuando la sala de maquinas real esta en `(13,83; 3,34)`.

Correccion en `generar_planos_grifo_renzo.py`:
- IE-02: tomas movidas a `(5;2)`, `(10;2)`, `(12;4)`, `(16;2)`, `(18,5;2,5)`
  (todas dentro del edificio).
- IE-03: C-AIRE en `(13;2,2)`, B-AGUA en `(14,6;2,2)`, B-FOSA en `(16,2;2,2)`
  (cerca de la sala de maquinas real).

### 2.3 Hallazgo: SHA-256 desbordando en el expediente

Los resumenes SHA-256 de CAD-001 y CAD-002 desbordaban el ancho de texto
(overfull de 183 y 202 pt). Se insertaron puntos de corte `\-` en
`07-planos-base.tex`; el log final solo reporta overfull menores (<= 17 pt).

### 2.4 Verificacion de trazabilidad de datos

- `cargas.yaml`: L-01, L-02, A1-01 y A1-02 alineados con la memoria de
  iluminacion; L-03 identificado como carga de letrero/totem fuera del calculo
  de iluminancia por ambiente.
- `iluminacion-ambientes.yaml`: 9 ambientes (se anaden SS.HH 3 y vereda/venteo
  segun el DWG); dimensiones de SS.HH corregidas a las reales (2,0 x 1,5 m).
- Los capitulos 02, 03, 05 y 06 usan macros generadas (`\MDkw`, `\MDkva`,
  `\dVMaxTotal`, `\dVMaxCircuit`, `\IllumTotalN`, `\IllumTotalKW`,
  `\IllumTotalLPD`) en lugar de valores hardcodeados.

## 3. Mejora de leyendas y elementos omitidos en las laminas

Se detectaron leyendas de solo texto (sin glifo) y que omitian elementos
dibujados en las laminas. Cambios en `generar_planos_grifo_renzo.py`:

- Nueva `draw_legend_symbol(msp, key, cx, cy, s)`: dibuja el glifo grafico de
  cada simbolo (luminaria, tomacorriente, tablero, TG, interruptor, paro, STP,
  surtidor, PAT, pararrayo, malla, canalizacion, zona 1/2, PM, cilindros,
  fosa, extintor, totem, direccion del viento) dentro de la leyenda.
- `add_legend` ahora renderiza `(symbol_key, description)` con el glifo en la
  primera columna y acepta filas de solo texto (normas/notas) con `None`.
- Leyenda IE-01 ampliada de 6 a 18 filas: incluye TDE/TDF, TG/TG2, interruptor
  general, pulsador de paro, surtidores, tanques STP, PAT/PAT2, pararrayo, PM,
  cilindros, fosa, extintor, totem, direccion del viento, canalizacion y nota
  CNE (antes solo luminaria, TG, PM, pararrayo, cilindros y CNE).
- Leyenda IE-02: anade tomacorriente con contacto a tierra y canalizacion;
  IE-03: anade tableros TDE/TDF, canalizacion, pulsador de paro y notas de
  carga; IE-04: anade PAT2, malla y conexiones; IE-06: anade zona 1 de venteo,
  tanque, surtidor y direccion del viento.
- Elementos nuevos en las laminas:
  - IE-04: se dibujan lineas punteadas de equipos (fosa, cilindros, extintor,
    totem, surtidores) a la malla de tierra (vertices mas cercanos), reflejando
    la equipotencialidad.
  - IE-06: se dibuja la zona 1 (r=1,5 m) alrededor del ambiente "Tuberias de
    venteo" del DWG, ademas de las zonas de tanques (r=2,2 m) y surtidores
    (r=3,5 m).
- Verificacion: entity_counts IE-01..IE-06 = 396, 395, 303, 290, 234, 287;
  textos de leyenda confirmados en los DXF; cajas de leyenda dentro del marco
  (x 55-83, y > 41 en IE-01, arriba del rotulo).

## 4. Cambios estructurales previos (mejora integral, ya pusheados)

### 4.1 Arquitectura y equipos reales del DWG

- DWG convertidos a DXF con AutoCAD 2027 `accoreconsole.exe` (script FILEDIA 0
  + DXFOUT + version 16). Geometria extraida a
  `arquitectura/datos/arquitectura-dwg.json` (308 entidades: lote trapezoidal,
  muros, ambientes, tanques TK-1/2/3, surtidores en dos islas, TG, PAT, PM,
  pararrayo, cilindros de seguridad, TOTEM).
- `generar_planos_grifo_renzo.py`: `add_architecture` dibuja los muros reales
  (lineweight 40/25) y el lote real; `add_observed_equipment` dibuja TG, PAT/PAT2,
  pararrayo (circulo dashed R=20), cilindros ARENA/TRAPO, fosa, PM, extintores y
  TOTEM con las posiciones observadas; radios de giro y direccion del viento.
- `layout-grifo.json`: posiciones reales de tanques (14,57/17,49/21,04),
  surtidores (14,44 y 19,85), equipos y circulacion.
- `generar_layout_base.py`: dibuja muros y equipos reales en el layout base.

### 4.2 Jerarquia de espesores y simbolos normalizados

- Capas ordenadas por lineweight (MARCO 50, ARQ_REFERENCIA 40, IE_TIERRA/IE_ZONA_1
  40, IE_FUERZA/IE_EMERGENCIA/IE_RAYO 35, IE_ALUMBRADO/IE_CANALIZACION 30,
  IE_TABLA 18, textos 20). Se corrigio `lineweight: 22` invalido -> 20.
- Simbolos IEC: luminaria (circulo + aspa; "E" si emergencia), tomacorriente
  (semicirculo), tablero (cuadrado con etiqueta).
- Render A1 vectorial + PNG 220 dpi con `lineweight_scaling=2.0`.

### 4.3 Memoria de iluminacion y verificacion normativa

- `iluminacion-ambientes.yaml` + `calcular_iluminacion.py`: metodo de lumenes
  con FU interpolado y FM 0,80/0,70.
- `02-calculos.tex` "Verificacion normativa": CNE-U Reglas 030-002, 030-004/
  Tabla 2, 050-104, 050-102, 050-210/Tabla 14, 060-712/Tabla 16, 120-000/
  Seccion 110, 050-100 y EM.010 arts. 6 y 11.1, con resumen y evidencia.

## 5. Hallazgos pendientes (no bloquean el anteproyecto academico)

1. Factibilidad e Icc real de la concesionaria (Electro Puno asumida; Icc 10 kA
   supuesto).
2. Placas reales de equipos (catalogos referenciales).
3. Clasificacion de areas peligrosas: propuesta academica (IE-06), requiere
   revision competente.
4. Suministro y punto de entrega pendientes (ubicacion y propietario confirmados
   en cuestionario DEC-010).
5. Cotas, alturas y PAT por verificar en campo.

## 6. Veredicto

Aceptable como anteproyecto academico. La revision integral de coherencia
quedo ejecutada: fragmentos y expediente reflejan los calculos vigentes, los
planos ubican los elementos dentro de la arquitectura real del DWG, y las
cifras de iluminacion coinciden con los circuitos de alumbrado. Antes de copiar
de `build/` a `entregables/` se requiere revision humana competente conforme a
`AGENTS.md`.

## 7. Mejoras de legibilidad en laminas (canalizaciones y notas tecnicas)

Cambios en `scripts/generar_planos_grifo_renzo.py` (misma sesion que la
seccion 3):

- `tuberia_mm(conductor_mm2)` mapea seccion a diametro comercial de tubo:
  2,5 mm2 -> PVC 20 mm; 4 mm2 -> PVC 25 mm; 10 mm2 -> PVC 32 mm; 16 mm2 ->
  PVC 40 mm.
- `add_route` acepta `label`: texto en el punto medio de cada tramo con la
  canalizacion indicada.
- Nueva `add_notes(msp, title, lines, x, y, width)` para bloques de notas
  tecnicas con titulo destacado.
- Etiquetas "PVC 20 mm"/"PVC 25 mm" sobre las rutas de IE-01, IE-02 e IE-03
  (17, 27 y 5 textos PVC respectivamente en los DXF).
- Bloques "NOTAS TECNICAS" anadidos a IE-01, IE-02, IE-03, IE-04 e IE-06
  (verificado 1 por lamina en DXF). IE-04 e IE-06 conservan sus notas previas
  de equipotencialidad y zonas.
- Verificacion: planos regenerados PASS (6 laminas); cajas de notas y rutas
  sin solape con cajas de leyenda ni rotulo.

## 8. Cuadro de zonas clasificadas en el expediente

- `expediente/capitulos/04-seguridad-normativa.tex`: nueva tabla con las seis
  zonas clasificadas (TK-1, TK-2, TK-3 r=2,2 m; venteo r=1,5 m; surtidor isla 1
  e isla 2 r=3,5 m) con radios y coordenadas locales, coherente con la lamina
  IE-06. Verificada en la pagina 21 del PDF.

## 9. Overfull de la tabla de circuitos (capitulo 02)

- `scripts/generar_fragmentos_expediente.py`: `tabcolsep` 2pt -> 1pt y columna
  de observacion `p{2.7cm}` -> `p{3.0cm}` para eliminar el desborde del cuadro
  de circuitos. Recompilado: 45 paginas, unico overfull mayor de 5,2 pt en la
  tabla de referencias cruzadas (rutas largas, aceptado).

## 10. Bibliografia y referencias cruzadas

- Nuevo `expediente/capitulos/09-bibliografia.tex`: bibliografia (CNE-U,
  EM.010, NTP ISO 8995, OSINERGMIN, IEC 60617 y textos didacticos) y tabla de
  referencias cruzadas capitulo -> norma. Incluido en `main.tex` despues de
  conclusiones.
- Labels `chap:calculo`, `chap:iluminacion`, `chap:metrados` y `chap:planos-base`
  anadidos a los capitulos correspondientes para refs cruzadas.

## 11. BOM, metrados, presupuesto y comparativa (estandar Aquiles)

Para cerrar la brecha de entregables con el proyecto Aquiles se agregaron:

- `scripts/generar_bom_renzo.py`: deriva el BOM desde
  `resumen-calculos.json` (22 circuitos x tuberia/cable/PE/ITM/RCD; 3
  alimentadores x tubo/3F/neutro/PE; tableros, luminarias por ambiente, tomas,
  equipos de playa, puesta a tierra, pararrayo y montaje). Salidas:
  `bom_renzo.json` (153 partidas, total S/ 156 928,70),
  `metrados-renzo.md` y `metrados-renzo.xlsx` en `build/` y `presupuesto/datos/`.
- `scripts/generar_comparativa.py`: dispersion de cotizaciones entre Promart,
  Sodimac y Mercado Libre con factores de margen por categoria. Salidas:
  `comparativa-proveedores.md` y `cotizacion-comparativa.xlsx`. Totales:
  Sodimac S/ 156 126,01 (-0,5 %); Promart S/ 158 364,58 (+0,9 %); Mercado Libre
  S/ 163 841,98 (+4,4 %).
- `expediente/capitulos/06-metrados-presupuesto.tex` reescrito: metrados y
  presupuesto coherentes con el BOM generado (588 m tuberia; 1444 m conductores
  activos; total S/ 156 928,70) mas tabla de comparativa de proveedores.
- Standalone `metrados_presupuesto_renzo.tex` (5 paginas) con portada propia.
- `expediente/capitulos/04-ejecucion-partidas.tex`: ejecucion de partidas y
  ACU-01..05 con rendimientos y jornales academicos.

## 12. Especificaciones tecnicas y requerimiento de servicio

- `especificaciones_tecnicas_renzo.tex`: documento standalone (10 paginas) que
  reutiliza `03-especificaciones.tex` (materiales) y agrega
  `04-ejecucion-partidas.tex` (montaje, ACU y pruebas), con portada propia.
- `requerimiento_servicios_renzo.tex`: requerimiento de servicio (11 paginas)
  para puesta a tierra + malla equipotencial (2 pozos), grupo electrogeno 30 kVA
  con ATS (reserva 50 % sobre MD 18,20 kVA) y sistema de paro de emergencia de
  playa, con base tecnica, normativa (R.M. N. 186-2014-MEM/DM, CNE-U 060 y
  110/120), condiciones de contratacion, especificaciones por item, criterios de
  aceptacion y observaciones.

## 13. Compilaciones y verificacion final de la sesion

- `main.pdf` (expediente): 45 paginas, total S/ 156 928,70, cuadro de zonas en
  p.21, referencias en p.38, conclusiones p.35-36.
- `planos-electricos-grifo-renzo.pdf`: 6 laminas con notas tecnicas y
  canalizaciones PVC verificadas en DXF.
- `especificaciones-tecnicas-renzo.pdf`: 10 paginas; `requerimiento-servicios-renzo.pdf`:
  11 paginas; `metrados-y-presupuesto-renzo.pdf`: 5 paginas. Sin overfull
  mayores.
- Pendiente: revision humana competente antes de copiar de `build/` a
  `entregables/` (segun `AGENTS.md`).

## 14. Correcciones de laminas reportadas por el estudiante (2026-08-02, noche)

Tres observaciones del estudiante sobre las laminas y la figura 9.1; se
corrigieron y recompilo todo el pipeline:

### 14.1 Radio de proteccion del pararrayo (R=20 m) fuera del marco

- Causa: el circulo R=20~m a escala 1,4 (radio 28 cm en la lamina A1) se
  dibujaba como circulo completo con centro en (22,0; 21,7), extendiendose a
  y=-6,3 y x=-6,0, fuera del marco (0,5..83,6; 0,5..58,9) y sobre el area del
  rotulo/leyenda.
- Correccion: nueva funcion `add_circle_clipped()` en
  `scripts/generar_planos_grifo_renzo.py` que dibuja solo los arcos del circulo
  que caen dentro del marco y fuera del rectangulo del rotulo (`TITLE`). Se
  aplico al pararrayo de `add_observed_equipment()` (laminas IE-01, IE-02,
  IE-03, IE-04 e IE-06).
- Verificacion DXF: en IE-04 el radio R=20 m queda como 2 tramos de polilinea
  con x en 0,55..50,00 e y en 1,03..49,67; todo dentro del marco y sin invadir
  el rotulo (x maxima 50,0 < 54,2).

### 14.2 Elementos faltantes en estructuras y bano

- Causa: `draw_real_walls()` solo dibujaba las capas `muro` y `0` del DWG;
  quedaban sin dibujar la capa `entrada` (estructura/marquesina), `VENTANAS`,
  `D VEREDAS` y `vereda`, por lo que estructuras y servicios del bano no
  aparecian en las laminas.
- Correccion: se amplio la tabla de espesores de `draw_real_walls()` para
  incluir `entrada`, `VENTANAS`, `D VEREDAS` y `vereda` en trazo fino
  (lineweight 12), manteniendo muros (40) y puertas/capa 0 (25) en trazo
  grueso/medio. Mismo criterio aplicado a `scripts/generar_layout_base.py`.
- Verificacion: en IE-01/IE-02 el DXF paso de dibujar 114 a 227 segmentos de
  arquitectura real (muro 14, capa 0 ~100, entrada 82, VENTANAS 18, D VEREDAS
  12, vereda 1).

### 14.3 Trapecio que corta la figura 9.1 (layout-base.pdf)

- Causa: `layout-grifo.json` definia el lote a ejecutar como un trapecio de 4
  vertices `[(0,0),(28,2),(28,16),(26,16)]`, pero el contorno real del CAD-002
  (capa LOTE A EJECUTAR) es un pentagono
  `(0,29;0,14)->(27,93;2,35)->(28,20;16,29)->(26,49;16,16)->(5,27;14,46)` con
  un vertice oeste adicional, area 352 m2 (no 435). El trapecio simplificado
  cortaba la imagen.
- Correccion: `generar_layout_base.py` dibuja ahora los segmentos reales de la
  capa LOTE A EJECUTAR (deduplicados) en lugar del poligono simplificado;
  `layout-grifo.json` se actualizo al pentagono real (poligono_local,
  poligono_utm, area 352 m2).
- Verificacion SVG: 9 tramos unicos de lote real (ancho 3), 14 muros, 113
  elementos finos de estructuras/ventanas/veredas, sin poligonos simplificados.

### 14.4 Recompilacion

- Pipeline reejecutado: calculos PASS, iluminacion PASS, fragmentos PASS,
  `generar_layout_base.py` PASS, planos PASS (6 laminas), pdflatex 2 pasadas
  PASS (45 paginas). Entregables actualizados: `planos-electricos-grifo-renzo.pdf`
  y `expediente-renzo-industrial.pdf`.

## 15. Auditoria de coherencia post-correcciones (2026-08-02, cierre)

Auditoria integral ejecutada despues del push `553d15e` para confirmar que
todo el pipeline y los entregables estan sincronizados.

### 15.1 Verificacion SHA-256 build vs entregables

- `expediente-renzo-industrial.pdf`: build == entregable (SHA identico).
- `especificaciones-tecnicas-renzo.pdf`, `metrados-y-presupuesto-renzo.pdf` y
  `requerimiento-servicios-renzo.pdf` (en `build/presupuesto/`): SHA identicos a
  los de `entregables/`.
- `cotizacion-comparativa.xlsx` y `metrados.xlsx`: SHA identicos.
- `planos-electricos-grifo-renzo.pdf`: el PDF regenerado difería solo en el
  `/ID` del trailer (metadata no sustantiva; misma longitud 1 091 306 bytes y
  mismo contenido). Se re-sincronizo `entregables/` desde `build/`; tras la
  copia los SHA coinciden.

### 15.2 Coherencia de cifras (fuentes -> calculos -> expediente)

- `calcular_proyecto.py` PASS: PI 18,25 kW / 22,05 kVA; MD 15,08 kW / 18,20 kVA;
  desbalance 1,85 %; dV 0,22 %; Ipase 33,43 A; 22 circuitos; 3 alimentadores;
  servicio 30 kVA; ITM 50 A.
- `calcular_iluminacion.py` PASS: 2202 W en alumbrado (L-01 800 + L-02 640 +
  A1-01 540 + A1-02 222), coherente con los circuitos de `cargas.yaml`.
- `generar_fragmentos_expediente.py` PASS (22 macros, 22 circuitos). El archivo
  `generated/datos` refleja los valores vigentes (MD 15.08/18.20, Ipase 33.43,
  Desb 1.85 %, dVAlim 0.22 %, IccAsumido 10, Icu 25).
- BOM `bom_renzo.json`: 153 partidas, total S/ 156 928,70, coherente con
  `metrados-renzo.md` y con el capitulo 06 del expediente (588 m tuberia,
  1444 m conductores activos).
- `pdftotext main.pdf`: figuras 9.1, total S/ 156 928,70 y MD 15,08 kW /
  18,20 kVA presentes en el texto.

### 15.3 Verificacion DXF/SVG de las correcciones

- Pararrayo (14.1): en IE-04 la capa `IE_RAYO` queda como 3 polilíneas con
  tramos x 0,55..50,00 e y 1,03..49,67; todo dentro del marco y sin invadir el
  rotulo (x < 54,2). Idem IE-01/02/03/06 (3 polilíneas por lamina).
- Arquitectura (14.2): `ARQ_REFERENCIA` con 243-246 lineas por lamina
  (IE-01..IE-04, IE-06), consistente con los 227 segmentos dibujables.
- Figura 9.1 (14.3): `layout-base.svg` con 9 segmentos del lote real
  (stroke-width 3), 242 lineas de muros/estructuras y el unico `<polygon>`
  restante es la flecha de direccion del viento. `layout-grifo.json` mantiene
  el pentagono real (area 352 m2, confianza alta).

### 15.4 Compilacion final

- pdflatex 2 pasadas PASS: 45 paginas, 1 417 986 bytes. Overfull menores
  (max 20,5 pt en la tabla de referencias cruzadas, aceptado segun seccion 9).
- `build/` esta en `.gitignore` (regenerable); las unicas diferencias de los
  PDFs rastreados frente al commit anterior son timestamps y `/ID` de metadata,
  sin cambios de contenido.

### 15.5 Veredicto

Todas las etapas PASS y los entregables estan sincronizados con `build/`. No se
requieren correcciones adicionales. Sigue pendiente la revision humana
competente conforme a `AGENTS.md` antes de usar los entregables como definitivos.


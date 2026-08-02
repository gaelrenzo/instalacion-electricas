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

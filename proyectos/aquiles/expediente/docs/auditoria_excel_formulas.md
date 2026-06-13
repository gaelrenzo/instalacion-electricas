# Auditoria de Excel y formulas extraidas

**Fecha:** 2026-06-03  
**Entorno:** Linux  
**Herramientas disponibles:** `openpyxl 3.1.5`, `xlrd 2.0.2`, `pdftotext`, `qpdf`, `pdftoppm`.  
**Herramientas no disponibles:** `libreoffice`, `xlsx2csv`, `ssconvert`, `mutool`.

## 1. Limitaciones de lectura

- Los archivos `.xlsx` y `.xlsm` pudieron revisarse con `openpyxl`.
- Los archivos `.xls` legacy pudieron abrirse con `xlrd` para hojas y dimensiones, pero no se extrajeron formulas confiables desde el formato binario.
- No se uso visualizacion de Excel/LibreOffice porque `libreoffice --headless` no esta instalado.
- Los PDF asociados se usaron como apoyo textual, pero la auditoria de formulas se basa principalmente en celdas de Excel leidas programaticamente.

## 2. Libros revisados

### `materiales/INSTALACIONES ELECTRICAS DVD 28.02-23/calculos justificativos/CALCULOS - CIRCUITOS Y TABLERO FRI.xlsx`

Hojas:

- `Computadoras`: 21x28, 38 formulas.
- `CUADRO DE CARGAS`: 1670x15, 741 formulas.
- `CALCULO POR CIRCUITOS`: 2375x6, 376 formulas.
- `CALCULOS  TAB. DIS.`: 313x8, 52 formulas.
- `CALCULO TAB. GEN. Y SUB. TAB`: 48x6, 8 formulas.

Formulas relevantes:

| Hoja / celda | Formula original | Interpretacion | Aplicabilidad Aquiles |
|---|---|---|---|
| `Computadoras!D5` | `=B5*C5` | Potencia parcial por cantidad y potencia unitaria. | Aplica como estructura general. |
| `CUADRO DE CARGAS!I5` | `=H5/(1.73*380*0.9)` | Corriente trifasica aproximada. | No aplica a suministro monofasico. |
| `CUADRO DE CARGAS!K5` | `=1.25*L5` | Corriente de diseno o margen sobre corriente base. | DUDOSA; debe justificarse en CNE correcto. |
| `CUADRO DE CARGAS!I7` | `=G7/(220)` | Corriente monofasica sin factor de potencia. | Aplica parcialmente; el motor usa `220*cosphi`. |
| `CUADRO DE CARGAS!J7` | `=0.8*H7` | Factor de demanda 0.80. | Aplica solo si el tipo de carga justifica ese FD. |
| `CUADRO DE CARGAS!L7` | `=H7/(1*220*1)` | Corriente monofasica con cosphi 1. | Diferente del motor, que usa 0.90. |
| `CALCULO POR CIRCUITOS!C12` | `=1.25*C11` | Factor 1.25 sobre corriente. | DUDOSA en vivienda si no se justifica. |
| `CALCULO POR CIRCUITOS!D21` | `=E20*C15/C13` | Relacion tipo resistencia/longitud/seccion para caida. | Aplica conceptualmente. |
| `CALCULO POR CIRCUITOS!B25` | `=1*C12*D21` | Caida/valor monofasico simplificado. | Parcial; no muestra factor 2 en esta celda. |
| `CALCULO POR CIRCUITOS!B50` | `=1.732*C37*D46*0.9` | Formula trifasica. | No aplica. |
| `CALCULO TAB. GEN. Y SUB. TAB!B23` | `=1.732*C10*D19*0.9` | Caida trifasica. | No aplica. |

Comparacion con script:

- El script coincide con la estructura `PI * FD`, `I = P/(V*cosphi)` y caida por longitud/seccion.
- El script adopta `cosphi=0.90` de forma global; Excel alterna entre cosphi 1.0, 0.9 y formulas trifasicas.
- El script no implementa las formulas trifasicas, correcto para Aquiles.
- El script usa factor 2 explicito en caida monofasica; las hojas tienen formulas heterogeneas, incluyendo una formula monofasica mas clara en PHARAok.

### `materiales/INSTALACIONES ELECTRICAS DVD 28.02-23/Metrado Electricas/METRADO DE INSTACONES ELECTRICAS-UNAP.xlsx`

Hoja:

- `Hoja 1`: 2058x26, 446 formulas.

Formulas relevantes:

| Celda | Formula | Interpretacion | Aplicabilidad |
|---|---|---|---|
| `G20` | `=D20*E20*F20` | Metrado por producto de dimensiones/cantidad. | Aplica para metrado, no Capitulo 2 actual. |
| `G25` | `=PRODUCT(C25:F25)` | Producto de factores de metrado. | Aplica a metrado. |
| `H30` | `=SUM(G31:G158)` | Subtotal de partida. | No aplica a calculo electrico actual. |

Comparacion con script:

- No hay correspondencia directa con el motor de calculo electrico.
- Servira en fase de metrados, no para validar demanda, corriente o caida.

### `materiales/INSTALACIONES ELECTRICAS DVD 28.02-23/Metrado Electricas/RESUMEN DE METRADO.xlsx`

- `Hoja 1`: 1029x6, sin formulas.
- No aporta formulas de Capitulo 2.

### `materiales/proyecto-guia-red-primaria/capitulo-ii-calculos/CALCULO DE MAXIMA DEMANDA - PHARAok.xlsm`

Hojas:

- `SELECCION DE EQUIPO E`: 21x6, 6 formulas.
- `R-MD-TOTAL `: 19x12, 15 formulas.
- `TGN`: 223x64, 579 formulas.
- `TDN`: 108x20, 162 formulas.
- `FACT. DE CORR`: 159x35, 238 formulas.

Formulas relevantes:

| Hoja / celda | Formula original | Interpretacion | Aplicabilidad Aquiles |
|---|---|---|---|
| `R-MD-TOTAL !J8` | `=I8*H8` | Demanda por factor aplicado a carga. | Aplica como concepto general. |
| `R-MD-TOTAL !H13` | `=SUM(H8:H12)` | Total de potencia. | Aplica como suma. |
| `R-MD-TOTAL !J13` | `=SUM(J8:J12)` | Total de demanda. | Aplica como suma. |
| `TDN!E15` | `=C15*D15` | Potencia instalada parcial. | Aplica como estructura. |
| `TDN!G15` | `=E15*F15` | Maxima demanda con factor. | Aplica como estructura. |
| `TDN!J14` | `=IF("1Ø"=I14,ROUND(SUM(G15:G19)/(220*$L$11),2)*(CONCATENATE("1.",$N$11)),ROUND(SUM(G15:G19)/(SQRT(3)*380*$L$11),2)*(CONCATENATE("1.",$N$11)))` | Corriente monofasica o trifasica con factor de seguridad textual. | Aplica parcialmente; contiene un problema: concatena texto para factor `1.xx`, lo que debe revisarse. |
| `TDN!L14` | `=IF("1Ø"=I14,2*J14*0.0175*H14/K14,SQRT(3)*J14*0.0175*H14/K14)` | Caida monofasica con factor 2 o trifasica con raiz 3. | Aplica. Es la evidencia mas clara para el factor 2 monofasico. |
| `TDN!M14` | `=IF("1Ø"=I14,L14/$J$11*100,L14/$I$11*100)` | Porcentaje de caida. | Aplica. |

Comparacion con script:

- El script coincide con `2*I*rho*L/S` y `%dV = dV/V*100`.
- PHARAok usa `rho=0.0175`, el script usa `0.0178`; la diferencia es pequena pero debe declararse.
- PHARAok es de red primaria y tableros generales, no vivienda. Solo se toma la estructura matematica, no los valores ni el alcance.

### `materiales/proyecto-guia-red-primaria/capitulo-ii-calculos/COORDINACION DE PROTECCION.xlsx`

Hojas:

- `CALCULO CORRRIENTES`: 94x30, 48 formulas.
- `DAÑO TERMICO`: 99x41, 279 formulas.
- `Cuadro fusibles`: 21x17, sin formulas.
- `CURVAS COORDINAC.`: 76x35, sin formulas.

Formulas relevantes:

| Hoja / celda | Formula | Interpretacion | Aplicabilidad |
|---|---|---|---|
| `CALCULO CORRRIENTES!F53` | `=+E53/(0.38*0.8*1.732)` | Corriente trifasica en 380 V. | No aplica. |
| `CALCULO CORRRIENTES!G53` | `=+F53*1.25` | Corriente con factor 1.25. | DUDOSA para vivienda; no basta como sustento normativo. |
| `CALCULO CORRRIENTES!M31` | `=(P27*0.9)/(SQRT(3)*P28*P29)` | Formula trifasica con factor. | No aplica. |
| `DAÑO TERMICO!C51` | `=$L$31*88.5*SQRT(0.18388/B51)` | Criterio de dano termico/protecciones MT. | No aplica. |

Comparacion con script:

- No sustenta directamente el motor residencial.
- Sirve para entender proteccion en red primaria, pero debe excluirse del caso Aquiles.

### `proyectos/renzo/calculos/cuadro-cargas/cuadro_cargas.xlsx`

**Nota:** el usuario pidio no tomar Renzo como modelo principal porque tambien esta en redaccion. Se revisa solo como comparacion secundaria y no como fuente normativa.

Hoja:

- `Cuadro de Cargas`: 9x13, 8 formulas.

Formulas relevantes:

| Celda | Formula | Interpretacion | Aplicabilidad |
|---|---|---|---|
| `I4:I8` | `=Hn/(Dn*0.9)` | Corriente por circuito con cosphi 0.90. | Coincide conceptualmente con el script. |
| `F9` | `=SUM(F4:F8)` | Potencia instalada total. | Aplica. |
| `H9` | `=SUM(H4:H8)` | Demanda total. | Aplica. |
| `I9` | `=H9/(220*0.9)` | Corriente total monofasica. | Aplica como comparacion. |

### `proyectos/renzo/calculos/cuadro-cargas/maxima_demanda.xlsx`

Hoja:

- `Maxima Demanda CNE`: 24x7, 5 formulas.

Formulas:

| Celda | Formula | Interpretacion | Aplicabilidad |
|---|---|---|---|
| `C10` | `=SUM(C5:C9)` | Suma de cargas instaladas. | Aplica. |
| `E10` | `=SUM(E5:E9)` | Suma de demandas. | Aplica. |
| `B16` | `=B13/(B14*B15)` | Corriente total. | Aplica. |
| `B18` | `=B16*B17` | Corriente de diseno con factor. | DUDOSA sin sustento normativo correcto. |

### Archivos `.xls` legacy de red primaria

Archivos abiertos solo para hojas/dimensiones:

- `CALCULOMECANICOCONDUCTORES 35.xls`: hojas `VR`, `COND`, `CMC`.
- `CALCULORETENIDA.xls`: hoja `CALRET`.
- `CALMECANICODEPOSTES.xls`: hojas `DATOSGENERALES`, `PR3-0`, `PSI-01`.
- `CIMENTACIONPOSTES.xls`: hojas `13300`, `TIPO DE SUELOS`.

Limitacion:

- `xlrd` no permitio extraer formulas confiables para esta auditoria.
- Estos libros corresponden a mecanica de conductores, retenidas, postes y cimentaciones de red primaria; no aplican al diseno interior residencial de Aquiles.

## 3. Discrepancias encontradas frente al script Python

| Tema | Excel/modelo | Script Python | Diagnostico |
|---|---|---|---|
| Resistividad cobre | PHARAok usa `0.0175`; script usa `0.0178` | Diferencia menor | Declarar valor adoptado y temperatura. |
| Corriente monofasica | Algunas hojas usan cosphi 1; otras 0.90 | Script usa 0.90 global | Aceptable como supuesto, pero debe parametrizarse. |
| Factor 1.25 | Varias hojas lo usan | Script lo aplica a todo | Requiere sustento normativo correcto; no citar 050-204. |
| Caida monofasica | PHARAok: `2*J*0.0175*L/S` | `2*L*In*rho/S` | Coincide conceptualmente. |
| Cocina electrica | CNE-U 050-200 exige 6000 W para primera cocina electrica | Script usa 3400 W * 0.80 | Discrepancia critica si la cocina es electrica. |
| Alumbrado minimo | CNE-U 030-002 exige 2.5 mm2 para alumbrado derivado | Script usa 1.5 mm2 | Discrepancia critica. |

## 4. Conclusion

Los Excel validan la forma general de las operaciones, pero no validan automaticamente los criterios finales adoptados para Aquiles. El script reproduce correctamente su propia logica; sin embargo, debe corregirse para incorporar el metodo CNE-U 050-200 como verificacion obligatoria, revisar conductores minimos y documentar los factores de demanda sin depender de Renzo como fuente principal.

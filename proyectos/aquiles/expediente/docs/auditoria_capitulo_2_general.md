# Auditoria general del Capitulo 2 - Calculos Justificativos

**Proyecto:** Instalaciones Electricas Interiores - Vivienda de Aquiles Taylor Ramos Yapo  
**Fecha de auditoria:** 2026-06-03  
**Estado de aprobacion:** **NO APROBADO para cierre definitivo**. El capitulo puede conservarse como borrador preliminar de trabajo, pero requiere correcciones criticas de criterio normativo, trazabilidad y datos de entrada.

## 1. Estructura y ubicacion de archivos

### Archivos verificados

- `proyectos/aquiles/expediente/capitulos/02-calculos-justificativos.tex`: existe y esta incluido en `main.tex`.
- `proyectos/aquiles/expediente/build/main.pdf`: existe y fue recompilado, 20 paginas, tamano carta.
- `proyectos/aquiles/expediente/docs/auditoria_fuentes_calculo.md`: existe.
- `proyectos/aquiles/expediente/docs/formulas_extraidas_capitulo_2.md`: existe.
- `proyectos/aquiles/expediente/preguntas_para_calculos.md`: existe.
- `herramientas/calculos/`: existe.
- `herramientas/calculos/data/proyecto_aquiles_base.json`: existe.
- `herramientas/calculos/scripts/calcular_instalacion.py`: existe.
- `herramientas/calculos/output/`: existe y contiene `resultados.json`, `tabla_cargas.tex`, `tabla_conductores.tex` y `reporte_calculos.md`.

### Estado Git observado

El repositorio tiene cambios no confirmados. Los cambios relacionados con esta fase estan en el proyecto LaTeX y el motor de calculo. Tambien existen cambios/residuos CAD ajenos al Capitulo 2:

- Eliminaciones locales en `proyectos/aquiles/trabajo-cad-casa/salidas/croquis_aquiles_v*.dxf/pdf`.
- Archivos temporales CAD `#piso1_v3.dxf` y `#piso2_v3.dxf`.

**Observacion:** esos residuos CAD no deben mezclarse con la auditoria del Capitulo 2 ni incluirse en un commit de calculos.

### Organizacion

- La ubicacion del motor Python es correcta: `herramientas/calculos/`.
- La ubicacion del expediente LaTeX es correcta: `proyectos/aquiles/expediente/`.
- Se detecta un archivo temporal de Excel en materiales: `materiales/INSTALACIONES ELECTRICAS DVD 28.02-23/calculos justificativos/~$CALCULOS - CIRCUITOS Y TABLERO FRI.xlsx`. Es residuo de Office/LibreOffice y debe limpiarse solo con aprobacion, porque esta dentro de fuentes.

## 2. Alcance del expediente LaTeX

`main.tex` incluye:

- Portada.
- Indice.
- Capitulo 1: memoria descriptiva.
- Capitulo 2: calculos justificativos.

`main.tex` no incluye capitulos 3 y 4, lo cual es correcto para esta fase. Sin embargo, los archivos `capitulos/03-especificaciones-materiales.tex` y `capitulos/04-especificaciones-montaje.tex` ya contienen desarrollo real. Esto incumple el criterio de no avanzar a especificaciones, aunque no aparezcan en el PDF actual.

**Estado:** MEDIO / ALTO por control de alcance. Recomendacion: mantener esos archivos fuera de `main.tex` y decidir si se revierten a estructura pendiente o se conservan como borrador no oficial.

## 3. Auditoria del motor Python

Archivo revisado: `herramientas/calculos/scripts/calcular_instalacion.py`.

### Datos que lee

- Entrada fija: `data/proyecto_aquiles_base.json`.
- No acepta argumentos CLI para elegir otro JSON o carpeta de salida.
- Salida fija: `output/resultados.json`, `output/tabla_cargas.tex`, `output/tabla_conductores.tex`, `output/reporte_calculos.md`.

### Formulas implementadas

- Potencia instalada por circuito: valor directo desde JSON.
- Maxima demanda por circuito: `MD = PI * FD`.
- Corriente nominal: `In = MD / (V * cosphi)`.
- Corriente de diseno: `Id = In * 1.25`.
- Caida de tension monofasica: `dV = 2 * L * In * rho / S`.
- Porcentaje de caida: `%dV = dV / V * 100`.
- Seleccion de interruptor: primer calibre comercial `>= In` y `<= ampacidad`, no `>= Id`.
- Ampacidad: tabla interna `AMPACITIES_CU`.

### Verificacion tecnica

| Punto auditado | Estado | Observacion |
|---|---|---|
| Uso de W, V, A, m, mm2 | CORRECTO PERO PRELIMINAR | Las unidades son consistentes, pero los datos no estan confirmados. |
| Tension 220 V | CORRECTO PERO PRELIMINAR | Coincide con cuestionario; falta confirmacion final de suministro. |
| Factor de potencia 0.90 | DUDOSO | Es razonable como supuesto, pero debe justificarse o parametrizarse por tipo de carga. |
| `I = P/(V*cosphi)` | CORRECTO | Coincide con el script y el capitulo. |
| Factor 1.25 | DUDOSO | El script lo aplica a todos los circuitos y al alimentador; la cita del capitulo a CNE 050-204 es incorrecta. |
| No duplicacion de 1.25 | CORRECTO | No se aplica dos veces. |
| Caida monofasica con factor 2 | CORRECTO | La formula esta implementada correctamente para 2 hilos. |
| % caida | CORRECTO | `dV/V*100`. |
| Coordinacion `Ib <= In <= Iz` | DUDOSA | El script selecciona ITM con corriente nominal de carga, pero el capitulo muestra `Id`; si se interpreta `Id` como `Ib`, C5, C6 y alimentador no cumplen. |
| Seleccion de conductores | INCORRECTA para alumbrado | Usa 1.5 mm2 para C1 y C4; el CNE-U 030-002 exige minimo 2.5 mm2 para circuitos derivados de fuerza y alumbrado. |
| Valores hardcodeados | DUDOSO | Ampacidades, ITM comerciales, diferencial y tubo alimentador de 35 mm estan hardcodeados. |
| Tablas LaTeX | CORRECTAS PERO MEJORABLES | Compilan y se leen, pero las rutas `../../herramientas/...` son fragiles. |

### Salida de consola del motor

El motor fue ejecutado desde `herramientas/calculos/` con:

```bash
python3 scripts/calcular_instalacion.py
```

Resumen reportado por consola:

- PI total: `8918 W`.
- MD total: `6992.0 W`.
- Corriente nominal del alimentador: `35.31 A`.
- Corriente de diseno del alimentador: `44.14 A`.
- Alimentador: `10.0 mm2`, `50 A`, caida `0.69%`, ITM `2P-40A`.
- Todos los circuitos fueron reportados como `CUMPLE/CUMPLE`.

**Diagnostico:** la ejecucion es reproducible y la aritmetica interna coincide con el recalcado independiente. El problema no es aritmetico; es de criterios de demanda, normas, seleccion minima de conductor y datos preliminares.

## 4. Auditoria del JSON de datos

Archivo revisado: `herramientas/calculos/data/proyecto_aquiles_base.json`.

### Datos coherentes

- Proyecto y propietario correctos.
- Ubicacion general coherente con fuentes de Aquiles.
- Sistema monofasico 220 V, 60 Hz, preliminar.
- Bomba de agua exterior incluida.
- Lavadora incluida.
- No se incluyen ducha electrica ni terma electrica, coherente con cuestionario previo.

### Datos en conflicto o pendientes

| Dato | JSON / Capitulo 2 | Fuente Aquiles | Diagnostico |
|---|---|---|---|
| Area techada total | 120 m2 en Capitulo 2 | Cuestionario: segundo piso aprox. 42.56 m2, terreno 134.18 m2; memoria menciona 80 m2 + 120 m2 | REVISAR. Hay contradiccion grave entre fuentes. |
| Area en memoria | 80 m2 primer piso + 120 m2 segundo piso | Cuestionario no confirma esos valores | REVISAR. Puede inflar o confundir demanda por area. |
| Cocina electrica | C6 = 3400 W y texto dice cocina electrica | Cuestionario solo dice microondas, lavadora, waflera y cargas de alto consumo; pregunta pendiente si cocina es electrica o gas | REVISAR. No debe cerrarse como cocina electrica sin respuesta. |
| Tomacorrientes 2do piso | 2340 W | Cuestionario dice varios tomacorrientes por definir | REVISAR. Numero real no confirmado. |
| Longitudes | 10 a 25 m, alimentador 12 m | No hay medicion final en croquis/CAD | PRELIMINAR. Deben medirse en plano regularizado. |
| Ubicacion TG | No esta parametrizada en JSON | Pregunta pendiente | REVISAR. Impacta longitudes y caida. |
| Secciones | Definidas por circuito | No confirmadas por norma final | REVISAR. Alumbrado 1.5 mm2 no cumple CNE-U 030-002. |
| Protecciones | Derivadas por script | No estan en JSON | REVISAR. Deben parametrizarse o justificarse. |
| Estado de datos | Solo algunos campos tienen `estado` | Preguntas pendientes abiertas | REVISAR. Falta marcar cada carga como confirmada/preliminar/supuesta. |

## 5. Auditoria de formulas

| Formula | Fuente documentada | Codigo Python | LaTeX Cap. 2 | Estado |
|---|---|---|---|---|
| `P_inst = sum(N_j * P_j)` | Principalmente Renzo / Excel | Parcial: el JSON ya trae PI por circuito | Si | CORRECTA PERO PRELIMINAR |
| `MD = PI * FD` | Excel UNA / criterio residencial | Si | Si | DUDOSA para demanda final de vivienda; sirve como metodo interno, pero debe compararse con CNE 050-200 y tomar el mayor aplicable. |
| `I = P/(V*cosphi)` | Excel / formulas residenciales | Si | Si | CORRECTA |
| `Id = 1.25 * In` | Documentada como CNE 050-204 | Si | Si | DUDOSA / MAL CITADA. La regla 050-204 no sustenta esto para vivienda. |
| `dV = 2*L*I*rho/S` | Excel PHARAok y criterio monofasico | Si | Si | CORRECTA para monofasico resistivo simplificado. |
| `%dV = dV/V*100` | Documentacion del motor | Si | Si | CORRECTA |
| `Ib <= In <= Iz` | Documentacion y capitulo | Parcial | Si | DUDOSA. Script usa `In_carga` para ITM; capitulo introduce `Id`, generando ambiguedad. |
| CNE 050-200 por area | CNE-U | No implementado en script | Mencionado pero no calculado correctamente | INCORRECTA / INCOMPLETA si existe cocina electrica. |
| SPAT Dwight / IEEE 142 | Documentacion formulas | No implementado | No calcula, solo describe | DUDOSA. No hay resistividad de suelo ni fuente local verificada. |

## 6. Problemas tecnicos principales

### Criticos

1. **Demanda maxima posiblemente subestimada.** Si C6 es una cocina electrica, CNE-U 050-200 indica 6000 W para la primera cocina electrica hasta 12 kW. El capitulo usa `3400 W * 0.80 = 2720 W`, reduciendo la demanda frente al criterio normativo.
2. **Conductor de alumbrado de 1.5 mm2.** CNE-U 030-002 exige minimo 2.5 mm2 para circuitos derivados de fuerza y alumbrado; 1.5 mm2 queda para control de alumbrado.
3. **Regla 050-204 mal usada.** El capitulo cita 050-204 para el factor 1.25, pero el texto extraido del CNE-U muestra esa regla como escuelas, no vivienda.
4. **Area techada incoherente.** Memoria, cuestionario y capitulo no coinciden.

### Altos

1. El script no implementa el criterio de "mayor resultado" entre CNE 050-200 y demanda por circuitos.
2. El documento afirma que se adopta `6992 W` como "base segura"; no es seguro si aplica cocina electrica.
3. El valor objetivo de puesta a tierra menor a `15 Ohmios` es mas exigente que CNE-U 060-712 (`<= 25 Ohmios`), pero no se justifica con norma/docente.
4. Las fuentes de formulas usan Renzo como referencia principal en varios puntos, aunque el usuario pidio no tomar Renzo como modelo.

### Medios

1. Tablas generadas por rutas relativas fragiles.
2. `main.tex` tiene anchors duplicados por redefinir contadores de seccion para el capitulo 2.
3. El pie de pagina dice "MEMORIA DESCRIPTIVA" tambien en el Capitulo 2.
4. Pagina final casi vacia por salto de contenido.

## 7. Veredicto

**NO APROBADO para entrega final.**

El Capitulo 2 es util como borrador preliminar porque:

- Compila.
- El motor corre.
- El recalcado independiente coincide con el motor.
- Las tablas son legibles.

Pero no puede aprobarse porque:

- La demanda maxima no esta cerrada conforme CNE-U 050-200.
- Hay una seleccion minima de conductor contraria al CNE-U 030-002.
- Hay citas normativas incorrectas o no verificadas.
- Los datos base de area, cocina electrica, longitudes y tomacorrientes siguen preliminares.

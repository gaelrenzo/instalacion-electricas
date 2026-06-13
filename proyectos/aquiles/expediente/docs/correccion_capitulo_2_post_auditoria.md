# Correccion del Capitulo 2 Post Auditoria

**Proyecto:** Instalaciones Electricas Interiores - Vivienda de Aquiles Taylor Ramos Yapo  
**Fecha:** 2026-06-03  
**Estado final:** APROBADO CON OBSERVACIONES para continuar como borrador tecnico preliminar. No esta aprobado para cierre definitivo hasta confirmar datos de Aquiles.

## 1. Errores detectados y correcciones aplicadas

| Hallazgo critico | Antes | Despues | Archivos modificados | Estado |
|---|---:|---:|---|---|
| Maxima demanda subestimada si existe cocina electrica | MD adoptada = 6,992 W | Dos escenarios: 6,992 W sin cocina electrica y 10,272 W con cocina electrica preliminar | `proyecto_aquiles_base.json`, `calcular_instalacion.py`, `02-calculos-justificativos.tex` | Corregido como escenario preliminar |
| Metodo CNE 050-200 incompleto para cocina electrica | No se adoptaba el minimo de 9,500 W del escenario CNE con cocina electrica | Se calcula MD CNE = 9,500 W y se adopta el mayor entre circuitos y CNE | Motor Python y Capitulo 2 | Corregido |
| Alumbrado con 1.5 mm2 | C1 y C4 = 1.5 mm2 | C1 y C4 = 2.5 mm2 | JSON, motor, tablas LaTeX, Capitulo 2 | Corregido conforme auditoria |
| Cita CNE-U 050-204 mal usada | Se citaba para justificar `Id = 1.25 In` | Se retiro como fundamento; 1.25 queda como criterio conservador preliminar | Capitulo 2 y docs de formulas | Corregido |
| Areas contradictorias | Memoria: 80 m2 + 120 m2; Capitulo 2: 120 m2 total | Tabla de areas con estado confirmado/preliminar/por confirmar; 120 m2 solo como escenario provisional | Memoria, JSON, Capitulo 2 | Corregido como dato preliminar |
| Cocina electrica no confirmada | C6 tratado como cocina electrica definitiva de 3,400 W | Dos escenarios: cocina a gas/sin alta potencia y cocina electrica preliminar | JSON, motor, Capitulo 2 | Corregido |
| Proteccion general potencialmente subdimensionada | 2P-40A fijo para el caso anterior | Escenario gas: 2P-40A; escenario electrico: 2P-63A | Motor y tablas | Corregido |
| Caida de tension no recalculada tras cambios | Alimentador 10 mm2, 0.69 % | Escenario electrico: alimentador 16 mm2, 0.630 % | Motor y Capitulo 2 | Corregido |
| Markdown literal en LaTeX | `**6,992 W**`, `**NH-80**` | Eliminado del Capitulo 2 | Capitulo 2 | Corregido |
| Pie de pagina de Capitulo 2 | Decia memoria descriptiva | Dice `CALCULOS JUSTIFICATIVOS - INSTALACIONES ELECTRICAS` | `main.tex`, `preambulo.tex` | Corregido |
| Capitulos 3 y 4 con contenido desarrollado | Archivos contenian desarrollo real | Contenido preservado como `NO COMPILAR - BORRADOR PRELIMINAR` con `\iffalse` | `03-especificaciones-materiales.tex`, `04-especificaciones-montaje.tex` | Controlado |

## 2. Resultados recalculados

| Concepto | Escenario 1: cocina a gas / sin cocina electrica | Escenario 2: cocina electrica preliminar |
|---|---:|---:|
| Potencia instalada | 8,918 W | 11,518 W |
| Maxima demanda por circuitos | 6,992 W | 10,272 W |
| Maxima demanda CNE 050-200 | 3,500 W | 9,500 W |
| Maxima demanda adoptada | 6,992 W | 10,272 W |
| Corriente de empleo `Ib` | 35.31 A | 51.88 A |
| Corriente de diseno preliminar `Id` | 44.14 A | 64.85 A |
| Alimentador sugerido | 10.0 mm2 | 16.0 mm2 |
| ITM general sugerido | 2P-40A | 2P-63A |
| Caida de tension alimentador | 0.686 % | 0.630 % |
| Metodo gobernante | Circuitos derivados | Circuitos derivados |

El recalcado independiente coincide con los resultados del motor para potencia instalada, maxima demanda, corriente de empleo, corriente de diseno y caida de tension del alimentador.

## 3. Archivos modificados

- `herramientas/calculos/data/proyecto_aquiles_base.json`
- `herramientas/calculos/scripts/calcular_instalacion.py`
- `herramientas/calculos/output/resultados.json`
- `herramientas/calculos/output/tabla_areas.tex`
- `herramientas/calculos/output/tabla_escenarios.tex`
- `herramientas/calculos/output/tabla_cargas*.tex`
- `herramientas/calculos/output/tabla_conductores*.tex`
- `herramientas/calculos/output/reporte_calculos.md`
- `herramientas/calculos/docs/notas_formulas.md`
- `proyectos/aquiles/expediente/capitulos/01-memoria-descriptiva.tex`
- `proyectos/aquiles/expediente/capitulos/02-calculos-justificativos.tex`
- `proyectos/aquiles/expediente/capitulos/03-especificaciones-materiales.tex`
- `proyectos/aquiles/expediente/capitulos/04-especificaciones-montaje.tex`
- `proyectos/aquiles/expediente/main.tex`
- `proyectos/aquiles/expediente/preambulo.tex`
- `proyectos/aquiles/expediente/preguntas_para_calculos.md`
- `proyectos/aquiles/expediente/docs/formulas_extraidas_capitulo_2.md`

## 4. Compilacion y revision visual

Comandos usados desde `proyectos/aquiles/expediente/`:

```bash
pdflatex -interaction=nonstopmode -output-directory=build main.tex
pdflatex -interaction=nonstopmode -output-directory=build main.tex
```

PDF actualizado:

`proyectos/aquiles/expediente/build/main.pdf`

Capturas generadas para revision visual:

- `docs/visual_post_portada-01.png`
- `docs/visual_post_indice-02.png`
- `docs/visual_post_indice-03.png`
- `docs/visual_post_memoria_inicio-04.png`
- `docs/visual_post_cap2_inicio-12.png`
- `docs/visual_post_cap2_tablas-15.png`
- `docs/visual_post_cap2_tablas-16.png`
- `docs/visual_post_cap2_tablas-17.png`
- `docs/visual_post_cap2_tablas-18.png`
- `docs/visual_post_cap2_final-19.png`

La revision visual muestra tablas legibles, pie de pagina correcto para Capitulo 2 y ausencia de capitulos 3 y 4 desarrollados en el PDF. El log conserva una advertencia repetida de `Overfull \hbox (11.41508pt)` asociada al estilo de pagina; no se observa corte visual ni tabla fuera del margen. Tambien queda una advertencia del sistema TeX sobre patrones de silabeo en espanol.

## 5. Datos que siguen pendientes

1. Area techada real del primer piso.
2. Area techada real del segundo piso.
3. Confirmacion de cocina a gas o cocina electrica.
4. Confirmacion de ducha electrica o terma electrica.
5. Ubicacion real del medidor.
6. Ubicacion real del Tablero General.
7. Decision sobre subtablero en segundo piso.
8. Potencia real de bomba de agua.
9. Cantidad final de tomacorrientes y luminarias por ambiente.
10. Longitud real medidor--Tablero General.

## 6. Veredicto post-correccion

**APROBADO CON OBSERVACIONES.**

El capitulo 2 ya no conserva los errores criticos de la auditoria: demanda con cocina electrica, conductor minimo de alumbrado, cita CNE-U 050-204, areas contradictorias y proteccion general quedaron corregidos o marcados como preliminares. No se aprueba como definitivo porque faltan datos de campo y confirmacion directa de Aquiles.

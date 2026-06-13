# Plan de trabajo de avance: capitulos I y II

## Alcance del encargo

El avance comprende el desarrollo ordenado de:

- Capitulo I: Memoria descriptiva del proyecto domiciliario.
- Capitulo II: Calculos justificativos de la instalacion electrica.

El objetivo es presentar al ingeniero una version revisable, con datos de la vivienda, criterios tecnicos, cuadro de cargas, demanda maxima, seleccion preliminar de circuitos, conductores, protecciones y puesta a tierra.

## Fuentes que se deben usar

| Fuente | Uso |
|---|---|
| `proyecto-casa/datos-vivienda.md` | Datos base de ubicacion, vivienda, ambientes y suministro |
| `proyecto-casa/cargas-electricas.md` | Cuadro oficial de cargas del mini proyecto |
| `informe_instalaciones_electricas.md` | Informe avanzado en Markdown para tomar contenido ya redactado |
| `latex/capitulos/01-memoria-descriptiva.tex` | Version avanzada del Capitulo I |
| `latex/capitulos/02-calculos-justificativos.tex` | Version avanzada del Capitulo II |
| `normativas/fuentes-oficiales.md` | Base normativa registrada |
| `normativas/matriz-cumplimiento.md` | Relacion norma-decision-evidencia |
| `materiales/proyecto-guia-red-primaria/` | Modelo de orden y presentacion del proyecto guia |
| `avance-capitulos-1-2/pautas-vivienda-2-pisos.md` | Criterio nuevo para el caso personal de vivienda de 2 pisos |

## Plan de avance

| Etapa | Actividad | Producto | Prioridad | Estado |
|---|---|---|---|---|
| 1 | Definir la vivienda propia de 2 pisos que reemplaza el caso del companero | Lista de ambientes, cargas y datos pendientes | Alta | En revision |
| 2 | Ordenar estructura del Capitulo I segun la vivienda propia | Indice interno de memoria descriptiva | Alta | Pendiente |
| 3 | Redactar Capitulo I con ubicacion, objetivo, alcance, ambientes y criterios tecnicos | Borrador revisable del Capitulo I | Alta | Pendiente |
| 4 | Revisar normas CNE-U y EM.010 aplicables | Base normativa resumida para citar en capitulos | Alta | Pendiente |
| 5 | Completar levantamiento de cargas por ambiente | Tabla de cargas por ambiente | Alta | Pendiente |
| 6 | Calcular potencia instalada, demanda maxima y corriente estimada | Cuadro de cargas resumido | Alta | Pendiente |
| 7 | Definir circuitos, conductores y protecciones preliminares | Tabla de seleccion tecnica | Alta | Pendiente |
| 8 | Verificar caida de tension con longitudes estimadas | Tabla de verificacion | Media | Pendiente |
| 9 | Redactar puesta a tierra y criterios de tablero | Texto tecnico y tabla de componentes | Media | Pendiente |
| 10 | Revisar coherencia entre Capitulo I y Capitulo II | Version lista para pasar a informe final | Alta | Pendiente |

## Distribucion sugerida por dias

| Dia | Trabajo principal | Resultado esperado |
|---|---|---|
| Dia 1 | Definir datos base de la vivienda propia y revisar material del docente | Datos confirmados de vivienda, ambientes, alcance y normativa |
| Dia 2 | Desarrollar Capitulo I | Memoria descriptiva completa en borrador |
| Dia 3 | Completar cuadro de cargas | Tabla de cargas por ambiente y circuito |
| Dia 4 | Desarrollar calculos principales del Capitulo II | Demanda maxima, corriente, circuitos y tablero |
| Dia 5 | Revisar conductores, protecciones, caida de tension y puesta a tierra | Calculos justificativos revisables |
| Dia 6 | Revision final y correcciones | Version de avance lista para entregar al ingeniero |

## Criterios de revision antes de entregar

- No debe quedar texto `EDITAR AQUI` en los capitulos de avance.
- Los datos de ubicacion, area, pisos y ambientes deben ser iguales en ambos capitulos.
- El proyecto debe corresponder a la vivienda propia de 2 pisos, no a la vivienda anterior de 3 pisos.
- La suma de cargas por ambiente debe coincidir con el resumen por circuitos.
- La corriente debe calcularse con la formula `I = P / (V x fp)`.
- La proteccion propuesta no debe ser menor que la corriente de diseno ni incoherente con el conductor.
- La caida de tension debe indicar longitud, seccion de conductor y porcentaje obtenido.
- Toda decision tecnica importante debe tener sustento en CNE-U, EM.010 o criterio academico del curso.

# Coordinacion de trabajo entre Codex, Gemini y OpenCode

## Objetivo

Organizar el avance del proyecto para que las tres IAs trabajen en paralelo sin mezclar archivos ni duplicar tareas. El proyecto actual corresponde a una vivienda propia de 2 pisos y el avance principal se concentra en los capitulos I y II.

## Regla principal

Ninguna IA debe editar al mismo tiempo los mismos archivos. Cada aporte debe quedar primero como documento de trabajo y solo despues integrarse a los archivos finales.

## Roles de trabajo

| IA | Rol principal | Producto esperado |
|---|---|---|
| Codex | Planificacion, cuestionario inicial y avance en LaTeX | Cuestionario del proyecto, archivo LaTeX compilable y PDF de avance |
| Gemini | Apoyo normativo y tecnico | Matriz de datos, requisitos normativos, preguntas complementarias y revision de PDFs |
| OpenCode | Integracion y control de coherencia | Revision de consistencia, orden del repositorio, control Git y preparacion de PR |

## Archivos bloqueados temporalmente

Mientras Codex trabaja, no se deben editar estos archivos o carpetas sin revisar primero su avance:

| Ruta | Motivo |
|---|---|
| `latex/` | Codex puede estar preparando el archivo LaTeX y su compilado |
| `avance-capitulos-1-2/capitulo-1-memoria-descriptiva.md` | Puede recibir contenido del cuestionario del Capitulo I |
| `avance-capitulos-1-2/capitulo-2-calculos-justificativos.md` | Puede conectarse con los datos del cuestionario y calculos |

Mientras Gemini trabaja, no se debe sobrescribir su documento de apoyo normativo cuando lo cree. El archivo esperado puede ser:

```text
avance-capitulos-1-2/apoyo-gemini-matriz-normativa.md
```

## Tareas que puede hacer OpenCode sin interferir

| Tarea | Estado |
|---|---|
| Mantener este archivo de coordinacion | En proceso |
| Revisar que los datos de la vivienda sean consistentes entre documentos | Pendiente |
| Integrar respuestas del cuestionario cuando el usuario las complete | Pendiente |
| Comparar el aporte de Codex con el de Gemini | Pendiente |
| Revisar que no se inventen numerales normativos no verificados | Pendiente |
| Preparar commit y PR cuando los avances esten listos | Pendiente |

## Flujo de integracion

1. Codex genera cuestionario, planificacion y LaTeX de avance.
2. Gemini genera matriz tecnica y normativa en un archivo separado.
3. OpenCode revisa ambos aportes y detecta diferencias o datos faltantes.
4. El usuario responde el cuestionario con datos reales de la vivienda.
5. OpenCode integra respuestas en los capitulos I y II de avance.
6. Se revisa coherencia entre memoria descriptiva, cargas y calculos.
7. Cuando el contenido este estable, se pasa a `proyecto-casa/`.
8. Al final se actualiza `latex/` y se compila el PDF.

## Datos minimos que deben quedar confirmados

| Dato | Estado actual | Responsable de confirmar |
|---|---|---|
| Ubicacion exacta de la vivienda | Pendiente | Usuario |
| Area aproximada del primer piso | Pendiente | Usuario |
| Area aproximada del segundo piso | Pendiente | Usuario |
| Cantidad final de focos del segundo piso | Pendiente | Usuario |
| Cantidad final de tomacorrientes del segundo piso | Pendiente | Usuario |
| Si la cocina tendra refrigeradora | Pendiente | Usuario |
| Si habra bano, lavanderia, bomba, terma o ducha electrica | Pendiente | Usuario |
| Longitudes aproximadas de circuitos | Pendiente | Usuario con apoyo de plano/croquis |
| Ubicacion del tablero general | Pendiente | Usuario |
| Tipo de canalizacion propuesta | Pendiente | Equipo |

## Control de calidad antes de integrar

- El proyecto debe mantenerse como vivienda unifamiliar de 2 pisos.
- No deben quedar datos del caso anterior de 3 pisos como si fueran vigentes.
- Las cargas del Capitulo II deben coincidir con los ambientes descritos en el Capitulo I.
- Las potencias, factores y corrientes deben mostrar formula o criterio usado.
- Las normas deben citarse solo cuando hayan sido verificadas en los documentos del repositorio.
- Si un PDF esta escaneado y no permite busqueda de texto, se debe anotar la pagina a revisar visualmente.
- No se debe modificar `proyecto-casa/` hasta que el avance de capitulos este revisado.
- No se debe modificar `latex/` si Codex aun esta trabajando en su compilado.

## Estado actual

| Frente | Estado |
|---|---|
| Caso de vivienda de 2 pisos | Definido e integrado (v6) |
| Cuestionario del proyecto | Completado e integrado |
| Matriz normativa y tecnica | Completado e integrado |
| Integracion general | Completado en v6 (Planos, MD y Cálculos) |
| Compilado LaTeX | Completado y verificado (build/main.pdf) |

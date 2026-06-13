# Pautas iniciales para vivienda propia de 2 pisos

## 1. Cambio de disposicion del trabajo

El desarrollo del proyecto debe cambiar de enfoque porque el ingeniero indico que cada estudiante debe trabajar con su propia vivienda, sus ambientes y sus planos. Por eso, el avance ya no debe basarse en la vivienda de 3 pisos del companero, sino en una vivienda modelo propia de 2 pisos.

La casa real puede ser demasiado grande para el alcance del curso, asi que se trabajara con una version simplificada y defendible: una vivienda unifamiliar de 2 pisos con ambientes definidos, cargas basicas, alumbrado, tomacorrientes, tablero, protecciones y puesta a tierra.

## 2. Datos generales iniciales

| Dato | Propuesta para el avance |
|---|---|
| Tipo de vivienda | Vivienda unifamiliar |
| Numero de pisos | 2 pisos |
| Sistema electrico | Monofasico, 220 V, 60 Hz |
| Uso | Residencial |
| Alcance | Instalacion electrica interior |
| Tablero | Tablero general en el primer piso, en zona accesible |
| Normativa base | Codigo Nacional de Electricidad - Utilizacion y RNE EM.010 |

## 3. Distribucion preliminar de ambientes

### Primer piso

| Ambiente | Alumbrado | Tomacorrientes | Observacion |
|---|---:|---:|---|
| Cuarto 1 grande | 2 focos | 4 tomacorrientes | Un tomacorriente por pared |
| Cuarto 2 grande | 2 focos | 4 tomacorrientes | Un tomacorriente por pared |
| Cocina | 2 focos | 1 tomacorriente | Para licuadora y pequenos artefactos |

### Segundo piso

| Ambiente | Alumbrado sugerido | Tomacorrientes sugeridos | Observacion |
|---|---:|---:|---|
| Habitacion 1 | 1 a 2 focos | 3 a 4 tomacorrientes | Definir segun tamano real |
| Habitacion 2 | 1 a 2 focos | 3 a 4 tomacorrientes | Definir segun tamano real |
| Habitacion 3 | 1 a 2 focos | 3 a 4 tomacorrientes | Definir segun tamano real |
| Habitacion 4 | 1 a 2 focos | 3 a 4 tomacorrientes | Definir segun tamano real |

Para una propuesta simple y ordenada se puede adoptar 1 foco y 3 tomacorrientes por habitacion del segundo piso. Si las habitaciones son grandes, se puede adoptar 2 focos y 4 tomacorrientes por habitacion.

## 4. Potencias referenciales para iniciar calculos

| Elemento | Potencia sugerida |
|---|---:|
| Foco LED | 12 W |
| Tomacorriente general | 180 W |
| Tomacorriente de cocina | 300 W |

Estas potencias son referenciales para un avance academico. Deben corregirse si el ingeniero entrega otra tabla o si se decide representar equipos especificos.

## 5. Levantamiento inicial del primer piso

| Ambiente | Carga | Cantidad | Potencia unitaria | Potencia total |
|---|---|---:|---:|---:|
| Cuarto 1 grande | Focos LED | 2 | 12 W | 24 W |
| Cuarto 1 grande | Tomacorrientes generales | 4 | 180 W | 720 W |
| Cuarto 2 grande | Focos LED | 2 | 12 W | 24 W |
| Cuarto 2 grande | Tomacorrientes generales | 4 | 180 W | 720 W |
| Cocina | Focos LED | 2 | 12 W | 24 W |
| Cocina | Tomacorriente de cocina | 1 | 300 W | 300 W |

### Resumen preliminar del primer piso

| Tipo de carga | Potencia |
|---|---:|
| Alumbrado | 72 W |
| Tomacorrientes generales | 1440 W |
| Cocina | 300 W |
| Total primer piso | 1812 W |

## 6. Circuitos recomendados

Para que el diseno sea ordenado, se recomienda separar alumbrado, tomacorrientes y cocina. La propuesta inicial queda asi:

| Circuito | Uso | Ambientes atendidos |
|---|---|---|
| C1 | Alumbrado primer piso | Cuarto 1, cuarto 2 y cocina |
| C2 | Tomacorrientes primer piso | Cuarto 1 y cuarto 2 |
| C3 | Cocina | Tomacorriente de cocina para licuadora y artefactos menores |
| C4 | Alumbrado segundo piso | 4 habitaciones |
| C5 | Tomacorrientes segundo piso | 4 habitaciones |

Esta separacion ayuda a justificar el diseno en el Capitulo II porque permite calcular cargas por circuito, seleccionar conductores y proponer protecciones de forma mas clara.

## 7. Pautas para empezar el Capitulo I

El Capitulo I no debe iniciar con calculos. Debe describir la vivienda y el alcance del proyecto.

Contenido recomendado:

1. Introduccion del proyecto.
2. Objetivo general.
3. Objetivos especificos.
4. Ubicacion de la vivienda.
5. Descripcion general de la vivienda.
6. Distribucion de ambientes por piso.
7. Alcance de la instalacion electrica interior.
8. Criterios tecnicos generales.
9. Normativa usada: CNE-U y RNE EM.010.
10. Restricciones del trabajo academico.

Texto base para iniciar:

> El presente proyecto desarrolla el diseno preliminar de la instalacion electrica interior de una vivienda unifamiliar de dos pisos, considerando circuitos de alumbrado, tomacorrientes, cocina, tablero de distribucion, protecciones y puesta a tierra, bajo criterios de seguridad y normativa peruana aplicable.

## 8. Pautas para empezar el Capitulo II

El Capitulo II debe iniciar con el levantamiento de cargas. Primero se registran los focos, tomacorrientes y cargas por ambiente. Luego se agrupan por circuito.

Orden recomendado:

1. Datos electricos del sistema.
2. Potencias referenciales usadas.
3. Levantamiento de cargas por ambiente.
4. Resumen por tipo de carga.
5. Distribucion de circuitos.
6. Calculo de potencia instalada.
7. Calculo de maxima demanda.
8. Calculo de corriente por circuito.
9. Seleccion preliminar de conductores.
10. Seleccion preliminar de protecciones.
11. Verificacion de caida de tension.
12. Criterio de puesta a tierra.

Formula base:

```text
Potencia total = cantidad x potencia unitaria
I = P / (V x fp)
```

Donde:

- `I`: corriente en amperios.
- `P`: potencia demandada en watts.
- `V`: tension nominal, inicialmente 220 V.
- `fp`: factor de potencia, inicialmente 0.90.

## 9. Datos que faltan confirmar

Antes de cerrar los capitulos I y II se deben confirmar estos puntos:

| Dato pendiente | Decision necesaria |
|---|---|
| Ubicacion exacta de la vivienda | Colocar direccion o referencia real |
| Area aproximada por piso | Definir medidas o croquis basico |
| Segundo piso | Elegir 1 o 2 focos por habitacion |
| Segundo piso | Elegir 3 o 4 tomacorrientes por habitacion |
| Cocina | Definir si solo habra licuadora/equipos pequenos o tambien refrigeradora |
| Otros ambientes | Confirmar si se incluira bano, lavanderia, ducha electrica, terma o bomba |
| Planos | Preparar croquis por piso para ubicar puntos electricos |
| Nivel de detalle | Elegir si sera propuesta simple o mas completa para obtener mejor calificacion |

## 10. Recomendacion de inicio

Para avanzar rapido y sin complicar demasiado el proyecto, se recomienda empezar con una vivienda modelo simple:

- Primer piso: 2 cuartos grandes y 1 cocina.
- Segundo piso: 4 habitaciones.
- Sin cargas especiales al inicio.
- Con circuitos separados para alumbrado, tomacorrientes y cocina.
- Agregar bano, lavanderia o carga especial solo si el ingeniero lo exige o si se desea un diseno mas completo.


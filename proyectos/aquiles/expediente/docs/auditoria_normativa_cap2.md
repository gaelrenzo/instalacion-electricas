# Auditoria normativa del Capitulo 2

**Normas locales revisadas:**

- `referencias/normativa/pdf/Código_Nacional_de_Electricidad__Utilización_.pdf`
- `referencias/normativa/pdf/EM.010 Instalaciones Eléctricas Interiores.pdf`
- `referencias/normativa/documentacion/fichas/cne-utilizacion.md`
- `referencias/normativa/documentacion/fichas/rne-em010.md`
- `proyectos/aquiles/fuentes/normativa-extraida/README.md`
- `proyectos/aquiles/documentacion/apoyo-gemini-matriz-normativa.md`

## 1. Verificaciones contra CNE-U

### 1.1 Regla 050-100 - tension para calculo de corrientes

Texto extraido del CNE-U:

- Lineas 4320-4325: para cargas en watts o VA en baja tension se deben usar tensiones nominales de `220 V` o `380 V`, segun corresponda.

**Estado en Capitulo 2:** CORRECTO. Usa `220 V` monofasico.

### 1.2 Regla 050-102 - caida de tension

Texto extraido del CNE-U:

- Lineas 4331-4333: alimentadores dimensionados para que la caida no sea mayor del `2.5%`.
- Lineas 4355-4357: caida total alimentador + circuitos derivados hasta el punto mas alejado no exceda `4%`.
- Lineas 4359-4363: circuitos derivados con caida no mayor del `2.5%`.
- Lineas 4367-4369: caida total maxima alimentador + derivados no exceda `4%`.

**Estado en Capitulo 2:** DUDOSO / PARCIAL.

- El capitulo usa `1.5%` para alimentador y `2.5%` para derivados.
- El valor `1.5%` es mas estricto que el CNE-U extraido, pero debe explicarse como criterio de diseno propio, no como exigencia textual del CNE-U.
- La documentacion `apoyo-gemini-matriz-normativa.md` contradice al CNE-U al indicar `1.5% + 1.5% + 2.5%`. Esta fuente debe tratarse como apoyo no oficial.

### 1.3 Regla 050-110 - determinacion de areas

Texto extraido del CNE-U:

- Lineas 4632-4648: el area de vivienda se determina por dimensiones interiores/areas techadas: 100% primer piso + 100% pisos superiores dedicados a vivienda + 75% sotano.
- Lineas 4650-4667: prevision opcional de demanda maxima cuando no se dispone de informacion especifica: 3000 W hasta 90 m2, 5000 W de 90 a 150 m2, 8000 W de 150 a 200 m2.

**Estado en Capitulo 2:** DUDOSO.

- El capitulo usa `120 m2` como area techada combinada.
- La memoria menciona `80 m2` en primer piso y `120 m2` en segundo piso.
- El cuestionario menciona segundo piso aprox. `42.56 m2` y terreno `134.18 m2`.

**Accion requerida:** confirmar area techada por piso antes de cerrar maxima demanda.

### 1.4 Regla 050-200 - viviendas unifamiliares

Texto extraido del CNE-U:

- Lineas 4673-4676: capacidad minima de acometida/alimentador debe ser la mayor de los parrafos aplicables.
- Lineas 4681-4687: carga basica `2500 W` para primeros `90 m2` + `1000 W` por cada `90 m2` o fraccion en exceso.
- Lineas 4714-4716: cualquier carga de cocina electrica: `6000 W` para cocina unica + 40% del exceso sobre `12 kW`.
- Lineas 4723-4730: cargas adicionales segun condiciones.
- Linea 4732: `40 amperes`.
- Lineas 4750-4752: la carga calculada por esta regla no debe considerarse carga continua en la aplicacion de 050-104.

**Estado en Capitulo 2:** INCORRECTO / INCOMPLETO.

- El capitulo menciona el metodo por area, pero no adopta el mayor resultado.
- Si C6 es cocina electrica, el capitulo debe usar `6000 W`, no `3400 W * FD 0.80`.
- El valor `6992 W` por circuitos no puede llamarse base segura si el metodo CNE 050-200 da `9500 W` con area 120 m2 y cocina electrica.

### 1.5 Regla 050-204

Texto extraido del CNE-U:

- Lineas 4920-4967: la regla 050-204 corresponde a escuelas.

**Estado en Capitulo 2:** INCORRECTO.

- El capitulo cita "Regla CNE 050-204" para aplicar `1.25 * In`.
- Esa cita no sustenta el factor en vivienda.

**Accion requerida:** corregir referencia normativa o retirar cita si el factor se usa como margen conservador interno.

### 1.6 Regla 030-002 - seccion minima de conductores

Texto extraido del CNE-U:

- Lineas 2460-2467: todos los conductores deben ser de cobre y no pueden tener seccion menor que `2.5 mm2` para circuitos derivados de fuerza y alumbrado, y `1.5 mm2` para circuitos de control de alumbrado.

**Estado en Capitulo 2:** INCORRECTO.

- C1 y C4 se calculan con conductor de `1.5 mm2` como circuitos derivados de alumbrado.
- Debe corregirse a minimo `2.5 mm2`, salvo que se trate solo de retornos/control, que no es el caso del circuito completo.

### 1.7 Regla 020-132 - proteccion diferencial

Texto extraido del CNE-U:

- Lineas 2022-2031: toda instalacion con equipo de utilizacion debe contar con interruptor diferencial de no mas de `30 mA`; no sustituye al sistema de puesta a tierra.

**Estado en Capitulo 2:** CORRECTO PERO MEJORABLE.

- El capitulo y el motor asignan diferenciales de `30 mA` a tomacorrientes, cocina y bomba.
- La norma extraida exige diferencial para toda instalacion; debe aclararse si habra diferencial general o diferenciales por grupos/circuitos.

### 1.8 Regla 060-712 - resistencia de electrodos

Texto extraido del CNE-U:

- Lineas 7047-7053: resistencia de puesta a tierra no debe ser mayor a `25 ohm`; si un electrodo simple supera ese valor, se requiere electrodo adicional.

**Estado en Capitulo 2:** CORRECTO PERO SIN JUSTIFICACION.

- El capitulo propone `menor a 15 ohmios`, que es mas exigente que 25 ohm.
- Debe justificarse como criterio del docente/proyecto o cambiarse a "no mayor a 25 ohm, adoptando 15 ohm como objetivo de diseno si se confirma".

## 2. Verificaciones EM.010

La EM.010 esta disponible como fuente. Las fichas internas indican:

- Alcance de instalaciones interiores.
- Componentes del proyecto.
- Iluminancias minimas por ambiente.
- Documentos minimos del expediente.

**Estado en Capitulo 2:** PARCIAL.

- Se cita EM.010, pero no se verifican iluminancias ni metodo de lumenes.
- Esto puede quedar para calculos de iluminacion, pero no debe afirmarse cumplimiento lumino-tecnico sin calculo.

## 3. Reglas citadas que requieren revision

| Cita / criterio | Estado | Motivo |
|---|---|---|
| CNE 050-204 para factor 1.25 | INCORRECTA | Regla corresponde a escuelas. |
| Caida alimentador 1.5% como exigencia CNE | DUDOSA | CNE extraido indica 2.5% y total 4%; 1.5% puede ser criterio conservador, no exigencia textual. |
| Conductor 1.5 mm2 para alumbrado derivado | INCORRECTA | CNE 030-002 exige 2.5 mm2 para alumbrado derivado. |
| Cocina electrica 3400 W * 0.80 | INCORRECTA si es cocina electrica | CNE 050-200 exige 6000 W para primera cocina electrica hasta 12 kW. |
| Puesta a tierra < 15 ohm | CORRECTA PERO PRELIMINAR | Es mas exigente que CNE 25 ohm; falta justificar. |

## 4. Conclusion normativa

El Capitulo 2 no queda aprobado normativamente. Las correcciones minimas antes de cierre son:

1. Corregir conductor minimo de alumbrado a `2.5 mm2`.
2. Implementar CNE-U 050-200 como criterio obligatorio y tomar el mayor resultado aplicable.
3. Corregir o retirar cita a CNE 050-204 para `1.25`.
4. Definir si la cocina es electrica o a gas.
5. Confirmar area techada real.
6. Aclarar el criterio de caida de tension usado: exigencia CNE o criterio conservador propio.

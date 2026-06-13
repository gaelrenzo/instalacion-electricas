# Recalculo independiente del Capitulo 2

**Fecha:** 2026-06-03  
**Metodo:** recalcado independiente con lectura directa de `proyecto_aquiles_base.json` y comparacion contra `resultados.json`. No se modifico el motor principal.

## 1. Datos base del motor

- Tension nominal: `220 V`.
- Factor de potencia: `0.90`.
- Resistividad de cobre: `0.0178 ohm*mm2/m`.
- Longitud alimentador: `12 m`.
- Circuitos: C1 a C8.
- Area de diseno indicada en Capitulo 2: `120 m2`, preliminar.

## 2. Recalculo aritmetico contra el motor

| Concepto | Resultado motor | Resultado auditoria | Diferencia | Estado |
|---|---:|---:|---:|---|
| Potencia instalada total (W) | 8918 | 8918 | 0 | CORRECTO |
| Maxima demanda por metodo del motor (W) | 6992.0 | 6992.0 | 0 | CORRECTO aritmeticamente |
| Corriente nominal total (A) | 35.31 | 35.31 | 0 | CORRECTO |
| Corriente de diseno total (A) | 44.14 | 44.14 | 0 | CORRECTO aritmeticamente |

## 3. Recalculo por circuito

| Circuito | MD motor (W) | MD auditoria (W) | In motor (A) | In auditoria (A) | Id motor (A) | Id auditoria (A) | dV% motor | dV% auditoria | Estado |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| C1 | 120.0 | 120.00 | 0.61 | 0.61 | 0.76 | 0.76 | 0.098 | 0.098 | CORRECTO |
| C2 | 756.0 | 756.00 | 3.82 | 3.82 | 4.77 | 4.77 | 0.445 | 0.445 | CORRECTO |
| C3 | 240.0 | 240.00 | 1.21 | 1.21 | 1.52 | 1.52 | 0.078 | 0.078 | CORRECTO |
| C4 | 132.0 | 132.00 | 0.67 | 0.67 | 0.83 | 0.83 | 0.158 | 0.158 | CORRECTO |
| C5 | 1638.0 | 1638.00 | 8.27 | 8.27 | 10.34 | 10.34 | 1.339 | 1.339 | CORRECTO aritmeticamente; coordinacion con ITM requiere aclaracion |
| C6 | 2720.0 | 2720.00 | 13.74 | 13.74 | 17.17 | 17.17 | 1.111 | 1.111 | CORRECTO aritmeticamente; criterio de cocina electrica es dudoso |
| C7 | 640.0 | 640.00 | 3.23 | 3.23 | 4.04 | 4.04 | 0.314 | 0.314 | CORRECTO |
| C8 | 746.0 | 746.00 | 3.77 | 3.77 | 4.71 | 4.71 | 0.341 | 0.341 | CORRECTO |

## 4. Coordinacion revisada

El script selecciona ITM con la corriente nominal de carga `In_carga`, no con la corriente de diseno `Id`.

| Circuito | In carga (A) | Id (A) | ITM | Iz (A) | `In_carga <= ITM <= Iz` | `Id <= ITM <= Iz` | Diagnostico |
|---|---:|---:|---:|---:|---|---|---|
| C1 | 0.61 | 0.76 | 10 | 15 | Cumple | Cumple | Correcto |
| C2 | 3.82 | 4.77 | 10 | 20 | Cumple | Cumple | Correcto |
| C3 | 1.21 | 1.52 | 10 | 20 | Cumple | Cumple | Correcto |
| C4 | 0.67 | 0.83 | 10 | 15 | Cumple | Cumple | Correcto |
| C5 | 8.27 | 10.34 | 10 | 20 | Cumple | No cumple | REVISAR definicion de `Ib` |
| C6 | 13.74 | 17.17 | 16 | 28 | Cumple | No cumple | REVISAR definicion de `Ib` |
| C7 | 3.23 | 4.04 | 10 | 20 | Cumple | Cumple | Correcto |
| C8 | 3.77 | 4.71 | 10 | 20 | Cumple | Cumple | Correcto |
| Alimentador | 35.31 | 44.14 | 40 | 50 | Cumple | No cumple | REVISAR criterio de 1.25 |

**Diagnostico:** si `Ib` se interpreta como corriente de carga nominal, la coordinacion por ITM pasa. Si el documento trata `Id` como corriente base para proteccion, C5, C6 y alimentador quedan mal coordinados. El Capitulo 2 debe separar con precision:

- `Ib`: corriente de carga o de empleo.
- `Id`: corriente para dimensionamiento termico del conductor si corresponde.
- `In_ITM`: corriente nominal del interruptor.
- `Iz`: ampacidad del conductor.

## 5. Comprobacion normativa alternativa CNE-U 050-200

Se verifica el escenario que el Capitulo 2 asume al llamar `C6` "cocina electrica".

Datos:

- Area techada preliminar usada en Capitulo 2: `120 m2`.
- Carga basica CNE 050-200: `2500 W` para primeros `90 m2` + `1000 W` por fraccion adicional = `3500 W`.
- Primera cocina electrica hasta 12 kW: `6000 W`.

Resultado alternativo:

| Concepto | Valor |
|---|---:|
| Carga basica por area (W) | 3500 |
| Cocina electrica normativa (W) | 6000 |
| MD CNE 050-200 con cocina electrica (W) | 9500 |
| Corriente con 220 V y cosphi 0.90 (A) | 47.98 |
| MD del motor (W) | 6992 |
| Diferencia CNE - motor (W) | 2508 |

**Diagnostico critico:** si la vivienda tendra cocina electrica, la maxima demanda del motor queda subestimada en `2508 W` frente al criterio CNE-U 050-200 usado en esta comprobacion. No debe adoptarse `6992 W` como "base segura" hasta resolver si la cocina es electrica o a gas.

## 6. Resultado del recalcado

- La aritmetica del script es consistente.
- Las tablas generadas coinciden con el JSON de salida.
- El resultado principal `6992 W` no queda aprobado como maxima demanda final.
- La seleccion de alimentador y protecciones depende de corregir la demanda normativa y aclarar el uso de `Id`.

## 7. Acciones requeridas antes de cierre

1. Confirmar si existe cocina electrica real. Si existe, aplicar CNE 050-200 con `6000 W` para la primera cocina electrica.
2. Confirmar area techada total real.
3. Cambiar conductores de alumbrado a minimo `2.5 mm2` si se mantiene criterio CNE-U 030-002.
4. Recalcular alimentador e ITM con el mayor resultado entre demanda normativa por vivienda y demanda por circuitos.
5. Separar en tablas `Ib`, `Id`, `In_ITM` e `Iz`.

# MEMORIA DE CÁLCULO

## Instalaciones eléctricas interiores - vivienda unifamiliar de 3 pisos

Proyecto académico para vivienda de tres niveles en Jr. Lima S/N (Coordenadas: 15°38'32.7"S 69°49'51.8"W), Capachica, Puno. Sistema monofásico 220 V, 60 Hz.

## Circuitos y Demanda Adoptados

El sistema eléctrico se organiza en 6 circuitos (2 por nivel: uno para alumbrado y uno para tomacorrientes generales). Se han integrado o eliminado todas las cargas especiales independientes:

| Circuito | Uso | Puntos | Pot. Instalada (W) | F. Demanda | Máx. Demanda (W) |
| --- | --- | :---: | :---: | :---: | :---: |
| **C1** | Alumbrado primer piso | 5 | 250 W | 1.00 | 250 W |
| **C2** | Tomacorrientes primer piso | 6 | 1080 W | 0.70 | 756 W |
| **C3** | Alumbrado segundo piso | 6 | 300 W | 1.00 | 300 W |
| **C4** | Tomacorrientes segundo piso | 11 | 1980 W | 0.70 | 1386 W |
| **C5** | Alumbrado tercer piso | 7 | 350 W | 1.00 | 350 W |
| **C6** | Tomacorrientes tercer piso | 10 | 1800 W | 0.70 | 1260 W |
| **Total** | | **45** | **5760 W** | | **4302 W** |

- **Potencia Instalada Total:** 5,760 W
- **Máxima Demanda Estimada:** 4,302 W

## Corriente de Diseño ($I_{dem}$)

Fórmula monofásica aplicada:

```text
I = P / (V x cos φ)
```

Con:
- $P = 4,302\text{ W}$ (Máxima Demanda)
- $V = 220\text{ V}$ (Tensión nominal)
- $\cos \phi = 0.90$ (Factor de potencia)

Cálculo:

```text
I = 4302 / (220 x 0.90) = 4302 / 198 = 21.73 A
```

## Conductores y Protecciones Generales

1.  **Interruptor General Termomagnético:** Se selecciona una llave general de **2P - 32 A** (sección mínima de protección para cubrir la corriente de diseño de 21.73 A).
2.  **Interruptor Diferencial General:** Se propone un interruptor diferencial de **2P - 40 A / 30 mA** para protección contra fugas de corriente.
3.  **Conductor Alimentador Principal:** Se adopta un cable alimentador de **2 x 10 mm² Cu + 1 x 10 mm² Cu (PE)** desde el medidor hasta el TG-01.

## Conductores y Protecciones de Circuitos Derivados

| Circuito | Uso | Interruptor Termomagnético | Conductor Eléctrico |
| --- | --- | --- | --- |
| **C1** | Alumbrado primer piso | 2P-10A | 3 x 1.5 mm² Cu (PW) |
| **C2** | Tomacorrientes primer piso | 2P-16A / ID-25A | 3 x 2.5 mm² Cu (PW) |
| **C3** | Alumbrado segundo piso | 2P-10A | 3 x 1.5 mm² Cu (PW) |
| **C4** | Tomacorrientes segundo piso | 2P-16A / ID-25A | 3 x 2.5 mm² Cu (PW) |
| **C5** | Alumbrado tercer piso | 2P-10A | 3 x 1.5 mm² Cu (PW) |
| **C6** | Tomacorrientes tercer piso | 2P-16A / ID-25A | 3 x 2.5 mm² Cu (PW) |

*Nota: Los circuitos de tomacorrientes (C2, C4, C6) incorporan de manera obligatoria conductores de protección a tierra y protección diferencial independiente de 25A - 30mA para salvaguardar la vida de las personas.*

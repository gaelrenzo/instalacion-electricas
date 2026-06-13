# Notas sobre Fórmulas y Criterios Normativos (CNE-U)

Este documento sirve como anexo teórico para el motor de cálculo en Python, resumiendo los fundamentos normativos y las reglas de diseño aplicadas.

---

## 1. Demanda Máxima de Viviendas Unifamiliares (Regla 050-200)

De acuerdo con el CNE-Utilización, para dimensionar el conductor alimentador de una vivienda se calcula la demanda por el área construida total (primer piso, segundo piso, etc.):

- **Carga básica:**
  - $2500\text{ W}$ para los primeros $90\text{ m}^2$ construidos.
  - $1000\text{ W}$ adicionales por cada $90\text{ m}^2$ o fracción subsiguiente.
- **Cargas especiales adicionales:**
  - Cocina eléctrica: potencia nominal al $100\%$ si está por debajo de $12\text{ kW}$ (o según el número de circuitos independientes, con factores de demanda reducidos de $0.80$).
  - Calentadores de agua (termas): $100\%$ de la potencia nominal.
  - Aire acondicionado o calefacción: $100\%$ de la potencia nominal (se toma el mayor de ambos si no pueden operar simultáneamente).
  - Motores de agua, ascensores, bombas: $100\%$ de la potencia nominal.

---

## 2. Coordinación de Protecciones Termomagnéticas (Regla CNE 050-104)

El interruptor automático termomagnético (ITM) tiene la función de proteger al conductor de sobrecalentamientos y cortocircuitos. Se rige por la relación:

$$I_b \leq I_n \leq I_z$$

Donde:
- $I_b$: Corriente nominal o de trabajo de la carga conectada.
- $I_n$: Calibre nominal de la corriente de disparo térmico del interruptor automático.
- $I_z$: Capacidad admisible de conducción de corriente continua del cable conductor (corregida por temperatura ambiente y agrupamiento de conductores en el mismo ducto).

---

## 3. Caída de Tensión (Regla CNE 050-102)

Para evitar pérdidas excesivas y mal funcionamiento de los equipos receptores, la caída de tensión en el sistema debe limitarse según las siguientes reglas:

- **Alimentador principal:** El proyecto usa $1.5\%$ como criterio conservador preliminar. REVISAR EN CNE-U antes de citarlo como exigencia normativa textual.
- **Circuitos derivados:** La caída de tensión en el tramo más largo del circuito derivado (desde el tablero hasta la última salida) no debe superar el $2.5\%$ ($5.5\text{ V}$ para $220\text{ V}$), según el criterio aplicado en el capítulo.
- **Caída acumulada:** La caída de tensión total combinada entre el alimentador principal y los circuitos derivados no debe superar el $4.0\%$ ($8.8\text{ V}$).

### Fórmula de caída de tensión monofásica:

$$\Delta V = \frac{2 \times L \times I_n \times \rho}{S}$$

Donde:
- $L$: Distancia física del circuito (m).
- $I_n$: Corriente de operación (A).
- $\rho$: Resistividad del cobre. Se adopta $\rho = 0.0178\ \Omega\cdot\text{mm}^2/\text{m}$ a la temperatura de operación normal ($20^\circ\text{C}$).
- $S$: Sección transversal de cobre ($mm^2$).

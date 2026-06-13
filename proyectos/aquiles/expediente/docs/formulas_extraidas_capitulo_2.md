# Compendio de Fórmulas Extraídas - Capítulo 2
**Rol:** Ingeniero Electricista Senior / Redactor LaTeX  
**Fecha:** 3 de junio de 2026  
**Proyecto:** Instalaciones Eléctricas Interiores - Vivienda de Aquiles

Este documento resume las expresiones matemáticas y criterios empíricos de diseño extraídos de los libros de cálculo Excel y memorias del repositorio, formulándolos en sintaxis LaTeX y evaluando su aplicabilidad técnica para el diseño de la vivienda de dos pisos de Aquiles Taylor Ramos Yapo.

---

## 1. Fórmulas de Carga y Demanda Eléctrica

### A. Potencia Instalada Total ($P_{inst}$)
* **Fuente original:** Cuadros de carga de los modelos Excel revisados en `materiales/INSTALACIONES ELECTRICAS DVD 28.02-23/calculos justificativos/`.
* **Ecuación en LaTeX:**
  $$P_{inst} = \sum_{j=1}^{n} (N_j \times P_j)$$
* **Variables y Unidades:**
  - $P_{inst}$: Potencia instalada total (W)
  - $N_j$: Cantidad de puntos de utilización o equipos de la carga tipo $j$ (Adimensional)
  - $P_j$: Potencia activa unitaria nominal de la carga tipo $j$ (W)
* **Interpretación Técnica:** Suma algebraica directa de todas las potencias nominales de los equipos y salidas de alumbrado y tomacorrientes presentes en la instalación.
* **Aplicabilidad a Vivienda Aquiles:** **Aplica plenamente**. Es la base de partida para determinar el cuadro de cargas de la instalación interior.

### B. Máxima Demanda por Criterio de Área Techada ($P_{dem\_bas}$)
* **Fuente original:** CNE-U Regla 050-200, contrastada con la auditoria normativa del repositorio.
* **Ecuación en LaTeX:**
  $$P_{dem\_bas} = \begin{cases} 
  2500 \text{ W} & \text{si } A_{techada} \le 90\text{ m}^2 \\
  2500 + 1000 \times \left\lceil \frac{A_{techada} - 90}{90} \right\rceil \text{ W} & \text{si } A_{techada} > 90\text{ m}^2
  \end{cases}$$
* **Variables y Unidades:**
  - $P_{dem\_bas}$: Demanda máxima de carga básica por área techada (W)
  - $A_{techada}$: Área construida techada total sumando todos los pisos de la vivienda ($m^2$)
* **Interpretación Técnica:** Es la carga básica obligatoria que exige el Código Nacional de Electricidad para alumbrado y tomacorrientes generales según el tamaño físico de la vivienda. Los factores de demanda ya están pre-calculados e integrados en este valor (F.D. = 1.0).
* **Aplicabilidad a Vivienda Aquiles:** **Aplica plenamente**. Con un área preliminar estimada de $120\text{ m}^2$, el subtotal de carga techada para el cálculo básico es de $3,500\text{ W}$.

### C. Máxima Demanda por Circuito ($P_{md\_circ}$)
* **Fuente original:** `materiales/INSTALACIONES ELECTRICAS DVD 28.02-23/calculos justificativos/CALCULOS - CIRCUITOS Y TABLERO FRI.xlsx` (Hoja `CUADRO DE CARGAS`)
* **Ecuación en LaTeX:**
  $$P_{md\_circ} = P_{inst\_circ} \times FD$$
* **Variables y Unidades:**
  - $P_{md\_circ}$: Demanda máxima del circuito derivado (W)
  - $P_{inst\_circ}$: Potencia instalada total en el circuito derivado (W)
  - $FD$: Factor de demanda asignado al tipo de carga del circuito (Adimensional, entre 0 y 1)
* **Interpretación Técnica:** Aplica un factor de simultaneidad teórico para estimar cuánta de la potencia instalada de un circuito específico estará encendida al mismo tiempo.
* **Valores normativos estándar:** Alumbrado ($FD = 1.0$), Tomacorrientes generales ($FD = 0.70$), Carga de Cocina y Lavadora ($FD = 0.80$), Bomba de Agua ($FD = 1.00$).
* **Aplicabilidad a Vivienda Aquiles:** **Aplica plenamente**. Se usa para estimar la demanda por cada uno de los circuitos $C1$ a $C8$.

---

## 2. Fórmulas de Corriente y Dimensionamiento de Alimentadores

### A. Corriente Nominal Monofásica ($I_n$)
* **Fuente original:** Fórmula eléctrica monofásica estándar, usada por los modelos Excel revisados.
* **Ecuación en LaTeX:**
  $$I_n = \frac{P_{dem}}{V \times \cos\phi}$$
* **Variables y Unidades:**
  - $I_n$: Corriente nominal de línea monofásica (A)
  - $P_{dem}$: Máxima demanda total calculada (W)
  - $V$: Tensión nominal monofásica entre fase y neutro ($220\text{ V}$)
  - $\cos\phi$: Factor de potencia de la carga (comercialmente asumido como $0.90$ o $1.0$ según el circuito)
* **Interpretación Técnica:** Determina la corriente de carga total que fluirá de manera continua por los conductores en condiciones normales de uso máximo.
* **Aplicabilidad a Vivienda Aquiles:** **Aplica plenamente** para el alimentador monofásico principal de la vivienda.

### B. Corriente Nominal Trifásica ($I_{n\_3\phi}$)
* **Fuente original:** `materiales/INSTALACIONES ELECTRICAS DVD 28.02-23/calculos justificativos/CALCULOS - CIRCUITOS Y TABLERO FRI.xlsx` (Hoja `CALCULO TAB. GEN. Y SUB. TAB`)
* **Ecuación en LaTeX:**
  $$I_{n\_3\phi} = \frac{P_{dem}}{\sqrt{3} \times V_L \times \cos\phi}$$
* **Variables y Unidades:**
  - $I_{n\_3\phi}$: Corriente nominal de línea trifásica (A)
  - $V_L$: Tensión nominal entre líneas o fases ($380\text{ V}$)
* **Aplicabilidad a Vivienda Aquiles:** **No aplica**. La vivienda cuenta con una acometida residencial monofásica de 220 V. Se incluye únicamente como referencia de los modelos del repositorio.

### C. Corriente de Diseño ($I_d$)
* **Fuente original:** Criterio preliminar conservador de diseño. La auditoria normativa indica que no debe citarse CNE-U 050-204 para vivienda.
* **Ecuación en LaTeX:**
  $$I_d = 1.25 \times I_n$$
* **Variables y Unidades:**
  - $I_d$: Corriente de diseño del conductor (A)
  - $I_n$: Corriente nominal calculada (A)
* **Interpretación Técnica:** Introduce un margen del 25% para verificar capacidad del conductor en esta etapa preliminar.
* **Aplicabilidad a Vivienda Aquiles:** **Correcta pero preliminar**. Se usa en el motor como criterio conservador, pero debe revisarse el sustento normativo final antes de cerrar el expediente.

---

## 3. Fórmulas de Caída de Tensión y Conductores

### A. Caída de Tensión Monofásica ($\Delta V$)
* **Fuente original:** Modelos Excel de calculos justificativos y formula monofasica verificada en auditoria.
* **Ecuación en LaTeX:**
  $$\Delta V = \frac{2 \times L \times I_n \times \rho}{S}$$
* **Variables y Unidades:**
  - $\Delta V$: Caída de tensión absoluta en voltios (V)
  - $L$: Longitud física del recorrido del circuito desde el tablero hasta el punto de carga más alejado (m)
  - $I_n$: Corriente nominal del circuito (A) (Nota: Algunas hojas usan la corriente de diseño $I_d$, pero técnicamente la verificación se realiza para la corriente nominal de operación $I_n$ o corriente de carga real $I_b$)
  - $\rho$: Resistividad del cobre electrolítico a temperatura de operación ($0.0178\ \Omega\cdot\text{mm}^2/\text{m}$)
  - $S$: Sección transversal de cobre del conductor ($mm^2$)
* **Interpretación Técnica:** El factor de multiplicación de 2 considera que la corriente recorre el conductor de ida (fase) y de retorno (neutro).
* **Aplicabilidad a Vivienda Aquiles:** **Aplica plenamente**. Es la fórmula de cálculo obligatoria para comprobar caídas de tensión en alimentadores y circuitos derivados.

### B. Caída de Tensión Trifásica ($\Delta V_{3\phi}$)
* **Fuente original:** `materiales/INSTALACIONES ELECTRICAS DVD 28.02-23/calculos justificativos/CALCULOS - CIRCUITOS Y TABLERO FRI.xlsx` (Hoja `CALCULO TAB. GEN. Y SUB. TAB`)
* **Ecuación en LaTeX:**
  $$\Delta V_{3\phi} = \frac{\sqrt{3} \times L \times I_n \times \rho \times \cos\phi}{S}$$
* **Aplicabilidad a Vivienda Aquiles:** **No aplica** por ser un sistema de alimentación monofásico.

### C. Caída de Tensión Porcentual ($\%\Delta V$)
* **Ecuación en LaTeX:**
  $$\%\Delta V = \left( \frac{\Delta V}{V_{nominal}} \right) \times 100$$
* **Límites Normativos (CNE-U Regla 050-102):**
  - Alimentador principal: $\%\Delta V \leq 1.5\%$ como criterio conservador preliminar; REVISAR EN CNE-U antes de citarlo como exigencia textual.
  - Circuito derivado: $\%\Delta V \leq 2.5\%$
  - Caída acumulada total: $\%\Delta V_{total} \le 4.0\%$
* **Aplicabilidad a Vivienda Aquiles:** **Aplica plenamente**. Todos los tramos calculados deben cumplir estas restricciones porcentuales.

---

## 4. Fórmulas de Coordinación y Dispositivos de Protección

### A. Regla Fundamental de Coordinación de Protecciones
* **Fuente original:** CNE-U / criterio de coordinacion verificado en auditoria normativa.
* **Ecuación en LaTeX:**
  $$I_b \leq I_n \leq I_z$$
* **Variables y Unidades:**
  - $I_b$: Corriente nominal del circuito o carga real de trabajo (A)
  - $I_n$: Corriente nominal del interruptor termomagnético (A)
  - $I_z$: Capacidad de conducción del conductor de cobre en ducto empotrado (A), corregido por temperatura y factor de agrupamiento si correspondiese.
* **Interpretación Técnica:** Asegura que el interruptor automático proteja al conductor del circuito contra sobrecorrientes prolongadas antes de que este alcance temperaturas críticas de degradación del aislamiento, pero sin dispararse de manera falsa bajo la corriente de operación normal.
* **Aplicabilidad a Vivienda Aquiles:** **Aplica plenamente**. Utilizado para coordinar las llaves termomagnéticas de 10 A, 16 A, 20 A y la llave general en el Tablero General.

---

## 5. Fórmulas de Puesta a Tierra (SPAT)

### A. Resistencia Eléctrica de Pozo de Tierra Vertical Unico ($R_{spat}$)
* **Fuente original:** Estándar IEEE Std 142 / Ecuación simplificada de Dwight para un electrodo vertical.
* **Ecuación en LaTeX:**
  $$R_{spat} = \frac{\rho_{suelo}}{2\pi L_{electrodo}} \left[ \ln\left( \frac{4L_{electrodo}}{d_{electrodo}} \right) - 1 \right]$$
* **Variables y Unidades:**
  - $R_{spat}$: Resistencia de puesta a tierra ($\Omega$)
  - $\rho_{suelo}$: Resistividad eléctrica promedio del terreno ($\Omega\cdot\text{m}$)
  - $L_{electrodo}$: Longitud de la varilla de cobre ($2.40\text{ m}$)
  - $d_{electrodo}$: Diámetro exterior de la varilla ($0.019\text{ m}$ o $3/4''$)
* **Interpretación Técnica:** Estima la resistencia que el electrodo vertical ofrece al paso de corrientes de falla hacia la masa terrestre.
* **Aplicabilidad a Vivienda Aquiles:** **Aplica plenamente** para fundamentar teóricamente la resistencia objetivo del pozo de puesta a tierra residencial ($\le 15\ \Omega$).

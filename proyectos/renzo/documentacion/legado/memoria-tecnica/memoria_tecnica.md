# MEMORIA TÉCNICA Y CÁLCULOS JUSTIFICATIVOS
## Proyecto: Instalación Eléctrica Residencial - Vivienda Unifamiliar de 3 Pisos

### 1. Normas de Referencia y Criterios de Diseño
El diseño de la instalación eléctrica se basa en las siguientes normativas:
* **National Electrical Code (NEC - NFPA 70):** Para el cálculo de secciones de conductores (NEC 310), dimensionamiento de circuitos ramales (NEC 210), protecciones (NEC 240) y sistemas de puesta a tierra (NEC 250).
* **Reglamento Nacional de Edificaciones (RNE EM.010):** Normativa aplicable en Perú para instalaciones interiores.
* **Código Nacional de Electricidad - Utilización (CNE-U):** Sección 050 para cargas e iluminación y Sección 060 para puesta a tierra.

### 2. Parámetros Eléctricos del Sistema
* **Tensión de suministro ($V$):** $220\text{ V}$ (Tensión monofásica de servicio).
* **Frecuencia ($f$):** $60\text{ Hz}$.
* **Factor de Potencia ($\cos \phi$):** $0.90$ (estimado para cargas residenciales combinadas).
* **Caída de Tensión Máxima Permitida:**
  * Alimentador principal: $2.5\%$
  * Circuitos derivados (ramales): $3.0\%$ (NEC 210.19(A) FPN 4)
  * Caída de tensión total combinada: $5.0\%$

---

### 3. Fórmulas de Cálculo
#### 3.1. Corriente de Diseño ($I$)
Para un sistema monofásico, la corriente nominal o de diseño se calcula mediante la fórmula:
$$I = \frac{P}{V \cdot \cos \phi}$$
Donde:
* $P$: Potencia en Watts ($W$).
* $V$: Tensión nominal ($220\text{ V}$).
* $\cos \phi$: Factor de potencia ($0.90$).

#### 3.2. Caída de Tensión ($\Delta V$)
Para circuitos monofásicos de cobre, la caída de tensión se calcula mediante la fórmula:
$$\Delta V = \frac{2 \cdot L \cdot I \cdot \rho}{S}$$
Donde:
* $L$: Longitud del conductor (metros).
* $I$: Corriente del circuito (Amperios).
* $\rho$: Resistividad del cobre a la temperatura de operación ($0.0175\ \Omega \cdot \text{mm}^2/\text{m}$).
* $S$: Sección o calibre del conductor ($\text{mm}^2$).

Porcentaje de caída de tensión:
$$\Delta V\% = \left(\frac{\Delta V}{V}\right) \cdot 100$$

---

### 4. Cuadro de Cargas y Demanda Máxima
El cuadro de cargas se ha calculado basándose en el análisis riguroso de los planos PNG actuales, donde se identificaron exactamente **13 tomacorrientes dobles** (3 en primer piso, 6 en segundo piso, 4 en tercer piso):

| Cto. | Piso | Descripción del Circuito | P. Inst. ($W$) | F.D. | P. Dem. ($W$) | $I_{\text{dem}}$ ($A$) | Protección ITM | Calibre Cond. (F+N+PE) |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **C1** | Piso 1 | Alumbrado primer piso | 72 | 1.00 | 72 | 0.36 | 2P - 10 A | $3 \times 1.5\text{ mm}^2$ Cu |
| **C2** | Piso 1 | Tomacorrientes generales | 180 | 1.00 | 180 | 0.91 | 2P - 16 A | $3 \times 2.5\text{ mm}^2$ Cu |
| **C3** | Piso 1 | Tomacorrientes de cocina | 360 | 1.00 | 360 | 1.82 | 2P - 20 A | $3 \times 2.5\text{ mm}^2$ Cu |
| **C4** | Piso 2 | Alumbrado segundo piso | 72 | 1.00 | 72 | 0.36 | 2P - 10 A | $3 \times 1.5\text{ mm}^2$ Cu |
| **C5** | Piso 2 | Tomacorrientes generales | 1080 | 0.70 | 756 | 3.82 | 2P - 16 A | $3 \times 2.5\text{ mm}^2$ Cu |
| **C6** | Piso 3 | Alumbrado tercer piso | 84 | 1.00 | 84 | 0.42 | 2P - 10 A | $3 \times 1.5\text{ mm}^2$ Cu |
| **C7** | Piso 3 | Tomacorrientes generales | 720 | 0.70 | 504 | 2.55 | 2P - 16 A | $3 \times 2.5\text{ mm}^2$ Cu |
| **Total**| | **Vivienda Unifamiliar** | **2,568** | | **2,028** | **10.24** | | |

* **Potencia Instalada Total ($P_{\text{inst}}$):** $2,568\text{ W}$ ($2.57\text{ kW}$)
* **Máxima Demanda Calculada ($P_{\text{dem}}$):** $2,028\text{ W}$ ($2.03\text{ kW}$)
* **Corriente de Demanda Total ($I_{\text{dem}}$):** $10.24\text{ A}$

---

### 5. Selección y Coordinación Conductor-Protección
Para cada circuito se ha seleccionado la sección del conductor de cobre y su interruptor de protección según la regla:
$$I_b \leq I_n \leq I_z$$

#### 5.1. Circuito General de Alimentación (Acometida a TG-01)
* **Corriente de diseño:** $10.24\text{ A}$.
* **Protección adoptada:** Interruptor termomagnético de **2P - 32 A**.
* **Conductor seleccionado:** **$2 \times 10\text{ mm}^2\text{ Cu} + 1 \times 10\text{ mm}^2\text{ Cu (PE)}$** tipo THW en canalización PVC de $1"$.
* **Capacidad del conductor ($I_z$):** $50\text{ A}$ (a 60°C). Cumple con holgura: $10.24\text{ A} \leq 32\text{ A} \leq 50\text{ A}$.

#### 5.2. Circuitos de Alumbrado (C1, C4, C6)
* **Corriente máxima:** $0.42\text{ A}$ (C6).
* **Protección adoptada:** Termomagnético de **2P - 10 A**.
* **Conductor:** **$2 \times 1.5\text{ mm}^2\text{ Cu} + 1.5\text{ mm}^2\text{ Cu (PE)}$** tipo TW.
* **Capacidad del conductor ($I_z$):** $15\text{ A}$ (a 60°C). Coordinación: $0.42\text{ A} \leq 10\text{ A} \leq 15\text{ A}$.

#### 5.3. Circuitos de Tomacorrientes Generales (C2, C5, C7)
* **Corriente máxima:** $3.82\text{ A}$ (C5).
* **Protección adoptada:** Termomagnético de **2P - 16 A** + Interruptor Diferencial de **2P - 25 A / 30 mA**.
* **Conductor:** **$2 \times 2.5\text{ mm}^2\text{ Cu} + 2.5\text{ mm}^2\text{ Cu (PE)}$** tipo THW.
* **Capacidad del conductor ($I_z$):** $20\text{ A}$ (a 60°C). Coordinación: $3.82\text{ A} \leq 16\text{ A} \leq 20\text{ A}$.

#### 5.4. Circuito de Cocina (C3)
* **Corriente de diseño:** $1.82\text{ A}$.
* **Protección adoptada:** Termomagnético de **2P - 20 A** + Interruptor Diferencial de **2P - 25 A / 30 mA**.
* **Conductor:** **$2 \times 2.5\text{ mm}^2\text{ Cu} + 2.5\text{ mm}^2\text{ Cu (PE)}$** tipo THW.
* **Capacidad del conductor ($I_z$):** $20\text{ A}$ (a 60°C). Coordinación: $1.82\text{ A} \leq 20\text{ A} \leq 20\text{ A}$.

---

### 6. Cálculos de Caída de Tensión
La caída de tensión en el tramo más largo (C7 en el tercer piso) se estima para una longitud de $25\text{ m}$:
$$\Delta V = \frac{2 \cdot L \cdot I \cdot \rho}{S} = \frac{2 \cdot 25\text{ m} \cdot 2.55\text{ A} \cdot 0.0175\ \Omega \cdot \text{mm}^2/\text{m}}{2.5\text{ mm}^2} = \frac{2.231}{2.5} = 0.89\text{ V}$$

Porcentaje de caída de tensión:
$$\Delta V\% = \left(\frac{0.89\text{ V}}{220\text{ V}}\right) \cdot 100 = 0.40\%$$

---

### 7. Dimensionamiento de la Puesta a Tierra (SPAT)
* **Varilla de cobre:** Diámetro $5/8"$, longitud $2.40\text{ m}$.
* **Conductor de enlace:** Cobre de $6\text{ mm}^2$ (mínimo exigido por NEC 250.66).
* **Resistencia objetivo:** $< 25\ \Omega$ (NEC 250.53).

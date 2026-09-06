# MEMORIA DE CÁLCULO ELÉCTRICO Y DISEÑO DE INSTALACIONES
## PROYECTO 1 RENZO - VIVIENDA UNIFAMILIAR DE 1 PISO

**Propietario / Responsable:** Renzo Gabriel Mamani Galindo  
**Docente:** Richar Renzo Julio Amachi Quispe  
**Ubicación:** Puno, Perú  
**Normativa Aplicable:** Código Nacional de Electricidad - Utilización (CNE 2006 / R.M. 037-2006-MEM/DM), Norma Técnica IEC 60364, CNE Suministro.

---

### 1. DESCRIPCIÓN DEL PROYECTO

El presente proyecto abarca el diseño del sistema eléctrico interior para una **vivienda unifamiliar de un (1) piso**. 

De acuerdo al plano arquitectónico y de distribución eléctrica suministrado (`/storage/emulated/0/universida-datos/Protecto/IMG-20260905-WA0067.jpg`), la edificación cuenta con una alimentación **monofásica de 220 V / 60 Hz** y la siguiente distribución de puntos de utilización:

- **Circuito C-1 (Alumbrado / Iluminación):** 
  - 11 Luminarias LED (8 distribuidas en el ambiente principal + 3 externas/superiores).
  - 8 Interruptores de control manual (simples / conmutados).
- **Circuito C-2 (Tomacorrientes de Uso General - TUG):** 
  - 29 Puntos de tomacorrientes bipolares dobles con toma a tierra (2P+T).
  - Equipos alimentados: Refrigerador (300–500 W), TV (100–200 W), Laptops (50–100 W), PC de escritorio (300–600 W) y electrodomésticos portátiles de uso doméstico.

---

### 2. CRITERIOS DE DISEÑO Y SELECCIÓN DE CONDUCTORES

1. **Sección Mínima de Conductores:** De acuerdo a la regla **CNE Utilización 050-102** y buenas prácticas de ingeniería, se establece un calibre mínimo de **2.5 mm² Cu (≈12 AWG)** para todos los circuitos derivados de alumbrado y tomacorrientes. Se rechaza categóricamente el uso de cable 2.08 mm² (14 AWG) en la instalación nueva para evitar calentamientos y garantizar resistencia mecánica.
2. **Sistema de Protección:** Todos los circuitos cuentan con protección termomagnética (ITM) y el circuito de tomacorrientes cuenta obligatoriamente con protección diferencial de alta sensibilidad ($30\,\text{mA}$).
3. **Puesta a Tierra (PAT):** Todo tomacorriente cuenta con conductor de protección (PE) conectado a un pozo a tierra vertical ($R_{\text{PAT}} \le 25\,\Omega$).

---

### 3. CÁLCULO DE CARGAS Y MÁXIMA DEMANDA (MD)

#### 3.1. Circuito C-1: Alumbrado General
- **Luminarias:** 11 luminarias LED de 20 W cada una.
- **Potencia Instalada (PI_C1):** 
  $$P_{\text{C1}} = 11 \times 20\,\text{W} = 220\,\text{W}$$
- **Corriente Nominal / Diseño ($I_{\text{C1}}$):**
  $$I_{\text{C1}} = \frac{P_{\text{C1}}}{V \cdot \cos\phi} = \frac{220\,\text{W}}{220\,\text{V} \times 0.90} = 1.11\,\text{A}$$
- **Conductor Seleccionado:** $2 \times 2.5\,\text{mm}^2\,\text{Cu THHN/THW-90} + 1 \times 2.5\,\text{mm}^2\,\text{Cu PE}$ en conduit PVC-P $20\,\text{mm}$ ($3/4''$).
- **Capacidad del conductor en ducto ($I_z$):** $21\,\text{A}$.
- **Interruptor Termomagnético (ITM):** **2P - 10 A**, Curva C, Poder de Corte $6\,\text{kA}$.
- **Verificación:** $1.11\,\text{A} \le 10\,\text{A} \le 21\,\text{A}$ $\Rightarrow$ **CUMPLE**.

---

#### 3.2. Circuito C-2: Tomacorrientes de Uso General (TUG)
- **Tomacorrientes:** 29 salidas dobles 2P+T.
- **Potencia Instalada Asignada (PI_C2):** $29 \times 200\,\text{VA} = 5,800\,\text{VA}$.
- **Máxima Demanda Simultánea Estimada (MD_C2):** 
  En operación continua residencial máxima (Refrigerador + TV + PC + Electrodomésticos intermitentes):
  $$P_{\text{demanda C2}} = 3,000\,\text{W}$$
- **Corriente de Demanda / Diseño ($I_{\text{C2}}$):**
  $$I_{\text{C2}} = \frac{3,000\,\text{W}}{220\,\text{V} \times 0.90} = 15.15\,\text{A}$$
  *(En pico de $3.5\,\text{kW}$, $I = 17.68\,\text{A}$)*.
- **Conductor Seleccionado:** $2 \times 2.5\,\text{mm}^2\,\text{Cu THHN/THW-90} + 1 \times 2.5\,\text{mm}^2\,\text{Cu PE}$ en conduit PVC-P $20\,\text{mm}$ ($3/4''$).
- **Capacidad del conductor en ducto ($I_z$):** $21\,\text{A}$.
- **Protección Termomagnética (ITM):** **2P - 20 A** (o 16 A según ajuste de simultaneidad), Curva C, Poder de Corte $6\,\text{kA}$.
- **Protección Diferencial (ID):** **2P - 25 A / 30 mA** (Obligatorio CNE 060-400).
- **Verificación:** $15.15\,\text{A} \le 20\,\text{A} \le 21\,\text{A}$ $\Rightarrow$ **CUMPLE**.

---

#### 3.3. Alimentador Principal (Medidor M -> Tablero General TG)
- **Potencia Instalada Total (PI):** $220\,\text{W} + 5,800\,\text{W} = 6,020\,\text{W}$.
- **Cálculo de Máxima Demanda (CNE Utilización 050-200 - Vivienda Unifamiliar):**
  - Primeros $1,500\,\text{W}$ al 100%: $1,500\,\text{W}$
  - Exceso $(6,020 - 1,500) \times 50\% = 2,260\,\text{W}$
  - **$\text{MD}_{\text{Total}} = 1,500 + 2,260 = 3,760\,\text{W} = 3.76\,\text{kW}$**.
- **Corriente del Alimentador ($I_{\text{alim}}$):**
  $$I_{\text{alim}} = \frac{3,760\,\text{W}}{220\,\text{V} \times 0.90} = 18.99\,\text{A} \approx 19.0\,\text{A}$$
- **Corriente de Diseño ($1.25 \times I_{\text{alim}}$):**
  $$I_{\text{diseño}} = 1.25 \times 19.0\,\text{A} = 23.75\,\text{A}$$
- **Conductor del Alimentador Seleccionado:** $2 \times 4\,\text{mm}^2\,\text{Cu THHN/THW-90} + 1 \times 4\,\text{mm}^2\,\text{Cu PE}$ en ducto PVC-P $25\,\text{mm}$ ($1''$).
- **Capacidad de corriente del cable $4\,\text{mm}^2$ ($I_z$):** $31\,\text{A}$.
- **Interruptor Termomagnético Principal (ITM General):** **2P - 25 A**, Curva C, Poder de corte $10\,\text{kA}$.
- **Verificación:** $19.0\,\text{A} \le 25\,\text{A} \le 31\,\text{A}$ $\Rightarrow$ **CUMPLE**.

---

### 4. CÁLCULO DE CAÍDA DE TENSIÓN ($\Delta V$)

Fórmula monofásica:
$$\Delta V = \frac{2 \cdot L \cdot I \cdot \rho}{S}$$
donde $\rho = 0.0175\,\Omega\cdot\text{mm}^2/\text{m}$ (resistividad del cobre electrolítico a 20°C).

| Tramo | Conductor | Longitud ($L$) | Corriente ($I$) | $\Delta V$ (Voltios) | $\% \Delta V$ | Límite Máximo CNE | Estado |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Alimentador (Medidor - TG)** | $2 \times 4\,\text{mm}^2$ | 15.0 m | 19.0 A | 2.49 V | **1.13 %** | 2.5 % | **APROBADO** |
| **C-1 Alumbrado** | $2 \times 2.5\,\text{mm}^2$ | 20.0 m | 1.11 A | 0.31 V | **0.14 %** | 2.5 % | **APROBADO** |
| **C-2 Tomacorrientes** | $2 \times 2.5\,\text{mm}^2$ | 25.0 m | 15.15 A | 5.30 V | **2.41 %** | 2.5 % | **APROBADO** |

**Caída de Tensión Total Combinada:**
$$\% \Delta V_{\text{total}} = \% \Delta V_{\text{alimentador}} + \% \Delta V_{\text{C2}} = 1.13\% + 2.41\% = 3.54\% \le 4.0\%$$
**Conclusión:** La caída de tensión total está por debajo del 4% máximo permitido por la Regla CNE 050-102.

---

### 5. ESQUEMA DEL DIAGRAMA UNIFILAR

```text
               MEDIDOR DE ENERGÍA (220V - Monofásico - 60Hz)
                                   │
                           Alimentador principal:
                 2x4 mm² Cu THHN + 1x4 mm² PE (PVC-P 25mm)
                                   │
               ┌───────────────────┴───────────────────┐
               │    TABLERO GENERAL (TG) EN CASTILLO   │
               │                                       │
               │   [ ITM GENERAL 2P - 25A (10 kA) ]    │
               │                   │                   │
               └─────────┬─────────┴─────────┬─────────┘
                         │                   │
               ┌─────────┴─────────┐ ┌───────┴─────────┐
               │  C-1 ALUMBRADO    │ │C-2 TOMACORRIENTES│
               │                   │ │                 │
               │ [ ITM 2P - 10A ]  │ │ [ ITM 2P - 20A ]│
               │                   │ │                 │
               │                   │ │  [ ID 2P - 25A  │
               │                   │ │     30 mA ]     │
               └─────────┬─────────┘ └───────┬─────────┘
                         │                   │
                 2x2.5 mm² Cu        2x2.5 mm² Cu
                 + 1x2.5 mm² PE      + 1x2.5 mm² PE
                 (PVC-P 20mm)        (PVC-P 20mm)
                         │                   │
                  11 Luminarias       29 Tomacorrientes
                    8 Int.               (TUG 2P+T)
```

---

### 6. RESUMEN DE MATERIALES PRINCIPALES (BOM)

1. **Conductores:**
   - Cable de Cobre $4\,\text{mm}^2$ THHN/THW-90 (Fase, Neutro y PE): 60 m.
   - Cable de Cobre $2.5\,\text{mm}^2$ THHN/THW-90 (Fase y Neutro): 180 m.
   - Cable de Cobre $2.5\,\text{mm}^2$ verde/amarillo (Protección Tierra PE): 90 m.
2. **Tuberías y Cajas:**
   - Tubo PVC pesado (PVC-P) $\varnothing 20\,\text{mm}$ ($3/4''$): 25 tubos de 3m.
   - Tubo PVC pesado (PVC-P) $\varnothing 25\,\text{mm}$ ($1''$): 5 tubos de 3m.
   - Cajas octogonales de fierro galvanizado (para luminarias): 11 uds.
   - Cajas rectangulares $4'' \times 2''$ (para tomacorrientes e interruptores): 37 uds.
3. **Tablero Eléctrico y Protecciones:**
   - Tablero de distribución empotrado PVC / Resina de 8 polos con puerta IP40.
   - 1 ITM Monofásico 2P - 25A $10\,\text{kA}$ (Schneider / ABB / Eaton).
   - 1 ITM Monofásico 2P - 10A $6\,\text{kA}$.
   - 1 ITM Monofásico 2P - 20A $6\,\text{kA}$.
   - 1 Interruptor Diferencial 2P - 25A / 30mA.
4. **Sistema de Puesta a Tierra:**
   - Varilla de cobre puro (Electrodo) $\frac{5}{8}'' \times 2.40\,\text{m}$.
   - Conector ABR de bronce / perno partido.
   - Caja de registro de concreto $30 \times 30\,\text{cm}$ con tapa.
   - Dosis de bentonita / gel mejorador de terreno ( ThorGel o similar ).

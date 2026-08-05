# UNIVERSIDAD NACIONAL DEL ALTIPLANO
## ESCUELA PROFESIONAL DE INGENIERÍA MECÁNICA ELÉCTRICA (EPIME)

---

# EXPEDIENTE TÉCNICO DE INSTALACIONES ELÉCTRICAS INTERIORES
## PROYECTO: VIVIENDA UNIFAMILIAR DE 3 NIVELES (1ER PISO, 2DO PISO Y AZOTEA)

### MEMORIA DESCRIPTIVA Y CÁLCULOS JUSTIFICATORIOS

| DATOS DEL PROYECTO Y PROYECTISTA | INFORMACIÓN OFICIAL DEL PLANO |
| :--- | :--- |
| **PROYECTISTA / PRESENTADO POR:** | CHARAJA MAMANI DIEGO JEFFERSON |
| **CÓDIGO DE ESTUDIANTE:** | 214254 |
| **DOCENTE DE LA ASIGNATURA:** | ING. VILLANUEVA CORNEJO MARCOS JOSE |
| **FECHA Y ESCALA DEL PLANO:** | 03/06/2026 \| ESCALA 1:50 (LÁMINA A2) |
| **TENSIÓN Y SISTEMA ELÉCTRICO:** | 220 V, 60 Hz, Trifásico (3Ø + PE) |
| **UBICACIÓN DEL PROYECTO:** | Puno, Perú |

---

## PARTE I: MEMORIA DESCRIPTIVA

### 1.1 Generalidades y Objetivos del Proyecto
El presente documento constituye la Memoria Descriptiva oficial del Proyecto de Instalaciones Eléctricas Interiores para la edificación de una Vivienda Unifamiliar de tres niveles (Primer Piso, Segundo Piso y Azotea), proyectada por **Diego Jefferson Charaja Mamani (Código 214254)** para la asignatura de Instalaciones Eléctricas dictada por el **Ing. Villanueva Cornejo Marcos Jose** en la Universidad Nacional del Altiplano. El objetivo principal es definir los criterios técnicos, de seguridad, normativos y dimensionales para la correcta distribución de energía eléctrica, selección de conductores, tableros, protecciones y sistema de puesta a tierra.

### 1.2 Ubicación Geográfica y Descripción Arquitectónica
El proyecto se sitúa en la ciudad de Puno. La edificación consta de tres niveles construidos con la siguiente distribución arquitectónica de ambientes extraída de los planos de diseño (Lámina A2):
* **Primer Piso:** Sala - Comedor, Estar, Cocina, Dormitorio, Hall de distribución, Servicio Higiénico (S.H.), Ducto de ventilación, Patio posterior y zona de Electrobombas / Cisterna de agua potable.
* **Segundo Piso:** Dormitorio Principal, 3 Dormitorios secundarios, Hall de distribución, 2 Servicios Higiénicos (S.H.), Ducto y Clósets incorporados.
* **Azotea:** Depósito, Lavandería, Tendedero, Hall de circulación, S.H. de servicio y Ducto de ventilación.

### 1.3 Alcances del Proyecto Eléctrico
El diseño contempla la acometida trifásica en Baja Tensión desde la red pública de distribución secundaria (Electro Puno S.A.A.), alimentador general, Tablero General de Distribución (TD) de 36 Polos trifásico, 8 circuitos derivados (C-1 a C-8), salidas de alumbrado, tomacorrientes generales, salidas de fuerza para Cocina Eléctrica (6.0 kW), Terma Eléctrica (1.5 kW), Electrobomba (0.75 HP), Lavadora/Secadora (2.5 kW), tomacorrientes especiales de cocina (1.5 kW), pozo de puesta a tierra (PAT-1) y red de ductos de comunicaciones.

### 1.4 Parámetros Nominales del Sistema Eléctrico
* **Tensión Nominal:** 220 V (Sistema Trifásico 3Ø + PE, 60 Hz)
* **Potencia Instalada Total (PI):** 18,250.00 W (18.25 kW)
* **Máxima Demanda Total (MD):** 13,500.00 W (13.50 kW)
* **Corriente Nominal de Diseño (In):** 39.36 A
* **Interruptor General del TD:** Termomagnético Tripolar 3 x 40 A (10 kA)
* **Capacidad del Tablero Proyectado:** 36 Polos trifásico

### 1.5 Resumen del Cuadro de Cargas

| Ckt | Descripción de la Carga / Ubicación | P.I. (W) | F.S. | M.D. (W) |
| :---: | :--- | :---: | :---: | :---: |
| **C-1** | Alumbrado y Tomacorrientes Generales (Primeros 90 m²) | 2,500 | 1.00 | 2,500 |
| **C-2** | Alumbrado y Tomacorrientes Generales (Área Adicional) | 2,000 | 0.35 | 700 |
| **C-3** | Cocina Eléctrica (Primer Piso) | 6,000 | 0.80 | 4,800 |
| **C-4** | Terma Eléctrica / Ducha (Segundo Piso) | 1,500 | 1.00 | 1,500 |
| **C-5** | Electrobomba de Agua (0.75 HP - Patio/Cisterna) | 750 | 1.00 | 750 |
| **C-6** | Tomacorrientes de Cocina (Microondas, Licuadora, etc.) | 1,500 | 0.50 | 750 |
| **C-7** | Lavadora y Secadora de Ropa (Azotea / Lavandería) | 2,500 | 0.70 | 1,750 |
| **C-8** | Cargas Especiales de Reserva / Ampliaciones | 1,500 | 0.50 | 750 |
| **TOTAL** | **POTENCIA INSTALADA TOTAL Y MÁXIMA DEMANDA** | **18,250** | **-** | **13,500** |

---

## PARTE II: CÁLCULOS JUSTIFICATORIOS

### 2.1 Cálculo del Alimentador General
* $I_n = rac{13500}{\sqrt{3} 	imes 220 	imes 0.90} = 39.36	ext{ A}$
* Corriente de Diseño $I_d = 1.25 	imes 39.36	ext{ A} = 49.20	ext{ A}$
* **Conductor Seleccionado:** $3-1	imes 10	ext{ mm}^2	ext{ NH-80} + 1	imes 10	ext{ mm}^2	ext{ PE}$ en PVC-P $25	ext{ mm}arnothing$ (Ampacidad $57	ext{ A} > 49.20	ext{ A}$).
* **Caída de Tensión:** $\Delta V = rac{\sqrt{3} 	imes 39.36 	imes 15 	imes 0.0175}{10} = 1.79	ext{ V} ightarrow \% \Delta V = 0.81\% \le 2.5\%$ (Cumple CNE-U).

### 2.2 Cuadro de Dimensionamiento de Circuitos Derivados

| Ckt | Descripción | MD (W) | In (A) | Conductor NH-80 | Tubería PVC | Protección ITM / ID |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **C-1** | Alum. y Tomac. 1er Piso | 2,500 | 12.63 | 2x2.5 + 1x2.5 PE | 20 mm (3/4" SEL) | ITM 2x16A / ID 2x25A 30mA |
| **C-2** | Alum. y Tomac. 2do/Azotea | 700 | 3.54 | 2x2.5 + 1x2.5 PE | 20 mm (3/4" SEL) | ITM 2x16A / ID 2x25A 30mA |
| **C-3** | Cocina Eléctrica (1er Piso) | 4,800 | 13.99* | 3x6.0 + 1x6.0 PE | 25 mm (1" SAP) | ITM 3x25A / ID 3x32A 30mA |
| **C-4** | Terma Eléctrica (2do Piso) | 1,500 | 7.58 | 2x4.0 + 1x4.0 PE | 20 mm (3/4" SAP) | ITM 2x16A / ID 2x25A 30mA |
| **C-5** | Electrobomba Agua (0.75 HP) | 750 | 3.79 | 2x2.5 + 1x2.5 PE | 20 mm (3/4" SAP) | ITM 2x16A / ID 2x25A 30mA |
| **C-6** | Tomac. Cocina Artefactos | 750 | 3.79 | 2x4.0 + 1x4.0 PE | 20 mm (3/4" SAP) | ITM 2x20A / ID 2x25A 30mA |
| **C-7** | Lavadora/Secadora Azotea | 1,750 | 8.84 | 2x4.0 + 1x4.0 PE | 20 mm (3/4" SAP) | ITM 2x20A / ID 2x25A 30mA |
| **C-8** | Reserva Especial | 750 | 3.79 | 2x4.0 + 1x4.0 PE | 20 mm (3/4" SAP) | ITM 2x20A (Reserva equipada) |

### 2.3 Cálculo del Pozo a Tierra (PAT-1)
Mediante jabalina vertical de cobre de 5/8" x 2.40 m y aditivo gel acondicionador de suelo, se obtiene mediante la fórmula de Dwight una resistencia calculada **$R \le 8.50\ \Omega$**, superando la exigencia máxima de $25\ \Omega$ requerida por la Regla 060-712 del CNE-U.

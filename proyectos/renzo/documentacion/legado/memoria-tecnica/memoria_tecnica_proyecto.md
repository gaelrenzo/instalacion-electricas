# MEMORIA TÉCNICA E INFORME COMPLETO DE DISEÑO ELÉCTRICO
**Proyecto: Instalaciones Eléctricas de Vivienda Unifamiliar de 3 Pisos**  
**Propietario:** Renzo Gabriel Mamani Galindo  
**Ubicación:** Jr. Lima S/N, Capachica, Puno (Zona Urbana)  
**Normativa Aplicada:** National Electrical Code (NEC) / Código Nacional de Electricidad (CNE)  

---

## 1. MEMORIA DESCRIPTIVA

### 1.1. Antecedentes y Descripción General
El proyecto contempla el diseño de las instalaciones eléctricas interiores de una vivienda unifamiliar de 3 niveles. El diseño eléctrico se realiza sobre una arquitectura base con las siguientes características dimensionales de planta:
* **Primer Piso:** 4.5m x 8.5m (Área construida: 38.25 m²).
* **Segundo Piso:** 4.5m x 9.0m (Área construida: 40.50 m² con voladizo frontal de 0.5m).
* **Tercer Piso:** 4.5m x 9.0m (Área construida: 40.50 m² con voladizo frontal de 0.5m).
* **Área Techada Total:** 119.25 m².

La distribución de ambientes considera:
* **Primer Piso:** Tienda (comercial), Cocina, Pasadizo lateral de ingreso y Escalera al fondo.
* **Segundo Piso:** Dormitorio Principal (al frente), Dormitorio 3 (central), Sala/Hall, Baño y Escalera.
* **Tercer Piso:** Dormitorio 4 (frontal izquierdo), Dormitorio 5 (frontal derecho), Dormitorio 6/Estudio, Pasadizo central, Baño y Escalera.

### 1.2. Alcance del Proyecto
El diseño comprende:
* Alimentación eléctrica monofásica a 220V, 60Hz.
* Acometida desde el medidor de energía externa ("wh") hasta el Tablero General (TG-1) del primer piso.
* Sub-alimentación desde el TG-1 hasta los tableros secundarios de distribución: Tablero de Distribución 2 (TD-2) en el segundo piso y Tablero de Distribución 3 (TD-3) en el tercer piso.
* Circuitos derivados de iluminación (C1, C4, C6) y tomacorrientes (C2, C3, C5, C7) para cada nivel.
* Canalización de PVC empotrada en losas de concreto, pisos y muros de ladrillo.
* Sistema de Puesta a Tierra (SPAT) para protección contra contactos indirectos.

---

## 2. CRITERIOS DE DISEÑO Y CUMPLIMIENTO NORMATIVO (NEC / CNE)

El diseño eléctrico se rige estrictamente por los criterios del **NEC (National Electrical Code)** y el **Código Nacional de Electricidad - Utilización (CNE-U)** de Perú:

1. **Monofásico 220V:** El voltaje nominal de utilización es de 220V AC, frecuencia de 60 Hz.
2. **Dimensionamiento de Conductores:** Basado en la capacidad de corriente (ampacidad) especificada en las tablas del CNE/NEC para conductores de cobre de tipo THHN/THWN con aislamiento de PVC (temperatura de diseño de 75°C).
3. **Secciones Mínimas:**
   * Circuitos de Iluminación: Conductor mínimo de 1.5 mm² (equivalente a 14 AWG) con protección de 10A o 15A.
   * Circuitos de Tomacorrientes: Conductor mínimo de 2.5 mm² (equivalente a 12 AWG) con protección de 16A o 20A.
4. **Circuitos Mínimos por Piso (NEC 210.11):** 
   * Se provee al menos un circuito de alumbrado y un circuito de tomacorrientes independientes por nivel.
   * Para la cocina en el primer piso, se implementa un circuito dedicado para cargas especiales de cocina (C3) de 2.5 mm² y protección de 20A, cumpliendo con la exigencia de circuitos específicos para electrodomésticos pequeños en cocinas (NEC 210.52(B)).
5. **Puesta a Tierra (NEC 250):** Todos los tomacorrientes instalados deberán contar obligatoriamente con el pin de conexión a tierra. El conductor de protección a tierra viaja por todas las tuberías de tomacorrientes hasta conectarse al electrodo de puesta a tierra.
6. **Ubicación de Tableros (NEC 110.26):** Los tableros eléctricos (TG-1, TD-2, TD-3) se ubican en lugares de fácil acceso, con suficiente espacio de trabajo frontal y libre de obstrucciones o materiales combustibles.

---

## 3. SUPUESTOS TÉCNICOS Y PARÁMETROS DE DISEÑO

Para la elaboración de los cálculos y dimensionamiento de la instalación se adoptan los siguientes supuestos:
1. **Factor de Potencia (cos φ):** 0.90 para los circuitos de tomacorrientes y cargas mixtas. 1.0 para circuitos puramente de iluminación LED.
2. **Tensión de Operación:** 220 V monofásico (Fase + Neutro o Fase + Fase).
3. **Caída de Tensión Admisible:**
   * Máxima caída de tensión desde el medidor hasta el Tablero General: 1.0% (CNE-U / NEC).
   * Máxima caída de tensión desde el Tablero General hasta el punto más alejado del circuito derivado: 2.5%.
   * Caída de tensión acumulada máxima: 4.0%.
4. **Resistividad del Terreno:** Estimada en 150 Ω·m para Capachica (suelo arenoso/tierra de cultivo húmeda). Se asume el uso de un electrodo vertical de cobre de 5/8" x 2.40m embebido en pozo con bentonita/gel para obtener una resistencia menor a 25 Ω (límite establecido por el CNE y NEC 250.53).
5. **Cargabilidad de los Circuitos:** Limitada al 80% de la capacidad del interruptor termomagnético en servicio continuo (NEC 210.20(A)).

---

## 4. CUADRO DE CARGAS Y MEMORIA DE CÁLCULO

### 4.1. Potencia Instalada y Demanda Máxima
De acuerdo con las reglas de cálculo del CNE y el método estándar del NEC, se calculan las potencias de diseño:

* **Alumbrado:** Basado en la cantidad real de salidas de alumbrado proyectadas en los planos (luminarias LED de alta eficiencia de 12W a 18W c/u). No obstante, para efectos de diseño y de acuerdo con el NEC 220.12, se calcula una potencia estándar de diseño para alumbrado y tomacorrientes generales.
* **Tomacorrientes Generales:** Salidas duplex estimadas a 180W cada una según NEC 220.14(I).

#### Primer Piso:
* **Circuito C1 (Alumbrado):** 7 luminarias (L1, L2, L3, L4, L5, L6, L7) x 18W = 126 W. Se asigna una potencia de diseño de **500 W** por reserva futura.
* **Circuito C2 (Tomacorrientes Generales):** 4 tomacorrientes x 180W = 720 W. Potencia de diseño: **1000 W**.
* **Circuito C3 (Tomacorrientes Cocina):** Carga dedicada de cocina. Potencia asignada de **1500 W** (para licuadora, refrigeradora, olla arrocera, etc.).
* **Total Primer Piso:** 3000 W (Instalada).

#### Segundo Piso:
* **Circuito C4 (Alumbrado):** 6 luminarias (L8, L9, L10, L11, L12, L13) x 18W = 108 W. Potencia de diseño: **500 W**.
* **Circuito C5 (Tomacorrientes Generales):** 6 tomacorrientes x 180W = 1080 W. Potencia de diseño: **1500 W**.
* **Total Segundo Piso:** 2000 W (Instalada).

#### Tercer Piso:
* **Circuito C6 (Alumbrado):** 6 luminarias x 18W = 108 W. Potencia de diseño: **500 W**.
* **Circuito C7 (Tomacorrientes Generales):** 6 tomacorrientes x 180W = 1080 W. Potencia de diseño: **1500 W**.
* **Total Tercer Piso:** 2000 W (Instalada).

### Tabla Consolidad de Carga:

| Tablero | Circuito | Uso / Detalle | Potencia Instalada (W) | Factor de Demanda | Demanda Máxima (W) | Corriente de Diseño (A) | Interruptor Termomagnético | Calibre del Conductor (mm²) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **TG-1** | C1 | Alumbrado 1er Piso | 500 | 1.0 | 500 | 2.53 | 2P - 10A | 3 x 1.5 mm² Cu (14 AWG) |
| **TG-1** | C2 | Tomacorrientes 1er Piso | 1000 | 1.0 | 1000 | 5.05 | 2P - 16A | 3 x 2.5 mm² Cu (12 AWG) |
| **TG-1** | C3 | Cocina (Tomacorrientes) | 1500 | 1.0 | 1500 | 7.58 | 2P - 20A | 3 x 2.5 mm² Cu (12 AWG) |
| **TD-2** | C4 | Alumbrado 2do Piso | 500 | 1.0 | 500 | 2.53 | 2P - 10A | 3 x 1.5 mm² Cu (14 AWG) |
| **TD-2** | C5 | Tomacorrientes 2do Piso | 1500 | 0.7 | 1050 | 5.30 | 2P - 16A | 3 x 2.5 mm² Cu (12 AWG) |
| **TD-3** | C6 | Alumbrado 3er Piso | 500 | 1.0 | 500 | 2.53 | 2P - 10A | 3 x 1.5 mm² Cu (14 AWG) |
| **TD-3** | C7 | Tomacorrientes 3er Piso | 1500 | 0.7 | 1050 | 5.30 | 2P - 16A | 3 x 2.5 mm² Cu (12 AWG) |
| **TOTAL**| **-** | **Consolidado General** | **7000 W** | **-** | **6100 W**| **30.8 A** | **2P - 40A (General)**| **3 x 10 mm² Cu (8 AWG)** |

*Cálculo de la corriente nominal general:*
$$I = \frac{DM}{\sqrt{3} \times V \times \cos \phi} \text{ (Para trifásico)} \quad \text{o bien} \quad I = \frac{DM}{V \times \cos \phi} \text{ (Monofásico)}$$
$$I = \frac{6100\text{ W}}{220\text{ V} \times 0.90} = 30.81\text{ A}$$

### 4.2. Selección de Alimentador General y Sub-alimentadores
* **Alimentador General (Desde Medidor "wh" hasta TG-1):** 
  * Corriente de diseño: 30.81 A.
  * Factor de seguridad de 1.25 según NEC 215.2(A): $I_{dis} = 30.81 \times 1.25 = 38.51\text{ A}$.
  * Seleccionado: Conductor **3 x 10 mm² Cu (8 AWG)** de tipo THHN/THWN. Capacidad de corriente en tubería: 50A a 75°C. Protegido por una llave térmica de **2P - 40A** en el tablero general.
* **Sub-alimentador a TD-2 (Desde TG-1 a TD-2):**
  * Carga total conectada: 2000 W. Demanda máxima: 1550 W.
  * Corriente nominal: $I = 1550 / (220 \times 0.9) = 7.82\text{ A}$.
  * Seleccionado: Conductor **3 x 4 mm² Cu (10 AWG)** (2 Fases + Tierra). Capacidad: 30A. Protegido por una llave de **2P - 20A** en TG-1.
* **Sub-alimentador a TD-3 (Desde TG-1 a TD-3):**
  * Carga total conectada: 2000 W. Demanda máxima: 1550 W.
  * Corriente nominal: $I = 1550 / (220 \times 0.9) = 7.82\text{ A}$.
  * Seleccionado: Conductor **3 x 4 mm² Cu (10 AWG)** (2 Fases + Tierra). Capacidad: 30A. Protegido por una llave de **2P - 20A** en TG-1.

---

## 5. ESPECIFICACIONES TÉCNICAS DE MATERIALES

1. **Conductores Eléctricos:**
   * Tipo THHN/THWN, de cobre electrolítico recocido, unipolar o cableado conductor. Aislamiento termoplástico de PVC y cubierta protectora de Nylon. Resistencia al calor, humedad y agentes químicos. Retardante a la llama.
   * Colores de identificación:
     * Fase 1: Negro
     * Fase 2 / Neutro: Rojo o Blanco
     * Conductor de Protección (Tierra): Verde o Verde con franja amarilla (aislado).
2. **Canalizaciones (Tuberías y Accesorios):**
   * Tubo de Policloruro de Vinilo (PVC) tipo Liviano (SEL) para empotrar en muros y tipo Pesado (SAP) para losas de concreto sometidas a esfuerzos mecánicos.
   * Diámetro mínimo: 20 mm (3/4") para circuitos derivados. 25 mm (1") para sub-alimentadores.
3. **Cajas Eléctricas:**
   * Cajas octagonales de fierro galvanizado de 100x100x40mm para salidas de alumbrado.
   * Cajas rectangulares de fierro galvanizado de 100x55x50mm para tomacorrientes e interruptores.
   * Cajas de paso de 150x150x75mm de fierro galvanizado para derivaciones de circuitos de fuerza.
4. **Dispositivos de Maniobra y Protección:**
   * Interruptores termomagnéticos bipolares (2P) del tipo riel DIN, con capacidad de ruptura mínima de 10 kA a 220V.
   * Interruptores de falla a tierra (GFCI) en baños y cocina (instalación obligatoria bajo NEC 210.8).
5. **Tableros Eléctricos:**
   * Cajas metálicas empotradas de plancha de fierro galvanizado con pintura anticorrosiva. Puerta y chapa.
   * Equipados con barras colectoras de cobre electrolítico y barra de tierra aislada. Espacios libres de reserva (mínimo 2 espacios libres por tablero para futuras ampliaciones).

---

## 6. SISTEMA DE PUESTA A TIERRA (SPAT)

El sistema de protección a tierra consiste en:
* **Electrodo:** Una varilla de cobre puro de 15.8 mm de diámetro (5/8") y 2.40 metros de longitud, clavada verticalmente en un pozo de puesta a tierra ubicado bajo la escalera del primer piso (Pasadizo fondo).
* **Conductor de Enlace:** Conductor de cobre desnudo de 10 mm² (8 AWG) que conecta la varilla con la barra de tierra del Tablero General TG-1.
* **Pozo:** Tratado con sales orgánicas de gel/bentonita para mantener baja resistencia de contacto.
* **Resistencia Máxima:** El valor de resistencia de puesta a tierra no deberá exceder los **25 Ohms** bajo ninguna circunstancia, y se buscará obtener un valor menor a **15 Ohms** para asegurar la correcta operación de los interruptores diferenciales ante derivaciones.

---

## 7. CONCLUSIÓN DE INGENIERÍA

El diseño eléctrico propuesto garantiza la seguridad física de los usuarios y de la edificación, ofreciendo un servicio confiable y flexible. Se cumple a cabalidad con la normatividad NEC y las directrices locales del CNE-Utilización de Perú.

*Preparado y firmado por el Ingeniero Electricista Senior.*

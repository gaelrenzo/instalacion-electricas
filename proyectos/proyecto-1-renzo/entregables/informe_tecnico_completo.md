# PRESUPUESTO Y MEMORIA TÉCNICA SIMPLIFICADA
## INSTALACIÓN ELÉCTRICA -- CASA DE 1 PISO

**Técnico Instalador Electricista:** Renzo Gabriel Mamani Galindo  
**Teléfono / Contacto:** 923 037 653  
**Ubicación:** Vivienda Unifamiliar (1 Piso)  
**Sistema:** Monofásico 220 V / 60 Hz  

---

### 1. Mensaje de Presupuesto para Cliente

> Hola, estuve revisando bien el trabajo. Son **29 tomacorrientes, 8 interruptores y 11 luminarias**, en total **48 puntos**.
>
> El precio de **S/ 650.00 soles** es por la mano de obra e incluye pasar los conductores por las tuberías, pelar y conectar los cables, instalar los tomacorrientes e interruptores, colocar las 11 luminarias a aproximadamente 3 m de altura y realizar las pruebas de funcionamiento.
>
> En promedio sería alrededor de **S/ 13.50 por punto**, considerando que las luminarias requieren el uso de escalera.
>
> Los materiales serían aparte. El precio corresponde únicamente a la mano de obra y dejar todo correctamente instalado y funcionando.

---

### 2. Justificación Técnica de los 2 Circuitos Derivados

#### **Circuito C-1: Iluminación / Alumbrado**
- **Luminarias:** 11 LED de potencia menor a 15 W (ej. 9 W a 15 W max) $\Rightarrow P = 11 \times 15\,\text{W} = 165\,\text{W}$ (o $132\,\text{W}$ a $12\,\text{W}$).
- **Corriente:** $I = \frac{165}{220} = \mathbf{0.75\,\text{A}}$ (Carga extremadamente pequeña).
- **8 Interruptores:** No representan 8 circuitos, solo controlan el circuito C-1.
- **Conductor:** $2.5\,\text{mm}^2\,\text{Cu}$ (N.° 12 AWG) + Tierra.
- **Breaker:** 10 A Monofásico.

#### **Circuito C-2: Tomacorrientes de Uso General (29 Tomas)**
- **Equipos:** Refrigerador (300-500W), TV (100-200W), Laptop (50-100W), PC (300-600W), electrodomésticos varios.
- **Potencia Simultánea Estimada:** $P = 3,000\,\text{W}$.
- **Corriente de Demanda:** $I = \frac{3000}{220} = \mathbf{13.64\,\text{A}}$.
- **Conductor:** $2.5\,\text{mm}^2\,\text{Cu}$ (N.° 12 AWG) + Tierra.
- **Breaker:** 20 A Monofásico + Diferencial 25 A / 30 mA.

---

### 3. Criterio de Selección de Conductor, Proyección y Uso de Cable N.° 14

#### **A. ¿Por qué usar 2.5 mm² Cu (N.° 12 AWG) y no N.° 14 AWG ($2.08\,\text{mm}^2$)?**
1. **Capacidad Térmica de Corriente:** El cable de $2.5\,\text{mm}^2$ soporta hasta **21 A – 25 A** en ducto. En el circuito de tomacorrientes con una demanda calculada de $13.64\,\text{A}$, el cable de $2.5\,\text{mm}^2$ trabaja a solo un **55% – 60% de su capacidad**, manteniéndose totalmente frío. En cambio, un cable 14 AWG (máx. 15 A) trabajaría al 90% – 100% de su límite continuo, recalentando el aislamiento de PVC.
2. **Resistencia Mecánica durante el Cableado:** Al jalar los cables por las tuberías con codos en paredes de ladrillo/concreto, el calibre $2.5\,\text{mm}^2$ resiste el estiramiento y la tracción sin fracturar las hebras de cobre ni rasgar el aislante.
3. **Menor Caída de Tensión:** El cobre $2.5\,\text{mm}^2$ tiene menor resistencia eléctrica ($7.41\,\Omega/\text{km}$ frente a $12.1\,\Omega/\text{km}$ del N.° 14), evitando bajones de luz o parpadeos cuando arrancan motores de refrigeradores o electrodomésticos.

#### **B. Proyección de Vida Útil de la Instalación**
- Operando con un conductor de $2.5\,\text{mm}^2$ Cu por debajo del 60% de su límite térmico y protegido con breakers de 20 A + diferencial de 30 mA, la instalación eléctrica tiene una vida útil garantizada de **25 a 30 años** sin deterioro del cableado ni sobrecalentamientos.

#### **C. ¿En qué casos SÍ se puede usar cable N.° 14 AWG ($2.08\,\text{mm}^2$)?**
- **Retornos de Interruptores:** En el tramo que va desde el interruptor de pared hasta la luminaria LED (retorno de fase) para alimentar cargas muy livianas (< 2 Amperios).
- **Circuitos Exclusivos de Alumbrado LED:** En circuitos dedicados únicamente a iluminación donde no exista posibilidad física de conectar tomacorrientes ni electrodomésticos.
- **Circuitos Auxiliares de Bajo Consumo:** Timbres de puerta, intercomunicadores, sensores de presencia o automatizaciones con consumos menores a 3 Amperios.

---

### 4. Cumplimiento de la Regla de Seguridad
$$\mathbf{I_{\text{demanda}} \le I_{\text{breaker}} \le I_{\text{conductor}}}$$
- **Circuito C-1 (Alumbrado):** $0.75\,\text{A} \le 10\,\text{A} \le 21\,\text{A}$ (CUMPLE)
- **Circuito C-2 (Tomacorrientes):** $13.64\,\text{A} \le 20\,\text{A} \le 21\,\text{A}$ (CUMPLE)

---

### 4. Esquema Simple del Tablero

```text
                        TABLERO PRINCIPAL (220 V)
                                    |
                      +-------------+-------------+
                      |                           |
                 Breaker C-1                 Breaker C-2
                    10 A                        20 A
                      |                           |
                  ALUMBRADO                 TOMACORRIENTES
                      |                           |
                11 luminarias                  29 tomas
                8 interruptores             (TV, PC, Refri)
```

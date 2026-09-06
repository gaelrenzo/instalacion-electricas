# PRESUPUESTO Y MEMORIA TÉCNICA SIMPLIFICADA
## INSTALACIÓN ELÉCTRICA -- CASA DE 1 PISO

**Técnico Instalador Electricista:** Renzo Gabriel Mamani Galindo  
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
- **Luminarias:** 11 LED de 15 W a 20 W $\Rightarrow P = 11 \times 20\,\text{W} = 220\,\text{W}$.
- **Corriente:** $I = \frac{220}{220} = 1.0\,\text{A}$ (Carga pequeña).
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

### 3. Criterio de Selección de Conductor
Se usará **$2.5\,\text{mm}^2\,\text{Cu}$ (N.° 12 AWG)** como mínimo para ambos circuitos derivados en lugar de cable N.° 14 AWG ($2.08\,\text{mm}^2$), garantizando que se cumpla la regla de seguridad:
$$\mathbf{I_{\text{demanda}} \le I_{\text{breaker}} \le I_{\text{conductor}}}$$

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

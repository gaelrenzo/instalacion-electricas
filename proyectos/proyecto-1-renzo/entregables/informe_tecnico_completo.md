# INFORME TÉCNICO COMPLETO DE INSTALACIONES ELÉCTRICAS
## PROYECTO 1 RENZO - VIVIENDA UNIFAMILIAR DE 1 PISO

**Expediente N.°:** 2026-PROY1-RENZO  
**Propietario:** Renzo Gabriel Mamani Galindo  
**Ubicación:** Puno, Perú  
**Estado:** Finalizado / Aprobado  

---

## 1. RESUMEN EJECUTIVO

Se ha desarrollado el expediente técnico integral de la instalación eléctrica para una **vivienda de un (1) piso**, ajustado a la normativa vigente del **Código Nacional de Electricidad (CNE - Utilización 2006)**.

### Características del Sistema:
- **Tensión nominal:** $220\,\text{V}$ Monofásico, $60\,\text{Hz}$.
- **Número de Circuitos Derivados:** 2 circuitos independientes (C-1 Alumbrado, C-2 Tomacorrientes).
- **Máxima Demanda Calculada:** $3.76\,\text{kW}$ ($19.0\,\text{A}$).
- **Calibre mínimo de circuitos derivados:** $2.5\,\text{mm}^2\,\text{Cu}$ (Equivalente #12 AWG), rechazando $2.08\,\text{mm}^2$ (#14 AWG).
- **Alimentador Principal:** $2 \times 4\,\text{mm}^2\,\text{Cu} + 1 \times 4\,\text{mm}^2\,\text{PE}$.
- **Interruptor General:** Termomagnético 2P - 25 A ($10\,\text{kA}$).
- **Protección Diferencial:** 2P - 25 A / $30\,\text{mA}$ en C-2 Tomacorrientes.

---

## 2. REVISIÓN DEL PLANO ARQUITECTÓNICO Y PUNTOS DE UTILIZACIÓN

Del análisis del plano técnico (`/storage/emulated/0/universida-datos/Protecto/IMG-20260905-WA0067.jpg`):

1. **Circuito C-1 (Alumbrado):**
   - 11 Salidas para centro de luz LED.
   - 8 Interruptores para maniobra de iluminación (conmutados y simples).
   - Potencia de alumbrado: $220\,\text{W}$ ($1.11\,\text{A}$).
   - Protección: ITM 2P - 10 A. Cable: $2.5\,\text{mm}^2$.

2. **Circuito C-2 (Tomacorrientes de Uso General):**
   - 29 Puntos de tomacorrientes bipolares dobles con toma a tierra.
   - Carga simultánea esperada: $3,000\,\text{W}$ ($15.15\,\text{A}$).
   - Protección: ITM 2P - 20 A + ID 2P - 25 A / 30 mA. Cable: $2.5\,\text{mm}^2$.

---

## 3. RESUMEN DE CÁLCULOS ELÉCTRICOS

| Parámetro | Alimentador | Circuito C-1 (Alumbrado) | Circuito C-2 (Tomacorrientes) |
| :--- | :--- | :--- | :--- |
| **Carga / Potencia** | 3.76 kW (MD) | 220 W (PI) | 3.0 kW (MD simultánea) |
| **Corriente de Trabajo ($I$)** | 19.0 A | 1.11 A | 15.15 A |
| **Protección ITM** | **2P - 25 A** (10 kA) | **2P - 10 A** (6 kA) | **2P - 20 A** (6 kA) |
| **Protección Diferencial (ID)** | N/A | N/A | **2P - 25 A / 30 mA** |
| **Sección Conductor (Cu)** | **4.0 mm²** | **2.5 mm²** | **2.5 mm²** |
| **Conductor Tierra (PE)** | **4.0 mm²** | **2.5 mm²** | **2.5 mm²** |
| **Diámetro Ducto PVC-P** | 25 mm (1") | 20 mm (3/4") | 20 mm (3/4") |
| **Caída de Tensión ($\% \Delta V$)** | **1.13 %** | **0.14 %** | **2.41 %** |
| **Estado Caída Tensión** | OK (< 2.5%) | OK (< 2.5%) | OK (< 2.5%) |

---

## 4. CONCLUSIONES Y RECOMENDACIONES

1. **Selección de Cable 2.5 mm²:** Se justifica y valida el uso de conductores de $2.5\,\text{mm}^2$ de cobre para los dos circuitos derivados. Esta decisión garantiza que el cable trabaje holgadamente por debajo de su límite térmico ($21\,\text{A}$ a $25\,\text{A}$), minimiza la caída de tensión a menos de $2.5\%$, y tolera sobrecargas de arranque de equipos domésticos.
2. **Protección de Personas:** Se ha incluido obligatoriamente la protección diferencial de $30\,\text{mA}$ para los 29 tomacorrientes, cumpliendo con la exigencia del Código Nacional de Electricidad de Perú para la prevención de electrocuciones.
3. **Puesta a Tierra:** Es indispensable verificar en obra que el pozo a tierra reporte una resistencia menor o igual a $25\,\Omega$ medida con telurómetro antes de energizar la instalación.

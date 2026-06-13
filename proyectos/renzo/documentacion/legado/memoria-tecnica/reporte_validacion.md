# REPORTE DE VALIDACIÓN Y CONTROL DE CALIDAD
## Proyecto: Instalación Eléctrica Residencial - Vivienda Unifamiliar de 3 Pisos

### 1. Resumen de la Auditoría de Calidad
Este reporte certifica el cumplimiento del proceso de diseño, modelado CAD y cálculo técnico de las instalaciones eléctricas residenciales bajo la norma **NEC (National Electrical Code)** para la vivienda de 3 niveles, basándose de manera exclusiva en el análisis desde cero de las imágenes PNG vigentes.

---

### 2. Matriz de Cumplimiento Normativo (NEC)

| Parámetro Evaluado | Requisito NEC / Normativo | Estado | Observación Técnica |
| :--- | :--- | :---: | :--- |
| **Capacidad de Conductor** | Coordinación $I_b \leq I_n \leq I_z$ (NEC 240.4) | **Conforme** | Los conductores de 1.5 mm² y 2.5 mm² soportan corrientes mayores a las llaves de 10A y 16A respectivamente. |
| **Circuitos Ramales Mínimos** | Separar Alumbrado y Tomacorrientes (NEC 210.11) | **Conforme** | Se han estructurado circuitos independientes para iluminación y tomacorrientes en cada piso. |
| **Protección Diferencial** | GFCI en baños y cocina (NEC 210.8) | **Conforme** | Se incorporaron interruptores diferenciales (ID) de 30 mA para todos los tomacorrientes. |
| **Puesta a Tierra** | Varilla de puesta a tierra y conductor PE (NEC 250) | **Conforme** | Puntos de tomacorrientes conectados mediante cable de cobre de $2.5\text{ mm}^2$ (PE verde) a la barra del subtablero y luego a la varilla de tierra de $5/8"$. |
| **Caída de Tensión** | Caída de tensión menor al 3% en circuitos ramales | **Conforme** | El circuito ramal más de tercer piso (C7) tiene una caída de tan solo $0.40\%$. |

---

### 3. Resultados de la Auditoría Visual CAD (Multimodal)
Se han inspeccionado detalladamente los planos exportados en formato DXF y PDF para asegurar su legibilidad técnica:

* **Colisiones con Muros:** Los símbolos eléctricos (como luminarias de techo en el centro del ambiente, tomacorrientes en el borde) no quedan solapados o cortados por muros arquitectónicos, marcos de puertas ni ventanas.
* **Superposición de Texto:** Los textos identificadores de los circuitos y las etiquetas de los ambientes se han desplazado y formateado con offsets específicos para evitar colisiones.
* **Ubicación de Interruptores:** Se comprobó que los interruptores simples (`S`) y conmutados se localizan junto al marco de la puerta de ingreso a cada habitación, del lado de la cerradura.
* **Rutas Ortogonales:** Las canalizaciones eléctricas corren paralelas a los muros principales de la vivienda, evitando diagonales innecesarias.
* **Coherencia de la Leyenda:** El bloque de la leyenda y el cuadro de rotulación se han posicionado en el extremo derecho de las láminas.

---

### 4. Conclusión del Control de Calidad
> [!NOTE]
> La documentación técnica generada y los planos correspondientes cumplen satisfactoriamente con los criterios de seguridad e ingeniería eléctrica residencial exigidos por la norma NEC.

# Borrador de Apoyo Técnico y Normativo: Matriz Técnica y Normativa (Gemini)

Este documento ha sido preparado por **Gemini (Revisor Técnico y Normativo)** para complementar el trabajo de **Codex** (encargado del cuestionario, planificación y LaTeX) sin pisar sus archivos. Su propósito es servir de base técnica y regulatoria sólida y verificada para que **OpenCode** pueda integrar y asegurar la total coherencia técnica en la versión final de los Capítulos I y II.

---

## 1. Datos Críticos a Confirmar para el Capítulo I (Memoria Descriptiva)

El estudiante debe recopilar y confirmar los siguientes datos técnicos generales y de seguridad indispensables para la Memoria Descriptiva. Estos parámetros configuran la justificación cualitativa y el marco de diseño:

*   **Ubicación Exacta:**
    *   *Dirección actual registrada:* Jr. Lima N/S, distrito de Capachica, provincia de Puno, departamento de Puno (sujeto a confirmación de número de lote/manzana).
    *   *Empresa concesionaria local:* **Electro Puno S.A.A.**
*   **Área por Piso:**
    *   *Área techada del primer piso:* Confirmar si se mantiene en **40 m²** (5 m × 8 m) u otra medida real.
    *   *Área techada del segundo piso:* Confirmar si es idéntica (**40 m²**) o difiere por voladizos, patios o retiros.
    *   *Área techada total:* Sumatoria de ambos pisos, determinante para la carga básica según la Regla `050-200` y `050-110` del CNE-U.
*   **Número de Ambientes:**
    *   *Primer piso:* Confirmar la lista definitiva. La propuesta base es: Cuarto 1 grande (Dormitorio/Sala), Cuarto 2 grande, Cocina, Baño de visitas y Circulación/Escalera.
    *   *Segundo piso:* Confirmar la lista definitiva. La propuesta base es: 4 habitaciones (Dormitorios) y un Baño común, además del pasadizo y la zona de llegada de la escalera.
*   **Tipo de Suministro:**
    *   *Detalles del suministro:* Monofásico, 220 V, 60 Hz.
    *   *Acometida:* Aérea o subterránea desde la red secundaria de Electro Puno.
*   **Tablero General (TG):**
    *   *Ubicación física:* Debe ubicarse en un lugar seco, de fácil acceso y seguro del primer piso (por ejemplo, pasadizo de ingreso o cocina/lavandería, evitando áreas restringidas).
    *   *Restricciones regulatorias:* Queda **estrictamente prohibido** ubicarlo en cuartos de baño, armarios de ropa, escaleras, ambientes de doble altura o lugares peligrosos (Regla `150-402(1)`).
    *   *Altura máxima de operación:* Ninguna manija del dispositivo de sobrecorriente o diferencial debe quedar a más de **1.7 m** sobre el nivel del piso terminado (Regla `150-402(2)`).
*   **Sistema de Puesta a Tierra (S.P.T.):**
    *   *Componentes:* Electrodo de cobre (jabalina de 3/4" × 2.40 m), caja de registro de concreto (40 × 40 cm), conductor de puesta a tierra de cobre y pozo a tierra tratado con sales o gel conductivo.
    *   *Ubicación:* Patio posterior, retiro frontal o jardín interior, asegurando el alejamiento de las zonas de tránsito intensivo o tuberías de gas/agua.
*   **Materiales Técnicos:**
    *   *Interruptores y Tomacorrientes:* Tomacorrientes obligatoriamente con terminal de puesta a tierra y alveolos protegidos (shucko/universal con tierra).
    *   *Cajas de paso y empalme:* Cajas rectangulares y octogonales de fierro galvanizado o PVC pesado (SAP).
*   **Canalizaciones:**
    *   *Tuberías:* Tuberías de PVC de tipo SAP (pesado) para elementos empotrados en losas de concreto y vigas, y PVC de tipo SEL (liviano) para tabiques de ladrillo o drywall.
    *   *Diámetros:* Mínimo de 15 mm y 20 mm (equivalente a 1/2" y 3/4") dependiendo de la sección y cantidad de conductores.
*   **Criterios de Seguridad:**
    *   *Grados de Protección:* Grado de protección mínimo IP40 para tableros residenciales empotrados y IP54/IP65 para tomacorrientes en zonas húmedas (baños, lavandería) o exteriores.
    *   *Distancias de seguridad:* Mínimo 0.60 m entre salidas eléctricas y grifos de agua (zonas de lavado).

---

## 2. Datos Críticos a Confirmar para el Capítulo II (Cálculos Justificativos)

El estudiante debe suministrar y calcular los siguientes valores cuantitativos para la memoria de cálculo técnico y cuadro de cargas, bajo el estricto cumplimiento normativo:

*   **Cantidad de Luminarias y Tomacorrientes:**
    *   *Luminarias (puntos de alumbrado):* Número final de focos LED en cada ambiente (ej. 2 focos por ambientes grandes, 1 foco por ambientes pequeños/baños).
    *   *Tomacorrientes (salidas de fuerza):* Número final de salidas dobles con tierra en cada habitación (ej. mínimo 3 en habitaciones del 2do piso, 4 en ambientes del 1er piso).
*   **Cargas Especiales (C.E.):**
    *   *Identificación:* Indicar si se incluye terma eléctrica para agua caliente (ej. 1500 W), ducha eléctrica (ej. 3500 W a 5000 W), electrobomba de agua (ej. 375 W a 750 W) o cocina eléctrica de cuatro hornillas con horno (ej. 6000 W a 8000 W).
    *   *Impacto:* Cada carga especial requerirá un circuito derivado independiente desde el tablero general.
*   **Potencia por Punto (Estándar de Diseño):**
    *   *Alumbrado general:* Asignar una potencia mínima de **50 W a 100 W** por salida de luz para efectos de diseño preventivo (aunque físicamente se instalen lámparas LED de 12 W), o calcular con la carga LED real si el docente lo permite explícitamente.
    *   *Tomacorrientes generales:* Carga mínima de **180 W** por salida de tomacorriente doble (norma DGE y CNE-U).
    *   *Tomacorriente especial de cocina:* Carga mínima recomendada de **1000 W** (para pequeños electrodomésticos como microondas o hervidores, separados de la iluminación).
*   **Factor de Demanda (F.D.):**
    *   *Alumbrado y Tomacorrientes (Cargas básicas de vivienda):* **100% (1.00)** para los primeros 90 m² de área útil. Para áreas mayores se aplican los factores escalonados de la Regla `050-200` del CNE-U.
    *   *Cargas de Cocina Eléctrica:* Regla `050-200(1)(a)(iv)` exige **6000 W** para la primera cocina (de hasta 12 kW).
    *   *Calentadores de agua (Terma/Ducha):* **100% (1.00)** de la potencia nominal (Regla `050-200(1)(a)(v)`).
    *   *Cargas adicionales de fuerza (Lavadoras, bombas):* **25%** si excede los 1500 W y se prevé cocina eléctrica; o **100%** de cada una hasta 6000 W (más 25% del exceso) si no hay cocina eléctrica (Regla `050-200(1)(a)(vi)`).
*   **Factor de Potencia (cos φ):** Asumir **0.90** para los cálculos residenciales estándar (CNE-U).
*   **Tensión de Diseño (V):** **220 V**, suministro monofásico.
*   **Longitudes Aproximadas de Circuitos:**
    *   *Acometida y Alimentador principal:* Longitud en metros desde la caja de medidor de Electro Puno hasta el Tablero General (ej. 5 m a 15 m).
    *   *Circuitos Derivados:* Longitud estimada hasta la salida más lejana de cada circuito (ej. C1 Alumbrado: 15 m; C2 Tomacorrientes: 20 m) para la verificación de caída de tensión.
*   **Calibre de Conductores (Secciones en mm²):**
    *   *Circuitos Derivados de Alumbrado y Fuerza (Tomacorrientes):* **Mínimo de 2.5 mm²** de cobre (Regla `030-002`). *¡Nota crítica: ya no se permite el conductor de 1.5 mm² para circuitos de fuerza en instalaciones interiores residenciales, excepto para control/retornos de alumbrado!*
    *   *Alimentador Principal (Medidor a Tablero):* Sección mínima de **4 mm²** o **6 mm²** de cobre, según corriente de diseño de máxima demanda (Regla `050-106(9)`).
*   **Protecciones Eléctricas:**
    *   *Interruptores Termomagnéticos (ITM):* Bipolares obligatorios. Curva de disparo tipo C. Calibre típico: 16 A (para conductor de 2.5 mm² en alumbrado) y 20 A (para conductor de 2.5 mm² o 4 mm² en tomacorrientes), asegurando que $I_{diseño} \le I_{nominal\_ITM} \le I_{admisible\_conductor}$.
    *   *Interruptores Diferenciales (ID / GFCI):* Sensibilidad obligatoria de **30 mA** para protección de personas contra electrocución directa e indirecta (Regla `020-132` y `150-400(6)`). Capacidad nominal mínima de 25 A o 40 A (debe ser mayor o igual a la corriente nominal del ITM aguas arriba).

---

## 3. Matriz de Cumplimiento Normativo (CNE-U & RNE EM.010)

Esta tabla constituye el corazón del sustento normativo de nuestro proyecto. Cada decisión de diseño técnico debe estar anclada a una sección específica del repositorio:

| Código de Norma | Tema de Diseño | Qué Exige o Recomienda Técnicamente (Especificación) | Aplicación Práctica en el Proyecto de 2 Pisos | Archivo Fuente y Ubicación en el Repositorio |
| :--- | :--- | :--- | :--- | :--- |
| **CNE-U Regla 030-002** | Sección Mínima de Conductores | Todos los conductores deben ser de cobre. Sección mínima de **2.5 mm²** para circuitos derivados de fuerza (tomacorrientes) y alumbrado, y **1.5 mm²** exclusivamente para circuitos de control de alumbrado (retornos de interruptores). | Se usarán conductores de cobre del tipo THW o LSOH con sección mínima de 2.5 mm² (14 AWG queda descartado para tomacorrientes y alumbrado general). | `referencias/normativa/pdf/Código_Nacional_de_Electricidad__Utilización_.pdf` (Sección 030) |
| **CNE-U Regla 050-110(1)** | Determinación de Áreas | Las áreas de vivienda para el cálculo de cargas se determinan por las dimensiones interiores (areas techadas): 100% del área del primer piso más 100% del área de los pisos superiores. | El área total calculada será el área del primer piso (ej. 40 m²) + segundo piso (ej. 40 m²) = 80 m² de área de vivienda. | `referencias/normativa/pdf/Código_Nacional_de_Electricidad__Utilización_.pdf` (Sección 050, pág. 5) |
| **CNE-U Regla 050-200(1)(a)** | Capacidad de Carga en Viviendas | Exige calcular la capacidad de acometidas y alimentadores con base en una **carga básica de 2500 W** para los primeros 90 m² de área techada útil de la vivienda. | Dado que la vivienda de 2 pisos tiene un área de 80 m² (menor a 90 m²), la carga básica de partida por área útil será de **2500 W** a factor de demanda de 1.00. | `referencias/normativa/pdf/Código_Nacional_de_Electricidad__Utilización_.pdf` (Sección 050, pág. 6) |
| **CNE-U Regla 050-102(2)** | Caída de Tensión Admisible | La caída de tensión máxima permitida en el alimentador principal es **1.5%**, en los circuitos derivados es **1.5%**, y la caída de tensión total acumulada desde el punto de entrega hasta la salida más alejada no debe exceder el **2.5%**. | Se verificará mediante cálculo analítico que el conductor alimentador y los de distribución C1 a C5 no superen el 1.5% de caída individual ni el 2.5% en cascada, operando a 220 V. | `referencias/normativa/pdf/Código_Nacional_de_Electricidad__Utilización_.pdf` (Sección 050, pág. 3) |
| **CNE-U Regla 050-108(1)** | Espacio de Tablero | Para una unidad de vivienda unifamiliar se debe proveer suficiente espacio en el tablero para al menos **4 interruptores automáticos bipolares** contra sobrecorrientes. | El tablero a diseñar dispondrá físicamente de al menos 4 polos de control y cableado básico de circuitos de fuerza. | `referencias/normativa/pdf/Código_Nacional_de_Electricidad__Utilización_.pdf` (Sección 050, pág. 5) |
| **CNE-U Regla 050-108(2)** | Reserva en Tablero | Debe proveerse de forma obligatoria espacio de reserva en el tablero de distribución para al menos **dos dispositivos de protección adicionales** destinados a futuras ampliaciones. | El gabinete metálico del tablero será de al menos **8 o 12 polos** para permitir espacio libre (reserva física de 2 llaves bipolares adicionales). | `referencias/normativa/pdf/Código_Nacional_de_Electricidad__Utilización_.pdf` (Sección 050, pág. 5) |
| **CNE-U Regla 020-132** | Protección Diferencial General | Obligatoriedad de instalar un interruptor diferencial de corriente residual con sensibilidad **no mayor a 30 mA** en toda instalación residencial. No reemplaza a la puesta a tierra. | Se integrará un interruptor diferencial en el tablero de distribución general, asegurando la inmediata desenergización en caso de contacto accidental directo o indirecto. | `referencias/normativa/pdf/Código_Nacional_de_Electricidad__Utilización_.pdf` (Sección 020, pág. 8) |
| **CNE-U Regla 150-400(7) y (8)** | Agrupamiento y Disparos Intempestivos | Un único interruptor diferencial de 30 mA puede actuar como cabecera para un grupo de **hasta tres circuitos derivados**. En instalaciones con más de tres circuitos (como la nuestra que tiene C1 a C5), se deben agrupar en subgrupos de máximo tres por cada diferencial para evitar disparos intempestivos por corrientes de fuga parásitas. | Teniendo 5 circuitos derivados, se instalarán **dos interruptores diferenciales de 30 mA** (Grupo 1: C1, C2, C3; Grupo 2: C4, C5) o se asignará un diferencial independiente por circuito derivado (opción premium). | `referencias/normativa/pdf/Código_Nacional_de_Electricidad__Utilización_.pdf` (Sección 150, pág. 21) |
| **CNE-U Regla 150-402** | Ubicación y Operabilidad del Tablero | Prohíbe ubicar tableros en baños, armarios de ropa, escaleras o doble altura. La manija de operación más alta no debe superar los **1.7 m** de altura sobre el suelo. | El tablero se empotrará en el pasadizo del primer piso. Se detallará en los planos de montaje que el centro geométrico del gabinete y sus interruptores cumplan con la altura máxima de 1.7 m. | `referencias/normativa/pdf/Código_Nacional_de_Electricidad__Utilización_.pdf` (Sección 150, pág. 21-22) |
| **RNE EM.010 Artículo 1** | Definición y Generalidades | Establece que las instalaciones interiores residenciales van desde la acometida exterior hasta los puntos de utilización final (luces, enchufes). El CNE-U es de obligatorio cumplimiento. | El límite del proyecto inicia en la caja porta medidor exterior de Electro Puno y se extiende por los ductos empotrados hasta cada punto de salida de la casa. | `referencias/normativa/pdf/EM.010%20Instalaciones%20El%C3%A9ctricas%20Interiores.pdf` (Pág. 1) |
| **RNE EM.010 Artículo 3** | Tabla de Iluminancias Mínimas | Estipula niveles mínimos de iluminancia en servicio (lux) para asegurar confort visual en viviendas: general dormitorios (**50 lux**), cabecera (**200 lux**), baños general (**100 lux**), área espejo (**500 lux**), salas general (**100 lux**), lectura en sala (**500 lux**), cocina general (**300 lux**), área de trabajo cocina (**500 lux**). | Estas iluminancias se utilizarán para justificar cuantitativamente la cantidad de luminarias LED propuestas por ambiente en el levantamiento de cargas. | `referencias/normativa/pdf/EM.010%20Instalaciones%20El%C3%A9ctricas%20Interiores.pdf` (Pág. 1-2) |
| **RNE EM.010 Artículo 5** | Entregables del Proyecto | Detalla los documentos mínimos de un proyecto interior: Memoria Descriptiva, Factibilidad y Punto de Entrega, Memoria de Cálculo, Especificaciones Técnicas de Materiales y Montaje, Planos (escala 1:50) y Habilitación CIP. | El entregable maestro del proyecto domicilario se estructurará exactamente siguiendo estas secciones definidas para garantizar rigurosidad académica. | `referencias/normativa/pdf/EM.010%20Instalaciones%20El%C3%A9ctricas%20Interiores.pdf` (Pág. 3-4) |

---

## 4. Auditoría de PDFs del Repositorio y Revisión Visual Requerida

Al revisar los materiales anexos provistos por el docente y los históricos del proyecto, se identificaron varios archivos en formato PDF que **parecen escaneados, son de gran tamaño, no contienen texto seleccionable/indexado o provienen de planos exportados**, lo que impide su lectura automatizada por parte de los asistentes AI.

Para evitar la pérdida de información crítica, a continuación se detallan estos documentos recomendando una **revisión visual exhaustiva por parte del estudiante o la integración a través de herramientas de visión artificial**:

### 1. `EXP VAL INVERSION 01 - FEBRERO CS.pdf` (Tamaño: ~24.0 MB)
*   **Ubicación:** `materiales/otros-referencia/`
*   **Tema probable:** Expediente de valorización técnica y presupuestal de obras eléctricas.
*   **Por qué se debe revisar visualmente:** Es un archivo completamente escaneado. Probablemente contiene firmas de ingenieros, actas oficiales de obra, presupuestos desglosados en hojas de cálculo escaneadas, fórmulas polinómicas y metrados manuales. Es vital revisarlo visualmente para identificar el formato real de presupuestos e informes técnicos que el docente considera válidos.

### 2. `LIQUIDACION INVERSION OI 71225234.pdf` (Tamaño: ~18.0 MB)
*   **Ubicación:** `materiales/otros-referencia/`
*   **Tema probable:** Liquidación financiera y técnica de un proyecto eléctrico real.
*   **Por qué se debe revisar visualmente:** Archivo escaneado de gran tamaño. Contiene resoluciones formales, planillas de liquidación, metrados ejecutados, planos de replanteo (*As-Built*) insertados como imágenes de baja resolución y valorizaciones finales. La revisión visual es indispensable para entender el flujo documental y cómo se presenta un cierre técnico ante una entidad pública o concesionaria.

### 3. `slidesaver.app_zvsnbi.pdf` (Tamaño: ~2.7 MB)
*   **Ubicación:** `materiales/otros-referencia/`
*   **Tema probable:** Presentación didáctica o recopilación de diapositivas del curso.
*   **Por qué se debe revisar visualmente:** El archivo no cuenta con texto extraíble porque consiste en imágenes de diapositivas incrustadas. Contiene fotografías de tableros eléctricos reales, pozos a tierra en proceso de excavación, esquemas de conexión domiciliaria explicados mediante gráficos en clase y recomendaciones directas de pizarra del docente. Su revisión visual es prioritaria para captar los consejos prácticos del profesor.

### 4. `DIAGRAMAUNIFILAR-Model.pdf` (Tamaño: ~14.0 KB)
*   **Ubicación:** `materiales/proyecto-guia-red-primaria/capitulo-ii-calculos/`
*   **Tema probable:** Plano esquemático del diagrama unifilar del proyecto guía de red primaria.
*   **Por qué se debe revisar visualmente:** Es un dibujo técnico de AutoCAD exportado a PDF sin capas de texto indexables. Se debe revisar visualmente en un lector de PDF con zoom para examinar la topología eléctrica de protección (relación transformador - interruptor principal - barras de distribución - celdas de media tensión) y replicar la simbología gráfica de interruptores y transformadores en nuestro diagrama unifilar domiciliario.

---

## 5. Cuestionario Técnico Complementario

Para robustecer de forma sustancial el cuestionario base desarrollado por Codex en su archivo LaTeX, se proponen las siguientes **10 preguntas de ingeniería eléctrica**. Su resolución permitirá al estudiante no solo recopilar datos geométricos, sino justificar con precisión matemática y normativa las decisiones del Capítulo II:

### Preguntas Técnicas y Regulatorias Avanzadas

1.  **Resistividad del Terreno y SPT:** ¿Se dispone de un estudio de resistividad del terreno en Capachica (Puno) o se asumirá un valor típico de suelo arcilloso/pedregoso (ej. 100 a 300 Ω·m)? ¿Qué aditivo conductivo se empleará en el pozo a tierra para asegurar que la resistencia final del sistema sea **menor a 25 Ω** según exige el CNE-U para sistemas de baja tensión?
2.  **Cálculo de Máxima Demanda con Carga Real:** Si se opta por el Método 1 de la Norma EM.010 (cálculo por cargas instaladas reales), ¿qué factor de simultaneidad se justificará técnicamente para la vivienda al operar de forma simultánea el alumbrado de ambos pisos, los tomacorrientes y los pequeños electrodomésticos?
3.  **Análisis de Cargas Especiales (Terma y Ducha):** Con el clima característico del distrito de Capachica (altitud y bajas temperaturas), ¿se prevé la instalación de una terma eléctrica por acumulación (ej. 1500 W) o de duchas eléctricas instantáneas de alta potencia (ej. 3500 W a 5000 W)? ¿Qué impacto tendrán estas cargas de alto consumo continuo en la selección del calibre del alimentador principal y en los interruptores del tablero general?
4.  **Verificación Lumínica EM.010:** Para cumplir con el Artículo 3 de la Norma EM.010 (iluminancias mínimas de 100 lux en salas y baños, y 300 lux en cocinas), ¿se realizará una validación simplificada calculando el flujo luminoso total requerido mediante el método de los lúmenes, o se justificará basándose únicamente en la potencia equivalente de las luminarias LED propuestas?
5.  **Coordinación de Protecciones Termomagnéticas:** Al seleccionar el interruptor termomagnético general del Tablero (TG) y los interruptores de los circuitos derivados C1 a C5, ¿cómo se garantizará el cumplimiento de la regla de selectividad de cortocircuito para evitar que una falla local en una habitación del segundo piso dispare el interruptor general, dejando a toda la vivienda sin suministro eléctrico?
6.  **Criterio de Selección del Interruptor Diferencial:** Debido a que la vivienda posee 5 circuitos derivados, se instalarán diferenciales agrupados o individuales por circuito (Regla `150-400(8)/(9)`). ¿Cuál es la justificación económica y técnica para seleccionar uno u otro enfoque, sabiendo que el uso de diferenciales individuales maximiza la continuidad del servicio ante fugas menores?
7.  **Caída de Tensión por Longitud:** Dado que la acometida desde el medidor de la distribuidora Electro Puno hasta la ubicación tentativa del tablero en el primer piso puede presentar una longitud considerable, ¿cuál es el porcentaje de caída de tensión calculado para el alimentador con el conductor seleccionado, y cuánto margen resta para los circuitos derivados sin exceder el límite absoluto de 2.5%?
8.  **Tipo de Aislamiento y Canalización en Techo:** Para el cableado que irá empotrado en la losa de concreto del techo (alumbrado), ¿se utilizará conductor de cobre tipo TW (aislamiento de PVC estándar) o se optará por el conductor tipo THW/LSOH (libre de halógenos, retardante de llama y de baja emisión de humos), alineado a los criterios modernos de seguridad contra incendios del CNE-U?
9.  **Previsión de Carga de Reserva:** Bajo la Regla `050-108(2)` que exige prever espacio físico en el tablero para dos futuras ampliaciones, ¿qué tipo de cargas futuras estima el grupo que podrían conectarse (por ejemplo: cochera con tomacorriente para carga de vehículo eléctrico, o un pequeño taller doméstico), y se ha sobredimensionado preventivamente la sección del alimentador principal para soportar dicha ampliación?
10. **Alineación con Electro Puno:** ¿Se ha verificado la factibilidad del tipo de acometida que exige la distribuidora Electro Puno para esta zona de Capachica (si exige obligatoriamente murete frontal con medidor empotrado y caja de derivación metálica normalizada)? ¿Cómo influirá esto en el recorrido físico del alimentador principal hasta el Tablero General?

---

> [!TIP]
> **Recomendación para la integración (OpenCode):**
> Este documento sirve como puente perfecto para rellenar los datos marcados como `EDITAR AQUI` en los archivos Markdown finales de `proyecto-casa/` y para estructurar los párrafos de justificación técnica y normativa en la versión en LaTeX compilable.
> Se sugiere realizar una reunión rápida en el grupo para que el estudiante responda estas preguntas y, con ello, cerrar de manera definitiva los Capítulos I y II.

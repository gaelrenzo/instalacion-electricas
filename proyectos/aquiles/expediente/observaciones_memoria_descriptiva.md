# Auditoría y Comparación de la Memoria Descriptiva
**Proyecto:** Instalaciones Eléctricas de Vivienda Unifamiliar (Aquiles Taylor Ramos Yapo)  
**Archivo Evaluado:** `capitulos/01-memoria-descriptiva.tex` / `build/main.pdf`  
**Referencia Principal:** `materiales/INSTALACIONES ELECTRICAS DVD 28.02-23/memoria descriptiva/memoria descriptiva l.pdf` (Universidad Nacional del Altiplano - Servicios Administrativos)

---

## 1. Auditoría de la Memoria Descriptiva Actual (Fase 1)

### A. Estructura y Organización del PDF
- **Observación:** El PDF actual compilado en `build/main.pdf` integra prematuramente el desarrollo de los capítulos 2 (Cálculos), 3 (Especificaciones de Materiales) y 4 (Especificaciones de Montaje).
- **Riesgo:** Presentar un entregable con capítulos sin justificar técnicamente puede causar que el revisor (docente/ingeniero) observe el documento de inmediato.
- **Recomendación:** El PDF de esta fase debe configurarse para compilar **únicamente** la Portada, el Índice y el Capítulo 1 (Memoria Descriptiva). Los demás capítulos deben excluirse de la compilación en `main.tex`.

### B. Resultados de Cálculo Prematuros
La memoria descriptiva actual incluye datos numéricos específicos que corresponden a decisiones de cálculo del Capítulo 2:
- **Alimentador principal:** Define una sección fija de 10 mm² tipo N2XOH en tubería de 35 mm (1 1/4'') sin haber calculado la máxima demanda.
- **Secciones de circuitos:** Establece secciones fijas de 1.5 mm² para alumbrado, 2.5 mm² para tomacorrientes y 4.0 mm² para cocina.
- **Protecciones y llaves:** Fija un interruptor general de 40 A, diferenciales de 30 mA y llaves de circuitos específicos.
- **Puesta a tierra:** Declara una resistencia final menor a 15 Ohmios.
- **Cuadro de cargas consolidado:** Indica una Potencia Instalada de 8,918 W y Máxima Demanda de 6,992 W.
- **Recomendación:** Estos valores deben ser retirados o redactados de forma condicional/preliminar en la memoria descriptiva, indicando que *"serán justificados en la fase de cálculos"*, para evitar inconsistencias si el área techada o las cargas cambian en el Capítulo 2.

### C. Datos Confirmados vs. Supuestos
- **Confirmados:** Propietario (Aquiles Taylor Ramos Yapo), Dirección (Av. Horacio con Jr. Marineros, lote 11 y 12), Distrito/Provincia (San Miguel / San Román / Puno).
- **Supuestos/Pendientes:**
  - Área techada por piso (se estimaron 80 m² y 120 m²). Esto afectará directamente la demanda básica por área del CNE.
  - Coordenadas geográficas exactas (se usó una referencia aproximada).
  - Número de circuitos (se asumen 8 circuitos preliminares, pero el cálculo podría reducir o aumentar este número).
  - Potencia real de la electrobomba de agua.

### D. Redacción y Estilo Visual
- El estilo visual de la UNA Puno (cabecera enmarcada, colores institucionales, portada y pie de página con barra azul) se mantiene de forma excelente.
- El formato de tablas y listas cumple con la estética técnica esperada.

---

## 2. Comparación con Modelos del Repositorio (Fase 2)

### A. Estructura y Estilo que Conviene Copiar
- **Nivel de Detalle en Generalidades:** La subdivisión en *Ubicación*, *Condiciones Climatológicas* (con tabla de temperaturas y vientos de Senamhi), *Coordenadas* y *Normas aplicables* es un estándar indispensable para proyectos de la región Puno y debe mantenerse.
- **Estructura de la Descripción del Proyecto:** Desglosar por *Alimentadores principales*, *Tableros*, *Canalizaciones*, *Conductores*, *Protecciones* e *Iluminación* ayuda a que el instalador entienda el alcance antes de ver los planos.

### B. Estructura que NO Conviene Copiar / Debe Adaptarse
- **Tipo de Proyecto:** El modelo guía es para un edificio administrativo de gran envergadura de la Universidad Nacional del Altiplano, por lo que incluye:
  - Alimentadores de media sección (6 a 150 mm²).
  - Tablero general autosoportado metálico (para corrientes altas).
  - Tuberías metálicas Conduit a la intemperie.
  - Soportes electrosoldados con acabado epóxico negro mate.
  - Sistemas de pararrayos y puesta a tierra con 5 pozos de tierra.
  - Suministros trifásicos diversificados de 171 kW.
- **Adaptación para la Vivienda de Aquiles:**
  - Reducir las especificaciones de canalizaciones a tuberías empotradas de PVC clase pesada (no Conduit metálica, salvo tramos expuestos muy cortos).
  - Redefinir el Tablero General como del tipo **empotrado** de resina o metal ligero, no autosoportado.
  - Simplificar la puesta a tierra a **1 solo pozo de tierra** en lugar de 5.
  - Omitir pararrayos si no es un requisito de seguridad de la zona o de la escala civil.
  - Normalizar las secciones a valores residenciales comunes (1.5, 2.5, 4.0 mm²).

---

## 3. Recomendaciones y Reubicación de Contenidos

Para mantener la integridad de la memoria descriptiva y evitar observaciones, se recomienda realizar las siguientes modificaciones de reubicación:

### A. Texto que debe QUEDARSE en la Memoria Descriptiva
- Criterios generales de diseño (seguridad, sectorización, facilidad de mantenimiento).
- Descripción cualitativa del sistema de alimentación (suministro monofásico de Electro Puno S.A.A.).
- Ubicación proyectada del Tablero General (primer piso en zona accesible).
- Normativas generales aplicables (CNE-U, EM.010).

### B. Contenido que debe MOVERSE a Cálculos Justificativos (Capítulo 2)
- La potencia instalada (8,918 W) y la máxima demanda (6,992 W).
- Las intensidades de corriente calculadas y de diseño.
- Las secciones de los conductores alimentadores y derivados.
- Los porcentajes calculados de caída de tensión.
- Las capacidades de los interruptores termomagnéticos y diferenciales.

### C. Contenido que debe MOVERSE a Especificaciones de Materiales (Capítulo 3)
- La tabla de dimensiones de cajas metálicas (rectangular, octogonal, cuadrada).
- Las especificaciones físicas del aislamiento de cables (N2XOH, THW).
- Los espesores de planchas metálicas para cajas y tableros (1.6 mm, 1.8 mm).
- Las características físicas de la cinta aislante de PVC.

### D. Contenido que debe MOVERSE a Especificaciones de Montaje (Capítulo 4)
- La tabla de alturas de montaje recomendadas (interruptores a 1.20m, tomas a 0.30m, etc.).
- Las especificaciones de excavación y preparación del pozo de puesta a tierra.
- Las pautas de tracción del cableado (uso de talco, no empalmes en tubos).
- La tabla de pruebas de aislamiento con megómetro.
- El procedimiento de pruebas de puesta en servicio (telurómetro).

# Auditoría de Fuentes de Cálculo - Proyecto Aquiles
**Rol:** Ingeniero Electricista Senior / Revisor de Expedientes Técnicos  
**Fecha:** 3 de junio de 2026  
**Proyecto:** Instalaciones Eléctricas Interiores - Vivienda Unifamiliar de 2 Pisos (Aquiles Ramos)

---

## 1. Archivos de Cálculo Encontrados en el Repositorio

Tras una inspección minuciosa del repositorio, se han identificado las siguientes fuentes de datos, hojas de cálculo y documentos técnicos:

1. **`materiales/INSTALACIONES ELECTRICAS DVD 28.02-23/calculos justificativos/CALCULOS - CIRCUITOS Y TABLERO FRI.xlsx`**
   - *Descripción:* Libro de Excel con cálculos detallados del proyecto del Local Administrativo de la UNA Puno.
   - *Hojas:* 
     - `Computadoras`: Cálculo de cargas no lineales y armónicos para centros de cómputo.
     - `CUADRO DE CARGAS`: Matriz general de cargas por circuitos para múltiples tableros de distribución (TD-1 a TD-10) y subtableros generales (STG-1).
     - `CALCULO POR CIRCUITOS`: Verificación térmica y por caída de tensión de los alimentadores secundarios.
     - `CALCULOS  TAB. DIS.`: Capacidad térmica y caídas de tensión por circuito derivado.
     - `CALCULO TAB. GEN. Y SUB. TAB`: Cálculo de alimentadores principales trifásicos de cabecera.

2. **`materiales/INSTALACIONES ELECTRICAS DVD 28.02-23/Metrado Electricas/`**
   - *`METRADO DE INSTACONES ELECTRICAS-UNAP.xlsx`*: Planilla de metrados detallada por partidas (salidas, canalizaciones, tableros).
   - *`RESUMEN DE METRADO.xlsx`*: Resumen consolidado para presupuesto de obra.

3. **`materiales/proyecto-guia-red-primaria/capitulo-ii-calculos/`**
   - *`CALCULO DE MAXIMA DEMANDA - PHARAok.xlsm`*: Archivo Excel macro-habilitado para redes de distribución primaria en media tensión (10 kV / 22.9 kV).
   - *`CALCULOMECANICOCONDUCTORES 35.xls`* y *`CALMECANICODEPOSTES.xls`*: Hojas de cálculo para esfuerzos mecánicos y tensión de conductores y postes de distribución aérea.
   - *`CALCULORETENIDA.xls`*, *`CIMENTACIONPOSTES.xls`* y *`COORDINACION DE PROTECCION.xlsx`*: Archivos de ingeniería civil y de protecciones de redes de distribución.
   - *`CALCULOSELECTRICOS.pdf` / `.doc`*: Documento que contiene ecuaciones para líneas de transmisión primaria (caída de tensión por reactancia inductiva, efecto corona, pérdidas por efecto Joule).

4. **`proyectos/renzo/calculos/cuadro-cargas/`**
   - *`cuadro_cargas.xlsx`* y *`maxima_demanda.xlsx`*: Hojas de cálculo específicas para el proyecto de vivienda unifamiliar de 3 pisos de Renzo Mamani.
   - *`proyectos/renzo/calculos/memoria/memoria_calculo.md`*: Informe de base muy claro con fórmulas específicas para instalaciones interiores de tipo residencial.

---

## 2. Documentos Modelo Útiles para el Caso Aquiles

Los documentos que sirven directamente como modelo técnico de redacción y metodología son:
- **`proyectos/renzo/calculos/memoria/memoria_calculo.md`**: Es la referencia más directa para el formato residencial unifamiliar. Usa el Código Nacional de Electricidad - Utilización (Sección 050-200) para calcular la demanda de vivienda.
- **`CALCULOS - CIRCUITOS Y TABLERO FRI.xlsx` (Hojas `CALCULO POR CIRCUITOS` y `CUADRO DE CARGAS`)**: Sirve como modelo para estructurar el formato de las tablas de cálculo de circuitos y la presentación estética en LaTeX de cuadros de cargas, adaptando los parámetros al caso monofásico.

---

## 3. Fórmulas Identificadas y su Aplicabilidad

A partir del análisis de las celdas y el código de las fuentes, se extrae la siguiente matriz de aplicabilidad:

### A. Fórmulas Aplicables a Vivienda Domiciliaria (Caso Aquiles)
* **Potencia Instalada por Área Techada:**
  $$P_{area} = A_{techada} \times P_{especifica}$$
  *Uso:* Carga básica inicial de 2500 W para los primeros 90 m² (F.D. 1.0) y 1000 W por cada 90 m² adicionales o fracción (CNE-U Regla 050-200).
* **Corriente Nominal de Línea (Monofásica, 220 V):**
  $$I_n = \frac{P_{dem}}{V \times \cos\phi}$$
  *Uso:* Determinar la corriente de operación normal. $\cos\phi = 0.90$ comercial.
* **Corriente de Diseño (Id):**
  $$I_d = I_n \times 1.25$$
  *Uso:* Dimensionamiento térmico del conductor del alimentador principal (Regla CNE 050-204).
* **Caída de Tensión Monofásica (Monofásico, 2 Hilos):**
  $$\Delta V = \frac{2 \times L \times I \times \rho}{S}$$
  *Uso:* Obligatorio para verificar la caída de tensión en el alimentador principal ($\le 1.5\%$) y circuitos derivados ($\le 2.5\%$). Resistividad del cobre $\rho = 0.0178\ \Omega\cdot\text{mm}^2/\text{m}$ (o $0.018$ según la hoja Excel de la UNA).
* **Coordinación de Protecciones:**
  $$I_b \leq I_n \leq I_z$$
  *Uso:* Selección segura de la corriente nominal del interruptor termomagnético ($I_n$) respecto a la corriente de diseño del circuito ($I_b$) y la capacidad del conductor ($I_z$).

### B. Fórmulas No Aplicables (Deben Omitirse)
* **Caída de Tensión Trifásica:**
  $$\Delta V = \frac{\sqrt{3} \times L \times I \times \rho \times \cos\phi}{S}$$
  *Motivo:* El suministro del predio de Aquiles es monofásico ($220\text{ V}$). No debe asumirse trifásico a menos que se justifique una carga de alta potencia trifásica (inexistente en el cuestionario).
* **Esfuerzos Mecánicos de Conductores y Flechas (Líneas de Distribución Aérea):**
  *Ecuación:* Ecuación de la catenaria y cálculo de tensiones mecánicas por carga de viento/hielo.
  *Motivo:* Corresponde al sistema de utilización en media tensión / red primaria.
* **Coordinación de Relés de Protección de Sobrecorriente (50/51, 50N/51N):**
  *Motivo:* Exclusivo para subestaciones y celdas de media tensión.
* **Resistividad por Efecto Corona y Pérdidas Dieléctricas:**
  *Motivo:* Propio de líneas de transmisión de alta/media tensión.

---

## 4. Datos Faltantes y Supuestos Preliminares para Aquiles

### A. Datos Críticos Faltantes (Sujetos a Confirmación)
1. **Área exacta por piso:** Existe una discrepancia entre la memoria descriptiva anterior (que mencionaba 80 m² en primer piso y 120 m² en segundo) y el cuestionario del predio real de Aquiles (terreno total 134.18 m² con un segundo piso de aprox. 42.56 m² construidos).
2. **Ubicación física definitiva del Tablero General (TG):** Afecta directamente la longitud de alimentación principal ($L$) y el cálculo de la caída de tensión.
3. **Placa de potencia nominal de la bomba de agua:** Se asume de 1 HP ($746\text{ W}$ o $750\text{ W}$), pero debe confirmarse.
4. **Resistencia de puesta a tierra objetivo:** Se proyecta $\le 15\ \Omega$ según exigencia de EM.010 para residencial, pero se requiere verificar las condiciones del terreno (resistividad del suelo en San Miguel, Puno).

### B. Datos asumidos como preliminares ("preliminar" / "referencial"):
- **Áreas de cálculo para CNE (Regla 050-200):** Se adopta provisionalmente un área total de construcción aproximada de $120\text{ m}^2$ (primer piso y segundo piso combinados en términos de área techada efectiva), lo cual genera una Carga Básica de $3,500\text{ W}$ (2,500 W por los primeros 90 m² y 1,000 W por los 30 m² adicionales de exceso).
- **Longitud del alimentador principal:** Se asume $L = 12\text{ m}$ (distancia preliminar estimada desde el medidor de la fachada hasta el Tablero General en el primer piso).
- **Tensión nominal de suministro:** Monofásico de $220\text{ V}$, $60\text{ Hz}$.
- **Sección mínima de conductores:** Alumbrado ($1.5\text{ mm}^2$), Tomacorrientes ($2.5\text{ mm}^2$), Cocina/Servicios ($4\text{ mm}^2$).
- **Aislamiento de conductores:** Libre de halógenos tipo **NH-80** para interiores empotrados en tuberías de PVC.

---

## 5. Conclusión del Revisor

El Capítulo II (Cálculos Justificativos) de la vivienda de Aquiles se estructurará aplicando la metodología simplificada de tipo **residencial unifamiliar**. Las fórmulas complejas de red primaria e instalaciones comerciales se descartarán por completo para evitar errores de sobrediseño y falta de coherencia técnica con el expediente de una vivienda. Todos los resultados numéricos obtenidos en esta fase se marcarán como **preliminares** en espera de la regularización definitiva del plano de arquitectura y el dibujo catastral.

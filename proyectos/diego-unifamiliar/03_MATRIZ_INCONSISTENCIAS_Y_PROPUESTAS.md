# UNIVERSIDAD NACIONAL DEL ALTIPLANO
## ESCUELA PROFESIONAL DE INGENIERÍA MECÁNICA ELÉCTRICA (EPIME)

---

# MATRIZ DE INCONSISTENCIAS Y PROPUESTAS TÉCNICAS DE MEJORA
## PROYECTO: VIVIENDA UNIFAMILIAR DE 3 NIVELES (CHARAJA MAMANI DIEGO JEFFERSON - 214254)

### 1.1 Presentación
Auditoría técnica cruzada entre los planos de Diego Charaja (Lámina A2), su cuadro de cargas en Excel y las exigencias del Código Nacional de Electricidad.

### 1.2 Matriz Consolidada de Inconsistencias y Soluciones Técnicas

| Item | Elemento Evaluado | Discrepancia Identificada | Solución / Propuesta Adoptada | Justificación Normativa |
| :---: | :--- | :--- | :--- | :--- |
| **1** | Concesionaria Eléctrica | Plano indica 'RED DE EDELNOR' (Lima Norte). | Se corrigió consignando a ELECTRO PUNO S.A.A. (o concesionaria local). | Coherencia geográfica con la ciudad de Puno / UNAP. |
| **2** | Tipología de Edificación | Word modelo citaba 'Vivienda Multifamiliar'. | Se reestructuró para 'Vivienda Unifamiliar de 3 niveles' según plano. | Fidelidad con la arquitectura del plano A2. |
| **3** | Protecciones Diferenciales | Excel omitía especificar diferenciales por circuito. | Se incorporó la exigencia de ID de 30 mA para C-1 a C-7. | CNE-Utilización Regla 020-204 obligatoria. |
| **4** | Tipo de Conductores | Word modelo mencionaba cable TW/THW tradicional. | Se especificó conductor ecológico Cero Halógenos NH-80 / N2XH. | CNE-Utilización 020-028 y RNE EM.010. |
| **5** | Capacidad del Tablero | Excel recomendaba 24 polos (saturado). | Se amplió a Tablero General de 36 Polos trifásico. | CNE-U Regla 080-400 (Reserva mínima 20%). |
| **6** | Pozo a Tierra (PAT) | Plano no detallaba la ubicación y resistencia del pozo. | Se proyectó Pozo PAT-1 en patio/cisterna con R ≤ 10 Ω. | CNE-U Regla 060-712 para protección rápida. |

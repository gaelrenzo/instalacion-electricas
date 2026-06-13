# Capitulo II: Calculos justificativos

## 1. Objetivo del capitulo

Justificar tecnicamente la instalacion electrica mediante el levantamiento de cargas, calculo de potencia instalada, maxima demanda, corriente de diseno, seleccion preliminar de circuitos, conductores, protecciones, tablero y puesta a tierra.

## 2. Estructura propuesta

| Seccion | Contenido a desarrollar | Fuente principal |
|---|---|---|
| 2.1 Normas aplicables | CNE-U, EM.010 y criterios del curso | `normativas/fuentes-oficiales.md` |
| 2.2 Datos electricos del sistema | Tension, frecuencia, factor de potencia, material conductor | `pautas-vivienda-2-pisos.md` |
| 2.3 Levantamiento de cargas | Tabla por ambiente, equipo, cantidad y potencia | `respuestas-cuestionario-aquiles.md` |
| 2.4 Cuadro de cargas por circuito | C1 a C8, potencia instalada, factor y demanda | `respuestas-cuestionario-aquiles.md` |
| 2.5 Calculo de maxima demanda | Formulas y resultado total | `proyecto-casa/02-calculos-justificativos/calculos-justificativos.md` |
| 2.6 Corriente de diseno | Formula `I = P / (V x fp)` | `proyecto-casa/02-calculos-justificativos/calculos-justificativos.md` |
| 2.7 Distribucion de circuitos | Alumbrado, tomacorrientes, cocinas, lavadora y bomba de agua | `respuestas-cuestionario-aquiles.md` |
| 2.8 Seleccion de conductores | Secciones preliminares segun corriente y uso | `proyecto-casa/02-calculos-justificativos/calculos-justificativos.md` |
| 2.9 Protecciones | Interruptores termomagneticos y diferencial | `proyecto-casa/02-calculos-justificativos/calculos-justificativos.md` |
| 2.10 Caida de tension | Verificacion con longitud estimada | `herramientas/calculadora-instalacion-casa.html` |
| 2.11 Puesta a tierra | Componentes y criterio preliminar | `latex/capitulos/02-calculos-justificativos.tex` |

## 3. Datos de calculo actuales

| Parametro | Valor |
|---|---:|
| Tension nominal | 220 V |
| Frecuencia | 60 Hz |
| Factor de potencia | 0.90 |
| Sistema | Monofasico |
| Material conductor | Cobre |
| Resistividad referencial del cobre | 0.0175 ohm mm2/m |

## 4. Resultado preliminar general (Escenario 2 - Cocina Eléctrica Considerada)

Con los datos de cargas y ambientes, el motor de cálculo procesa dos escenarios. Se adopta el **Escenario 2** (cocina eléctrica de 6000 W considerada) como criterio de dimensionamiento conservador para evitar subdimensionar el alimentador principal y las protecciones.

| Concepto | Valor del Escenario 2 |
|---|---:|
| Alumbrado total (C1 + C4) | 212 W |
| Tomacorrientes generales (C2 + C5) | 3,600 W |
| Cocina y servicio (C3 + C6 + C7) | 7,100 W |
| Bomba de agua exterior (C8) | 746 W |
| **Potencia instalada total (P.I.)** | **11,658 W** |
| **Máxima demanda adoptada** | **10,358 W** |
| **Corriente de empleo (Ib)** | **52.31 A** |
| **Corriente de diseño (Id = 1.25 x Ib)** | **65.39 A** |
| Conductor del alimentador principal | 16.0 mm² |
| Interruptor termomagnético general (ITM) | 2P-63A |
| Caída de tensión del alimentador | 0.635% (Límite: 1.5%) |

## 5. Circuitos de distribución y dimensionamiento

La selección preliminar de conductores, interruptores termomagnéticos (ITM) e interruptores diferenciales (ID) por circuito, bajo el Escenario 2, se presenta a continuación:

| Circuito | Uso / Descripción | P.I. (W) | F.D. | M.D. (W) | Ib (A) | Conductor | ITM | Caída de Tensión | Interruptor Diferencial |
|---|---|---|---|---|---|---|---|---|---|
| **C1** | Alumbrado primer piso | 80 | 1.00 | 80.0 | 0.40 | 2.5 mm² | 2P-10A | 0.039% | Ver diferencial general |
| **C2** | Tomacorrientes primer piso | 1,260 | 0.70 | 882.0 | 4.46 | 2.5 mm² | 2P-10A | 0.519% | 2P-25A-30mA |
| **C3** | Cocina primer piso (Auxiliar) | 300 | 0.80 | 240.0 | 1.21 | 2.5 mm² | 2P-10A | 0.078% | 2P-25A-30mA |
| **C4** | Alumbrado segundo piso | 132 | 1.00 | 132.0 | 0.67 | 2.5 mm² | 2P-10A | 0.095% | Ver diferencial general |
| **C5** | Tomacorrientes segundo piso | 2,340 | 0.70 | 1,638.0 | 8.27 | 2.5 mm² | 2P-10A | 1.339% | 2P-25A-30mA |
| **C6** | Cocina eléctrica segundo piso | 6,000 | 1.00 | 6,000.0 | 30.30 | 10.0 mm² | 2P-32A | 0.981% | 2P-40A-30mA |
| **C7** | Lavadora segundo piso | 800 | 0.80 | 640.0 | 3.23 | 2.5 mm² | 2P-10A | 0.314% | 2P-25A-30mA |
| **C8** | Bomba de agua exterior | 746 | 1.00 | 746.0 | 3.77 | 2.5 mm² | 2P-10A | 0.341% | 2P-25A-30mA |

## 6. Calculos que deben quedar completos

- Potencia total por carga: `cantidad x potencia unitaria`.
- Potencia instalada por circuito.
- Factor de demanda por tipo de carga.
- Maxima demanda por circuito.
- Corriente por circuito.
- Corriente total estimada.
- Seleccion de conductor por circuito.
- Seleccion de proteccion por circuito.
- Verificacion de caida de tension.
- Criterio de puesta a tierra.
- Tabla final de tablero o diagrama unifilar preliminar.

## 7. Pendientes del capitulo

| Pendiente | Accion |
|---|---|
| Confirmar potencias reales de equipos | Revisar placa o potencia comercial de bomba, lavadora, microondas/horno y waflera |
| Definir longitudes de circuitos | Usar croquis o plano preliminar |
| Completar caida de tension | Aplicar formula o calculadora HTML |
| Sustentar protecciones | Relacionar corriente, conductor y termomagnetico |
| Verificar puesta a tierra | Definir conductor, electrodo, caja de registro y barra de tierra |
| Agregar numerales normativos | Revisar CNE-U y EM.010 |
| Confirmar tomacorrientes del segundo piso | Definir sala, cuartos y cuarto de uso varios |

## 8. Criterio de Puesta a Tierra (SPAT)

El sistema de puesta a tierra (SPAT) es obligatorio según el Código Nacional de Electricidad (Utilización), Sección 060.
- **Criterio de sistema:** Se plantea un sistema de puesta a tierra independiente y dedicado para el Tablero General (TG), al cual se conectarán todos los conductores de protección (PE) de los distintos circuitos.
- **Ubicación:** El electrodo y caja de registro de puesta a tierra se ubican próximos al Tablero General y Medidor, en la zona exterior/frontal de la vivienda (Piso 1).
- **Conductor de protección:** Todos los circuitos, incluyendo tomacorrientes y cargas especiales, contarán con conductor de protección (PE) dimensionado según CNE-U. Desde el pozo de tierra se tenderá un conductor de conexión hasta la barra de tierra del Tablero General (TG), y de ahí subirá al Tablero de Distribución (T2).
- **Referencia normativa:** CNE-Utilización, Sección 060 Puesta a Tierra y Enlace Equipotencial.
- **Materiales mínimos considerados:**
  - Electrodo/varilla de cobre (mínimo 2.0 m).
  - Conector tipo AB o abrazadera.
  - Conductor de puesta a tierra (cobre desnudo o aislado amarillo/verde).
  - Caja de registro de puesta a tierra de concreto con tapa.
  - Tratamiento químico (bentonita/thorgel) según tipo de terreno.
- **Observación:** La resistencia final de la puesta a tierra (máximo 25 ohmios, según norma) debe verificarse en obra utilizando un telurómetro una vez finalizada la instalación.
- **Representación en plano (v6):** El SPAT se representa en el DXF maestro `electrico_piso1_v6.dxf` en la capa `ELEC_PUESTA_TIERRA`, en las coordenadas (15.45, 3.60), con símbolo estándar de tres líneas horizontales decrecientes. Versión generada mediante edición directa del DXF maestro v4.

## 9. Corrección de simbología de luminarias (v6)

En la versión 6 se corrigió la representación gráfica de las luminarias de techo. El símbolo anterior usaba una cruz ortogonal (+), mientras que el estándar DGE (código 09-93-51, Salida para lámpara incandescente en techo) utiliza cuatro trazos diagonales formando un aspa (X). La corrección se aplicó directamente sobre los DXF maestros v4 de ambos pisos:
- **Piso 1:** 10 luminarias corregidas (4 en planta + 1 en leyenda, × 2 por doble círculo).
- **Piso 2:** 12 luminarias corregidas (11 en planta + 1 en leyenda).
- **Método:** Se eliminaron las líneas ortogonales y se reemplazaron por diagonales a 45° que tocan el borde del círculo de la luminaria.

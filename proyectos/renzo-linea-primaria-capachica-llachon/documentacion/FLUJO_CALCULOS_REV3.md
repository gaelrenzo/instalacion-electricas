# Flujo de cálculo eléctrico y mecánico — Rev. 3

**Estado:** especificación del cálculo, no dimensionamiento ejecutado. Los campos sin evidencia permanecen nulos en datos/parametros_diseno_pendientes.json y datos/registro_datos_rev3.json. Una prueba numérica sintética comprueba código, no valida este corredor.

| Etapa | Entradas y fuente exigida | Fórmula o operación, unidades | Resultado | Criterio objetivo |
|---|---|---|---|---|
| Demanda | Potencia actual/proyectada kVA, horizonte, simultaneidad; estudio de carga y aprobación Electro Puno | Construir escenarios de punta y crecimiento | S diseño [kVA] | Escenario aceptado y trazable; sin dato no calcular |
| Corriente | S [kVA], U línea [kV], fases confirmadas | Trifásico: I[A] = S/(√3 U); monofásico: fórmula según configuración real | I diseño [A] | Topología y tensión oficiales |
| Conductor | I, material, sección, temperatura, altitud, agrupamiento, fichas del fabricante | Ampacidad corregida ≥ I diseño; comprobar resistencia, reactancia y capacidad térmica de falla | Sección candidata | CNE Suministro y estándar Electro Puno aplicables; valores documentados |
| Regulación | I por tramo, L [km], R y X [Ω/km], cosφ | ΔU[V] ≈ √3 Σ I L (R cosφ + X sinφ) en radial trifásico; modelo de flujo para derivaciones | ΔU y porcentaje | Límite oficial de red y escenario de carga confirmado |
| Pérdidas | I por tramo, R [Ω/km], L [km] | P[W] = 3 Σ I² R L para trifásico balanceado | Pérdidas técnicas | Evaluación con demanda y conductor reales |
| Cortocircuito | Z de fuente, red y transformadores; U prefalla; modos de operación | Red equivalente y corrientes máxima/mínima; no sustituir impedancias faltantes por cero | Icc [kA] | Poder de corte, sensibilidad y coordinación documentados |
| Protección/PAT | Unifilar, curvas, ajustes, esquema de neutro, resistividad | Coordinación temporal y estudio de puesta a tierra | Selección y ajustes | Aprobación del titular y reglas aplicables |
| Vano y clima | Topografía, longitud horizontal [m], conductor y accesorios [N/m], temperatura/viento [m/s o Pa] | Combinar cargas verticales/horizontales por hipótesis aprobadas | Carga distribuida [N/m] | Casos meteorológicos y factores según norma vigente/operador |
| Flecha/tensión | Peso resultante [N/m], vano [m], H [N], temperatura y creep | Aproximación inicial: f[m] ≈ w L²/(8H) para vano nivelado; cálculo final por ecuación de cambio de estado/catenaria | Flecha y H por caso | Límites de conductor y despejes verificados |
| Estructura/retenida | Ángulo, tensiones de ambos vanos, viento sobre conductores/poste, accesorios | Equilibrio vectorial de fuerzas y momentos [N, N·m] | Carga por apoyo | Resistencia certificada y factores exigidos |
| Despeje | Perfil topográfico preciso, flecha máxima, obstáculos y cruce clasificado | Cota conductor mínima − cota obstáculo/terreno [m] | Distancia real [m] | Tabla pertinente del CNE, Electro Puno y permiso de cruce |
| Cimiento | Reacciones [N, N·m], estratigrafía y capacidad portante, nivel freático | Método geotécnico para suelo/estructura real | Dimensiones | Estudio geotécnico y revisión profesional |

**Orden de ejecución:** validar documentos y unidades → fijar escenarios aprobados → cálculo eléctrico → optimizar apoyos con topografía/cruces → cálculo mecánico → repetir eléctrico si cambia longitud/topología → matriz de aceptación → planos y metrados → revisión y conformidad. Cada resultado deberá guardar valor, unidad, fuente, versión, fórmula, hipótesis, responsable, fecha y estado. Las funciones existentes de scripts/calculos_condicionales.py rechazan nulos; no se alimentaron con valores inventados.

**Referencias a cotejar al definir tensión y alcance:** [CNE Suministro 2011, RM 0214-2011-MEM](https://www.gob.pe/institucion/minem/normas-legales/108753-0214-2011-mem); [RD 018-2002-EM/DGE, procedimiento MT](https://www.gob.pe/institucion/osinergmin/normas-legales/739536-018-2002-em-dge); [RD 018-2003-EM/DGE, bases rurales](https://www.gob.pe/institucion/minem/normas-legales/4775002-018-2003-em-dge) si el proyecto pertenece a su ámbito; [RNE](https://www.gob.pe/institucion/vivienda/informes-publicaciones/2309793-reglamento-nacional-de-edificaciones-rn). La selección de artículos, tablas, límites y versiones de Electro Puno queda **pendiente**; no se asigna un umbral numérico sin confirmar su aplicabilidad.

# Metodología de ubicaciones para revisión — Rev. 3

La tabla datos/candidatos_nuevos_replanteo_rev3.csv contiene **sitios geométricos donde evaluar** un apoyo nuevo. Sus IDs PN-* son independientes de las 40 estructuras publicadas PC-* de GISEM. Ningún PN-* es orden de instalación, metrado de obra o autorización de servidumbre.

1. Leer las cuatro polilíneas KML en orden, comprobar EPSG:4326, transformar a WGS84/UTM 19S y calcular progresiva de la **suma de líneas observadas**, sin introducir los tres empalmes.
2. Retener extremos de cada segmento como puntos de replanteo: inicio y fin del corredor como terminales por confirmar; extremos interiores como empalmes por resolver. Ninguno es apoyo obligatorio.
3. Simplificar cada línea a 10 m y retener los vértices originales con giro geométrico absoluto ≥20°. Ambos parámetros son filtros de gabinete para reducir ruido y localizar cambios de rumbo; no proceden de una norma de vano, esfuerzo o despeje. Cambiar parámetros obliga a nueva revisión.
4. Conservar las coordenadas exactas de los vértices KML elegidos. Consultar la estructura GIS más cercana sin mover el sitio; registrar su código y separación. Una cercanía ≤25 m solo indica necesidad de cotejar posible reutilización.
5. Evaluar por separado cruces, servidumbres, suelo, accesos, perfil y apoyos existentes en campo. Después de resolver empalmes, proyectar vanos y comprobar flecha, cargas, distancias y ángulos con parámetros eléctricos/mecánicos aprobados.
6. En la siguiente iteración, comparar alternativas por seguridad, posibilidad de acceso, permisos, menor intervención y costo. Aprobar una ubicación solo con topografía, cálculo, derechos de paso, conformidad del titular y revisión profesional.

Cada fila registra coordenadas geográficas/UTM, progresiva, función geométrica, giro, justificación, restricción, relación con GISEM, fuente, confianza y estado. La función **eléctrica o mecánica** (alineamiento, ángulo, retención, terminal) permanece por definir. La falta de posiciones intermedias en un tramo largo **no autoriza** un vano largo: significa que la densificación de estructuras requiere cálculos y topografía aún no disponibles.

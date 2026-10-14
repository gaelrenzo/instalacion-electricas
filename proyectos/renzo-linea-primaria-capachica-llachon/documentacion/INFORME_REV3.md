# Resumen de cambios y control de cierre — Rev. 3

**Base:** commit Rev. 2 da69405; nueva rama feature/diseno-tecnico-rev3-capachica-llachon. El PR borrador #5 sigue abierto y sin fusionar al inicio de esta revisión. Se conservaron los cambios locales ajenos y todas las fuentes originales.

**Entregables nuevos:** conciliación KML–GIS con seis decimales y explicación de 40,405 m; tabla de tres empalmes; 27 sitios geométricos PN separados de 40 estructuras GIS PC; 44 indicios viales OSM georreferenciados; registro de datos por estado y procedencia; solicitud técnica a Electro Puno; plan de campo; flujo de cálculos; auditoría de cinco planos; bloqueos y puertas de avance; validador, pipeline, pruebas y manifiesto de huellas. El expediente editable incorpora el anexo 08. No se generaron nuevos detalles constructivos ni se reemplazaron las cinco láminas Rev. 2.

**Auditoría de longitudes:** KML 13 939,511910 m y GIS 13 834,028618 m (longitudes geométricas UTM 19S). La diferencia exacta es 105,483292 m; las cifras publicadas de Rev. 2 daban 105,482 m por redondeo. Las tres cuerdas entre segmentos suman 65,077277 m. La resta publicada 40,405 m no puede asignarse físicamente; para resolver la diferencia faltan continuidad, extremos y elección de eje. El empalme 3 presenta intersección de líneas con sobrantes de 1,781 m y 5,271 m.

**Verificación:** los cinco DXF Rev. 2 se reabrieron sin errores de auditoría ezdxf, en metros; los cinco PDF se abrieron como A3 horizontal y se inspeccionó una hoja de contacto PNG. El pipeline Rev. 3 validó datos, referencias y **25 pruebas automatizadas aprobadas**. Estas verificaciones son de software y formato; no certifican ingeniería, AutoCAD, campo ni aprobación externa.

**Bloqueos prioritarios:** P0 — factibilidad/punto de conexión, corredor topográfico continuo, demanda y configuración de red. P1 — cruces/servidumbres, apoyos existentes, conductor, topografía/geotecnia, protecciones y puesta a tierra. P2 — planos constructivos y metrados. Los documentos requeridos y criterios de cierre están en BLOQUEOS_Y_PUERTAS_REV3.md.

**Reproducción desde la raíz del repositorio:** instalar requirements.txt del proyecto en entorno virtual y ejecutar el script scripts/reproducir_rev3.py (con --archive-existing cuando ya hay salidas). El script archiva solo salidas Rev. 3 en build/, regenera, valida y prueba. El manifiesto derived/manifest_rev3.json guarda huellas y tamaños. El resultado continúa **no apto para construcción**.

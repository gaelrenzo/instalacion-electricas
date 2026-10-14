# Capachica–Llachón: anteproyecto y planos AutoCAD

## Revisión activa 3: conciliación y preparación del diseño

La [conciliación de ejes](documentacion/CONCILIACION_CORREDORES_REV3.md) distingue la diferencia publicada de **105,482 m** del KML frente al GIS, las tres brechas que suman **65,077 m** y los **40,405 m** que resultan solo de restar cifras redondeadas. Esa resta no identifica un tramo faltante. Las fuentes originales siguen inalteradas.

Los [27 sitios PN para replanteo](datos/candidatos_nuevos_replanteo_rev3.csv) son candidatos geométricos a evaluar para apoyos nuevos; están separados de las 40 estructuras GISEM PC del inventario Rev. 2. Su [método de selección](documentacion/METODOLOGIA_UBICACION_POSTES_REV3.md) y [registro de procedencia y estado](datos/registro_datos_rev3.json) impiden tratarlos como postes aprobados.

Se prepararon, **sin enviar**, la [solicitud a Electro Puno](documentacion/SOLICITUD_TECNICA_ELECTRO_PUNO_REV3.md), el [plan de campo y cruces](documentacion/PLAN_CAMPO_Y_CRUCES_REV3.md) con [44 indicios viales georreferenciados](datos/cruces_viales_rev3.csv), el [flujo de cálculos](documentacion/FLUJO_CALCULOS_REV3.md), la [auditoría de los cinco planos](documentacion/AUDITORIA_PLANOS_REV3.md) y los [bloqueos y criterios de avance](documentacion/BLOQUEOS_Y_PUERTAS_REV3.md). Los DXF/PDF Rev. 2 permanecen como antecedentes para corregir tras topografía y datos del operador.

Desde la raíz del repositorio, con el entorno virtual instalado según la sección inferior:

~~~powershell
python proyectos/renzo-linea-primaria-capachica-llachon/scripts/reproducir_rev3.py --archive-existing
python -m pytest proyectos/renzo-linea-primaria-capachica-llachon/tests -q
~~~

La opción --archive-existing respalda las salidas Rev. 3 ya incluidas en el repositorio bajo build/ antes de regenerarlas. Si no existen salidas, puede omitirse. Las pruebas verifican datos y software, **no** la ingeniería de construcción.

## Revisión activa 2: corredor manual KML

La [auditoría KML Rev. 2](documentacion/AUDITORIA_KML_REV2.md) es la referencia activa del corredor manual. Calcula **13 939,512 m UTM** en cuatro segmentos separados por brechas de 14,133, 43,965 y 6,979 m. Difiere **105,482 m** de la longitud GIS anterior. El punto de conexión informado está a 0,561 m del comienzo del KML y coincide con un tramo GISEM, pero su aprobación eléctrica está pendiente.

La [tabla de 40 puntos de inspección](datos/ubicaciones_postes_preliminares.csv) registra estructuras GIS situadas a 25 m o menos del KML. No son postes nuevos ni una solución de vanos aprobada. Las [estaciones](datos/estaciones_corredor.csv), [vértices](datos/vertices_corredor_manual.csv), [puntos críticos](datos/cruces_y_puntos_criticos.csv), [cálculos condicionados](documentacion/CALCULOS_Y_PENDIENTES_REV2.md) y [matriz normativa](documentacion/MATRIZ_NORMATIVA_REV2.md) explican el alcance.

Planos de revisión: [CL-01](plans/CL-01_REV2_MANUAL.pdf), [CL-02](plans/CL-02_REV2_MANUAL.pdf), [CL-03](plans/CL-03_REV2_MANUAL.pdf), [CL-04](plans/CL-04_REV2_MANUAL.pdf) y [CL-05](plans/CL-05_REV2_MANUAL.pdf). Cada uno tiene DXF y PNG del mismo nombre base. Los archivos Rev. 1 se conservan más abajo como antecedente del **corredor GIS distinto**.

Reproducir en Windows desde la raíz del repositorio, en un entorno virtual:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r proyectos/renzo-linea-primaria-capachica-llachon/requirements.txt
python -m pip install lxml shapely matplotlib
python proyectos/renzo-linea-primaria-capachica-llachon/scripts/auditar_corredor_manual.py
python proyectos/renzo-linea-primaria-capachica-llachon/scripts/generar_revision_manual.py
python -m pytest proyectos/renzo-linea-primaria-capachica-llachon/tests -q
```

Los generadores rechazan sobrescrituras. Antes de regenerar, archive explícitamente los CSV, JSON y planos `*_REV2_MANUAL.*` existentes; no modifique `sources/`. [Control de calidad y pendientes](documentacion/CALCULOS_Y_PENDIENTES_REV2.md). El expediente sigue siendo **preliminar y no apto para construcción**.

Para ejecutar y verificar todo en una sola orden desde la raíz del repositorio: `python proyectos/renzo-linea-primaria-capachica-llachon/scripts/reproducir_rev2.py --archive-existing`. La opción archiva únicamente las salidas Rev. 2 existentes bajo `build/renzo-linea-primaria-capachica-llachon/archive_rev2/` antes de regenerarlas.

**Este es el estudio de Capachica a Llachón.** Todos los datos y planos activos de este proyecto corresponden a ese corredor.

**Expediente integrado Rev. 1:** [abrir capítulos editables](expediente/README.md). El [informe de auditoría correctiva](documentacion/AUDITORIA_REV0.md) explica los hallazgos previos. La copia PDF y el ZIP **Rev. 1** para revisión están en `build/renzo-linea-primaria-capachica-llachon/` de esta máquina. Incluyen los dos planos A3; mantienen visible que faltan datos esenciales para ingeniería de construcción.

## Abrir los dos planos en AutoCAD

| Lámina | DXF con presentación A3 para AutoCAD | Vista del DXF | PDF cartográfico complementario |
|---|---|---|---|
| **CL-01 · Ubicación y corredor** | [CL-01 A3 DXF](plans/CL-01_A3_AUTOCAD_PRELIMINAR.dxf) | [PDF renderizado](plans/CL-01_A3_AUTOCAD_PRELIMINAR_vista.pdf) · [PNG](plans/CL-01_A3_AUTOCAD_PRELIMINAR_vista.png) | [PDF de ubicación](plans/CL-01_ubicacion_corredor.pdf) |
| **CL-02 · Perfil referencial del terreno** | [CL-02 A3 DXF](plans/CL-02_A3_AUTOCAD_PRELIMINAR.dxf) | [PDF renderizado](plans/CL-02_A3_AUTOCAD_PRELIMINAR_vista.pdf) · [PNG](plans/CL-02_A3_AUTOCAD_PRELIMINAR_vista.png) | [PDF de perfil](plans/CL-02_perfil_referencial.pdf) |

En AutoCAD, abre la pestaña **`CL-01_A3`** o **`CL-02_A3`** y selecciona A3 horizontal, escala de papel 1:1. La geometría en modelo está en metros. También se conservan los [DXF iniciales georreferenciados](plans/CL-01_corredor_utm19s.dxf) y [del perfil en metros](plans/CL-02_perfil_srtm_metros.dxf).

El origen de referencia es la estructura GIS `NMT000367723` próxima a Capachica y el final elegido es `NMT000027963` próximo a Llachón. La longitud calculada sobre el corredor GIS es **13,834 km**. Las coordenadas, los 27 tramos utilizados, las fuentes y las limitaciones están en el [planteamiento técnico](PLANTEAMIENTO_CAPACHICA_LLACHON.md), la [memoria del anteproyecto](documentacion/MEMORIA_ANTEPROYECTO.md) y el [control de calidad](documentacion/CONTROL_CALIDAD.md).

**Estado: borrador cartográfico.** La ruta azul del CL-01 sigue una red de media tensión publicada; no representa una línea nueva aprobada. El CL-02 usa terreno SRTM30m y no sirve para definir postes, flechas ni distancias de seguridad. Falta validar en campo y con Electro Puno el punto de conexión, la tensión, la capacidad y la necesidad de obra.

Las fuentes originales están en [`sources/`](sources/), con URL, fecha y SHA-256 en [`manifest.json`](sources/manifest.json). La geometría derivada está en [`route.json`](derived/route.json). El [cuadro GIS de tramos](datos/cuadro_tramos_gisem.csv) y el [reporte CAD](datos/reporte_generacion_cad.json) permiten comprobar el origen de las láminas. Los parámetros de diseño aún no validados se registran como `null` en [parametros_diseno_pendientes.json](datos/parametros_diseno_pendientes.json).

Los DXF A3 fueron generados por [`scripts/generar_anteproyecto_cad.py`](scripts/generar_anteproyecto_cad.py), reabiertos con `ezdxf` y renderizados por [`scripts/render_verificacion_cad.py`](scripts/render_verificacion_cad.py). Los scripts no sobrescriben las salidas existentes. Para reproducirlos, prepara una copia del proyecto sin los archivos de salida y ejecuta desde la raíz del repositorio:

```powershell
python -m pip install -r proyectos/renzo-linea-primaria-capachica-llachon/requirements.txt
python proyectos/renzo-linea-primaria-capachica-llachon/scripts/generar_anteproyecto_cad.py
python proyectos/renzo-linea-primaria-capachica-llachon/scripts/render_verificacion_cad.py
python -m pytest proyectos/renzo-linea-primaria-capachica-llachon/tests -q
python proyectos/renzo-linea-primaria-capachica-llachon/scripts/compilar_expediente.py
```

El compilador genera la Rev. 1 y rechaza la sobrescritura de una salida existente. Los paquetes anteriores se conservan como historial local; la revisión activa es la indicada en `proyecto.yaml`.

La extracción cartográfica inicial se hizo en el repositorio local `workspace/seace-cad-intelligence/studies/capachica_llachon`; sus archivos fuente y derivados necesarios están copiados aquí. **AutoCAD no se ejecutó en esta máquina**: el control realizado fue apertura y auditoría estructural con `ezdxf` más render de las presentaciones mediante su motor de dibujo.

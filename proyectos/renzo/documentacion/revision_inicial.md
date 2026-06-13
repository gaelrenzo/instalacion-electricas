# Auditoría Inicial del Repositorio
## Proyecto: Instalación Eléctrica Domiciliaria - Vivienda Unifamiliar de 3 Pisos
**Autor:** Antigravity (IA Coding Assistant)
**Fecha:** 2026-06-03
**Integrante del Proyecto:** Renzo Gabriel Mamani Galindo

---

### 1. Archivos Encontrados en el Repositorio

Tras realizar una inspección exhaustiva de la estructura de archivos en la raíz del repositorio y las carpetas secundarias, se han identificado las siguientes áreas de trabajo y archivos clave:

#### Raíz del Repositorio (`/`)
- `README.md`: Contiene las instrucciones generales del proyecto y la descripción de las carpetas.
- `generar_plano.ps1`: Script de automatización en PowerShell para Windows. Instala dependencias y llama a `dxf_generator.py` para compilar los archivos JSON a planos DXF y renderizarlos a PDF.
- `informe_instalaciones_electricas.md`: Documento consolidado del proyecto académico con memoria descriptiva y cálculos preliminares.
- `test.dxf`: Archivo DXF de prueba generado por las herramientas locales.
- Directorios principales:
  - `proyectos/aquiles/`: Contiene el avance y material del alumno Aquiles Taylor. Incluye notas normativas, borradores de informes y su propio espacio CAD (`trabajo-cad-casa/`).
  - `avance-capitulos-1-2/`: Carpeta con borradores iniciales del informe académico.
  - `herramientas/`: Aloja el motor de generación CAD y una calculadora web interactiva.
  - `latex/`: Carpeta que contiene subdirectorios `build/` y `planos/` con recursos de renderizado.
  - `materiales/`: Directorio con archivos PDF de normas, fotos de clase y proyectos de referencia.
  - `proyectos/renzo/`: **Carpeta de trabajo exclusivo para este proyecto**, que contiene el informe en LaTeX, planos base y entregables eléctricos.

#### Carpeta del Motor CAD (`/herramientas/cad/`)
- `README.md`: Explicación técnica del generador automático 2D.
- `generar_plano.sh`: Lanzador para entornos Bash en Linux.
- `cad-scripts/dxf2pdf.js`: Script de QCAD para renderizado a PDF (headless mode).
- `data/`: Contiene archivos de entrada estructurados en JSON:
  - `layout_example.json`
  - `primer_piso.json`
  - `segundo_piso.json`
  - `tercer_piso.json`
- `scripts/dxf_generator.py`: Script principal en Python que lee el archivo JSON y dibuja los muros dobles, puertas, ventanas y cotas en el archivo DXF usando `ezdxf` y `matplotlib`.

#### Carpeta del Proyecto de Renzo (`/proyectos/renzo/`)
- `README.md`: Instrucciones de compilación en LaTeX y organización de planos.
- `main.tex`: Archivo principal del reporte LaTeX.
- `capitulos/`: Archivos `.tex` sección por sección (portada, memoria descriptiva, cálculos, especificaciones, etc.).
- `planos/`: Contiene las imágenes base y copias de los planos generados:
  - `primer-piso.jpg`, `segundo-piso.jpg`, `tercer-piso.jpg`: Planos arquitectónicos originales en formato imagen (fuente de interpretación).
  - `primer-piso.pdf`, `segundo-piso.pdf`, `tercer-piso.pdf`
  - `primer-piso.dxf`, `segundo-piso.dxf`, `tercer-piso.dxf`
  - `AVANCE DEL PLANO ELECTRICO1.dwg` / `.pdf`: Archivo del avance inicial del plano.
  - `ejemplo-distribucion.dxf` / `.pdf`
  - `IE-02-alumbrado.pdf`, `IE-03-tomacorrientes.pdf`, `IE-04-circuitos-canalizaciones.pdf`, `IE-05-unifilar-cuadro-cargas.pdf`, `IE-06-puesta-tierra.pdf`: Planos eléctricos embebidos en el informe compilado.

#### Carpeta de Renderizado de Planos (`/latex/planos/`)
- `draw_planos.py`: Script en Python independiente que dibuja directamente en código (hardcoded) la distribución arquitectónica tridimensional de la vivienda unifamiliar y un rótulo para "Aquiles Taylor Ramos Yapo".
- `piso-1.jpg`, `piso-2.jpg`, `piso-3.jpg`: Copias de los planos base en formato JPG.
- `AVANCE DEL PLANO ELECTRICO1.dxf`: Salida generada por `draw_planos.py`.

---

### 2. Herramientas Identificadas

#### Herramientas Vigentes (Reutilizables y Robustas)
1.  **Motor IA-CAD-Casas (`dxf_generator.py`):** Es una herramienta muy potente que permite parametrizar las coordenadas, ambientes, puertas y ventanas en un archivo JSON y generar automáticamente planos consistentes en formato DXF. Cuenta con capas dedicadas (`MUROS`, `PUERTAS`, `VENTANAS`, `TEXTOS`, `ESCALERAS`, `COTAS`, `MARCO`) y membrete personalizado.
2.  **Script de Renderizado (`generar_plano.ps1`):** Ejecuta el flujo completo en Windows de forma limpia y asegura la instalación de `ezdxf` y `matplotlib`.
3.  **Matplotlib Backend de DXF:** Se utiliza en `dxf_generator.py` para generar automáticamente copias vectoriales en formato PDF a partir del archivo DXF, lo cual soluciona la necesidad de tener QCAD instalado de forma local.

#### Herramientas Experimentales / Secundarias
1.  **Script Directo (`latex/planos/draw_planos.py`):** Dibuja los muros e interruptores mediante coordenadas directas en código, sin usar archivos JSON. Es útil para comprender la geometría del terreno ($4.5\text{ m} \times 8.5\text{ m}$ útiles, $9.0\text{ m}$ totales) y la lógica de dibujo de escaleras y abatimiento de puertas.
2.  **Calculadora Web (`herramientas/calculadora-instalacion-casa.html`):** Una herramienta HTML interactiva para cálculos aproximados de circuitos de viviendas.

---

### 3. Archivos Duplicados y Superposiciones
- **Planos Base JPG:** Las imágenes de los planos base se encuentran duplicadas en `proyectos/renzo/planos/` (`primer-piso.jpg`...) y en `latex/planos/` (`piso-1.jpg`...). Ambas corresponden a la misma arquitectura de 3 niveles de la vivienda unifamiliar.
- **Códigos de renderizado:** Se identificaron una lógica basada en JSON y otra basada en coordenadas fijas en Python. La estructura actual conserva el generador multipiso en `proyectos/renzo/scripts/`.

---

### 4. Riesgos Técnicos del Proyecto
1.  **Falta de Trazabilidad en Modificaciones Manuales:** Si se modifica a mano un archivo DXF en QCAD o LibreCAD, la modificación no se verá reflejada en el archivo JSON original, lo que rompería el principio de "Single Source of Truth" (única fuente de verdad).
2.  **Incompatibilidad de Nombres y Membretes:** El proyecto guía de la carpeta `/proyectos/aquiles/` tiene referencias al alumno "Aquiles Taylor", mientras que este proyecto debe estar personalizado en su totalidad para **"Renzo Gabriel Mamani Galindo"**.
3.  **Conflictos de Compilación LaTeX:** Si se colocan archivos en directorios incorrectos, `pdflatex` fallará por falta de referencias a figuras o tablas de metrados.

---

### 5. Oportunidades de Reutilización
- El generador automático `dxf_generator.py` se puede extender con suma facilidad para admitir las rutas de layouts específicos de la vivienda y salidas personalizadas.
- Se reutilizarán las imágenes base JPG de los planos para modelar con precisión los ambientes reales del proyecto final en coordenadas cartesianas, asegurando la consistencia entre los planos del informe y el diseño físico del estudiante.
- El informe LaTeX de `proyectos/renzo` se mantiene como la base del entregable final de 72 páginas, por lo que toda mejora debe alimentar directamente sus figuras y cuadros.

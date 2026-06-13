# Análisis del motor CAD
**Autor:** Antigravity (IA Coding Assistant)
**Fecha:** 2026-06-03

---

### 1. Arquitectura General y Flujo de Trabajo
El motor de `herramientas/cad/` permite convertir una especificación abstracta de distribución arquitectónica en JSON a archivos CAD 2D vectoriales estándar.

El flujo se divide en dos etapas principales:
1.  **Generación Vectorial (Python - `dxf_generator.py`):**
    Lee un archivo JSON descriptivo, realiza validaciones geométricas elementales y escribe un archivo DXF utilizando la biblioteca `ezdxf` de Python. Genera muros dobles de $0.15\text{ m}$ de espesor, peldaños de escalera automáticos, vanos de puertas abatidas, ventanas con detalle de marco/vidrio, cotas generales y un marco decorativo con bloque de título (cajetín).
2.  **Exportación a PDF (QCAD/Matplotlib):**
    - En sistemas Windows/Linux sin QCAD Pro instalado, `dxf_generator.py` incluye un renderizador de respaldo basado en **`matplotlib`** (`ezdxf.addons.drawing`). Este renderiza el modelo vectorial directamente a un archivo PDF vectorial y centrado de forma nativa.
    - En entornos de integración compatibles con QCAD, se puede ejecutar el script ECMAScript `cad-scripts/dxf2pdf.js` en modo headless (`-no-gui -platform offscreen`) para cargar el DXF y exportarlo a PDF vectorial calibrado en tamaño A4 horizontal.

---

### 2. Estructura del Formato JSON Esperado

El archivo JSON debe contener un objeto raíz con la siguiente especificación de campos:

-   `project` (string): Nombre del proyecto (aparecerá en el cajetín).
-   `author` (string): Nombre del dibujante/estudiante (aparecerá en el cajetín).
-   `date` (string): Fecha del plano (AAAA-MM-DD).
-   `units` (string): Unidad del plano (comúnmente "meters").
-   `dimensions` (object): Objeto con las dimensiones del terreno:
    -   `width` (float): Ancho total de la planta (eje X, metros).
    -   `height` (float): Alto total de la planta (eje Y, metros).
    -   `margin` (float, opcional): Margen del marco exterior (por defecto $1.5\text{ m}$).
-   `rooms` (array of objects): Lista de habitaciones. Cada una tiene:
    -   `id` (string): Identificador único (ej. "R1").
    -   `name` (string): Nombre del ambiente (ej. "Sala / Comedor"). Si empieza con guion bajo (`_`), se dibuja la geometría pero se omiten las etiquetas de texto.
    -   `x` (float): Coordenada X inferior izquierda del ambiente.
    -   `y` (float): Coordenada Y inferior izquierda del ambiente.
    -   `width` (float): Ancho del ambiente (eje X).
    -   `height` (float): Alto del ambiente (eje Y).
-   `doors` (array of objects): Puertas a dibujar. Cada una tiene:
    -   `id` (string): Identificador.
    -   `room_from` (string): ID de habitación de origen.
    -   `room_to` (string): ID de habitación de destino.
    -   `x` (float): Coordenada X del eje de giro (bisagra) o punto de inicio del vano.
    -   `y` (float): Coordenada Y del eje de giro.
    -   `width` (float): Ancho de la hoja de la puerta (ej. $0.80\text{ m}$).
    -   `orientation` (string): `"horizontal"` o `"vertical"`. Define la orientación de la ranura del vano en el muro.
    -   `swing` (string): Dirección del abatimiento. Valores válidos:
        -   `"top-right"`, `"top-left"`, `"bottom-right"`, `"bottom-left"`
-   `windows` (array of objects, opcional): Ventanas. Cada una tiene:
    -   `id` (string): Identificador.
    -   `x` (float): Coordenada X del centro o inicio de la ventana.
    -   `y` (float): Coordenada Y del centro o inicio de la ventana.
    -   `width` (float): Ancho de la ventana.
    -   `orientation` (string): `"horizontal"` o `"vertical"`.
-   `stairs` (array of objects, opcional): Escaleras. Cada una tiene:
    -   `x1`, `y1` (float): Esquina inferior izquierda del contorno de la escalera.
    -   `x2`, `y2` (float): Esquina superior derecha del contorno.
    -   `steps` (int, opcional): Número de peldaños (por defecto 6).
-   `ignored_walls` (array of arrays, opcional): Muros colindantes que deben ser eliminados del dibujo (por ejemplo, para crear accesos libres o arcos de paso sin muros entre Sala y Comedor). Formato: `[[(x1, y1), (x2, y2)], ...]`.

---

### 3. Capas y Estilos de Dibujo CAD

El generador crea y organiza el dibujo en las siguientes capas estándar con colores ACI (AutoCAD Color Index):

1.  `MUROS` (Color 7 - Blanco/Negro, Grosor $0.35\text{ mm}$): Representa los muros exteriores e interiores con doble línea paralela ($0.15\text{ m}$ de separación).
2.  `PUERTAS` (Color 1 - Rojo): Líneas para la hoja de la puerta y arcos continuos de 90° para el abatimiento.
3.  `VENTANAS` (Color 4 - Cian): Dibuja un rectángulo estrecho sobre el eje del muro con una línea central que representa el vidrio.
4.  `TEXTOS` (Color 2 - Amarillo): Etiquetas de nombres de ambientes y textos generales.
5.  `ESCALERAS` (Color 5 - Azul): Contorno de la caja de escalera y peldaños paralelos (huellas).
6.  `COTAS` (Color 8 - Gris): Líneas de extensión, líneas de cota, marcas oblicuas de cota y textos de dimensiones.
7.  `MARCO` (Color 7 - Blanco/Negro, Grosor $0.50\text{ mm}$): Contorno perimetral decorativo y cajetín informativo.

---

### 4. Limitaciones del Motor CAD Actual

1.  **Muros diagonales no soportados:** La lógica para eliminar muros duplicados y dibujar líneas dobles asume que todos los muros son ortogonales (paralelos a los ejes X e Y). Los muros inclinados o con arcos de círculo producirán artefactos.
2.  **No detecta colisiones de textos:** Si las habitaciones son muy pequeñas, el nombre del ambiente y las cotas de texto en el centro pueden solaparse.
3.  **Puertas con giros fijos:** El script asume que la bisagra se encuentra exactamente en la coordenada $(x, y)$ proporcionada. Si el vano no está alineado adecuadamente, la hoja de la puerta puede cruzarse con los muros.

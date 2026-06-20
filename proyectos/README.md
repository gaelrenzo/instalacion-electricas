# Proyectos y Viviendas (proyectos/)

Este directorio contiene los casos de estudio y diseños específicos para cada vivienda. Cada proyecto está aislado y contiene sus propios datos de entrada, parámetros y entregables.

## Estructura de un Proyecto

Cada subcarpeta de proyecto (por ejemplo, `aquiles/`, `renzo/`) debe seguir la siguiente estructura:

*   **`proyecto.yaml`**: Archivo de configuración central que declara la identidad del proyecto, parámetros y estado de entregables.
*   **`fuentes/`**: Evidencia original (croquis, fotos, requerimientos del cliente). **Es de solo lectura**.
*   **`arquitectura/datos/`**: Archivo JSON/YAML con la geometría y ambientes aprobados.
*   **`diseno-electrico/datos/`**: Datos canónicos de circuitos, cargas y ubicaciones de tableros.
*   **`datos/`**: Constantes y especificaciones de cálculo de diseño.
*   **`documentacion/`**: Reportes de revisión humana, supuestos tomados y actas.
*   **`entregables/`**: Planos, metrados y presupuestos definitivos aprobados para entrega.

## Flujo de Trabajo
1. Colocar el plano original en `fuentes/`.
2. Ejecutar el pipeline de extracción.
3. Validar geometría y realizar diseño eléctrico en las carpetas de `datos/`.
4. Generar y publicar el expediente final en `entregables/`.

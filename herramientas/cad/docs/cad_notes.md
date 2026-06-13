# Notas Técnicas: Capacidades de Automatización de QCAD y LibreCAD en Linux

Este documento resume los hallazgos de la auditoría técnica local realizada sobre las instalaciones de QCAD y LibreCAD en el sistema.

---

## 1. QCAD (Versión 3.32.9)

### Ubicación del binario y estructura:
* Binario principal: `/sbin/qcad` (Enlace simbólico a `/usr/lib/qcad/qcad-bin`).
* Carpeta de scripts internos: `/usr/lib/qcad/scripts/`.

### Capacidades de Automatización Encontradas:
QCAD proporciona soporte completo para la ejecución headless y automatización basada en scripts (Qt Script/ECMAScript/JavaScript):

1. **Modo Headless (`-no-gui`)**:
   Permite ejecutar QCAD sin lanzar la interfaz gráfica, ideal para ejecuciones por consola y scripts de integración continua.

2. **Ejecución Offscreen (`-platform offscreen`)**:
   Permite que la consola conecte con el motor gráfico de renderizado sin necesidad de tener un servidor X11 activo (sin pantalla/display), evitando fallos en servidores de backend o tareas cron.

3. **Ejecución de Scripts (`-autostart [script.js]` o `-exec [script.js]`)**:
   - `-autostart`: Ejecuta un archivo de script como punto de entrada de la aplicación, puenteando la interfaz por defecto.
   - `-exec`: Arranca QCAD y corre el script inmediatamente después de cargar.

4. **Conversión a PDF (dxf2pdf.js)**:
   Aunque las herramientas de pago de QCAD Pro (como el ejecutable compilado `dwg2pdf`) no están en la edición comunitaria, QCAD permite cargar e importar archivos DXF y utilizar el módulo `scripts/File/Print/Print.js` para generar PDFs programáticamente. Hemos desarrollado `cad-scripts/dxf2pdf.js` para automatizar este flujo.

---

## 2. LibreCAD

### Ubicación del binario:
* Binario principal: `/sbin/librecad`.

### Capacidades de Automatización Encontradas:
* **Automatización en CLI**: Muy limitada. LibreCAD no está diseñado nativamente para procesamiento por lotes o scripting headless robusto desde la terminal.
* **Rol sugerido**: Actúa exclusivamente como un **visor y editor interactivo secundario**. Es extremadamente ligero y excelente para que el estudiante revise el DXF resultante, realice ajustes manuales en los nodos, cambie estilos de línea y exporte manualmente si así lo prefiere.

---

## 3. Arquitectura del Flujo de Trabajo Recomendado

```text
  [Datos JSON] ──(Python: dxf_generator.py)──> [Archivo DXF]
                                                     │
                                             (QCAD Headless Script)
                                                     │
                                                     ▼
                                              [Informe PDF / Planos]
```

1. **Python (`dxf_generator.py`)**: Se encarga de procesar los datos de entrada, validarlos y estructurar las entidades matemáticas en el archivo DXF (muros, textos, cotas, bloques de título).
2. **QCAD (`dxf2pdf.js`)**: Lee el DXF resultante, calcula su cuadro delimitador (bounding box) para auto-centrar el dibujo en un plano A4 y lo exporta a PDF de forma desatendida.
3. **QCAD / LibreCAD (GUI)**: Utilizados por el usuario de forma interactiva para visualizar, corregir o guardar el archivo final.

---

## 4. Validación del motor

- QCAD headless generó correctamente PDF a partir de varios planos de prueba.
- Las pruebas interactivas con `timeout qcad <archivo.dxf>` y `timeout librecad <archivo.dxf>` confirmaron que las aplicaciones intentan cargar los DXF; LibreCAD mostro las capas `MUROS`, `PUERTAS`, `VENTANAS`, `TEXTOS`, `COTAS`, `MARCO`, `ESCALERAS`, `TRAMAS`, `MOBILIARIO` y `ANOTACIONES`.
- `pdftoppm` no fue fiable para rasterizar los PDF generados por QCAD en esta maquina; emitio `Bogus memory allocation size`. Para revision visual se uso render temporal desde DXF con `ezdxf` y `matplotlib`.
- Se fijaron colores verdaderos negro/gris en las capas del DXF para evitar que muros o textos se vean blancos o demasiado claros sobre fondo blanco.

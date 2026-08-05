# Guía de Integración de QElectroTech (QET)

Este documento describe la integración de **QElectroTech** ([qelectrotech-source-mirror](https://github.com/qelectrotech/qelectrotech-source-mirror)) en el ecosistema de automatización de instalaciones eléctricas del repositorio.

QElectroTech es una herramienta libre y de código abierto (Qt/C++) especializada en el trazado de esquemas eléctricos, planos unifilares y diagramas de control.

---

## 1. ¿Por qué QElectroTech en el Proyecto?

En el diseño de instalaciones eléctricas bajo la normativa peruana (**Código Nacional de Electricidad - Utilización, CNE-U**, **Reglamento Nacional de Edificaciones EM.010** y **Simbología DGE del Ministerio de Energía y Minas**), se requiere generar dos tipos principales de gráficos CAD:

1. **Planos Arquitectónicos y Distribución en Planta (DWG/DXF):** Trazado de centros de luz, tomacorrientes y alimentadores sobre la arquitectura.
2. **Diagramas Unifilares y Esquemas de Tableros (SCH/QET/DXF):** Esquemas esquemáticos de la acometida, medidor, interruptor general (ITM), alimentadores, protecciones diferenciales (ID), barras colectoras y circuitos derivados.

**QElectroTech** destaca por:
* **Formatos de archivo abiertos basados en XML:** Los archivos de proyecto (`.qet`), elementos (`.elmt`) y rótulos/cartuchos (`.qpt`) son XML legibles y versionables directamente con Git.
* **Soporte de CLI para automatización:** Permite exportar proyectos `.qet` a PDF, SVG y DXF mediante línea de comandos sin interfaz gráfica (`qelectrotech --export-pdf ...`).
* **Simbología DGE / MEM:** Flexibilidad total para definir símbolos personalizados (`.elmt`) que cumplan con la norma peruana de símbolos gráficos en electricidad DGE-MEM.
* **Editor de Rótulos Integrado:** Definición de membretes normalizados con campos dinámicos (Propietario, Alumno, Código, Escala, Fecha, Lámina IE-01).

---

## 2. Estructura de Archivos QElectroTech (`.qet`, `.elmt`, `.qpt`)

El código fuente de QElectroTech ([qelectrotech-source-mirror](https://github.com/qelectrotech/qelectrotech-source-mirror)) define los siguientes formatos basados en XML:

### A. Proyectos (`.qet`)
Contienen los diagramas, esquemas, conexiones eléctricas, orientaciones de cableado y datos del proyecto.

```xml
<qet-project version="0.90" title="Diagrama Unifilar Tablero General TD">
  <properties>
    <property name="propietario" value="Diego Jefferson Charaja Mamani"/>
    <property name="codigo" value="214254"/>
    <property name="docente" value="Ing. Villanueva Cornejo Marcos Jose"/>
    <property name="universidad" value="UNAP - EPIME"/>
  </properties>
  <diagram width="1050" height="1485" title="Lámina IE-01 - Diagrama Unifilar">
    <!-- Componentes y conductores -->
  </diagram>
</qet-project>
```

### B. Elementos / Símbolos (`.elmt`)
Definen la geometría vectorial y los bornes/terminales de conexión de cada dispositivo.

* `itm_tripolar.elmt`: Interruptor Termomagnético 3Ø ($3 \times 40\text{ A}$, $10\text{ kA}$).
* `id_diferencial.elmt`: Interruptor Diferencial ($2P / 3P$, $30\text{ mA}$).
* `medidor_m1.elmt`: Medidor de Energía kWh Monofásico / Trifásico.

### C. Plantillas de Rótulo / Membrete (`.qpt`)
Definen la cajetilla normalizada según DGE/MEM con variables dinámicas de proyecto.

---

## 3. Automatización mediante Script Python (`qet_generator.py`)

El script `herramientas/cad/scripts/qet_generator.py` permite transformar un archivo canónico JSON de resultados de cálculo (`resultados.json`) directamente en un archivo de esquema QElectroTech (`.qet`).

### Ejemplo de uso:

```bash
python3 herramientas/cad/scripts/qet_generator.py \
  --resultados proyectos/diego-unifamiliar/resultados_diego.json \
  --output build/diego-unifamiliar/diagrama_unifilar.qet
```

---

## 4. Exportación en Línea de Comandos (CLI)

Una vez generado el archivo `.qet`, se puede exportar en el entorno CI/CD o contenedor mediante QElectroTech:

```bash
# Exportar a PDF vectorial de alta resolución
qelectrotech --export-pdf build/proyecto/diagrama_unifilar.pdf build/proyecto/diagrama_unifilar.qet

# Exportar a formato DXF CAD
qelectrotech --export-dxf build/proyecto/diagrama_unifilar.dxf build/proyecto/diagrama_unifilar.qet

# Exportar a gráfico vectorial SVG
qelectrotech --export-svg build/proyecto/diagrama_unifilar.svg build/proyecto/diagrama_unifilar.qet
```

---

## 5. Referencia del Repositorio de Origen

* **Repositorio Oficial Mirror:** [https://github.com/qelectrotech/qelectrotech-source-mirror](https://github.com/qelectrotech/qelectrotech-source-mirror)
* **Licencia:** GNU General Public License v2.0 (GPLv2).
* **Documentación Oficial QET:** [https://qelectrotech.org/](https://qelectrotech.org/)

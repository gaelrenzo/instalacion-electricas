# Motor CAD y Diagramas Eléctricos (QElectroTech & ezdxf)

Motor de generación y procesamiento de planos CAD arquitectónicos, layouts eléctricos y diagramas unifilares para expedientes técnicos según normativa peruana (CNE-U, RNE EM.010, Simbología DGE del MEM).

---

## 🛠️ Herramientas CAD Integradas

### 1. QElectroTech (`.qet`) - Esquemas Eléctricos y Diagrama Unifilar
[QElectroTech](https://github.com/qelectrotech/qelectrotech-source-mirror) es el software libre de esquemática eléctrica utilizado para la generación automática de diagramas unifilares, cajas de medición, tableros generales (TD), protecciones termomagnéticas (ITM) y diferenciales (ID).

* **Documentación completa:** Consulta [`QELECTROTECH.md`](QELECTROTECH.md).
* **Generación automática:**
  ```bash
  python3 herramientas/cad/scripts/qet_generator.py \
    --resultados proyectos/diego-unifamiliar/resultados_diego.json \
    --output build/diego-unifamiliar/diagrama_unifilar.qet
  ```

### 2. Generador DXF / ezdxf (`dxf_generator.py` y `generar_unifilar.py`)
Convierte datos estructurados en formato JSON a archivos DXF vectoriales compatibles con AutoCAD, LibreCAD y QCAD.

```bash
# Generar plano de disposición física
python3 herramientas/cad/scripts/dxf_generator.py \
  --input herramientas/cad/examples/layout.json \
  --output build/cad/plano.dxf

# Generar diagrama unifilar en DXF y PDF
python3 herramientas/cad/scripts/generar_unifilar.py \
  --resultados proyectos/diego-unifamiliar/resultados_diego.json \
  --output build/diego-unifamiliar/diagrama_unifilar.dxf
```

---

## 📐 Flujo de Salida CAD y Exportación

1. **JSON Canónico** (`resultados.json` / `layout.json`) -> Entrada de datos de ingeniería.
2. **Generación `.qet` / `.dxf`** -> Archivos vectoriales editables.
3. **Exportación CLI a PDF / SVG** -> Entregables finales para expediente técnico en `proyectos/<proyecto>/entregables/`.

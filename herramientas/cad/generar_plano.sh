#!/bin/bash
# Generador de Planos CAD 2D - Script Automatizado para Linux
# Puede ejecutarse desde cualquier directorio.

# Salir inmediatamente si algún comando falla
set -e

# Obtener la ruta absoluta de la carpeta donde se encuentra este script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

# Valores por defecto (se pueden pasar como argumentos)
REPO_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
INPUT_FILE="${1:-$SCRIPT_DIR/examples/layout.json}"
OUTPUT_DXF="${2:-$REPO_DIR/build/cad/plan_distribucion.dxf}"
OUTPUT_PDF="${3:-$REPO_DIR/build/cad/plan_distribucion.pdf}"

# Asegurar que existan los directorios de salida
mkdir -p "$(dirname "$OUTPUT_DXF")"
mkdir -p "$(dirname "$OUTPUT_PDF")"

echo "=========================================================="
echo "   Iniciando Generador Automático de Planos CAD 2D"
echo "=========================================================="
echo "   - Entrada: $INPUT_FILE"
echo "   - Salida DXF: $OUTPUT_DXF"
echo "   - Salida PDF: $OUTPUT_PDF"
echo "=========================================================="

# 1. Comprobar si Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 no está instalado en el sistema." >&2
    exit 1
fi

# 2. Crear entorno virtual si no existe
if [ ! -d "$VENV_DIR" ]; then
    echo "Creando entorno virtual de Python en $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

# 3. Activar entorno virtual
echo "Activando entorno virtual..."
source "$VENV_DIR/bin/activate"

# 4. Instalar dependencias necesarias
echo "Asegurando dependencias (ezdxf)..."
pip install --quiet ezdxf

# 5. Ejecutar generador de planos (DXF)
echo "Ejecutando script de generación DXF..."
python3 "$SCRIPT_DIR/scripts/dxf_generator.py" --input "$INPUT_FILE" --output "$OUTPUT_DXF"

# 6. Ejecutar QCAD headless para renderizar a PDF
if command -v qcad &> /dev/null; then
    echo "Ejecutando QCAD headless para renderizar a PDF..."
    ABS_OUTPUT_DXF=$(realpath "$OUTPUT_DXF")
    ABS_OUTPUT_PDF=$(realpath "$OUTPUT_PDF")
    ABS_SCRIPT=$(realpath "$SCRIPT_DIR/cad-scripts/dxf2pdf.js")
    qcad -no-gui -platform offscreen -quit -autostart "$ABS_SCRIPT" -input "$ABS_OUTPUT_DXF" -output "$ABS_OUTPUT_PDF"
else
    echo "Advertencia: QCAD no se encuentra en el PATH. No se pudo generar el PDF automáticamente."
fi

echo "=========================================================="
echo "   Proceso finalizado con exito"
echo "   Puedes ver el DXF en Linux usando QCAD o LibreCAD:"
echo "      qcad \"$OUTPUT_DXF\""
echo "      librecad \"$OUTPUT_DXF\""
echo "=========================================================="

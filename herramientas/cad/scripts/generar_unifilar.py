#!/usr/bin/env python3
"""
Generador de diagrama unifilar en formato DXF.

A partir del JSON de resultados de calculo, genera un diagrama unifilar
profesional listo para incluir en el expediente tecnico.

Uso:
  python3 generar_unifilar.py --resultados build/proyecto/calculos/resultados.json --output build/proyecto/diagrama_unifilar.dxf
  python3 generar_unifilar.py --resultados build/proyecto/calculos/resultados.json --output build/proyecto/diagrama_unifilar.pdf
"""

import argparse
import json
import math
import os
import sys

try:
    import ezdxf
    from ezdxf.enums import TextEntityAlignment
except ImportError:
    ezdxf = None
    TextEntityAlignment = None


LAYER_SPECS = {
    "UNIFILAR_LINEAS": {"color": 7, "lineweight": 25},
    "UNIFILAR_COMPONENTES": {"color": 7, "lineweight": 35},
    "UNIFILAR_TEXTOS": {"color": 7, "lineweight": 13},
    "UNIFILAR_MARCO": {"color": 8, "lineweight": 18},
    "UNIFILAR_MEDIDOR": {"color": 6, "lineweight": 25},
    "UNIFILAR_TABLERO": {"color": 1, "lineweight": 35},
    "UNIFILAR_PROTECCION": {"color": 3, "lineweight": 25},
    "UNIFILAR_CARGA": {"color": 5, "lineweight": 25},
    "UNIFILAR_TIERRA": {"color": 4, "lineweight": 13},
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_layer(doc, name, spec=None):
    if name not in doc.layers:
        doc.layers.new(name, dxfattribs=spec or {"color": 7})


def setup_layers(doc):
    for name, spec in LAYER_SPECS.items():
        ensure_layer(doc, name, spec)


def add_text(msp, text, x, y, height=0.15, layer="UNIFILAR_TEXTOS", rotation=0):
    entity = msp.add_text(
        str(text),
        dxfattribs={"layer": layer, "height": height, "rotation": rotation},
    )
    entity.set_placement((float(x), float(y)), align=TextEntityAlignment.MIDDLE_CENTER)
    return entity


def add_line(msp, x1, y1, x2, y2, layer="UNIFILAR_LINEAS"):
    msp.add_line((x1, y1), (x2, y2), dxfattribs={"layer": layer})


def add_rect(msp, x, y, w, h, layer="UNIFILAR_COMPONENTES"):
    pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]
    msp.add_lwpolyline(pts, dxfattribs={"layer": layer})


def add_circle(msp, x, y, r, layer="UNIFILAR_COMPONENTES"):
    msp.add_circle((x, y), r, dxfattribs={"layer": layer})


def draw_medidor(msp, x, y):
    add_circle(msp, x, y, 0.25, "UNIFILAR_MEDIDOR")
    add_text(msp, "M", x, y, 0.18, "UNIFILAR_MEDIDOR")
    add_line(msp, x - 0.4, y + 0.5, x, y + 0.5, "UNIFILAR_LINEAS")
    add_line(msp, x, y - 0.5, x, y - 0.25, "UNIFILAR_LINEAS")


def draw_tablero(msp, x, y, label, itm_text):
    add_rect(msp, x - 0.5, y - 0.3, 1.0, 0.6, "UNIFILAR_TABLERO")
    add_text(msp, label, x, y + 0.02, 0.16, "UNIFILAR_TABLERO")
    add_text(msp, itm_text, x, y - 0.45, 0.10, "UNIFILAR_TEXTOS")


def draw_itm(msp, x, y, rating, width=0.5):
    h = 0.22
    add_rect(msp, x - width / 2, y - h / 2, width, h, "UNIFILAR_PROTECCION")
    add_line(msp, x - width / 2, y, x + width / 2, y, "UNIFILAR_PROTECCION")
    add_text(msp, f"{rating}A", x, y, 0.10, "UNIFILAR_PROTECCION")


def draw_diferencial(msp, x, y, rating):
    h = 0.30
    add_rect(msp, x - 0.30, y - h / 2, 0.60, h, "UNIFILAR_PROTECCION")
    add_text(msp, f"{rating}", x, y, 0.09, "UNIFILAR_PROTECCION")


def draw_carga(msp, x, y, label, potencia, seccion, caida):
    add_text(msp, label, x, y, 0.12, "UNIFILAR_CARGA")
    add_text(msp, f"{potencia:.0f}W", x, y - 0.20, 0.09, "UNIFILAR_TEXTOS")
    add_text(msp, f"{seccion:.1f}mm2", x, y - 0.35, 0.08, "UNIFILAR_TEXTOS")
    add_text(msp, f"dV={caida:.2f}%", x, y - 0.50, 0.08, "UNIFILAR_TEXTOS")


def draw_ground(msp, x, y):
    add_line(msp, x, y, x, y - 0.3, "UNIFILAR_TIERRA")
    add_line(msp, x - 0.2, y - 0.3, x + 0.2, y - 0.3, "UNIFILAR_TIERRA")
    add_line(msp, x - 0.12, y - 0.45, x + 0.12, y - 0.45, "UNIFILAR_TIERRA")
    add_line(msp, x - 0.05, y - 0.60, x + 0.05, y - 0.60, "UNIFILAR_TIERRA")
    add_text(msp, "SPAT", x, y - 0.75, 0.09, "UNIFILAR_TIERRA")


def generar_unifilar(resultados, output_path):
    design = resultados["escenario_dimensionamiento"]
    resumen = design["resumen_general"]
    circuitos = design["circuitos_calculados"]

    doc = ezdxf.new("R2010", setup=True)
    setup_layers(doc)
    msp = doc.modelspace()

    X0, Y0 = 2.0, 1.0
    SPACING = 1.8
    BUS_W = 18.0

    # Titulo
    add_text(msp, f"DIAGRAMA UNIFILAR", BUS_W / 2 + X0, Y0 + 15.5, 0.35, "UNIFILAR_TEXTOS")
    add_text(msp, f"{resultados['proyecto']}", BUS_W / 2 + X0, Y0 + 15.0, 0.18, "UNIFILAR_TEXTOS")
    add_text(msp, f"Propietario: {resultados['propietario']}", X0, Y0 + 14.5, 0.12, "UNIFILAR_TEXTOS")
    add_text(
        msp,
        f"MD: {resumen['maxima_demanda_adoptada_w']:.0f} W  |  Ib: {resumen['corriente_empleo_ib_total_a']:.2f} A  |  Alimentador: {resumen['alimentador_seccion_mm2']:.1f} mm2",
        X0, Y0 + 14.0, 0.12, "UNIFILAR_TEXTOS"
    )

    # Bus principal (linea vertical)
    bus_x = X0 + 2.0
    y_start = Y0 + 1.0
    y_end = y_start + (len(circuitos) + 2) * SPACING

    add_line(msp, bus_x, y_start, bus_x, y_end, "UNIFILAR_LINEAS")
    add_text(msp, "FASE", bus_x, y_end + 0.3, 0.10, "UNIFILAR_TEXTOS")
    add_text(msp, "NEUTRO", bus_x - 0.8, y_end + 0.3, 0.10, "UNIFILAR_TEXTOS")
    add_line(msp, bus_x - 0.8, y_start, bus_x - 0.8, y_end, "UNIFILAR_LINEAS")

    # Medidor
    med_y = y_end - SPACING * 0.8
    draw_medidor(msp, bus_x + 1.5, med_y)
    add_line(msp, bus_x, med_y, bus_x + 1.5, med_y, "UNIFILAR_LINEAS")
    add_line(msp, bus_x + 1.5, med_y + 0.5, bus_x + 1.5, med_y + 1.5, "UNIFILAR_LINEAS")
    add_text(msp, "RED", bus_x + 1.5, med_y + 1.7, 0.10, "UNIFILAR_TEXTOS")
    add_text(msp, "PUBLICA", bus_x + 1.5, med_y + 1.5, 0.09, "UNIFILAR_TEXTOS")

    # Alimentador y TG
    tg_y = y_end - SPACING * 1.6
    draw_itm(msp, bus_x + 1.5, tg_y, f"{resumen['alimentador_itm_a']}")
    add_line(msp, bus_x, tg_y, bus_x + 1.5, tg_y, "UNIFILAR_LINEAS")

    tg_label_y = tg_y - SPACING * 0.7
    draw_tablero(msp, bus_x + 1.5, tg_label_y, "TG", f"ITM: {resumen['alimentador_itm_sugerido']} | Cond: {resumen['alimentador_seccion_mm2']:.1f}mm2")
    add_line(msp, bus_x, tg_label_y, bus_x + 1.5, tg_label_y, "UNIFILAR_LINEAS")

    diff_y = tg_label_y - SPACING * 0.5
    draw_diferencial(msp, bus_x + 1.5, diff_y, "2P-40A-30mA")
    add_line(msp, bus_x, diff_y, bus_x + 1.5, diff_y, "UNIFILAR_LINEAS")

    # Circuitos derivados
    y_pos = y_start
    for c in circuitos:
        cx = bus_x + 1.5
        cy = y_pos

        itm_rating = c["itm_a"]
        draw_itm(msp, cx, cy, itm_rating)

        if "diferencial_sugerido" in c and "Ver" not in c.get("diferencial_sugerido", ""):
            add_text(msp, c["diferencial_sugerido"], cx + 1.8, cy, 0.07, "UNIFILAR_PROTECCION")

        carga_y = cy - SPACING * 0.45
        has_ground = c.get("requiere_tierra", True)

        draw_carga(
            msp, cx, carga_y,
            f"{c['id']}: {c['descripcion']}",
            c["potencia_instalada_w"],
            c["seccion_conductor_mm2"],
            c["caida_tension_porc"]
        )

        estado = c.get("cumple_conductor", "")
        color_estado = "CUMPLE" in estado
        add_text(
            msp,
            f"OK" if color_estado else "REVISAR",
            cx + 2.0, carga_y, 0.08,
            "UNIFILAR_PROTECCION"
        )

        add_line(msp, bus_x, cy, cx, cy, "UNIFILAR_LINEAS")
        add_line(msp, bus_x - 0.8, cy, bus_x, cy, "UNIFILAR_LINEAS")

        y_pos += SPACING

    # Puesta a tierra
    spat_y = y_start - SPACING * 0.5
    add_line(msp, bus_x - 0.8, spat_y, bus_x - 0.8, y_start, "UNIFILAR_LINEAS")
    draw_ground(msp, bus_x - 0.8, spat_y)

    # Marco
    margin = 0.5
    mx1, my1 = X0 - margin, Y0 - margin - SPACING
    mx2, my2 = X0 + BUS_W + margin, y_end + margin + 2.0
    add_rect(msp, mx1, my1, mx2 - mx1, my2 - my1, "UNIFILAR_MARCO")

    # Leyenda
    lx = X0 + 14.0
    ly = y_start + SPACING * 0.5
    add_rect(msp, lx, ly, 5.0, 1.8, "UNIFILAR_MARCO")
    add_text(msp, "SIMBOLOGIA", lx + 2.5, ly + 1.6, 0.12, "UNIFILAR_TEXTOS")
    add_line(msp, lx, ly + 1.4, lx + 5.0, ly + 1.4, "UNIFILAR_MARCO")

    add_text(msp, "Medidor", lx + 2.5, ly + 1.1, 0.09, "UNIFILAR_TEXTOS")
    add_text(msp, "ITM / Proteccion", lx + 2.5, ly + 0.8, 0.09, "UNIFILAR_TEXTOS")
    add_text(msp, "Tablero general", lx + 2.5, ly + 0.5, 0.09, "UNIFILAR_TEXTOS")
    add_text(msp, "Carga / Circuito", lx + 2.5, ly + 0.2, 0.09, "UNIFILAR_TEXTOS")

    doc.saveas(output_path)
    print(f"Diagrama unifilar generado: {output_path}")


def exportar_pdf(dxf_path):
    try:
        import matplotlib.pyplot as plt
        from ezdxf.addons.drawing import RenderContext, Frontend
        from ezdxf.addons.drawing.matplotlib import MatplotlibBackend

        pdf_path = dxf_path.replace(".dxf", ".pdf")
        doc = ezdxf.readfile(dxf_path)
        msp = doc.modelspace()
        fig = plt.figure(figsize=(11.69, 8.27))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis("off")
        ctx = RenderContext(doc)
        out = MatplotlibBackend(ax)
        Frontend(ctx, out).draw_layout(msp, finalize=True)
        fig.savefig(pdf_path, dpi=300, bbox_inches="tight", pad_inches=0)
        plt.close(fig)
        print(f"PDF del unifilar generado: {pdf_path}")
    except Exception as e:
        print(f"No se pudo generar PDF: {e}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Genera diagrama unifilar en DXF desde resultados de calculo"
    )
    parser.add_argument("--resultados", required=True,
                       help="JSON de resultados generado por el motor de calculos")
    parser.add_argument("--output", required=True,
                       help="DXF o PDF de salida")
    return parser.parse_args()


def main():
    if ezdxf is None:
        print("Error: ezdxf no esta instalado.")
        sys.exit(1)

    args = parse_args()
    if not os.path.exists(args.resultados):
        print(f"Error: No existe {args.resultados}")
        sys.exit(1)

    resultados = load_json(args.resultados)
    output_path = args.output

    if output_path.endswith(".pdf"):
        dxf_path = output_path.replace(".pdf", ".dxf")
        generar_unifilar(resultados, dxf_path)
        exportar_pdf(dxf_path)
    else:
        generar_unifilar(resultados, output_path)
        exportar_pdf(output_path)


if __name__ == "__main__":
    main()

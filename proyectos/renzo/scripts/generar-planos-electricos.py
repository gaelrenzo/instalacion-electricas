#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path

import ezdxf
from ezdxf.enums import TextEntityAlignment
from ezdxf.math import Matrix44


def tc(rgb):
    return (rgb[0] << 16) + (rgb[1] << 8) + rgb[2]


COLORS = {
    "black": tc((20, 20, 20)),
    "gray": tc((120, 120, 120)),
    "light_gray": tc((205, 205, 205)),
    "red": tc((200, 30, 30)),
    "blue": tc((35, 85, 180)),
    "green": tc((30, 130, 70)),
    "orange": tc((220, 125, 25)),
    "violet": tc((120, 60, 160)),
    "cyan": tc((20, 150, 170)),
    "brown": tc((130, 80, 40)),
}

CIRCUIT_COLORS = {
    "C1": COLORS["orange"],
    "C2": COLORS["blue"],
    "C3": COLORS["red"],
    "C4": COLORS["orange"],
    "C5": COLORS["blue"],
    "C6": COLORS["orange"],
    "C7": COLORS["blue"],
    "C8": COLORS["violet"],
    "C9": COLORS["green"],
}

DGE_SYMBOL_PATH = Path(__file__).resolve().parents[3] / "herramientas" / "simbologia" / "simbologia_normativa_dge.json"
DGE_SYMBOLS = {}


def load_dge_symbols():
    global DGE_SYMBOLS
    if DGE_SYMBOLS:
        return DGE_SYMBOLS
    data = json.loads(DGE_SYMBOL_PATH.read_text(encoding="utf-8-sig"))
    DGE_SYMBOLS = {item["id"]: item for item in data["simbolos"]}
    return DGE_SYMBOLS


def draw_dge_symbol(msp, symbol_id, x, y, layer, color=None, scale=1.0):
    symbol = load_dge_symbols()[symbol_id]

    def px(v):
        return x + v * scale

    def py(v):
        return y + v * scale

    for prim in symbol["primitivas"]:
        attrs = {"layer": layer}
        if color:
            attrs["true_color"] = color
        kind = prim["tipo"]
        if kind == "linea":
            msp.add_line((px(prim["x1"]), py(prim["y1"])), (px(prim["x2"]), py(prim["y2"])), dxfattribs=attrs)
        elif kind == "rectangulo":
            rect(msp, px(prim["x"]), py(prim["y"]), prim["w"] * scale, prim["h"] * scale, layer, color)
        elif kind == "circulo":
            circle(msp, (px(prim["cx"]), py(prim["cy"])), prim["r"] * scale, layer, color)
        elif kind == "circulo_relleno":
            circle(msp, (px(prim["cx"]), py(prim["cy"])), prim["r"] * scale, layer, color)
        elif kind == "arco":
            msp.add_arc(
                (px(prim["cx"]), py(prim["cy"])),
                prim["r"] * scale,
                prim["ang_ini"],
                prim["ang_fin"],
                dxfattribs=attrs,
            )
        elif kind == "texto":
            add_text(
                msp,
                prim["contenido"],
                px(prim["x"]),
                py(prim["y"]),
                prim["h"] * scale,
                layer,
                align=TextEntityAlignment.MIDDLE_LEFT,
            )


def ensure_layer(doc, name, color=7, true_color=None, lineweight=18, linetype="CONTINUOUS"):
    if name not in doc.layers:
        attrs = {"color": color, "lineweight": lineweight, "linetype": linetype}
        if true_color is not None:
            attrs["true_color"] = true_color
        doc.layers.new(name, dxfattribs=attrs)


def add_text(msp, text, x, y, height=0.18, layer="ELEC_TEXTOS", rotation=0, align=TextEntityAlignment.MIDDLE_CENTER):
    msp.add_text(str(text), dxfattribs={"layer": layer, "height": height, "rotation": rotation}).set_placement((x, y), align=align)


def add_multiline(msp, text, x, y, height=0.18, layer="ELEC_TEXTOS", align=TextEntityAlignment.MIDDLE_LEFT):
    lines = str(text).splitlines()
    for i, line in enumerate(lines):
        add_text(msp, line, x, y - i * height * 1.35, height, layer, align=align)


def rect(msp, x, y, w, h, layer, color=None):
    pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]
    for a, b in zip(pts, pts[1:]):
        attrs = {"layer": layer}
        if color:
            attrs["true_color"] = color
        msp.add_line(a, b, dxfattribs=attrs)


def line(msp, a, b, layer, color=None, linetype=None):
    attrs = {"layer": layer}
    if color:
        attrs["true_color"] = color
    if linetype:
        attrs["linetype"] = linetype
    msp.add_line(a, b, dxfattribs=attrs)


def circle(msp, center, radius, layer, color=None):
    attrs = {"layer": layer}
    if color:
        attrs["true_color"] = color
    msp.add_circle(center, radius, dxfattribs=attrs)


ARCH_LAYER_MAP = {
    "MUROS": "ARQ_MUROS",
    "PUERTAS": "ARQ_PUERTAS",
    "VENTANAS": "ARQ_VENTANAS",
    "ESCALERAS": "ARQ_ESCALERAS",
}


def clean_label(text):
    return str(text).replace("BaÃ±o", "Bano").replace("Baño", "Bano")


def import_architecture_dxf(doc, msp, dxf_path, ox, oy, scale=1.0):
    src = ezdxf.readfile(dxf_path)
    matrix = Matrix44.chain(Matrix44.scale(scale, scale, scale), Matrix44.translate(ox, oy, 0))
    imported = 0
    for entity in src.modelspace():
        layer = entity.dxf.layer
        if layer not in ARCH_LAYER_MAP:
            continue
        copied = entity.copy()
        copied.dxf.layer = ARCH_LAYER_MAP[layer]
        try:
            copied.transform(matrix)
        except Exception:
            continue
        msp.add_entity(copied)
        imported += 1
    if imported == 0:
        raise ValueError(f"No se importaron entidades arquitectonicas desde {dxf_path}")


def add_room_labels(msp, layout, ox, oy, scale=1.0):
    for room in layout["rooms"]:
        x, y, w, h = room["x"], room["y"], room["width"], room["height"]
        name = clean_label(room["name"])
        
        # Default center
        rx = ox + (x + w / 2) * scale
        ry = oy + (y + h / 2) * scale
        
        # Apply custom adjustments based on room name
        # to prevent overlap with electrical symbols
        if name == "Tienda":
            ry = oy + 0.8 * scale
        elif name == "Cocina":
            ry = oy + 4.3 * scale
        elif name == "Pasadizo":
            if h > 5.0:  # First floor Pasadizo
                ry = oy + 1.8 * scale
            else:        # Third floor Pasadizo
                ry = oy + 7.8 * scale
        elif name == "Escalera":
            rx = ox + 1.8 * scale
            ry = oy + 7.3 * scale
        elif name == "Dormitorio Principal":
            ry = oy + 0.8 * scale
        elif name == "Dormitorio 3":
            ry = oy + 4.5 * scale
        elif name == "Sala / Hall":
            ry = oy + 4.5 * scale
        elif name == "Bano":
            # For second and third floor bathrooms
            ry = oy + 7.8 * scale
        elif name == "Dormitorio 4":
            ry = oy + 2.8 * scale
        elif name == "Dormitorio 5":
            ry = oy + 2.8 * scale

        # Dynamic font sizing based on room dimensions and label length
        max_h = 0.16
        length_factor = len(name) * 0.55
        if length_factor > 0:
            width_limit = max(0.08, (w - 0.2) / length_factor)
            max_h = min(max_h, width_limit)
        max_h = min(max_h, h * 0.14)
        font_height = max(0.10, max_h) * scale

        add_text(msp, name, rx, ry, font_height, "ARQ_TEXTOS")


def draw_architecture(msp, layout, ox, oy, scale=1.0):
    def p(x, y):
        return (ox + x * scale, oy + y * scale)

    for room in layout["rooms"]:
        x, y, w, h = room["x"], room["y"], room["width"], room["height"]
        rect(msp, ox + x * scale, oy + y * scale, w * scale, h * scale, "ARQ_MUROS", COLORS["black"])
        add_text(msp, clean_label(room["name"]), ox + (x + w / 2) * scale, oy + (y + h / 2) * scale, 0.16, "ARQ_TEXTOS")

    for door in layout.get("doors", []):
        x, y, w = door["x"], door["y"], door["width"]
        if door["orientation"] == "horizontal":
            line(msp, p(x, y), p(x + w, y), "ARQ_PUERTAS", COLORS["gray"])
            circle(msp, p(x, y), 0.08 * scale, "ARQ_PUERTAS", COLORS["gray"])
        else:
            line(msp, p(x, y), p(x, y + w), "ARQ_PUERTAS", COLORS["gray"])
            circle(msp, p(x, y), 0.08 * scale, "ARQ_PUERTAS", COLORS["gray"])

    for win in layout.get("windows", []):
        x, y, w = win["x"], win["y"], win["width"]
        if win["orientation"] == "horizontal":
            line(msp, p(x, y), p(x + w, y), "ARQ_VENTANAS", COLORS["cyan"])
        else:
            line(msp, p(x, y), p(x, y + w), "ARQ_VENTANAS", COLORS["cyan"])

    for stair in layout.get("stairs", []):
        x1, y1, x2, y2 = stair["x1"], stair["y1"], stair["x2"], stair["y2"]
        rect(msp, ox + x1 * scale, oy + y1 * scale, (x2 - x1) * scale, (y2 - y1) * scale, "ARQ_ESCALERAS", COLORS["gray"])
        steps = int(stair.get("steps", 8))
        for i in range(1, steps):
            yy = y1 + (y2 - y1) * i / steps
            line(msp, p(x1, yy), p(x2, yy), "ARQ_ESCALERAS", COLORS["light_gray"])
        add_text(msp, "ESC", ox + (x1 + x2) / 2 * scale, oy + (y1 + y2) / 2 * scale, 0.15, "ARQ_TEXTOS")


def sym_lum(msp, x, y, circuit):
    color = CIRCUIT_COLORS.get(circuit, COLORS["orange"])
    draw_dge_symbol(msp, "dge_09_93_51_salida_incandescente_techo", x, y, "ELEC_LUMINARIAS", color, 1.0)


def sym_switch(msp, x, y, kind, circuit):
    color = CIRCUIT_COLORS.get(circuit, COLORS["orange"])
    symbol_id = "dge_09_93_32_interruptor_tres_vias" if kind == "conmutado" else "dge_09_93_30_interruptor_unipolar"
    draw_dge_symbol(msp, symbol_id, x, y, "ELEC_INTERRUPTORES", color, 1.0)


def sym_outlet(msp, x, y, kind, circuit):
    color = CIRCUIT_COLORS.get(circuit, COLORS["blue"])
    symbol_id = {
        "doble": "dge_09_93_13_tomacorriente_monofasico",
        "tierra": "dge_09_93_17_tomacorriente_tierra",
        "protegido": "dge_09_93_22_tomacorriente_contacto_proteccion",
        "especial": "dge_09_93_18_salida_cocina",
        "cocina": "dge_09_93_18_salida_cocina",
        "lavadora": "dge_09_93_17_tomacorriente_tierra",
        "bomba": "dge_09_93_17_tomacorriente_tierra",
        "caja_paso": "dge_09_93_08_caja_paso",
    }.get(kind, "dge_09_93_13_tomacorriente_monofasico")
    draw_dge_symbol(msp, symbol_id, x, y, "ELEC_TOMACORRIENTES", color, 1.0)
    if kind == "bomba":
        add_text(msp, "B", x + 0.26, y + 0.10, 0.12, "ELEC_TOMACORRIENTES")


def sym_panel(msp, x, y, label):
    draw_dge_symbol(msp, "dge_09_91_17_tablero_empotrado", x, y, "ELEC_TABLEROS", COLORS["red"], 1.0)
    add_text(msp, label, x, y - 0.34, 0.12, "ELEC_TABLEROS")


def sym_meter(msp, x, y):
    w, h = 0.45, 0.25
    rect(msp, x - w/2, y - h/2, w, h, "ELEC_MEDIDOR", COLORS["green"])
    add_text(msp, "wh", x, y, 0.11, "ELEC_MEDIDOR")


def sym_ground(msp, x, y):
    line(msp, (x, y), (x, y - 0.18), "ELEC_PUESTA_TIERRA", COLORS["green"])
    line(msp, (x - 0.16, y - 0.18), (x + 0.16, y - 0.18), "ELEC_PUESTA_TIERRA", COLORS["green"])
    line(msp, (x - 0.11, y - 0.25), (x + 0.11, y - 0.25), "ELEC_PUESTA_TIERRA", COLORS["green"])
    line(msp, (x - 0.06, y - 0.32), (x + 0.06, y - 0.32), "ELEC_PUESTA_TIERRA", COLORS["green"])


def draw_symbols(msp, floor, ox, oy, scale, view):
    def tp(pt):
        return (ox + pt[0] * scale, oy + pt[1] * scale)

    def label_point(item, default_dx, default_dy):
        dx, dy = item.get("label_offset", [default_dx, default_dy])
        return dx * scale, dy * scale

    show_lights = view in ("alumbrado", "canalizaciones", "todo")
    show_outlets = view in ("tomacorrientes", "canalizaciones", "todo")
    show_routes = view in ("canalizaciones", "todo")

    if show_lights:
        for item in floor.get("luminarias", []):
            x, y = tp(item["pos"])
            sym_lum(msp, x, y, item["circuito"])
            dx, dy = label_point(item, 0.28, 0.18)
            add_text(msp, item["circuito"], x + dx, y + dy, 0.12, "ELEC_TEXTOS")
        for item in floor.get("interruptores", []):
            x, y = tp(item["pos"])
            sym_switch(msp, x, y, item.get("tipo", "simple"), item["circuito"])

    if show_outlets:
        for item in floor.get("tomacorrientes", []):
            x, y = tp(item["pos"])
            sym_outlet(msp, x, y, item.get("tipo", "doble"), item["circuito"])
            dx, dy = label_point(item, 0.25, -0.22)
            add_text(msp, item["circuito"], x + dx, y + dy, 0.12, "ELEC_TEXTOS")

    if view in ("canalizaciones", "todo"):
        for item in floor.get("tableros", []):
            x, y = tp(item["pos"])
            sym_panel(msp, x, y, item["id"])
        for item in floor.get("medidores", []):
            x, y = tp(item["pos"])
            sym_meter(msp, x, y)
        for item in floor.get("puesta_tierra", []):
            x, y = tp(item["pos"])
            sym_ground(msp, x, y)

    if show_routes:
        for route in floor.get("canalizaciones", []):
            pts = [tp(p) for p in route["puntos"]]
            color = CIRCUIT_COLORS.get(route.get("circuito"), COLORS["gray"])
            layer = f"ELEC_CIRCUITO_{route.get('circuito', 'GEN')}"
            for a, b in zip(pts, pts[1:]):
                line(msp, a, b, layer, color, "DASHED")
            if pts:
                if route.get("label_pos"):
                    lx, ly = tp(route["label_pos"])
                else:
                    lx, ly = pts[-1][0] + 0.16, pts[-1][1] + 0.16
                add_text(msp, route.get("circuito", ""), lx, ly, 0.12, "ELEC_TEXTOS")


def draw_legend(msp, x, y, title, circuits):
    rect(msp, x, y - 8.35, 7.2, 8.35, "ELEC_LEYENDA", COLORS["black"])
    add_text(msp, "LEYENDA ELECTRICA", x + 3.6, y - 0.35, 0.24, "ELEC_LEYENDA")
    yy = y - 0.9
    sym_lum(msp, x + 0.45, yy, "C1")
    add_text(msp, "Luminaria de techo", x + 0.9, yy, 0.16, "ELEC_LEYENDA", align=TextEntityAlignment.MIDDLE_LEFT)
    yy -= 0.55
    sym_switch(msp, x + 0.45, yy, "simple", "C1")
    add_text(msp, "Interruptor simple", x + 0.9, yy, 0.16, "ELEC_LEYENDA", align=TextEntityAlignment.MIDDLE_LEFT)
    yy -= 0.55
    sym_switch(msp, x + 0.45, yy, "conmutado", "C1")
    add_text(msp, "Interruptor conmutado", x + 0.9, yy, 0.16, "ELEC_LEYENDA", align=TextEntityAlignment.MIDDLE_LEFT)
    yy -= 0.55
    sym_outlet(msp, x + 0.45, yy, "tierra", "C2")
    add_text(msp, "Tomacorriente doble con tierra", x + 0.9, yy, 0.16, "ELEC_LEYENDA", align=TextEntityAlignment.MIDDLE_LEFT)
    yy -= 0.55
    sym_outlet(msp, x + 0.45, yy, "protegido", "C2")
    add_text(msp, "Tomacorriente protegido", x + 0.9, yy, 0.16, "ELEC_LEYENDA", align=TextEntityAlignment.MIDDLE_LEFT)
    yy -= 0.55
    sym_outlet(msp, x + 0.45, yy, "cocina", "C3")
    add_text(msp, "Tomacorriente especial con tierra", x + 0.9, yy, 0.16, "ELEC_LEYENDA", align=TextEntityAlignment.MIDDLE_LEFT)
    yy -= 0.55
    sym_panel(msp, x + 0.45, yy, "TG")
    add_text(msp, "Tablero general/subtablero", x + 0.9, yy, 0.16, "ELEC_LEYENDA", align=TextEntityAlignment.MIDDLE_LEFT)
    yy -= 0.55
    sym_meter(msp, x + 0.45, yy)
    add_text(msp, "Medidor referencial", x + 0.9, yy, 0.16, "ELEC_LEYENDA", align=TextEntityAlignment.MIDDLE_LEFT)
    yy -= 0.75
    add_text(msp, "CIRCUITOS", x + 3.6, yy, 0.20, "ELEC_LEYENDA")
    yy -= 0.35
    for c in circuits:
        line(msp, (x + 0.25, yy), (x + 0.75, yy), f"ELEC_CIRCUITO_{c['id']}", CIRCUIT_COLORS.get(c["id"], COLORS["gray"]), "DASHED")
        add_text(msp, f"{c['id']}: {c['uso']}", x + 0.9, yy, 0.115, "ELEC_LEYENDA", align=TextEntityAlignment.MIDDLE_LEFT)
        yy -= 0.25


def draw_title_block(msp, x, y, w, h, title, version):
    rect(msp, x, y, w, h, "ELEC_ROTULO", COLORS["black"])
    rows = [h - 0.65, h - 1.25, h - 1.85, h - 2.45, h - 3.05]
    for yy in rows:
        line(msp, (x, y + yy), (x + w, y + yy), "ELEC_ROTULO", COLORS["black"])
    line(msp, (x + 4.25, y), (x + 4.25, y + 1.20), "ELEC_ROTULO", COLORS["black"])
    add_text(msp, "PROYECTO: VIVIENDA UNIFAMILIAR", x + 0.25, y + h - 0.34, 0.17, "ELEC_ROTULO", align=TextEntityAlignment.MIDDLE_LEFT)
    add_text(msp, "PROPIETARIO: RENZO GABRIEL MAMANI GALINDO", x + 0.25, y + h - 0.95, 0.14, "ELEC_ROTULO", align=TextEntityAlignment.MIDDLE_LEFT)
    add_text(msp, "UBICACION: JR. LIMA S/N - CAPACHICA - PUNO", x + 0.25, y + h - 1.55, 0.14, "ELEC_ROTULO", align=TextEntityAlignment.MIDDLE_LEFT)
    add_text(msp, f"PLANO: {title}", x + 0.25, y + h - 2.15, 0.16, "ELEC_ROTULO", align=TextEntityAlignment.MIDDLE_LEFT)
    add_text(msp, f"VERSION: {version}", x + 0.25, y + h - 2.75, 0.13, "ELEC_ROTULO", align=TextEntityAlignment.MIDDLE_LEFT)
    add_text(msp, "ESCALA: REFERENCIAL", x + 4.45, y + h - 2.75, 0.13, "ELEC_ROTULO", align=TextEntityAlignment.MIDDLE_LEFT)
    add_text(msp, "NORMA: CNE-U / RNE EM.010", x + 0.25, y + 0.38, 0.13, "ELEC_ROTULO", align=TextEntityAlignment.MIDDLE_LEFT)
    add_text(msp, "FECHA: 2026-06-03", x + 4.45, y + 0.38, 0.13, "ELEC_ROTULO", align=TextEntityAlignment.MIDDLE_LEFT)


def setup_doc():
    doc = ezdxf.new("R2010")
    try:
        doc.linetypes.new("DASHED", dxfattribs={"pattern": [0.5, 0.25, -0.15]})
    except ezdxf.DXFTableEntryError:
        pass
    layers = [
        ("ARQ_MUROS", COLORS["black"], 25), ("ARQ_PUERTAS", COLORS["gray"], 15),
        ("ARQ_VENTANAS", COLORS["cyan"], 15), ("ARQ_ESCALERAS", COLORS["gray"], 15),
        ("ARQ_TEXTOS", COLORS["gray"], 10), ("ELEC_LUMINARIAS", COLORS["orange"], 25),
        ("ELEC_INTERRUPTORES", COLORS["orange"], 25), ("ELEC_TOMACORRIENTES", COLORS["blue"], 25),
        ("ELEC_TABLEROS", COLORS["red"], 30), ("ELEC_MEDIDOR", COLORS["green"], 25),
        ("ELEC_PUESTA_TIERRA", COLORS["green"], 25), ("ELEC_CANALIZACION", COLORS["gray"], 15),
        ("ELEC_TEXTOS", COLORS["black"], 10), ("ELEC_LEYENDA", COLORS["black"], 18),
        ("ELEC_ROTULO", COLORS["black"], 20), ("MARCO", COLORS["black"], 40),
    ]
    for name, color, lw in layers:
        ensure_layer(doc, name, true_color=color, lineweight=lw)
    for cid, color in CIRCUIT_COLORS.items():
        ensure_layer(doc, f"ELEC_CIRCUITO_{cid}", true_color=color, lineweight=20, linetype="DASHED")
    return doc


def render_pdf(dxf_path, pdf_path):
    import matplotlib.pyplot as plt
    from ezdxf.addons.drawing import RenderContext, Frontend
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend

    print(f"Renderizando PDF con matplotlib: '{pdf_path}'...")
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()
    
    fig = plt.figure(figsize=(11.69, 8.27))  # A4 horizontal
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    
    ctx = RenderContext(doc)
    out = MatplotlibBackend(ax)
    Frontend(ctx, out).draw_layout(msp, finalize=True)
    
    fig.savefig(pdf_path, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    print("¡Renderizado PDF completado con éxito!")

def main():
    parser = argparse.ArgumentParser(description="Genera overlays electricos residenciales sobre layouts arquitectonicos")
    parser.add_argument("--electrical", required=True)
    parser.add_argument("--view", choices=["alumbrado", "tomacorrientes", "canalizaciones", "todo"], required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--pdf")
    args = parser.parse_args()

    data = json.loads(Path(args.electrical).read_text(encoding="utf-8-sig"))
    doc = setup_doc()
    msp = doc.modelspace()

    rect(msp, -1.0, -1.0, 29.5, 14.8, "MARCO", COLORS["black"])
    add_text(msp, data["views"][args.view]["titulo"], 13.5, 13.25, 0.38, "ELEC_ROTULO")

    scale = 1.0
    positions = [(0, 3.0), (7.0, 2.5), (14.0, 2.5)]
    for floor, (ox, oy) in zip(data["floors"], positions):
        layout = json.loads(Path(floor["layout"]).read_text(encoding="utf-8-sig"))
        add_text(msp, floor["nombre"].upper(), ox + 2.25, oy + layout["dimensions"]["height"] + 0.45, 0.22, "ELEC_TEXTOS")
        if floor.get("base_dxf"):
            import_architecture_dxf(doc, msp, floor["base_dxf"], ox, oy, scale)
            add_room_labels(msp, layout, ox, oy, scale)
        else:
            draw_architecture(msp, layout, ox, oy, scale)
        draw_symbols(msp, floor, ox, oy, scale, args.view)

    draw_legend(msp, 19.7, 12.3, data["views"][args.view]["titulo"], data["circuitos"])
    draw_title_block(msp, 19.7, -0.4, 8.0, 3.55, data["views"][args.view]["titulo"], data.get("version", "v1"))

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(out)
    if args.pdf:
        render_pdf(str(out), args.pdf)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
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

REPO_ROOT = Path(__file__).resolve().parents[3]
DGE_SYMBOL_PATH = REPO_ROOT / "herramientas" / "simbologia" / "simbologia_normativa_dge.json"
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
        
        rx = ox + (x + w / 2) * scale
        ry = oy + (y + h / 2) * scale
        
        if name == "Tienda":
            ry = oy + 0.8 * scale
        elif name == "Cocina":
            ry = oy + 4.3 * scale
        elif name == "Pasadizo":
            if h > 5.0:
                ry = oy + 1.8 * scale
            else:
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
            ry = oy + 7.8 * scale
        elif name == "Dormitorio 4":
            ry = oy + 2.8 * scale
        elif name == "Dormitorio 5":
            ry = oy + 2.8 * scale

        max_h = 0.16
        length_factor = len(name) * 0.55
        if length_factor > 0:
            width_limit = max(0.08, (w - 0.2) / length_factor)
            max_h = min(max_h, width_limit)
        max_h = min(max_h, h * 0.14)
        font_height = max(0.10, max_h) * scale

        add_text(msp, name, rx, ry, font_height, "ARQ_TEXTOS")

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

def draw_symbols_floor(msp, floor, ox, oy, scale):
    def tp(pt):
        return (ox + pt[0] * scale, oy + pt[1] * scale)

    def label_point(item, default_dx, default_dy):
        dx, dy = item.get("label_offset", [default_dx, default_dy])
        return dx * scale, dy * scale

    for item in floor.get("luminarias", []):
        x, y = tp(item["pos"])
        sym_lum(msp, x, y, item["circuito"])
        dx, dy = label_point(item, 0.28, 0.18)
        add_text(msp, item["circuito"], x + dx, y + dy, 0.12, "ELEC_TEXTOS")
        
    for item in floor.get("interruptores", []):
        x, y = tp(item["pos"])
        sym_switch(msp, x, y, item.get("tipo", "simple"), item["circuito"])

    for item in floor.get("tomacorrientes", []):
        x, y = tp(item["pos"])
        sym_outlet(msp, x, y, item.get("tipo", "doble"), item["circuito"])
        dx, dy = label_point(item, 0.25, -0.22)
        add_text(msp, item["circuito"], x + dx, y + dy, 0.12, "ELEC_TEXTOS")

    for item in floor.get("tableros", []):
        x, y = tp(item["pos"])
        sym_panel(msp, x, y, item["id"])
        
    for item in floor.get("medidores", []):
        x, y = tp(item["pos"])
        sym_meter(msp, x, y)
        
    for item in floor.get("puesta_tierra", []):
        x, y = tp(item["pos"])
        sym_ground(msp, x, y)

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
    add_text(msp, "FECHA: 2026-06-08", x + 4.45, y + 0.38, 0.13, "ELEC_ROTULO", align=TextEntityAlignment.MIDDLE_LEFT)

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

def compute_image_extent(ox, oy, lw, lh, img_w, img_h, padding=0.5):
    """Compute image extent preserving aspect ratio while covering layout area."""
    ar_img = img_w / img_h
    ar_layout = lw / lh
    if ar_img > ar_layout:
        extent_h = lh + 2 * padding
        extent_w = extent_h * ar_img
    else:
        extent_w = lw + 2 * padding
        extent_h = extent_w / ar_img
    cx = ox + lw / 2
    cy = oy + lh / 2
    return [cx - extent_w / 2, cx + extent_w / 2, cy + extent_h / 2, cy - extent_h / 2]


def add_north_arrow(ax, x, y, size=0.35):
    from matplotlib.patches import Polygon
    tip = (x, y + size * 0.5)
    bl = (x - size * 0.3, y - size * 0.4)
    br = (x + size * 0.3, y - size * 0.4)
    arrow = Polygon([tip, bl, br], closed=True, facecolor='#1a3a5c', edgecolor='black', linewidth=0.8, zorder=200)
    ax.add_patch(arrow)
    ax.text(x, y + size * 0.55, 'N', ha='center', va='bottom', fontsize=11, fontweight='bold', fontfamily='sans-serif', zorder=201)


def add_scale_bar(ax, x, y, meters=2.0):
    ax.plot([x, x + meters], [y, y], 'k-', linewidth=3, zorder=200)
    tick_h = 0.06
    for i in range(3):
        xp = x + i * (meters / 2)
        ax.plot([xp, xp], [y - tick_h, y + tick_h], 'k-', linewidth=2, zorder=200)
        ax.text(xp, y - tick_h * 2.5, f'{int(i * meters / 2)}', ha='center', va='top', fontsize=7, fontfamily='sans-serif', zorder=200)
    ax.text(x + meters / 2, y - tick_h * 4, 'metros', ha='center', va='top', fontsize=7, fontfamily='sans-serif', zorder=200)


def render_pdf_and_svg(dxf_path, pdf_path, svg_path, croquis_path=None, extent=None, img_shape=None):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    from ezdxf.addons.drawing import RenderContext, Frontend
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend

    print(f"Renderizando PDF y SVG con matplotlib: '{pdf_path}'...")
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()

    fig = plt.figure(figsize=(11.69, 8.27))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    if croquis_path and Path(croquis_path).exists():
        print(f"  Superponiendo croquis de fondo: {croquis_path}")
        img = mpimg.imread(str(croquis_path))
        ax.imshow(img, extent=extent, aspect='auto', alpha=0.3, zorder=0)

    arch_layers = ['ARQ_MUROS', 'ARQ_PUERTAS', 'ARQ_VENTANAS', 'ARQ_ESCALERAS', 'ARQ_TEXTOS']
    for name in arch_layers:
        try:
            doc.layers.get(name).off()
        except Exception:
            pass

    ctx = RenderContext(doc)
    out = MatplotlibBackend(ax)
    Frontend(ctx, out).draw_layout(msp, finalize=True)

    add_north_arrow(ax, extent[1] - 0.4, extent[2] - 0.4 if extent[2] > extent[3] else extent[3] - 0.4)
    add_scale_bar(ax, extent[0] + 0.3, extent[3] + 0.15 if extent[3] < extent[2] else extent[2] + 0.15, meters=2.0)

    fig.savefig(pdf_path, dpi=600, bbox_inches='tight', pad_inches=0.05)
    fig.savefig(svg_path, format='svg', bbox_inches='tight', pad_inches=0.05)
    plt.close(fig)
    print("¡Renderizado PDF y SVG completado con éxito!")

def main():
    project_root = Path(__file__).resolve().parents[1]
    repo_root = REPO_ROOT
    json_path = project_root / "diseno-electrico" / "datos" / "modelo-electrico.json"
    data = json.loads(json_path.read_text(encoding="utf-8-sig"))

    # Generate individual floor plans
    floor_slugs = ("primer-piso", "segundo-piso", "tercer-piso")
    for i, floor in enumerate(data["floors"]):
        floor_num = i + 1
        floor_name = floor["nombre"]
        print(f"Procesando {floor_name}...")

        doc = setup_doc()
        msp = doc.modelspace()

        # Marco: 21.0 x 14.0
        rect(msp, -1.0, -1.0, 21.0, 14.0, "MARCO", COLORS["black"])
        
        plan_code = floor_num + 1
        title_text = f"IE-{plan_code:02d} PLANO ELECTRICO - {floor_name.upper()}"
        add_text(msp, title_text, 9.5, 12.25, 0.35, "ELEC_ROTULO")

        # Load architectural base
        ox, oy = 1.0, 2.0
        scale = 1.0
        
        layout_path = repo_root / floor["layout"]
        layout = json.loads(layout_path.read_text(encoding="utf-8-sig"))
        
        add_text(msp, floor["nombre"].upper(), ox + 2.25, oy + layout["dimensions"]["height"] + 0.45, 0.22, "ELEC_TEXTOS")
        
        base_dxf_path = repo_root / floor["base_dxf"]
        import_architecture_dxf(doc, msp, str(base_dxf_path), ox, oy, scale)
        add_room_labels(msp, layout, ox, oy, scale)
        
        # Draw electrical overlay
        draw_symbols_floor(msp, floor, ox, oy, scale)
        
        # Filter circuits for this floor
        # Floor 1: C1, C2, C3
        # Floor 2: C4, C5
        # Floor 3: C6, C7
        floor_circuits = []
        for c in data["circuitos"]:
            if floor_num == 1 and c["id"] in ("C1", "C2", "C3"):
                floor_circuits.append(c)
            elif floor_num == 2 and c["id"] in ("C4", "C5"):
                floor_circuits.append(c)
            elif floor_num == 3 and c["id"] in ("C6", "C7"):
                floor_circuits.append(c)

        # Draw legend and title block
        draw_legend(msp, 11.5, 11.5, title_text, floor_circuits)
        draw_title_block(msp, 11.5, -0.4, 8.0, 3.55, title_text, data.get("version", "v1"))

        # Save DXF
        output_dir = repo_root / "build" / "renzo" / "planos"
        floor_slug = floor_slugs[i]
        out_dxf_path = output_dir / "dxf" / f"IE-{plan_code:02d}-{floor_slug}.dxf"
        out_dxf_path.parent.mkdir(parents=True, exist_ok=True)
        doc.saveas(out_dxf_path)
        print(f"DXF generado: {out_dxf_path}")
        
        # Save PDF and SVG with croquis background
        out_pdf_path = output_dir / "pdf" / f"IE-{plan_code:02d}-{floor_slug}.pdf"
        out_pdf_path.parent.mkdir(parents=True, exist_ok=True)
        out_svg_path = output_dir / "svg" / f"IE-{plan_code:02d}-{floor_slug}.svg"
        out_svg_path.parent.mkdir(parents=True, exist_ok=True)
        
        croquis_path = repo_root / "proyectos" / "renzo" / "fuentes" / "croquis" / f"piso-{floor_num}.png"
        lw = layout["dimensions"]["width"]
        lh = layout["dimensions"]["height"]

        import numpy as np
        from PIL import Image
        try:
            pil_img = Image.open(str(croquis_path))
            img_w, img_h = pil_img.size
        except Exception:
            img_w, img_h = lw * 100, lh * 100

        img_extent = compute_image_extent(ox, oy, lw, lh, img_w, img_h, padding=0.5)
        
        render_pdf_and_svg(str(out_dxf_path), str(out_pdf_path), str(out_svg_path),
                           croquis_path=str(croquis_path), extent=img_extent)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Overlay electrico sobre un DXF arquitectonico existente."""

import argparse
import json
import math
import os
import sys
from pathlib import Path

try:
    import ezdxf
    from ezdxf.enums import TextEntityAlignment
except ImportError:
    ezdxf = None
    TextEntityAlignment = None


ARQ_LAYER_MAP = {
    "MUROS": "ARQ_MUROS",
    "PUERTAS": "ARQ_PUERTAS",
    "VENTANAS": "ARQ_VENTANAS",
    "TEXTOS": "ARQ_TEXTOS",
    "ESCALERAS": "ARQ_ESCALERAS",
    "TRAMAS": "ARQ_TRAMAS",
    "MOBILIARIO": "ARQ_MOBILIARIO",
    "COTAS": "ELEC_COTAS_REF",
    "ANOTACIONES": "ARQ_ANOTACIONES",
}

LAYER_SPECS = {
    "ARQ_MUROS": {"color": 7, "true_color": 0x000000, "lineweight": 30},
    "ARQ_PUERTAS": {"color": 7, "true_color": 0x000000, "lineweight": 18},
    "ARQ_VENTANAS": {"color": 7, "true_color": 0x000000, "lineweight": 18},
    "ARQ_TEXTOS": {"color": 8, "true_color": 0x444444, "lineweight": 13},
    "ARQ_ESCALERAS": {"color": 8, "true_color": 0x555555, "lineweight": 13},
    "ARQ_TRAMAS": {"color": 9, "true_color": 0x999999, "lineweight": 9},
    "ARQ_MOBILIARIO": {"color": 8, "true_color": 0x777777, "lineweight": 9},
    "ARQ_ANOTACIONES": {"color": 8, "true_color": 0x555555, "lineweight": 9},
    "ELEC_LUMINARIAS": {"color": 2, "true_color": 0xFFB000, "lineweight": 25},
    "ELEC_INTERRUPTORES": {"color": 3, "true_color": 0x00A651, "lineweight": 25},
    "ELEC_TOMACORRIENTES": {"color": 5, "true_color": 0x0066CC, "lineweight": 25},
    "ELEC_TABLERO": {"color": 1, "true_color": 0xCC0000, "lineweight": 35},
    "ELEC_MEDIDOR": {"color": 6, "true_color": 0x8A2BE2, "lineweight": 30},
    "ELEC_CANALIZACION": {"color": 4, "true_color": 0x009999, "lineweight": 13},
    "ELEC_TEXTOS": {"color": 7, "true_color": 0x000000, "lineweight": 13},
    "ELEC_LEYENDA": {"color": 7, "true_color": 0x000000, "lineweight": 18},
    "ELEC_COTAS_REF": {"color": 8, "true_color": 0x777777, "lineweight": 9},
    "MARCO": {"color": 7, "true_color": 0x000000, "lineweight": 35},
}

for circuit, rgb in {
    "C1": 0xCC8A00,
    "C2": 0x004C99,
    "C3": 0x008CBA,
    "C4": 0xD49A00,
    "C5": 0x004C99,
    "C6": 0xCC0000,
    "C7": 0x8A2BE2,
    "C8": 0x008000,
}.items():
    LAYER_SPECS[f"ELEC_CIRCUITO_{circuit}"] = {
        "color": 4,
        "true_color": rgb,
        "lineweight": 18,
    }


DGE_LIBRARY_JSON = Path(__file__).resolve().parents[2] / "simbologia" / "simbologia_normativa_dge.json"
DGE_SYMBOLS = None


def load_dge_symbols():
    global DGE_SYMBOLS
    if DGE_SYMBOLS is not None:
        return DGE_SYMBOLS
    DGE_SYMBOLS = {}
    if not DGE_LIBRARY_JSON.exists():
        return DGE_SYMBOLS
    with open(DGE_LIBRARY_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    for symbol in data.get("simbolos", []):
        block_name = symbol.get("block_name")
        if block_name:
            DGE_SYMBOLS[block_name] = symbol.get("primitivas", [])
    return DGE_SYMBOLS


def transform_point(x, y, ox, oy, scale=1.0, rotation=0.0):
    angle = math.radians(rotation)
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    sx = float(x) * scale
    sy = float(y) * scale
    return (ox + sx * cos_a - sy * sin_a, oy + sx * sin_a + sy * cos_a)


def add_dge_symbol(msp, block_name, x, y, scale=1.0, layer="ELEC_TEXTOS", rotation=0.0):
    primitives = load_dge_symbols().get(block_name)
    if not primitives:
        return False

    def point(px, py):
        return transform_point(px, py, x, y, scale, rotation)

    for prim in primitives:
        kind = prim.get("tipo")
        if kind == "linea":
            msp.add_line(
                point(prim["x1"], prim["y1"]),
                point(prim["x2"], prim["y2"]),
                dxfattribs={"layer": layer},
            )
        elif kind in {"circulo", "circulo_relleno", "punto"}:
            cx = prim.get("cx", prim.get("x", 0.0))
            cy = prim.get("cy", prim.get("y", 0.0))
            radius = abs(float(prim.get("r", 0.02)) * scale)
            msp.add_circle(point(cx, cy), radius, dxfattribs={"layer": layer})
        elif kind in {"rectangulo", "rectangulo_relleno"}:
            x0 = float(prim["x"])
            y0 = float(prim["y"])
            w = float(prim["w"])
            h = float(prim["h"])
            pts = [
                point(x0, y0),
                point(x0 + w, y0),
                point(x0 + w, y0 + h),
                point(x0, y0 + h),
                point(x0, y0),
            ]
            msp.add_lwpolyline(pts, dxfattribs={"layer": layer})
        elif kind == "arco":
            center = point(prim["cx"], prim["cy"])
            radius = abs(float(prim["r"]) * scale)
            start = float(prim["ang_ini"]) + rotation
            end = float(prim["ang_fin"]) + rotation
            msp.add_arc(center, radius, start, end, dxfattribs={"layer": layer})
        elif kind == "texto":
            text = msp.add_text(
                str(prim.get("contenido", "")),
                dxfattribs={
                    "layer": layer,
                    "height": float(prim.get("h", 0.12)) * scale,
                    "rotation": rotation,
                },
            )
            text.set_placement(point(prim.get("x", 0.0), prim.get("y", 0.0)), align=TextEntityAlignment.MIDDLE_CENTER)
    return True


def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_layer(doc, name, spec=None):
    if name in doc.layers:
        return
    doc.layers.new(name, dxfattribs=spec or {"color": 7})


def setup_layers(doc):
    for name, spec in LAYER_SPECS.items():
        ensure_layer(doc, name, spec)
    if "DASHED" not in doc.linetypes:
        try:
            doc.linetypes.new(
                "DASHED",
                dxfattribs={
                    "description": "Dashed __ __ __",
                    "pattern": [0.60, 0.35, -0.15],
                },
            )
        except Exception:
            pass


def remap_architecture_layers(msp):
    for entity in msp:
        old_layer = entity.dxf.layer
        if old_layer in ARQ_LAYER_MAP:
            entity.dxf.layer = ARQ_LAYER_MAP[old_layer]


def add_text(msp, text, x, y, height=0.18, layer="ELEC_TEXTOS", rotation=0, align=None):
    if align is None:
        align = TextEntityAlignment.MIDDLE_CENTER
    entity = msp.add_text(
        str(text),
        dxfattribs={"layer": layer, "height": height, "rotation": rotation},
    )
    entity.set_placement((float(x), float(y)), align=align)
    return entity


def add_multiline(msp, text, x, y, height=0.18, layer="ELEC_TEXTOS", spacing=1.35):
    lines = str(text).splitlines()
    if not lines:
        return
    start = float(y) + (len(lines) - 1) * height * spacing / 2
    for index, line in enumerate(lines):
        add_text(msp, line, x, start - index * height * spacing, height, layer)


def layer_for_circuit(circuit, default_layer="ELEC_CANALIZACION"):
    if circuit:
        return f"ELEC_CIRCUITO_{circuit}"
    return default_layer


def draw_label(msp, item, default_text, x, y, height=0.14, dx=0.0, dy=-0.36):
    label = item.get("label", default_text)
    if label:
        dx = float(item.get("label_dx", dx))
        dy = float(item.get("label_dy", dy))
        add_multiline(msp, label, x + dx, y + dy, height=height, layer="ELEC_TEXTOS")


def draw_luminaire(msp, item):
    x, y = float(item["x"]), float(item["y"])
    r = float(item.get("size", 0.18))
    layer = "ELEC_LUMINARIAS"
    if not add_dge_symbol(msp, "DGE_09_93_51_SALIDA_TECHO", x, y, scale=r / 0.18, layer=layer):
        msp.add_circle((x, y), r, dxfattribs={"layer": layer})
        # Dibujar aspa "X" en lugar de "+"
        d_in = r * 0.4
        d_out = r * 0.9
        msp.add_line((x - d_out, y - d_out), (x - d_in, y - d_in), dxfattribs={"layer": layer})
        msp.add_line((x + d_in, y + d_in), (x + d_out, y + d_out), dxfattribs={"layer": layer})
        msp.add_line((x - d_out, y + d_out), (x - d_in, y + d_in), dxfattribs={"layer": layer})
        msp.add_line((x + d_in, y - d_in), (x + d_out, y - d_out), dxfattribs={"layer": layer})
    draw_label(msp, item, item.get("circuit", ""), x, y)


def draw_earthing(msp, item):
    x, y = float(item["x"]), float(item["y"])
    layer = "ELEC_PUESTA_TIERRA"
    ensure_layer(msp.doc, layer, {"color": 3, "true_color": 0x00A651, "lineweight": 25})
    # Dibujar simbolo de puesta a tierra (3 lineas decrecientes y linea vertical)
    r = float(item.get("size", 0.15))
    msp.add_line((x, y), (x, y - r), dxfattribs={"layer": layer})
    msp.add_line((x - r, y - r), (x + r, y - r), dxfattribs={"layer": layer})
    msp.add_line((x - r*0.6, y - r*1.3), (x + r*0.6, y - r*1.3), dxfattribs={"layer": layer})
    msp.add_line((x - r*0.2, y - r*1.6), (x + r*0.2, y - r*1.6), dxfattribs={"layer": layer})
    draw_label(msp, item, item.get("label", "SPAT"), x, y, dy=-r*2.2)



def draw_switch(msp, item):
    x, y = float(item["x"]), float(item["y"])
    r = float(item.get("size", 0.12))
    layer = "ELEC_INTERRUPTORES"
    block = "DGE_09_93_32_INTERRUPTOR_CONMUTADO" if item.get("kind") == "conmutado" else "DGE_09_93_30_INTERRUPTOR_UNIPOLAR"
    if not add_dge_symbol(msp, block, x, y, scale=r / 0.09, layer=layer):
        msp.add_circle((x, y), r, dxfattribs={"layer": layer})
        msp.add_line((x, y), (x + r * 1.6, y + r * 1.1), dxfattribs={"layer": layer})
        symbol = "S3" if item.get("kind") == "conmutado" else "S"
        add_text(msp, symbol, x, y + 0.23, height=0.13, layer="ELEC_TEXTOS")
    draw_label(msp, item, item.get("circuit", ""), x, y, dy=-0.52)


def draw_outlet(msp, item):
    x, y = float(item["x"]), float(item["y"])
    r = float(item.get("size", 0.13))
    circuit = item.get("circuit", "")
    layer = "ELEC_TOMACORRIENTES"
    kind = item.get("kind", "doble")
    block = "DGE_09_93_18_SALIDA_COCINA" if kind in {"especial", "cocina"} else "DGE_09_93_17_TOMACORRIENTE_TIERRA"
    if not add_dge_symbol(msp, block, x, y, scale=r / 0.13, layer=layer):
        if kind in {"especial", "bomba"}:
            pts = [(x, y + r * 1.25), (x + r * 1.25, y), (x, y - r * 1.25), (x - r * 1.25, y), (x, y + r * 1.25)]
            msp.add_lwpolyline(pts, dxfattribs={"layer": layer})
        else:
            msp.add_circle((x, y), r, dxfattribs={"layer": layer})
        msp.add_line((x - r * 0.55, y - r * 0.15), (x + r * 0.55, y - r * 0.15), dxfattribs={"layer": layer})
        msp.add_line((x - r * 0.55, y + r * 0.20), (x + r * 0.55, y + r * 0.20), dxfattribs={"layer": layer})
        if kind == "tierra":
            msp.add_line((x, y - r * 0.95), (x, y - r * 0.35), dxfattribs={"layer": layer})
    draw_label(msp, item, circuit, x, y)


def draw_panel(msp, item):
    x, y = float(item["x"]), float(item["y"])
    w, h = float(item.get("width", 0.55)), float(item.get("height", 0.38))
    layer = "ELEC_TABLERO"
    if not add_dge_symbol(msp, "DGE_09_91_17_TABLERO_EMPOTRADO", x, y, scale=max(w / 0.50, h / 0.30), layer=layer):
        rect = [(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2), (x - w / 2, y - h / 2)]
        msp.add_lwpolyline(rect, dxfattribs={"layer": layer})
    add_text(msp, item.get("label", "TG"), x, y, height=0.16, layer="ELEC_TEXTOS")
    if item.get("note"):
        add_multiline(msp, item["note"], x, y - 0.55, height=0.12, layer="ELEC_TEXTOS")


def draw_meter(msp, item):
    x, y = float(item["x"]), float(item["y"])
    r = float(item.get("size", 0.22))
    layer = "ELEC_MEDIDOR"
    msp.add_circle((x, y), r, dxfattribs={"layer": layer})
    add_text(msp, item.get("label", "M"), x, y, height=0.16, layer="ELEC_TEXTOS")
    if item.get("note"):
        add_multiline(msp, item["note"], x, y - 0.45, height=0.12, layer="ELEC_TEXTOS")


def draw_equipment(msp, item):
    x, y = float(item["x"]), float(item["y"])
    kind = item.get("kind", "equipo")
    layer = "ELEC_TOMACORRIENTES"
    if kind == "bomba":
        msp.add_circle((x, y), 0.18, dxfattribs={"layer": layer})
        add_text(msp, "B", x, y, height=0.14, layer="ELEC_TEXTOS")
    elif kind == "ducto":
        msp.add_circle((x, y), 0.16, dxfattribs={"layer": "ELEC_CANALIZACION"})
        msp.add_line((x - 0.12, y - 0.12), (x + 0.12, y + 0.12), dxfattribs={"layer": "ELEC_CANALIZACION"})
        msp.add_line((x - 0.12, y + 0.12), (x + 0.12, y - 0.12), dxfattribs={"layer": "ELEC_CANALIZACION"})
    else:
        s = 0.16
        msp.add_lwpolyline(
            [(x - s, y - s), (x + s, y - s), (x + s, y + s), (x - s, y + s), (x - s, y - s)],
            dxfattribs={"layer": layer},
        )
    draw_label(msp, item, item.get("label", item.get("circuit", "")), x, y)


def draw_route(msp, item):
    points = [(float(x), float(y)) for x, y in item["points"]]
    if len(points) < 2:
        return
    layer = layer_for_circuit(item.get("circuit"))
    attribs = {"layer": layer}
    if item.get("linetype", "DASHED").upper() == "DASHED":
        attribs["linetype"] = "DASHED"
    msp.add_lwpolyline(points, dxfattribs=attribs)
    label = item.get("label", item.get("circuit", ""))
    if label:
        if "label_x" in item and "label_y" in item:
            label_x = float(item["label_x"])
            label_y = float(item["label_y"])
        else:
            mid = points[len(points) // 2]
            label_x = mid[0] + float(item.get("label_dx", 0.0))
            label_y = mid[1] + float(item.get("label_dy", 0.18))
        add_multiline(msp, label, label_x, label_y, height=0.12, layer="ELEC_TEXTOS")


def draw_legend_box(msp, x, y, width, height, title):
    layer = "ELEC_LEYENDA"
    msp.add_lwpolyline([(x, y), (x + width, y), (x + width, y - height), (x, y - height), (x, y)], dxfattribs={"layer": layer})
    add_text(msp, title, x + width / 2, y - 0.28, height=0.18, layer="ELEC_TEXTOS")
    msp.add_line((x, y - 0.48), (x + width, y - 0.48), dxfattribs={"layer": layer})


def draw_legend(msp, data):
    legend = data.get("legend", {})
    x = float(legend.get("x", 16.7))
    y = float(legend.get("y", 9.2))
    width = float(legend.get("width", 5.2))
    height = float(legend.get("height", 6.0))
    draw_legend_box(msp, x, y, width, height, legend.get("title", "LEYENDA ELECTRICA"))

    entries = [
        ("Luminaria de techo", draw_luminaire, {"x": x + 0.35, "y": y - 0.85, "label": ""}),
        ("Interruptor simple", draw_switch, {"x": x + 0.35, "y": y - 1.25, "label": ""}),
        ("Tomacorriente", draw_outlet, {"x": x + 0.35, "y": y - 1.65, "label": ""}),
        ("Tomacorriente especial", draw_outlet, {"x": x + 0.35, "y": y - 2.05, "label": "", "kind": "especial"}),
        (legend.get("panel_label", "Tablero general"), draw_panel, {"x": x + 0.35, "y": y - 2.45, "label": legend.get("panel_symbol", "TG"), "width": 0.36, "height": 0.25}),
    ]
    if legend.get("show_meter", True):
        entries.append(("Medidor", draw_meter, {"x": x + 0.35, "y": y - 2.85, "label": "M", "size": 0.15}))
    for text, draw_fn, item in entries:
        draw_fn(msp, item)
        add_text(msp, text, x + 0.78, item["y"], height=0.12, layer="ELEC_TEXTOS", align=TextEntityAlignment.MIDDLE_LEFT)

    y0 = y - 3.25
    add_text(msp, "Circuitos:", x + 0.25, y0, height=0.13, layer="ELEC_TEXTOS", align=TextEntityAlignment.MIDDLE_LEFT)
    for i, row in enumerate(data.get("circuit_summary", [])):
        add_text(
            msp,
            f"{row['id']}: {row['label']}",
            x + 0.25,
            y0 - 0.28 * (i + 1),
            height=0.105,
            layer="ELEC_TEXTOS",
            align=TextEntityAlignment.MIDDLE_LEFT,
        )


def draw_title(msp, data):
    title = data.get("title", {})
    if not title:
        return
    x = float(title.get("x", 7.5))
    y = float(title.get("y", 10.7))
    add_text(msp, title.get("text", "PLANO ELECTRICO"), x, y, height=float(title.get("height", 0.28)), layer="ELEC_TEXTOS")
    subtitle = title.get("subtitle")
    if subtitle:
        add_text(msp, subtitle, x, y - 0.36, height=0.16, layer="ELEC_TEXTOS")


def draw_notes(msp, data):
    for note in data.get("notes", []):
        add_multiline(
            msp,
            note.get("text", ""),
            float(note["x"]),
            float(note["y"]),
            height=float(note.get("height", 0.13)),
            layer=note.get("layer", "ELEC_TEXTOS"),
        )


def draw_all(msp, data):
    draw_title(msp, data)
    for item in data.get("rutas", []):
        draw_route(msp, item)
    for item in data.get("luminarias", []):
        draw_luminaire(msp, item)
    for item in data.get("interruptores", []):
        draw_switch(msp, item)
    for item in data.get("tomacorrientes", []):
        draw_outlet(msp, item)
    for item in data.get("tableros", []):
        draw_panel(msp, item)
    for item in data.get("medidores", []):
        draw_meter(msp, item)
    for item in data.get("equipos", []):
        draw_equipment(msp, item)
    for item in data.get("puesta_tierra", []):
        draw_earthing(msp, item)
    draw_legend(msp, data)
    draw_notes(msp, data)



def validate(data):
    required_lists = ["luminarias", "interruptores", "tomacorrientes", "rutas"]
    for key in required_lists:
        if key in data and not isinstance(data[key], list):
            raise ValueError(f"'{key}' debe ser una lista")
    for key in ["luminarias", "interruptores", "tomacorrientes", "tableros", "medidores", "equipos", "puesta_tierra"]:
        for i, item in enumerate(data.get(key, [])):
            if "x" not in item or "y" not in item:
                raise ValueError(f"{key}[{i}] debe tener x/y")



def parse_args():
    parser = argparse.ArgumentParser(description="Agrega simbologia electrica a un DXF arquitectonico existente.")
    parser.add_argument("--base", required=True, help="DXF arquitectonico base")
    parser.add_argument("--electrical", required=True, help="JSON electrico")
    parser.add_argument("--output", required=True, help="DXF de salida")
    return parser.parse_args()


def main():
    if ezdxf is None:
        print("Error: ezdxf no esta instalado. Instale las dependencias del repositorio.", file=sys.stderr)
        sys.exit(1)
    args = parse_args()
    if not os.path.exists(args.base):
        print(f"Error: no existe el DXF base: {args.base}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.electrical):
        print(f"Error: no existe el JSON electrico: {args.electrical}", file=sys.stderr)
        sys.exit(1)
    data = read_json(args.electrical)
    try:
        validate(data)
    except ValueError as exc:
        print(f"Error de validacion: {exc}", file=sys.stderr)
        sys.exit(1)

    doc = ezdxf.readfile(args.base)
    setup_layers(doc)
    msp = doc.modelspace()
    remap_architecture_layers(msp)
    draw_all(msp, data)

    out_dir = os.path.dirname(os.path.abspath(args.output))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    doc.saveas(args.output)
    print(f"DXF electrico generado: {args.output}")


if __name__ == "__main__":
    main()

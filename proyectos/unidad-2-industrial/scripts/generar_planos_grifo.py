#!/usr/bin/env python3
"""Genera las seis laminas electricas A1 del anteproyecto del grifo.

La arquitectura procede de una copia derivada e inmutable del DXF recibido.
Las superposiciones electricas son una propuesta academica y todos los rotulos
se componen desde ``datos/rotulo-planos.yaml``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path
from typing import Any, Callable

import ezdxf
import yaml
from ezdxf import bbox
from ezdxf.addons import Importer
from ezdxf.addons.drawing import matplotlib as ezdxf_matplotlib
from ezdxf.enums import TextEntityAlignment


PAGE_W = 84.1
PAGE_H = 59.4
FRAME = (0.5, 0.5, 83.6, 58.9)
ARCH_SCALE = 0.5
TITLE_REFERENCE_EXTENTS = (56.4, 1.5, 83.0, 7.6)

# Ventanas utiles de la A-01 local. La fuente contiene marco, cuadricula UTM,
# detalles de aprobacion y tres plantas separadas; importar la hoja completa
# vuelve secundarios los circuitos y deja elementos sin relacion aparente.
SITE_VIEW = (45.0, 12.0, 113.0, 78.5)
LEVEL_VIEWS = {
    # Las plantas son en L. En N1 la ventana compuesta evita importar los
    # tanques que ocupan la misma franja de coordenadas a la derecha.
    "N1": ((59.0, 70.0, 79.0, 78.0), (59.0, 64.0, 68.5, 70.0)),
    "N2": ((58.0, 87.0, 79.0, 94.0), (58.0, 82.0, 64.5, 87.0)),
    "N3": ((58.0, 105.0, 80.0, 112.0), (58.0, 100.0, 64.8, 105.0)),
}
LEVEL_LAYOUTS = {
    "N1": {"windows": LEVEL_VIEWS["N1"], "scale": 0.90, "offset": (-50.1, -33.6)},
    "N2": {"windows": LEVEL_VIEWS["N2"], "scale": 0.90, "offset": (-22.2, -49.8)},
    "N3": {"windows": LEVEL_VIEWS["N3"], "scale": 0.90, "offset": (4.8, -66.0)},
}
BACKGROUND_LAYERS_OMITTED = {
    "cuadricula coordenadas",
    "letras",
    "instalaciones electricas",
    "puesta a tierra",
    "seguridad",
}
LEVEL_LAYERS_OMITTED = {"voladizos", "radio de giro", "tanques", "cotras", "contorno-01"}


def repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def add_layer(doc: ezdxf.document.Drawing, name: str, color: int, lineweight: int = 18, linetype: str = "CONTINUOUS") -> None:
    if name not in doc.layers:
        doc.layers.add(name=name, color=color, lineweight=lineweight, linetype=linetype)


def new_document() -> ezdxf.document.Drawing:
    doc = ezdxf.new("R2018", setup=True)
    doc.header["$INSUNITS"] = 6  # metros
    doc.header["$LUNITS"] = 2
    doc.header["$LUPREC"] = 3
    layers = (
        ("MARCO", 7, 35, "CONTINUOUS"),
        ("ROTULO", 5, 25, "CONTINUOUS"),
        ("ROTULO_TEXTO", 7, 18, "CONTINUOUS"),
        ("ADVERTENCIA", 1, 25, "CONTINUOUS"),
        ("IE_ALUMBRADO", 2, 25, "CONTINUOUS"),
        ("IE_FUERZA", 1, 30, "CONTINUOUS"),
        ("IE_EMERGENCIA", 6, 30, "CONTINUOUS"),
        ("IE_CANALIZACION", 4, 18, "DASHED"),
        ("IE_TIERRA", 3, 35, "CONTINUOUS"),
        ("IE_RAYO", 30, 30, "CONTINUOUS"),
        ("IE_ZONA_1", 1, 35, "DASHED"),
        ("IE_ZONA_2", 30, 25, "DASHED"),
        ("IE_TABLA", 7, 13, "CONTINUOUS"),
        ("IE_TEXTO", 7, 18, "CONTINUOUS"),
        ("ARQ_REFERENCIA", 8, 9, "CONTINUOUS"),
    )
    for layer in layers:
        add_layer(doc, *layer)
    return doc


def rect(msp: ezdxf.layouts.BaseLayout, x0: float, y0: float, x1: float, y1: float, layer: str, color: int | None = None) -> None:
    attribs: dict[str, Any] = {"layer": layer}
    if color is not None:
        attribs["color"] = color
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], dxfattribs=attribs, close=True)


def text_left(msp: ezdxf.layouts.BaseLayout, value: str, x: float, y: float, height: float = 0.28, layer: str = "IE_TEXTO", color: int | None = None) -> None:
    attribs: dict[str, Any] = {"layer": layer, "height": height}
    if color is not None:
        attribs["color"] = color
    msp.add_text(str(value), dxfattribs=attribs).set_placement((x, y), align=TextEntityAlignment.LEFT)


def text_center(msp: ezdxf.layouts.BaseLayout, value: str, x: float, y: float, height: float = 0.28, layer: str = "IE_TEXTO", color: int | None = None) -> None:
    attribs: dict[str, Any] = {"layer": layer, "height": height}
    if color is not None:
        attribs["color"] = color
    msp.add_text(str(value), dxfattribs=attribs).set_placement((x, y), align=TextEntityAlignment.MIDDLE_CENTER)


def add_frame(msp: ezdxf.layouts.BaseLayout) -> None:
    rect(msp, *FRAME, layer="MARCO")
    text_left(msp, "PROYECTO ACADEMICO - ANTEPROYECTO ELECTRICO", 0.9, 58.05, 0.28, "ADVERTENCIA")
    text_left(msp, "NO CONSTRUIR SIN FACTIBILIDAD, VERIFICACION DE CAMPO Y REVISION PROFESIONAL", 32.0, 58.05, 0.25, "ADVERTENCIA")


def entity_center(entity: ezdxf.entities.DXFGraphic, cache: bbox.Cache) -> tuple[float, float] | None:
    try:
        ext = bbox.extents([entity], cache=cache)
    except Exception:
        return None
    if not ext.has_data:
        return None
    center = ext.center
    return float(center.x), float(center.y)


def entity_bounds(entity: ezdxf.entities.DXFGraphic, cache: bbox.Cache) -> tuple[float, float, float, float] | None:
    try:
        ext = bbox.extents([entity], cache=cache)
    except Exception:
        return None
    if not ext.has_data:
        return None
    return float(ext.extmin.x), float(ext.extmin.y), float(ext.extmax.x), float(ext.extmax.y)


def point_in_window(point: tuple[float, float], window: tuple[float, float, float, float]) -> bool:
    x, y = point
    x0, y0, x1, y1 = window
    return x0 <= x <= x1 and y0 <= y <= y1


def bounds_intersect_window(bounds: tuple[float, float, float, float], window: tuple[float, float, float, float]) -> bool:
    bx0, by0, bx1, by1 = bounds
    wx0, wy0, wx1, wy1 = window
    return bx1 >= wx0 and bx0 <= wx1 and by1 >= wy0 and by0 <= wy1


def entity_matches_windows(
    bounds: tuple[float, float, float, float] | None,
    center: tuple[float, float] | None,
    windows: tuple[tuple[float, float, float, float], ...],
) -> bool:
    if bounds is None:
        return center is not None and any(point_in_window(center, window) for window in windows)
    bx0, by0, bx1, by1 = bounds
    wx0 = min(window[0] for window in windows)
    wy0 = min(window[1] for window in windows)
    wx1 = max(window[2] for window in windows)
    wy1 = max(window[3] for window in windows)
    oversized = (bx1 - bx0) > (wx1 - wx0) * 1.5 or (by1 - by0) > (wy1 - wy0) * 1.5
    if oversized:
        effective_center = center or ((bx0 + bx1) / 2, (by0 + by1) / 2)
        return any(point_in_window(effective_center, window) for window in windows)
    return any(bounds_intersect_window(bounds, window) for window in windows)


def add_architecture(doc: ezdxf.document.Drawing, source_path: Path, sheet_code: str) -> int:
    """Importa solo la arquitectura pertinente, sin cuadricula ni detalles sueltos."""
    source = ezdxf.readfile(source_path)
    cache = bbox.Cache()
    entities_by_view: dict[str, list[ezdxf.entities.DXFGraphic]] = (
        {level: [] for level in LEVEL_LAYOUTS} if sheet_code == "IE-02" else {"SITE": []}
    )
    for entity in source.modelspace():
        # Las DIMENSION de la copia derivada perdieron sus bloques graficos al
        # separarse de la lamina fuente; se omiten para evitar entidades rotas.
        if entity.dxftype() in {"HATCH", "SOLID", "TRACE", "WIPEOUT", "IMAGE", "DIMENSION"}:
            continue
        if entity.dxf.layer.casefold() in BACKGROUND_LAYERS_OMITTED:
            continue
        if sheet_code == "IE-02" and entity.dxf.layer.casefold() in LEVEL_LAYERS_OMITTED:
            continue
        if entity.dxftype() == "INSERT" and entity.dxf.name.upper() == "ROTULO":
            continue
        bounds = entity_bounds(entity, cache)
        center = entity_center(entity, cache)
        if bounds is None and center is None:
            continue
        if sheet_code == "IE-02":
            for level, layout in LEVEL_LAYOUTS.items():
                selected = entity_matches_windows(bounds, center, layout["windows"])
                if selected:
                    entities_by_view[level].append(entity)
                    break
        elif point_in_window(center, SITE_VIEW):
            entities_by_view["SITE"].append(entity)

    imported_count = 0
    for view, entities in entities_by_view.items():
        block_name = f"ARQUITECTURA_A01_{view}"
        block = doc.blocks.new(name=block_name)
        importer = Importer(source, doc)
        importer.import_entities(entities, block)
        importer.finalize()
        if view == "SITE":
            scale, offset = ARCH_SCALE, (0.0, 0.0)
        else:
            scale = float(LEVEL_LAYOUTS[view]["scale"])
            offset = tuple(LEVEL_LAYOUTS[view]["offset"])
        doc.modelspace().add_blockref(
            block_name,
            offset,
            dxfattribs={"xscale": scale, "yscale": scale, "zscale": scale, "layer": "ARQ_REFERENCIA"},
        )
        imported_count += len(entities)
    return imported_count


def source_point(level: str, point: tuple[float, float]) -> tuple[float, float]:
    """Lleva una coordenada arquitectonica A-01 al panel ampliado del nivel."""
    layout = LEVEL_LAYOUTS[level]
    dx, dy = layout["offset"]
    scale = float(layout["scale"])
    return point[0] * scale + dx, point[1] * scale + dy


def validate_ie02_electrical_zones(doc: ezdxf.document.Drawing) -> None:
    """Impide publicar instalaciones interiores fuera de sus tres paneles."""
    panels = {
        "N1": (1.5, 18.0, 27.5, 42.0),
        "N2": (28.5, 18.0, 54.5, 42.0),
        "N3": (55.5, 18.0, 82.0, 42.0),
    }
    electrical_layers = {"IE_ALUMBRADO", "IE_FUERZA", "IE_EMERGENCIA", "IE_CANALIZACION"}
    cache = bbox.Cache()
    counts = {level: 0 for level in panels}
    outside: list[str] = []
    for entity in doc.modelspace():
        if entity.dxf.layer not in electrical_layers or entity.dxftype() in {"TEXT", "MTEXT"}:
            continue
        center = entity_center(entity, cache)
        if center is None:
            continue
        matches = [level for level, window in panels.items() if point_in_window(center, window)]
        if not matches:
            outside.append(f"{entity.dxftype()}#{entity.dxf.handle}@{center[0]:.2f},{center[1]:.2f}")
        else:
            counts[matches[0]] += 1
    if outside:
        raise RuntimeError("IE-02 contiene entidades electricas fuera de panel: " + "; ".join(outside[:8]))
    sparse = [level for level, count in counts.items() if count < 20]
    if sparse:
        raise RuntimeError(f"IE-02 no contiene suficiente detalle electrico en: {', '.join(sparse)}")


def validate_ie03_site_zone(doc: ezdxf.document.Drawing) -> None:
    """Evita paros, bombas, surtidores o rutas electricas fuera del predio util."""
    site = (28.5, 9.0, 54.0, 39.0)
    layers = {"IE_FUERZA", "IE_EMERGENCIA", "IE_CANALIZACION"}
    cache = bbox.Cache()
    outside: list[str] = []
    for entity in doc.modelspace():
        if entity.dxf.layer not in layers or entity.dxftype() in {"TEXT", "MTEXT"}:
            continue
        center = entity_center(entity, cache)
        if center is not None and not point_in_window(center, site):
            outside.append(f"{entity.dxftype()}#{entity.dxf.handle}@{center[0]:.2f},{center[1]:.2f}")
    if outside:
        raise RuntimeError("IE-03 contiene equipos o rutas fuera del predio: " + "; ".join(outside[:8]))


def add_title_block(
    msp: ezdxf.layouts.BaseLayout,
    source_path: Path,
    title_data: dict[str, Any],
    sheet: dict[str, str],
    number: int,
    total: int,
    scale: str,
) -> None:
    """Adapta el cajetin ROTULO del A-01 sin crear una mascara nueva.

    La lamina arquitectonica ya trae un cajetin compacto en la franja inferior
    derecha. Se importa su geometria y se cambian sus atributos; de esta forma
    se conserva el lenguaje del expediente de referencia y no se tapa una banda
    de dibujo mayor que la prevista originalmente.
    """
    source = ezdxf.readfile(source_path)
    source_insert = next(
        (entity for entity in source.modelspace().query("INSERT") if entity.dxf.name.upper() == "ROTULO"),
        None,
    )
    if source_insert is None:
        raise ValueError("La base A-01 no contiene el bloque ROTULO que debe adaptarse")

    container_name = f"ROTULO_AQUILES_{sheet['codigo'].replace('-', '_')}"
    container = msp.doc.blocks.new(name=container_name)
    importer = Importer(source, msp.doc)
    importer.import_entities([source_insert], container)
    importer.finalize()
    imported_insert = next(iter(container.query("INSERT")))

    # Retira autoria empresarial fija del antecedente. Se conservan lineas,
    # mapa de Puno y etiquetas de campos del formato original.
    original_block = msp.doc.blocks.get(imported_insert.dxf.name)
    obsolete_tokens = (
        "GHANDY CORPORACION",
        "DIVISION DE MEDIO AMBIENTE",
        "DIVISIÓN MEDIO AMBIENTE",
        "DE INGENIEROS SRL",
    )
    for entity in list(original_block):
        if entity.dxftype() not in {"TEXT", "MTEXT"}:
            continue
        value = str(getattr(entity.dxf, "text", "")).upper()
        if any(token in value for token in obsolete_tokens):
            original_block.delete_entity(entity)

    project = title_data["proyecto"]
    replacements = {
        "AV.INTEROCEANICA": "PREDIO REUMITA B-8/B-9; C.C. SAN FRANCISCO DE BUENAVISTA",
        "JAVIERCHAMBICHAHUARA": project["propietario"],
        "CONSTRUCCIONDEGRIFO": "INSTALACIONES ELECTRICAS BT - GRIFO",
        "DICIEMBRE2016": title_data["presentacion"]["fecha_base"],
        "1/100": scale.replace(" / IND.", ""),
        "DISTRIBUCIONYCIRCULACION": sheet["titulo"],
        "J.CH.CH": "A. T. RAMOS YAPO",
        "CENTROPOBLADODE": "CARRETERA JULIACA-PUNO",
        "A-01": sheet["codigo"],
    }
    location_values = iter((project["departamento"], project["provincia"].replace("_", " "), project["distrito"]))
    for attrib in imported_insert.attribs:
        tag = attrib.dxf.tag.upper()
        if tag == "PUNO":
            attrib.dxf.text = next(location_values)
        elif tag in replacements:
            attrib.dxf.text = replacements[tag]
        if tag == "DISTRIBUCIONYCIRCULACION" and len(sheet["titulo"]) > 42:
            attrib.dxf.height *= 0.72
        if tag == "AV.INTEROCEANICA":
            attrib.dxf.height *= 0.82

    msp.add_blockref(
        container_name,
        (0.0, 0.0),
        dxfattribs={"xscale": ARCH_SCALE, "yscale": ARCH_SCALE, "zscale": ARCH_SCALE, "layer": "ROTULO"},
    )

    # Datos academicos agregados dentro de la misma huella vertical del cajetin.
    inst = title_data["institucion"]
    acad = title_data["academico"]
    text_center(msp, inst["universidad"], 69.4, 7.42, 0.22, "ROTULO_TEXTO")
    text_center(msp, f"{acad['curso']} | {acad['estudiante']}", 69.4, 7.13, 0.16, "ROTULO_TEXTO")
    text_center(msp, f"DOCENTE: {acad['docente']} | HOJA {number:02d}/{total:02d}", 69.4, 6.88, 0.15, "ROTULO_TEXTO")
    text_left(msp, "PROPIETARIO TRANSCRITO DE REFERENCIA FACILITADA POR DREM; NO ACREDITA APROBACION", 56.7, 1.14, 0.13, "ADVERTENCIA")
    text_left(msp, "ANTEPROYECTO ACADEMICO: SIN CIP, FIRMA NI SELLO; REQUIERE CAMPO, FACTIBILIDAD Y REVISION PROFESIONAL", 56.7, 0.78, 0.13, "ADVERTENCIA")


def add_luminaire(msp: ezdxf.layouts.BaseLayout, point: tuple[float, float], label: str = "", emergency: bool = False) -> None:
    x, y = point
    layer = "IE_EMERGENCIA" if emergency else "IE_ALUMBRADO"
    msp.add_circle((x, y), 0.22, dxfattribs={"layer": layer})
    msp.add_line((x - 0.15, y - 0.15), (x + 0.15, y + 0.15), dxfattribs={"layer": layer})
    msp.add_line((x - 0.15, y + 0.15), (x + 0.15, y - 0.15), dxfattribs={"layer": layer})
    if label:
        text_left(msp, label, x + 0.28, y + 0.15, 0.18, layer)


def add_outlet(msp: ezdxf.layouts.BaseLayout, point: tuple[float, float], label: str = "TC") -> None:
    x, y = point
    msp.add_circle((x, y), 0.20, dxfattribs={"layer": "IE_FUERZA"})
    msp.add_line((x - 0.13, y), (x + 0.13, y), dxfattribs={"layer": "IE_FUERZA"})
    msp.add_line((x, y), (x, y + 0.13), dxfattribs={"layer": "IE_FUERZA"})
    if label:
        text_left(msp, label, x + 0.25, y + 0.10, 0.17, "IE_FUERZA")


def add_panel(msp: ezdxf.layouts.BaseLayout, point: tuple[float, float], label: str, layer: str = "IE_FUERZA") -> None:
    x, y = point
    rect(msp, x - 0.32, y - 0.25, x + 0.32, y + 0.25, layer)
    text_center(msp, label, x, y, 0.18, layer)


def add_route_tag(msp: ezdxf.layouts.BaseLayout, point: tuple[float, float], circuit_id: str, layer: str) -> None:
    x, y = point
    msp.add_circle((x, y), 0.31, dxfattribs={"layer": layer})
    text_center(msp, circuit_id, x, y, 0.16 if len(circuit_id) <= 5 else 0.13, layer)


def add_route(
    msp: ezdxf.layouts.BaseLayout,
    points: list[tuple[float, float]],
    layer: str = "IE_CANALIZACION",
    circuit_id: str | None = None,
    tag_point: tuple[float, float] | None = None,
) -> None:
    polyline = msp.add_lwpolyline(points, dxfattribs={"layer": layer, "linetype": "DASHED"})
    polyline.dxf.const_width = 0.035
    if circuit_id:
        add_route_tag(msp, tag_point or points[len(points) // 2], circuit_id, layer)


def add_service_point(msp: ezdxf.layouts.BaseLayout, point: tuple[float, float], label: str, layer: str = "IE_FUERZA") -> None:
    x, y = point
    rect(msp, x - 0.25, y - 0.20, x + 0.25, y + 0.20, layer)
    text_left(msp, label, x + 0.34, y + 0.02, 0.17, layer)


def add_legend(msp: ezdxf.layouts.BaseLayout, title: str, rows: list[tuple[str, str]], x: float = 55.0, y: float = 55.8, width: float = 28.0) -> None:
    row_h = 0.72
    height = 1.05 + row_h * len(rows)
    rect(msp, x, y - height, x + width, y, "IE_TABLA")
    text_center(msp, title, x + width / 2, y - 0.48, 0.32, "IE_TEXTO")
    msp.add_line((x, y - 0.90), (x + width, y - 0.90), dxfattribs={"layer": "IE_TABLA"})
    for index, (code, description) in enumerate(rows):
        yy = y - 1.30 - index * row_h
        text_left(msp, code, x + 0.25, yy, 0.23, "IE_TEXTO")
        text_left(msp, description, x + 4.0, yy, 0.22, "IE_TEXTO")


def add_symbol_legend(
    msp: ezdxf.layouts.BaseLayout,
    title: str,
    rows: list[tuple[str, str, str]],
    x: float = 2.0,
    y: float = 55.8,
    width: float = 31.0,
) -> None:
    """Leyenda grafica compacta en la franja superior libre de las A1."""
    row_h = 1.02
    height = 1.05 + row_h * len(rows)
    rect(msp, x, y - height, x + width, y, "IE_TABLA")
    text_center(msp, title, x + width / 2, y - 0.48, 0.31, "IE_TEXTO")
    msp.add_line((x, y - 0.90), (x + width, y - 0.90), dxfattribs={"layer": "IE_TABLA"})
    for index, (symbol, code, description) in enumerate(rows):
        cy = y - 1.38 - index * row_h
        sx = x + 1.35
        if symbol == "LUM":
            msp.add_circle((sx, cy), 0.20, dxfattribs={"layer": "IE_TABLA"})
            msp.add_line((sx - 0.14, cy - 0.14), (sx + 0.14, cy + 0.14), dxfattribs={"layer": "IE_TABLA"})
            msp.add_line((sx - 0.14, cy + 0.14), (sx + 0.14, cy - 0.14), dxfattribs={"layer": "IE_TABLA"})
        elif symbol == "OUTLET":
            msp.add_circle((sx, cy), 0.20, dxfattribs={"layer": "IE_TABLA"})
            msp.add_line((sx - 0.13, cy), (sx + 0.13, cy), dxfattribs={"layer": "IE_TABLA"})
            msp.add_line((sx, cy), (sx, cy + 0.13), dxfattribs={"layer": "IE_TABLA"})
        elif symbol == "PANEL":
            rect(msp, sx - 0.28, cy - 0.20, sx + 0.28, cy + 0.20, "IE_TABLA")
        elif symbol == "PUMP":
            msp.add_circle((sx, cy), 0.23, dxfattribs={"layer": "IE_TABLA"})
            text_center(msp, "M", sx, cy, 0.15, "IE_TABLA")
        elif symbol == "ESTOP":
            msp.add_circle((sx, cy), 0.25, dxfattribs={"layer": "IE_TABLA"})
            text_center(msp, "PE", sx, cy, 0.13, "IE_TABLA")
        elif symbol == "EARTH":
            msp.add_line((sx, cy + 0.26), (sx, cy), dxfattribs={"layer": "IE_TABLA"})
            for half, dy in ((0.26, 0.0), (0.18, -0.10), (0.09, -0.20)):
                msp.add_line((sx - half, cy + dy), (sx + half, cy + dy), dxfattribs={"layer": "IE_TABLA"})
        elif symbol == "CAP":
            msp.add_circle((sx, cy), 0.22, dxfattribs={"layer": "IE_TABLA"})
            msp.add_line((sx, cy - 0.35), (sx, cy + 0.35), dxfattribs={"layer": "IE_TABLA"})
        elif symbol == "ZONE1":
            msp.add_circle((sx, cy), 0.28, dxfattribs={"layer": "IE_TABLA", "linetype": "DASHED"})
            text_center(msp, "Z1", sx, cy, 0.12, "IE_TABLA")
        elif symbol == "ZONE2":
            rect(msp, sx - 0.32, cy - 0.22, sx + 0.32, cy + 0.22, "IE_TABLA")
            text_center(msp, "Z2", sx, cy, 0.12, "IE_TABLA")
        else:  # rutas normal, emergencia o equipotencial
            line = msp.add_line((sx - 0.55, cy), (sx + 0.55, cy), dxfattribs={"layer": "IE_TABLA"})
            if symbol == "ROUTE":
                line.dxf.linetype = "DASHED"
            elif symbol == "EMERGENCY":
                msp.add_circle((sx, cy), 0.11, dxfattribs={"layer": "IE_TABLA"})
        text_left(msp, code, x + 2.55, cy - 0.08, 0.20, "IE_TEXTO")
        text_left(msp, description, x + 7.0, cy - 0.08, 0.20, "IE_TEXTO")


def sheet_ie01(doc: ezdxf.document.Drawing, _: dict[str, Any], __: dict[str, Any]) -> None:
    msp = doc.modelspace()
    # Marquesina: 18 luminarias en tres circuitos alternados.
    canopy: list[tuple[float, float]] = []
    index = 0
    for y in (18.0, 20.5, 23.0, 25.5, 28.0, 30.5):
        for x in (36.0, 38.4, 40.8):
            index += 1
            canopy.append((x, y))
            add_luminaire(msp, (x, y), f"L{index:02d}", emergency=index <= 6)
    exterior = ((26.0, 12.8), (31.0, 13.0), (43.0, 13.0), (49.0, 14.5), (26.0, 36.5), (32.0, 38.5), (43.0, 38.5), (50.0, 36.0))
    for index, point in enumerate(exterior, 1):
        add_luminaire(msp, point, f"PE{index}", emergency=index <= 4)

    tge = (31.58, 37.15)
    tdf = (34.6, 37.15)
    tde = (33.5, 36.55)
    add_panel(msp, tge, "TGE")
    add_panel(msp, (32.5, 36.6), "ATS", "IE_EMERGENCIA")
    add_panel(msp, tde, "TDE", "IE_EMERGENCIA")
    add_panel(msp, tdf, "TDF")

    # Cada circuito ocupa un carril y se identifica en una burbuja. Se evita
    # superponer cinco diagonales desde el tablero, que hacia ilegible la ruta.
    canopy_circuits = (
        ("L-01", tde, canopy[0:6], 35.05, "IE_EMERGENCIA"),
        ("L-02", tdf, canopy[6:12], 34.60, "IE_CANALIZACION"),
        ("L-03", tdf, canopy[12:18], 34.15, "IE_CANALIZACION"),
    )
    for circuit_id, source, points, lane_x, layer in canopy_circuits:
        first_row = points[:3]
        second_row = points[3:]
        route = [
            source,
            (lane_x, source[1]),
            (lane_x, first_row[0][1]),
            first_row[0],
            first_row[1],
            first_row[2],
            (first_row[2][0], second_row[2][1]),
            second_row[2],
            second_row[1],
            second_row[0],
        ]
        add_route(msp, route, layer, circuit_id, (lane_x, (first_row[0][1] + source[1]) / 2))

    exterior_routes = (
        ("L-04", tde, [tde, (25.5, tde[1]), (25.5, 12.8), exterior[0], (exterior[1][0], 12.8), exterior[1], exterior[2], (exterior[3][0], 13.0), exterior[3]], "IE_EMERGENCIA", (25.5, 25.0)),
        ("L-05", tdf, [tdf, (50.5, tdf[1]), (50.5, 36.0), exterior[7], (43.0, 36.0), exterior[6], exterior[5], (26.0, 38.5), exterior[4]], "IE_CANALIZACION", (50.5, 33.5)),
    )
    for circuit_id, _, route, layer, tag in exterior_routes:
        add_route(msp, route, layer, circuit_id, tag)
    sign = (27.0, 10.8)
    add_service_point(msp, sign, "AVISO PRECIOS")
    add_route(msp, [tdf, (33.7, tdf[1]), (33.7, 10.8), sign], "IE_CANALIZACION", "L-06", (33.7, 15.3))
    add_legend(msp, "IE-01 | LEYENDA Y CRITERIOS", [
        ("X", "Luminaria LED; verde = circuito normal, magenta = critico"),
        ("TGE", "Tablero general 380/220 V, 80 A, 4P"),
        ("TDE", "Tablero de emergencia mediante ATS 4P, 63 A"),
        ("(L-xx)", "Burbuja de circuito; rutas en carriles con derivaciones ortogonales"),
        ("NOTA", "18 x 100 W marquesina y 8 x 120 W exterior como criterio"),
        ("CNE", "dV ramal <= 2.5 % y total <= 4 %; PE en todo circuito"),
    ])
    add_symbol_legend(msp, "SIMBOLOGIA IE-01", [
        ("LUM", "L", "Luminaria LED exterior o de marquesina"),
        ("PANEL", "TGE/TDE", "Tablero general o de emergencia"),
        ("ROUTE", "CAN", "Canalizacion de circuito normal"),
        ("EMERGENCY", "EM", "Circuito critico o de emergencia"),
    ])


def sheet_ie02(doc: ezdxf.document.Drawing, _: dict[str, Any], __: dict[str, Any]) -> None:
    msp = doc.modelspace()
    # Coordenadas tomadas de los nombres de ambiente de la A-01. Cada nivel se
    # representa como un panel independiente, con recorridos ortogonales dentro
    # de su huella y sin prolongaciones hacia el espacio vacio de la lamina.
    levels = {
        "N1": {
            "panel": (62.6, 70.4),
            "panel_name": "TD-A1",
            "lights": ((71.5, 75.0), (76.0, 75.0), (64.8, 73.1), (66.0, 71.1), (62.9, 68.6), (63.0, 66.0)),
            "outlets": ((69.5, 74.1), (77.0, 74.1), (64.0, 72.2), (67.0, 70.2), (62.0, 67.5), (64.2, 65.5)),
            "corridor_y": 71.8,
            "circuits": ("A1-01", "A1-02", "A1-03"),
        },
        "N2": {
            "panel": (60.7, 85.7),
            "panel_name": "TD-A2",
            "lights": ((69.3, 90.5), (74.0, 90.5), (64.5, 88.0), (61.8, 87.8), (60.5, 83.5)),
            "outlets": ((68.0, 89.6), (75.0, 89.6), (63.8, 87.2), (62.5, 86.8), (59.7, 84.1), (62.0, 82.9)),
            "corridor_y": 88.7,
            "circuits": ("A2-01", "A2-02", "A2-03"),
        },
        "N3": {
            "panel": (61.0, 103.6),
            "panel_name": "TD-A3",
            "lights": ((69.6, 108.3), (74.3, 108.3), (64.7, 105.8), (62.1, 105.6), (60.7, 101.4)),
            "outlets": ((68.3, 107.4), (75.3, 107.4), (64.0, 105.0), (62.7, 104.7), (59.9, 102.0), (62.2, 100.8)),
            "corridor_y": 106.5,
            "circuits": ("A3-01", "A3-02", "A3-03"),
        },
    }
    for level, data in levels.items():
        panel = source_point(level, data["panel"])
        lights = tuple(source_point(level, point) for point in data["lights"])
        outlets = tuple(source_point(level, point) for point in data["outlets"])
        corridor_y = source_point(level, (0.0, data["corridor_y"]))[1]
        panel_name = str(data["panel_name"])
        add_panel(msp, panel, panel_name)
        for index, point in enumerate(lights, 1):
            add_luminaire(msp, point)
        for index, point in enumerate(outlets, 1):
            add_outlet(msp, point, "")
        lighting_id, outlet_a, outlet_b = data["circuits"]

        light_end_x = max(point[0] for point in lights)
        add_route(
            msp,
            [panel, (panel[0], corridor_y), (light_end_x, corridor_y)],
            "IE_CANALIZACION",
            lighting_id,
            ((panel[0] + light_end_x) / 2, corridor_y),
        )
        for light in lights:
            msp.add_lwpolyline([(light[0], corridor_y), light], dxfattribs={"layer": "IE_CANALIZACION", "linetype": "DASHED"})

        outlet_groups = (outlets[:3], outlets[3:])
        for circuit_id, group, lane_offset in ((outlet_a, outlet_groups[0], -0.45), (outlet_b, outlet_groups[1], -0.85)):
            lane_y = corridor_y + lane_offset
            end_x = max(point[0] for point in group)
            add_route(msp, [panel, (panel[0], lane_y), (end_x, lane_y)], "IE_FUERZA", circuit_id, ((panel[0] + end_x) / 2, lane_y))
            for outlet in group:
                msp.add_lwpolyline([(outlet[0], lane_y), outlet], dxfattribs={"layer": "IE_FUERZA"})

        title_x = {"N1": 3.0, "N2": 30.0, "N3": 57.0}[level]
        text_left(msp, f"{level} | INSTALACIONES INTERIORES", title_x, 41.5, 0.36, "IE_TEXTO")

    # Cargas dedicadas del primer nivel, visibles y separadas de los circuitos
    # generales de tomacorrientes.
    dedicated_points: list[tuple[str, tuple[float, float]]] = []
    for circuit_id, label, source_location in (
        ("A1-04", "POS", (70.3, 73.8)),
        ("A1-05", "REF-1", (72.6, 73.8)),
        ("A1-06", "REF-2", (74.9, 73.8)),
    ):
        point = source_point("N1", source_location)
        add_service_point(msp, point, label, "IE_EMERGENCIA")
        dedicated_points.append((circuit_id, point))
    panel = source_point("N1", levels["N1"]["panel"])
    lane_y = source_point("N1", (0.0, 72.8))[1]
    end_x = max(point[0] for _, point in dedicated_points)
    add_route(msp, [panel, (panel[0], lane_y), (end_x, lane_y)], "IE_EMERGENCIA", "A1-04/06", ((panel[0] + end_x) / 2, lane_y))
    for circuit_id, point in dedicated_points:
        msp.add_lwpolyline([(point[0], lane_y), point], dxfattribs={"layer": "IE_EMERGENCIA"})
        text_left(msp, circuit_id, point[0] - 0.30, point[1] - 0.42, 0.15, "IE_EMERGENCIA")
    add_legend(msp, "IE-02 | EDIFICIO ADMINISTRATIVO", [
        ("N1", "120.35 m2: minimarket, administracion, atencion y servicios"),
        ("N2", "160.20 m2: oficinas 1 a 3 y SS.HH."),
        ("N3", "160.20 m2: oficinas 4 a 6 y SS.HH."),
        ("TC", "Tomacorriente doble 220 V, 2P+T; RCBO 30 mA"),
        ("L", "Punto de alumbrado LED; conductor minimo 2.5 mm2 Cu"),
        ("(A#-##)", "Burbuja de circuito; alumbrado, tomas y cargas dedicadas separados"),
        ("NOTA", "Posiciones sujetas a replanteo con arquitectura acotada"),
    ])
    add_symbol_legend(msp, "SIMBOLOGIA IE-02", [
        ("LUM", "L", "Punto de alumbrado LED"),
        ("OUTLET", "TC", "Tomacorriente doble 220 V, 2P+T"),
        ("PANEL", "TD-A#", "Tablero de distribucion del nivel"),
        ("ROUTE", "A#-##", "Canalizacion del circuito identificado"),
        ("EMERGENCY", "DED", "Carga dedicada o circuito respaldado"),
    ])


def sheet_ie03(doc: ezdxf.document.Drawing, architecture: dict[str, Any], __: dict[str, Any]) -> None:
    msp = doc.modelspace()
    tdf = (31.58, 37.15)
    tde = (32.65, 36.55)
    ups = (33.85, 36.55)
    add_panel(msp, tdf, "TDF")
    add_panel(msp, tde, "TDE", "IE_EMERGENCIA")
    add_panel(msp, ups, "UPS-F", "IE_EMERGENCIA")

    dispenser_points: list[tuple[float, float]] = []
    for index, dispenser in enumerate(architecture["dispensing"]["dispensers_local_A01"], 1):
        point = tuple(value * ARCH_SCALE for value in dispenser["point"])
        dispenser_points.append(point)
        add_panel(msp, point, f"SD{index}", "IE_FUERZA")
    # Un corredor UPS-FUEL y seis derivaciones cortas reemplazan seis trazos
    # superpuestos. Cada derivacion conserva su identificador F-05..F-10.
    dispenser_trunk_x = 35.25
    add_route(msp, [ups, (dispenser_trunk_x, ups[1]), (dispenser_trunk_x, min(point[1] for point in dispenser_points))], "IE_EMERGENCIA", "F05-10", (dispenser_trunk_x, 31.0))
    for index, point in enumerate(dispenser_points, 5):
        add_route(msp, [(dispenser_trunk_x, point[1]), point], "IE_EMERGENCIA", f"F-{index:02d}", ((dispenser_trunk_x + point[0]) / 2, point[1]))

    tank_points: list[tuple[float, float]] = []
    for index, tank in enumerate(architecture["fuel_storage"]["tanks"], 1):
        point = tuple(value * ARCH_SCALE for value in tank["local_A01_center"])
        tank_points.append(point)
        msp.add_circle(point, 0.25, dxfattribs={"layer": "IE_FUERZA"})
        text_left(msp, f"STP-{index} 1.5 hp", point[0] + 0.32, point[1], 0.19, "IE_FUERZA")
    # Cuatro carriles cortos y paralelos sobre el banco de tanques. Se evita la
    # columna de trazos coincidentes que ocultaba bombas y rotulos.
    for circuit_id, source, point, lane_y, layer in (
        ("F-01", tde, tank_points[0], 35.75, "IE_EMERGENCIA"),
        ("F-02", tdf, tank_points[1], 35.40, "IE_FUERZA"),
        ("F-03", tde, tank_points[2], 35.05, "IE_EMERGENCIA"),
        ("F-04", tdf, tank_points[3], 34.70, "IE_FUERZA"),
    ):
        add_route(msp, [source, (source[0], lane_y), (point[0], lane_y), point], layer, circuit_id, ((source[0] + point[0]) / 2, lane_y))
    # Paros ubicados en accesos reconocibles: ingreso vehicular y edificio.
    for index, (point, label_point) in enumerate((((32.0, 16.0), (32.45, 16.0)), ((52.8, 27.0), (50.7, 27.0))), 1):
        msp.add_circle(point, 0.32, dxfattribs={"layer": "IE_EMERGENCIA"})
        text_center(msp, "PE", point[0], point[1], 0.20, "IE_EMERGENCIA")
        text_left(msp, f"PARO-{index}", label_point[0], label_point[1], 0.20, "IE_EMERGENCIA")
    add_legend(msp, "IE-03 | FUERZA Y CONTROL DE COMBUSTIBLE", [
        ("STP", "4 bombas sumergibles 1.5 hp; arranque secuencial"),
        ("SD", "6 cabezales de surtidor 220 V, 103 VA de referencia"),
        ("PE", "Paro de emergencia remoto; corta bombas y surtidores"),
        ("UPS", "UPS-FUEL 3 kVA senoidal para cabezales/control/ATG"),
        ("CNE", "Equipos y sellos certificados para la zona donde se instalen"),
        ("(F-##)", "Burbuja de circuito; troncales y derivaciones se leen por separado"),
        ("NOTA", "Rutas y placas definitivas requieren coordinacion del proveedor"),
    ])
    add_symbol_legend(msp, "SIMBOLOGIA IE-03", [
        ("PANEL", "SD", "Cabezal electrico de surtidor"),
        ("PUMP", "STP", "Bomba sumergible de combustible"),
        ("ESTOP", "PE", "Paro de emergencia remoto"),
        ("ROUTE", "F-##", "Canalizacion de fuerza o control"),
        ("EMERGENCY", "UPS", "Circuito respaldado para control"),
    ])


def earth_symbol(msp: ezdxf.layouts.BaseLayout, point: tuple[float, float], label: str) -> None:
    x, y = point
    msp.add_line((x, y + 0.45), (x, y), dxfattribs={"layer": "IE_TIERRA"})
    for width, yy in ((0.45, 0.0), (0.30, -0.15), (0.15, -0.30)):
        msp.add_line((x - width, y + yy), (x + width, y + yy), dxfattribs={"layer": "IE_TIERRA"})
    text_left(msp, label, x + 0.55, y - 0.12, 0.18, "IE_TIERRA")


def sheet_ie04(doc: ezdxf.document.Drawing, architecture: dict[str, Any], __: dict[str, Any]) -> None:
    msp = doc.modelspace()
    ring = [(30.0, 10.8), (53.0, 10.8), (53.0, 38.0), (31.0, 38.0), (30.0, 10.8)]
    msp.add_lwpolyline(ring, dxfattribs={"layer": "IE_TIERRA", "closed": True})
    rods = ((30.2, 11.1), (41.5, 11.1), (52.7, 11.1), (52.7, 24.0), (52.7, 37.7), (42.0, 37.7), (31.2, 37.7), (30.2, 24.0))
    for index, point in enumerate(rods, 1):
        earth_symbol(msp, point, f"PT-{index}")
    for dispenser in architecture["dispensing"]["dispensers_local_A01"]:
        point = tuple(value * ARCH_SCALE for value in dispenser["point"])
        add_route(msp, [point, (point[0], 32.5), (31.0, 32.5)], "IE_TIERRA")
    for tank in architecture["fuel_storage"]["tanks"]:
        point = tuple(value * ARCH_SCALE for value in tank["local_A01_center"])
        add_route(msp, [point, (43.2, point[1]), (43.2, 38.0)], "IE_TIERRA")
    # Captadores convencionales y anillo de marquesina.
    lps = [(35.0, 16.5), (41.8, 16.5), (41.8, 32.5), (35.0, 32.5), (35.0, 16.5)]
    msp.add_lwpolyline(lps, dxfattribs={"layer": "IE_RAYO", "closed": True})
    for point in lps[:-1]:
        msp.add_circle(point, 0.23, dxfattribs={"layer": "IE_RAYO"})
        text_left(msp, "CAP", point[0] + 0.28, point[1], 0.16, "IE_RAYO")
    add_legend(msp, "IE-04 | TIERRA, EQUIPOTENCIALIDAD Y RAYO", [
        ("ANILLO", "Cu desnudo 35 mm2 como criterio; verificar por calculo y corrosion"),
        ("PT-1..8", "Electrodos distribuidos; cantidad final depende de resistividad"),
        ("R <= 25", "Limite CNE-U 060-712; objetivo de diseno <= 10 ohm"),
        ("BOND", "Unir tanques, tuberias, surtidores, marquesina y masas"),
        ("LPS", "Sistema convencional coordinado; evaluar riesgo IEC 62305"),
        ("SPD", "SPD Tipo 1+2 en TGE y Tipo 2 en tableros sensibles"),
    ])
    add_symbol_legend(msp, "SIMBOLOGIA IE-04", [
        ("EARTH", "PT", "Electrodo del sistema de puesta a tierra"),
        ("ROUTE", "ANILLO", "Conductor perimetral de cobre desnudo"),
        ("BOND", "BOND", "Conexion equipotencial de masas metalicas"),
        ("CAP", "CAP", "Captador del sistema contra rayos"),
    ])


def breaker_symbol(msp: ezdxf.layouts.BaseLayout, point: tuple[float, float], label: str) -> None:
    x, y = point
    msp.add_line((x, y + 0.4), (x, y + 0.12), dxfattribs={"layer": "IE_FUERZA"})
    msp.add_line((x - 0.18, y - 0.10), (x + 0.18, y + 0.12), dxfattribs={"layer": "IE_FUERZA"})
    msp.add_line((x, y - 0.10), (x, y - 0.40), dxfattribs={"layer": "IE_FUERZA"})
    text_left(msp, label, x + 0.30, y, 0.20, "IE_TEXTO")


def add_unifilar(msp: ezdxf.layouts.BaseLayout) -> None:
    y = 53.7
    nodes = ((3.5, "RED\n380/220V"), (9.5, "MEDIDOR"), (15.5, "ITM\n80A 4P"), (23.0, "TGE"), (35.5, "ATS\n63A 4P"), (44.0, "TDE"))
    for index, (x, label) in enumerate(nodes):
        rect(msp, x - 1.25, y - 1.0, x + 1.25, y + 1.0, "IE_FUERZA")
        for offset, line in enumerate(label.split("\n")):
            text_center(msp, line, x, y + 0.25 - offset * 0.48, 0.26, "IE_TEXTO")
        if index:
            msp.add_line((nodes[index - 1][0] + 1.25, y), (x - 1.25, y), dxfattribs={"layer": "IE_FUERZA"})
    text_center(msp, "ACOMETIDA / MEDICION: POR CONFIRMAR", 7.0, 55.35, 0.18, "IE_TEXTO")
    text_center(msp, "Cu 4x35 mm2 + PE 16 mm2 | ducto 75 mm", 19.2, 55.35, 0.18, "IE_TEXTO")
    text_center(msp, "AL-TDE: Cu 4x10 + PE 6 mm2", 39.8, 55.35, 0.18, "IE_TEXTO")

    rect(msp, 34.0, 48.0, 37.0, 49.7, "IE_EMERGENCIA")
    text_center(msp, "GE 37.5 kVA", 35.5, 48.85, 0.24, "IE_EMERGENCIA")
    msp.add_line((35.5, 49.7), (35.5, y - 1.0), dxfattribs={"layer": "IE_EMERGENCIA"})

    # Salidas normales del TGE: barra horizontal y bajantes ortogonales.
    normal_branches = (
        (8.0, "TD-A3 20A", "4x4+PE2.5"),
        (14.0, "TD-A2 20A", "4x4+PE2.5"),
        (20.0, "TD-A1 25A", "4x6+PE4"),
        (26.0, "TDF 40A", "4x10+PE6"),
    )
    bus_y = 50.8
    msp.add_line((23.0, y - 1.0), (23.0, bus_y), dxfattribs={"layer": "IE_FUERZA"})
    msp.add_line((normal_branches[0][0], bus_y), (normal_branches[-1][0], bus_y), dxfattribs={"layer": "IE_FUERZA"})
    for x, label, cable in normal_branches:
        msp.add_line((x, bus_y), (x, 47.0), dxfattribs={"layer": "IE_FUERZA"})
        rect(msp, x - 2.2, 45.6, x + 2.2, 47.0, "IE_FUERZA")
        text_center(msp, label, x, 46.48, 0.21, "IE_TEXTO")
        text_center(msp, cable, x, 45.95, 0.16, "IE_TEXTO")

    # Salidas de emergencia: otra barra, sin diagonales cruzadas.
    emergency_branches = (
        (50.5, "UPS-FUEL 3kVA", "F-05..F-11"),
        (58.5, "UPS-IT 2kVA", "S-01"),
        (66.5, "CARGAS CRITICAS", "L-01/L-04/S-02/03"),
    )
    msp.add_line((44.0, y - 1.0), (44.0, bus_y), dxfattribs={"layer": "IE_EMERGENCIA"})
    msp.add_line((44.0, bus_y), (emergency_branches[-1][0], bus_y), dxfattribs={"layer": "IE_EMERGENCIA"})
    for x, label, circuits in emergency_branches:
        msp.add_line((x, bus_y), (x, 47.0), dxfattribs={"layer": "IE_EMERGENCIA"})
        rect(msp, x - 3.0, 45.6, x + 3.0, 47.0, "IE_EMERGENCIA")
        text_center(msp, label, x, 46.48, 0.21, "IE_TEXTO")
        text_center(msp, circuits, x, 45.95, 0.15, "IE_TEXTO")
    text_left(msp, "DIAGRAMA ORDENADO POR BARRAS: NORMAL (ROJO) Y EMERGENCIA (MAGENTA). N Y PE SEPARADOS.", 2.0, 57.0, 0.28, "IE_TEXTO")


def add_load_table(msp: ezdxf.layouts.BaseLayout, calculations: dict[str, Any]) -> None:
    x0, x1 = 1.2, 53.2
    y_top = 42.0
    row_h = 0.70
    widths = (4.1, 19.8, 5.0, 4.0, 4.4, 4.2, 5.0, 5.5)
    headers = ("ID", "DESCRIPCION", "TABLERO", "FASE", "kVA MD", "ITM A", "Cu/PE", "dV %")
    xs = [x0]
    for width in widths:
        xs.append(xs[-1] + width)
    rows = calculations["circuits"]
    y_bottom = y_top - row_h * (len(rows) + 1)
    rect(msp, x0, y_bottom, x1, y_top, "IE_TABLA")
    for x in xs[1:-1]:
        msp.add_line((x, y_bottom), (x, y_top), dxfattribs={"layer": "IE_TABLA"})
    for index in range(1, len(rows) + 1):
        yy = y_top - row_h * index
        msp.add_line((x0, yy), (x1, yy), dxfattribs={"layer": "IE_TABLA"})
    for index, header in enumerate(headers):
        text_center(msp, header, (xs[index] + xs[index + 1]) / 2, y_top - row_h / 2, 0.20, "IE_TEXTO")
    for row_index, circuit in enumerate(rows, 1):
        values = (
            circuit["id"],
            circuit["description"][:38],
            circuit["panel"],
            circuit["phase"],
            f"{circuit['demand_kva']:.2f}",
            f"{float(circuit['breaker_a']):.0f}",
            f"{float(circuit['conductor_mm2']):g}/{float(circuit['pe_mm2']):g}",
            f"{circuit['total_voltage_drop_percent']:.2f}",
        )
        yy = y_top - row_h * row_index - row_h / 2
        for col, value in enumerate(values):
            height = 0.15 if col == 1 else 0.18
            text_center(msp, str(value), (xs[col] + xs[col + 1]) / 2, yy, height, "IE_TEXTO")
    text_left(msp, "CUADRO DE CARGAS - TODOS LOS CIRCUITOS CON RCBO <= 30 mA", x0, y_top + 0.45, 0.30, "IE_TEXTO")


def sheet_ie05(doc: ezdxf.document.Drawing, _: dict[str, Any], calculations: dict[str, Any]) -> None:
    msp = doc.modelspace()
    add_unifilar(msp)
    add_load_table(msp, calculations)
    summary = calculations["summary"]
    generator = calculations["generator"]
    x0, y0, x1, y1 = 55.0, 15.0, 83.0, 42.0
    rect(msp, x0, y0, x1, y1, "IE_TABLA")
    text_center(msp, "RESUMEN DE DIMENSIONAMIENTO", (x0 + x1) / 2, 41.2, 0.34, "IE_TEXTO")
    lines = (
        f"Potencia instalada: {summary['installed_kw']:.2f} kW / {summary['installed_kva']:.2f} kVA",
        f"Maxima demanda: {summary['maximum_demand_kw']:.2f} kW / {summary['maximum_demand_kva']:.2f} kVA",
        f"Demanda + 20 % reserva: {summary['service_design_kva_with_reserve']:.2f} kVA",
        "Suministro propuesto: 50 kVA, 380/220 V, 3F+N+PE",
        f"Corriente maxima de fase: {summary['maximum_phase_current_with_reserve_a']:.2f} A",
        f"Desbalance de fases: {summary['phase_unbalance_percent']:.2f} %",
        "Principal: ITM 80 A, 4P, Icu >= 25 kA (por validar)",
        "Alimentador: Cu 4x35 mm2 + PE 16 mm2",
        f"GE: {generator['selected_nameplate_kva']:.1f} kVA standby; factor altitud {generator['altitude_factor']:.4f}",
        f"GE disponible en sitio: {generator['available_standby_kva_at_site']:.2f} kVA",
        f"Arranque con margen: {generator['starting_with_margin_kva']:.2f} kVA - CUMPLE",
        "Caida: ramal <= 2.5 % y total <= 4 % (CNE-U 050-102)",
        "Selectividad, Icc y placas: PENDIENTES DE FACTIBILIDAD/CAMPO",
        "N y PE separados; ATS 4 polos con neutro conmutado",
        "Todas las cifras son de anteproyecto academico reproducible.",
    )
    for index, line in enumerate(lines):
        text_left(msp, line, x0 + 0.5, 39.9 - index * 1.48, 0.25, "IE_TEXTO")


def zone_circle(msp: ezdxf.layouts.BaseLayout, point: tuple[float, float], radius: float, label: str, layer: str) -> None:
    msp.add_circle(point, radius, dxfattribs={"layer": layer})
    if label:
        text_left(msp, label, point[0] + radius * 0.72, point[1] + radius * 0.72, 0.18, layer)


def sheet_ie06(doc: ezdxf.document.Drawing, architecture: dict[str, Any], __: dict[str, Any]) -> None:
    msp = doc.modelspace()
    dispenser_points = [tuple(value * ARCH_SCALE for value in item["point"]) for item in architecture["dispensing"]["dispensers_local_A01"]]
    # La union conservadora reemplaza seis circulos superpuestos. Los nodos de
    # surtidor permanecen visibles y la nota conserva el radio normativo.
    min_x = min(point[0] for point in dispenser_points) - 3.0
    max_x = max(point[0] for point in dispenser_points) + 3.0
    min_y = min(point[1] for point in dispenser_points) - 3.0
    max_y = max(point[1] for point in dispenser_points) + 3.0
    rect(msp, min_x, min_y, max_x, max_y, "IE_ZONA_2")
    text_left(msp, "ENVOLVENTE CONSERVADORA Z2 | r=6 m DESDE CADA SURTIDOR", max_x + 0.35, max_y - 0.20, 0.20, "IE_ZONA_2")
    for point in dispenser_points:
        msp.add_circle(point, 0.25, dxfattribs={"layer": "IE_ZONA_2"})

    fill_points = [tuple(value * ARCH_SCALE for value in item["point"]) for item in architecture["fuel_storage"]["fill_points_local_A01"]]
    fill_center = (sum(point[0] for point in fill_points) / len(fill_points), sum(point[1] for point in fill_points) / len(fill_points))
    zone_circle(msp, fill_center, 1.5, "", "IE_ZONA_1")

    vent_points = [tuple(value * ARCH_SCALE for value in item["point"]) for item in architecture["fuel_storage"]["vent_points_local_A01"]]
    vent_center = (sum(point[0] for point in vent_points) / len(vent_points), sum(point[1] for point in vent_points) / len(vent_points))
    zone_circle(msp, vent_center, 0.45, "", "IE_ZONA_1")
    zone_circle(msp, vent_center, 0.75, "", "IE_ZONA_2")
    msp.add_line(fill_center, (45.2, 40.4), dxfattribs={"layer": "IE_ZONA_1"})
    msp.add_line(vent_center, (45.2, 39.8), dxfattribs={"layer": "IE_ZONA_2"})
    text_left(msp, "LLENADO | ENVOLVENTE Z1/Z2", 45.4, 40.4, 0.20, "IE_ZONA_1")
    text_left(msp, "VENTEO | ENVOLVENTE Z1/Z2", 45.4, 39.8, 0.20, "IE_ZONA_2")
    add_legend(msp, "IE-06 | AREAS PELIGROSAS - PROPUESTA ACADEMICA", [
        ("ZONA 0", "Interior de tanques y tuberias con vapor inflamable"),
        ("ZONA 1", "Envolventes de llenado/venteo segun CNE-U 120"),
        ("ZONA 2", "Union conservadora; radio horizontal 6 m desde cada surtidor"),
        ("EQUIPO", "Seleccion Ex y temperatura compatibles con combustible"),
        ("SELLO", "Sellos y canalizaciones conforme a limite de zona"),
        ("ALERTA", "Validar alturas, ventilacion y geometria con especialista"),
        ("DS 054", "Las divisiones sectoriales se contrastan; no se igualan 1:1"),
    ])
    add_symbol_legend(msp, "SIMBOLOGIA IE-06", [
        ("ZONE1", "Z1", "Area con presencia probable de atmosfera peligrosa"),
        ("ZONE2", "Z2", "Area con presencia poco probable o breve"),
        ("PANEL", "EQ-Ex", "Equipo electrico certificado para la zona"),
        ("ROUTE", "SELLO", "Limite sellado de canalizacion clasificada"),
    ])
    # Detalle esquematico para que la altura no quede implicita solo en planta.
    x0, y0 = 55.0, 32.0
    rect(msp, x0, y0, 82.8, 44.5, "IE_TABLA")
    text_center(msp, "DETALLE ESQUEMATICO DE VENTEO Y LLENADO", 68.9, 43.9, 0.30, "IE_TEXTO")
    msp.add_line((x0 + 1.0, 34.0), (82.0, 34.0), dxfattribs={"layer": "IE_TABLA"})
    msp.add_line((61.0, 34.0), (61.0, 41.5), dxfattribs={"layer": "IE_FUERZA"})
    zone_circle(msp, (61.0, 41.5), 0.9, "Venteo: Z1 0.9m; Z2 hasta 1.5m", "IE_ZONA_1")
    rect(msp, 70.0, 33.4, 76.0, 35.8, "IE_FUERZA")
    zone_circle(msp, (73.0, 35.8), 1.5, "Llenado: verificar envolvente vertical", "IE_ZONA_2")
    text_left(msp, "DIMENSIONES DE PLANTA ESCALADAS DESDE CNE-U 120; ELEVACIONES REQUIEREN CAMPO", 56.0, 32.7, 0.20, "ADVERTENCIA")


SHEET_BUILDERS: dict[str, Callable[[ezdxf.document.Drawing, dict[str, Any], dict[str, Any]], None]] = {
    "IE-01": sheet_ie01,
    "IE-02": sheet_ie02,
    "IE-03": sheet_ie03,
    "IE-04": sheet_ie04,
    "IE-05": sheet_ie05,
    "IE-06": sheet_ie06,
}


def sheet_stem(sheet: dict[str, str]) -> str:
    return f"{sheet['codigo'].lower()}-{sheet['titulo'].lower().replace(' ', '-').replace(',', '').replace('/', '-')[:48]}"


def render(doc: ezdxf.document.Drawing, png_path: Path, pdf_path: Path) -> None:
    def render_filter(entity: ezdxf.entities.DXFGraphic) -> bool:
        return entity.dxftype() not in {"HATCH", "SOLID", "TRACE", "IMAGE"}

    ezdxf_matplotlib.qsave(
        doc.modelspace(),
        png_path,
        bg="#FFFFFF",
        fg="#111111",
        dpi=220,
        size_inches=(16.54, 11.69),
        filter_func=render_filter,
    )
    # PDF vectorial A1 horizontal. No convertir desde PNG: esa ruta rasteriza
    # textos y lineas y se vuelve borrosa al ampliar o imprimir.
    ezdxf_matplotlib.qsave(
        doc.modelspace(),
        pdf_path,
        bg="#FFFFFF",
        fg="#111111",
        size_inches=(33.11, 23.39),
        filter_func=render_filter,
    )


def apply_render_font_fallbacks(
    doc: ezdxf.document.Drawing,
) -> list[dict[str, str]]:
    """Normaliza SHX/no resueltas solo despues de guardar el DXF."""
    fallbacks: list[dict[str, str]] = []
    truetype_extensions = {".ttf", ".otf", ".ttc"}
    for style in doc.styles:
        filename = str(style.dxf.font or "")
        if Path(filename).suffix.lower() in truetype_extensions:
            continue
        fallbacks.append(
            {
                "style": str(style.dxf.name),
                "source_font": filename,
                "render_font": "arial.ttf",
            }
        )
        style.dxf.font = "arial.ttf"
    return fallbacks


def main() -> int:
    root = repository_root()
    project = root / "proyectos/unidad-2-industrial"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--architecture-base", type=Path, default=root / "build/unidad-2-industrial/cad/base/a_01_referencia_local.dxf")
    parser.add_argument("--output", type=Path, default=root / "build/unidad-2-industrial/cad/planos")
    parser.add_argument("--skip-render", action="store_true")
    parser.add_argument("--sheet", action="append", choices=tuple(SHEET_BUILDERS), help="regenera solo una lamina; puede repetirse")
    args = parser.parse_args()

    title_data = load_yaml(project / "datos/rotulo-planos.yaml")
    architecture = load_json(project / "arquitectura/datos/grifo.json")
    calculations = load_json(root / "build/unidad-2-industrial/calculos/resumen-calculos.json")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    if not args.architecture_base.is_file():
        raise SystemExit(f"No existe la base arquitectonica derivada: {args.architecture_base}")
    if calculations["status"] != "PASS":
        raise SystemExit("El calculo electrico no esta en estado PASS")

    manifest_path = output / "manifest.json"
    previous_manifest = load_json(manifest_path) if manifest_path.is_file() else None
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "generated_on": date.today().isoformat(),
        "title_block_source": "bloque ROTULO de la base A-01, adaptado con proyectos/unidad-2-industrial/datos/rotulo-planos.yaml",
        "architecture_source": str(args.architecture_base.resolve()),
        "architecture_source_sha256": sha256(args.architecture_base.resolve()),
        "calculation_source_sha256": calculations["source_sha256"],
        "sheets": [],
    }
    all_sheets = title_data["laminas_previstas"]
    sheets = [sheet for sheet in all_sheets if not args.sheet or sheet["codigo"] in args.sheet]
    architecture_count: int | None = None
    for sheet in sheets:
        number = next(index for index, item in enumerate(all_sheets, 1) if item["codigo"] == sheet["codigo"])
        code = sheet["codigo"]
        print(f"Generando {code}: {sheet['titulo']}", flush=True)
        doc = new_document()
        msp = doc.modelspace()
        add_frame(msp)
        if code != "IE-05":
            architecture_count = add_architecture(doc, args.architecture_base.resolve(), code)
        SHEET_BUILDERS[code](doc, architecture, calculations)
        if code == "IE-02":
            validate_ie02_electrical_zones(doc)
        elif code == "IE-03":
            validate_ie03_site_zone(doc)
        scale = "1:100 / IND." if code != "IE-05" else "S/E"
        add_title_block(msp, args.architecture_base.resolve(), title_data, sheet, number, len(all_sheets), scale)
        stem = sheet_stem(sheet)
        dxf_path = output / f"{stem}.dxf"
        png_path = output / f"{stem}.png"
        pdf_path = output / f"{stem}.pdf"
        # El importador puede conservar referencias de estilo de ATTRIB que no
        # existen en el documento destino. ezdxf las tolera al leer, pero
        # AutoCAD rechaza por completo el DXF. La auditoria elimina esas
        # referencias huerfanas antes de serializar el plano entregable.
        audit = doc.audit()
        if audit.errors:
            raise RuntimeError(
                f"DXF invalido para {sheet['codigo']}: "
                + "; ".join(error.message for error in audit.errors)
            )
        doc.saveas(dxf_path)
        render_font_fallbacks: list[dict[str, str]] = []
        if not args.skip_render:
            # El DXF conserva los estilos importados. La sustitucion se aplica
            # solo a las vistas Matplotlib para evitar fuentes SHX defectuosas
            # o no disponibles en Windows.
            render_font_fallbacks = apply_render_font_fallbacks(doc)
            render(doc, png_path, pdf_path)
        manifest["sheets"].append({
            "code": code,
            "title": sheet["titulo"],
            "dxf": str(dxf_path.relative_to(root)),
            "png": None if args.skip_render else str(png_path.relative_to(root)),
            "pdf": None if args.skip_render else str(pdf_path.relative_to(root)),
            "entity_count": len(msp),
            "render_font_fallbacks": render_font_fallbacks,
            "title_block": {
                "university": title_data["institucion"]["universidad"],
                "student": title_data["academico"]["estudiante"],
                "teacher": title_data["academico"]["docente"],
                "owner": title_data["proyecto"]["propietario"],
                "site": "CARACOTO, SAN ROMAN, PUNO",
            },
        })
    if not args.skip_render:
        all_pdf_paths = [output / f"{sheet_stem(sheet)}.pdf" for sheet in all_sheets]
        missing = [path.name for path in all_pdf_paths if not path.is_file()]
        if missing and not args.sheet:
            raise SystemExit(f"Faltan PDF vectoriales para componer el juego: {', '.join(missing)}")
        if not missing:
            combined = output / "planos-electricos-grifo-unap-aquiles.pdf"
            temporary = output / ".planos-electricos-grifo-unap-aquiles.tmp.pdf"
            if temporary.exists():
                temporary.unlink()
            from pypdf import PdfWriter

            writer = PdfWriter()
            for path in all_pdf_paths:
                writer.append(str(path))
            with temporary.open("wb") as stream:
                writer.write(stream)
            writer.close()
            temporary.replace(combined)
            manifest["combined_pdf"] = str(combined.relative_to(root))
        else:
            manifest["combined_pdf"] = None
            manifest["missing_for_combined_pdf"] = missing
        manifest["pdf_quality"] = "vectorial_directo_A1; PNG_solo_vista_previa_220_dpi"
    if args.sheet and previous_manifest:
        records = {record["code"]: record for record in previous_manifest.get("sheets", [])}
        records.update({record["code"]: record for record in manifest["sheets"]})
        manifest["sheets"] = [records[sheet["codigo"]] for sheet in all_sheets if sheet["codigo"] in records]
    manifest["architecture_entities_imported_per_sheet"] = (
        architecture_count
        if architecture_count is not None
        else (previous_manifest or {}).get("architecture_entities_imported_per_sheet")
    )
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "sheets": len(sheets), "output": str(output)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Genera las laminas electricas A1 del anteproyecto del grifo de Renzo.

La arquitectura procede de ``arquitectura/datos/layout-grifo.json`` (coordenadas
locales en metros, origen en la esquina suroeste del lote a ejecutar). Las
superposiciones electricas son una propuesta academica y todos los rotulos se
componen desde ``datos/rotulo-planos.yaml``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from datetime import date
from pathlib import Path
from typing import Any

import ezdxf
import yaml
from ezdxf.addons.drawing import matplotlib as ezdxf_matplotlib
from ezdxf.enums import TextEntityAlignment

PAGE_W = 84.1
PAGE_H = 59.4
FRAME = (0.5, 0.5, 83.6, 58.9)
TITLE = (54.2, 0.8, 83.6, 14.0)

ARCH = (-3.0, 0.0, 31.0, 23.0)
ARCH_SCALE = 1.4
ARCH_OFFSET_X = 4.0
ARCH_OFFSET_Y = 16.0

ARQ_REAL = "arquitectura/datos/arquitectura-dwg.json"


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
    doc.header["$INSUNITS"] = 6
    doc.header["$LUNITS"] = 2
    doc.header["$LUPREC"] = 3
    # Jerarquia de espesores para A1 (1/100 mm):
    # marco/rotulo = grueso, arquitectura = medio-grueso, circuitos = medio,
    # canalizaciones/tierra = medio, tableros/equipos = medio, textos/tablas = fino.
    layers = (
        ("MARCO", 7, 50, "CONTINUOUS"),
        ("ROTULO", 5, 35, "CONTINUOUS"),
        ("ROTULO_TEXTO", 7, 20, "CONTINUOUS"),
        ("ADVERTENCIA", 1, 25, "CONTINUOUS"),
        ("IE_ALUMBRADO", 2, 30, "CONTINUOUS"),
        ("IE_FUERZA", 1, 35, "CONTINUOUS"),
        ("IE_EMERGENCIA", 6, 35, "CONTINUOUS"),
        ("IE_CANALIZACION", 4, 30, "DASHED"),
        ("IE_TIERRA", 3, 40, "CONTINUOUS"),
        ("IE_RAYO", 30, 35, "CONTINUOUS"),
        ("IE_ZONA_1", 1, 40, "DASHED"),
        ("IE_ZONA_2", 30, 30, "DASHED"),
        ("IE_TABLA", 7, 18, "CONTINUOUS"),
        ("IE_TEXTO", 7, 20, "CONTINUOUS"),
        ("ARQ_REFERENCIA", 8, 40, "CONTINUOUS"),
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
    text_left(msp, "ANTEPROYECTO ACADEMICO - INSTALACIONES ELECTRICAS", 0.9, 58.05, 0.28, "ADVERTENCIA")
    text_left(msp, "NO CONSTRUIR SIN FACTIBILIDAD, VERIFICACION DE CAMPO Y REVISION PROFESIONAL", 34.0, 58.05, 0.25, "ADVERTENCIA")


def local_to_page(x: float, y: float) -> tuple[float, float]:
    """Convierte coordenadas locales del grifo (metros) al espacio A1."""
    return (ARCH_OFFSET_X + (x - ARCH[0]) * ARCH_SCALE, ARCH_OFFSET_Y + (y - ARCH[1]) * ARCH_SCALE)


def add_architecture(doc: ezdxf.document.Drawing, architecture: dict[str, Any]) -> None:
    """Dibuja la arquitectura del grifo desde el layout canonico con jerarquia
    de espesores: lote y edificio en trazo grueso, ambientes en trazo medio.

    Prefiere los muros y lote extraidos del DWG original
    (``arquitectura-dwg.json``) para reflejar la geometria real; si no estan
    disponibles, cae al layout aproximado.
    """
    msp = doc.modelspace()
    layer = "ARQ_REFERENCIA"

    root = repository_root() / "proyectos" / "renzo-industrial"
    real_path = root / ARQ_REAL
    real_entities: list[dict[str, Any]] = []
    if real_path.exists():
        real_entities = json.loads(real_path.read_text(encoding="utf-8"))

    def draw_real_walls() -> None:
        for ent in real_entities:
            if ent.get("type") != "seg" or ent.get("layer") not in ("muro", "0"):
                continue
            a, b = ent["pts"]
            lw = 40 if ent["layer"] == "muro" else 25
            msp.add_line(local_to_page(*a), local_to_page(*b), dxfattribs={"layer": layer, "lineweight": lw})

    def draw_lote_real() -> bool:
        # Reconstruye el poligono del lote a ejecutar desde sus segmentos.
        segs = [ent["pts"] for ent in real_entities if ent.get("type") == "seg" and ent.get("layer") == "LOTE A EJECUTAR"]
        if len(segs) < 4:
            return False
        # Cadena desde el vertice mas al sur.
        vertices: list[tuple[float, float]] = []
        remaining = list(segs)
        start = min((s[0] for s in remaining), key=lambda p: (p[1], p[0]))
        current = start
        vertices.append(current)
        for _ in range(len(segs) + 2):
            match = None
            for s in remaining:
                if math.dist(s[0], current) < 0.1:
                    match, nxt = s[0], s[1]
                    break
                if math.dist(s[1], current) < 0.1:
                    match, nxt = s[1], s[0]
                    break
            if match is None:
                break
            remaining.remove(next(s for s in remaining if s in (s for s in remaining)))
            remaining = [s for s in remaining if math.dist(s[0], current) >= 0.1 and math.dist(s[1], current) >= 0.1]
            current = nxt
            if math.dist(current, start) < 0.1:
                break
            vertices.append(current)
        if len(vertices) < 4:
            return False
        msp.add_lwpolyline([local_to_page(x, y) for x, y in vertices], dxfattribs={"layer": layer, "lineweight": 50}, close=True)
        return True

    if real_entities:
        draw_real_walls()
        draw_lote_real()
        for ent in real_entities:
            if ent.get("type") == "text" and ent.get("layer") in ("TEXT-AMB", "TEXTO-AMB"):
                px, py = ent["pos"]
                text_center(msp, ent["text"], *local_to_page(px, py + 0.25), 0.22, layer)
    else:
        lote = architecture["lote_a_ejecutar"]["poligono_local"]
        msp.add_lwpolyline([local_to_page(x, y) for x, y in lote], dxfattribs={"layer": layer, "lineweight": 50}, close=True)

        bbox = architecture["edificio"]["bbox_local"]
        (x0, y0, x1, y1) = bbox
        msp.add_lwpolyline(
            [local_to_page(x0, y0), local_to_page(x1, y0), local_to_page(x1, y1), local_to_page(x0, y1)],
            dxfattribs={"layer": layer, "lineweight": 40}, close=True,
        )

        for ambiente in architecture["ambientes"]:
            cx, cy = local_to_page(*ambiente["centro_local"])
            rect(msp, cx - 2.0, cy - 1.5, cx + 2.0, cy + 1.5, layer, 8)
            text_center(msp, ambiente["nombre"], cx, cy, 0.20, layer)

    for tanque in architecture["tanques"]:
        cx, cy = local_to_page(*tanque["pos_local"])
        msp.add_circle((cx, cy), 0.45, dxfattribs={"layer": layer, "lineweight": 35})
        text_left(msp, f"{tanque['numero']} {tanque['combustible']}", cx + 0.5, cy, 0.18, layer)

    for punto in architecture["dispensadores_y_surtidores"]["posiciones_local"]:
        cx, cy = local_to_page(*punto)
        rect(msp, cx - 0.4, cy - 0.4, cx + 0.4, cy + 0.4, layer, 8)
        text_center(msp, "SURT", cx, cy - 0.55, 0.16, layer)


def add_title_block(msp: ezdxf.layouts.BaseLayout, title_data: dict[str, Any], sheet: dict[str, str], number: int, total: int, scale: str) -> None:
    x0, y0, x1, y1 = TITLE
    msp.add_wipeout([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], dxfattribs={"layer": "ROTULO"})
    rect(msp, x0, y0, x1, y1, "ROTULO", 5)
    for y in (12.85, 11.65, 9.95, 8.55, 6.95, 5.35, 3.75, 2.15):
        msp.add_line((x0, y), (x1, y), dxfattribs={"layer": "ROTULO"})
    for x in (61.7, 69.5, 75.0, 79.2):
        msp.add_line((x, y0), (x, 3.75), dxfattribs={"layer": "ROTULO"})
    msp.add_line((68.4, 3.75), (68.4, 6.95), dxfattribs={"layer": "ROTULO"})

    inst = title_data["institucion"]
    acad = title_data["academico"]
    project = title_data["proyecto"]
    resp = title_data["responsabilidades"]
    text_center(msp, inst["universidad"], (x0 + x1) / 2, 13.55, 0.50, "ROTULO_TEXTO")
    text_center(msp, inst["facultad"], (x0 + x1) / 2, 13.15, 0.24, "ROTULO_TEXTO")
    text_center(msp, inst["escuela"], (x0 + x1) / 2, 12.55, 0.28, "ROTULO_TEXTO")
    text_center(msp, "PROYECTO: INSTALACIONES ELECTRICAS EN BAJA TENSION", (x0 + x1) / 2, 12.20, 0.25, "ROTULO_TEXTO")
    text_center(msp, "ESTACION DE SERVICIO (GRIFO) DE COMBUSTIBLES LIQUIDOS - ANTEPROYECTO NUEVO", (x0 + x1) / 2, 11.25, 0.30, "ROTULO_TEXTO")
    text_center(msp, "DIESEL B5-S50 / GASOHOL REGULAR / GASOHOL PREMIUM - SIN GLP NI GNV", (x0 + x1) / 2, 10.72, 0.24, "ROTULO_TEXTO")
    text_center(msp, sheet["titulo"], (x0 + x1) / 2, 9.28, 0.40, "ROTULO_TEXTO")

    text_left(msp, f"PROPIETARIO: {project['propietario']}", x0 + 0.25, 8.08, 0.28, "ROTULO_TEXTO")
    text_left(msp, "DISTRITO/PROV.: SAN ROMAN - DEP.: PUNO", x0 + 0.25, 7.63, 0.20, "ROTULO_TEXTO")
    text_left(msp, "UBICACION: PREDIO RUSTICO REUMITA PARCELA B-8 Y B-9, CARRETERA JULIACA-PUNO", x0 + 0.25, 7.19, 0.19, "ROTULO_TEXTO")

    text_left(msp, f"CURSO: {acad['curso']}", x0 + 0.25, 6.05, 0.28, "ROTULO_TEXTO")
    text_left(msp, f"DOCENTE: {acad['docente']}", x0 + 0.25, 5.58, 0.28, "ROTULO_TEXTO")
    text_left(msp, f"DISENADO Y DIBUJADO: {resp['disenado_por']}", 68.7, 6.05, 0.25, "ROTULO_TEXTO")
    text_left(msp, "REVISION DOCENTE: CAMPO ACADEMICO - SIN FIRMA NI APROBACION AFIRMADA", 68.7, 5.58, 0.19, "ROTULO_TEXTO")

    text_left(msp, "MODALIDAD: INDIVIDUAL", x0 + 0.25, 4.78, 0.25, "ROTULO_TEXTO")
    text_left(msp, f"CODIGO EST.: {acad['codigo_estudiante']}", x0 + 0.25, 4.30, 0.24, "ROTULO_TEXTO")
    text_left(msp, f"SEMESTRE: {acad['semestre_academico']}", 68.7, 4.78, 0.24, "ROTULO_TEXTO")
    text_left(msp, "SEDE: PUNO - PERU", 68.7, 4.30, 0.24, "ROTULO_TEXTO")

    labels = (
        (x0 + 0.25, "LAMINA", sheet["codigo"]),
        (61.95, "ESCALA", scale),
        (69.75, "FECHA", title_data["presentacion"]["fecha_base"]),
        (75.25, "REV.", "R00"),
        (79.45, "HOJA", f"{number:02d}/{total:02d}"),
    )
    for x, label, value in labels:
        text_left(msp, label, x, 3.28, 0.19, "ROTULO_TEXTO")
        text_left(msp, value, x, 2.63, 0.42 if label == "LAMINA" else 0.29, "ROTULO_TEXTO")

    text_center(msp, "UNAP - PUNO | ANTEPROYECTO SUJETO A VERIFICACION DE CAMPO, FACTIBILIDAD Y REVISION PROFESIONAL", (x0 + x1) / 2, 1.62, 0.20, "ADVERTENCIA")
    text_center(msp, "NO SE CONSIGNA CIP, SELLO NI FIRMA POR NO EXISTIR ESOS DATOS EN LAS FUENTES", (x0 + x1) / 2, 1.12, 0.19, "ADVERTENCIA")


def add_luminaire(msp: ezdxf.layouts.BaseLayout, point: tuple[float, float], label: str = "", emergency: bool = False) -> None:
    x, y = point
    layer = "IE_EMERGENCIA" if emergency else "IE_ALUMBRADO"
    msp.add_circle((x, y), 0.22, dxfattribs={"layer": layer, "lineweight": 35})
    msp.add_line((x - 0.15, y - 0.15), (x + 0.15, y + 0.15), dxfattribs={"layer": layer, "lineweight": 25})
    msp.add_line((x - 0.15, y + 0.15), (x + 0.15, y - 0.15), dxfattribs={"layer": layer, "lineweight": 25})
    if emergency:
        text_left(msp, "E", x, y + 0.35, 0.14, layer)
    if label:
        text_left(msp, label, x + 0.28, y + 0.15, 0.18, layer)


def add_outlet(msp: ezdxf.layouts.BaseLayout, point: tuple[float, float], label: str = "TC") -> None:
    x, y = point
    # Simbolo IEC 60617 de tomacorriente (semicirculo sobre soporte vertical).
    msp.add_line((x, y - 0.14), (x, y + 0.14), dxfattribs={"layer": "IE_FUERZA", "lineweight": 30})
    msp.add_arc(center=(x, y), radius=0.20, start_angle=0.0, end_angle=180.0, dxfattribs={"layer": "IE_FUERZA", "lineweight": 30})
    msp.add_line((x - 0.20, y), (x + 0.20, y), dxfattribs={"layer": "IE_FUERZA", "lineweight": 30})
    text_left(msp, label, x + 0.28, y + 0.10, 0.17, "IE_FUERZA")


def add_panel(msp: ezdxf.layouts.BaseLayout, point: tuple[float, float], label: str, layer: str = "IE_FUERZA") -> None:
    x, y = point
    rect(msp, x - 0.32, y - 0.25, x + 0.32, y + 0.25, layer, 1)
    text_center(msp, label, x, y, 0.18, layer)


def add_route(msp: ezdxf.layouts.BaseLayout, points: list[tuple[float, float]], layer: str = "IE_CANALIZACION") -> None:
    msp.add_lwpolyline([local_to_page(x, y) for x, y in points], dxfattribs={"layer": layer, "linetype": "DASHED"})


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


def add_north_arrow(msp: ezdxf.layouts.BaseLayout, cx: float = 49.5, cy: float = 54.0) -> None:
    msp.add_lwpolyline([(cx, cy - 1.4), (cx - 0.5, cy), (cx, cy + 1.4), (cx + 0.5, cy)], dxfattribs={"layer": "IE_TEXTO", "color": 7}, close=True)
    msp.add_lwpolyline([(cx, cy + 0.15), (cx - 0.35, cy - 0.55), (cx + 0.35, cy - 0.55)], dxfattribs={"layer": "IE_TEXTO", "color": 7}, close=True)
    text_center(msp, "N", cx, cy + 1.8, 0.55, "IE_TEXTO", 7)


def add_scale_bar(msp: ezdxf.layouts.BaseLayout, cx: float = 30.0, cy: float = 14.6, meters: float = 10.0, length: float = 14.0) -> None:
    """Barra de escala grafica: `length` cm en lamina representan `meters` reales."""
    segment = length / 4.0
    for index in range(4):
        x0 = cx - length / 2 + index * segment
        y_top = cy + 0.35
        if index % 2 == 0:
            msp.add_lwpolyline(
                [(x0, cy - 0.35), (x0 + segment, cy - 0.35), (x0 + segment, y_top), (x0, y_top)],
                dxfattribs={"layer": "IE_TABLA", "color": 30, "lineweight": 60}, close=True,
            )
        else:
            msp.add_lwpolyline(
                [(x0, cy - 0.35), (x0 + segment, cy - 0.35), (x0 + segment, y_top), (x0, y_top)],
                dxfattribs={"layer": "IE_TABLA", "color": 7, "lineweight": 18}, close=True,
            )
    text_center(msp, f"0   2   4   6   8   {meters:.0f} m", cx, cy - 0.85, 0.22, "IE_TEXTO")
    text_center(msp, f"ESCALA GRAFICA: {length / meters:.2f} cm = {meters:.0f} m", cx, cy + 0.9, 0.22, "IE_TEXTO")


def sheet_ie01(doc: ezdxf.document.Drawing, architecture: dict[str, Any], calc: dict[str, Any]) -> None:
    msp = doc.modelspace()
    add_architecture(doc, architecture)
    for x in (6.0, 9.0, 12.0, 15.0, 18.0, 21.0, 24.0, 27.0, 30.0):
        add_luminaire(msp, local_to_page(x, 12.0), f"L{x:02.0f}", emergency=x in (15.0, 24.0))
    tde = local_to_page(9.0, 6.0)
    tdf = local_to_page(10.0, 5.0)
    add_panel(msp, tde, "TDE", "IE_EMERGENCIA")
    add_panel(msp, tdf, "TDF")
    for x in (6.0, 12.0, 18.0, 24.0, 30.0):
        add_route(msp, [(9.0, 6.0), (9.0, 8.0), (x, 8.0), (x, 12.0)])
    add_north_arrow(msp)
    add_scale_bar(msp)
    add_legend(msp, "IE-01 | LEYENDA Y CRITERIOS", [
        ("X", "Luminaria LED; magenta = circuito de emergencia"),
        ("TDE", "Tablero de emergencia mediante ATS"),
        ("TDF", "Tablero de fuerza normal"),
        ("---", "Canalizacion enterrada/techo segun tramo; verificar recorrido"),
        ("CNE", "dV ramal <= 2.5 % y total <= 4 %; PE en todo circuito"),
    ])


def sheet_ie02(doc: ezdxf.document.Drawing, architecture: dict[str, Any], calc: dict[str, Any]) -> None:
    msp = doc.modelspace()
    add_architecture(doc, architecture)
    td1 = local_to_page(9.0, 5.0)
    add_panel(msp, td1, "TD-A1")
    for x, y in ((4.0, 4.0), (8.0, 4.0), (13.0, 3.0), (16.0, 2.0), (18.0, 2.0), (22.0, 3.0)):
        add_luminaire(msp, local_to_page(x, y))
    for x, y in ((5.0, 2.0), (10.0, 2.0), (12.0, 4.0), (20.0, 2.0), (24.0, 3.0)):
        add_outlet(msp, local_to_page(x, y))
    for x, y in ((4.0, 4.0), (8.0, 4.0), (13.0, 3.0), (16.0, 2.0), (18.0, 2.0), (22.0, 3.0), (5.0, 2.0), (10.0, 2.0), (12.0, 4.0), (20.0, 2.0), (24.0, 3.0)):
        add_route(msp, [(9.0, 5.0), (9.0, 6.0), (x, 6.0), (x, y)])
    add_north_arrow(msp)
    add_scale_bar(msp)
    add_legend(msp, "IE-02 | LEYENDA", [
        ("X", "Luminaria LED interior"),
        ("TC", "Tomacorriente"),
        ("TD-A1", "Tablero de distribucion edificio"),
        ("CNE", "Tomacorrientes con diferencial 30 mA"),
    ])


def sheet_ie03(doc: ezdxf.document.Drawing, architecture: dict[str, Any], calc: dict[str, Any]) -> None:
    msp = doc.modelspace()
    add_architecture(doc, architecture)
    tde = local_to_page(9.0, 6.0)
    tdf = local_to_page(10.0, 5.0)
    add_panel(msp, tde, "TDE", "IE_EMERGENCIA")
    add_panel(msp, tdf, "TDF")
    for tanque in architecture["tanques"]:
        add_panel(msp, local_to_page(*tanque["pos_local"]), tanque["numero"], "IE_EMERGENCIA")
    for punto in architecture["dispensadores_y_surtidores"]["posiciones_local"]:
        add_panel(msp, local_to_page(*punto), "SURT", "IE_FUERZA")
    add_panel(msp, local_to_page(22.0, 2.0), "C-AIRE", "IE_FUERZA")
    add_panel(msp, local_to_page(24.0, 2.0), "B-AGUA", "IE_FUERZA")
    add_panel(msp, local_to_page(26.0, 2.0), "B-FOSA", "IE_FUERZA")
    for tanque in architecture["tanques"]:
        add_route(msp, [(9.0, 6.0), (12.0, 6.0), tanque["pos_local"]])
    for punto in architecture["dispensadores_y_surtidores"]["posiciones_local"]:
        add_route(msp, [(10.0, 5.0), (12.0, 7.0), punto])
    add_north_arrow(msp)
    add_scale_bar(msp)
    add_legend(msp, "IE-03 | LEYENDA", [
        ("STP", "Bomba sumergible de tanque (emergencia)"),
        ("SURT", "Surtidor / cabeza electronica"),
        ("C-AIRE", "Compresor de aire"),
        ("B-AGUA / B-FOSA", "Bombas de agua y efluentes"),
        ("NOTA", "Paro de emergencia y pulsador segun normativa"),
    ])


def sheet_ie04(doc: ezdxf.document.Drawing, architecture: dict[str, Any], calc: dict[str, Any]) -> None:
    msp = doc.modelspace()
    add_architecture(doc, architecture)
    for punto in architecture["equipos_electricos_observados"]:
        if "pos_local" not in punto:
            continue
        if punto["tipo"] in ("pozo_tierra", "pozo_tierra_secundario"):
            cx, cy = local_to_page(*punto["pos_local"])
            msp.add_circle((cx, cy), 0.35, dxfattribs={"layer": "IE_TIERRA"})
            text_left(msp, punto["tipo"].replace("_", " ").upper(), cx + 0.4, cy, 0.17, "IE_TIERRA")
        if punto["tipo"] == "pararrayo":
            cx, cy = local_to_page(*punto["pos_local"])
            msp.add_circle((cx, cy), 0.4, dxfattribs={"layer": "IE_RAYO"})
            msp.add_circle((cx, cy), 0.5, dxfattribs={"layer": "IE_RAYO"})
            text_left(msp, "PARARRAYO h=12 m", cx + 0.6, cy, 0.18, "IE_RAYO")
    msp.add_lwpolyline([
        local_to_page(6.0, 5.0), local_to_page(9.0, 6.0), local_to_page(10.0, 5.0),
        local_to_page(12.0, 7.0), local_to_page(14.0, 8.0), local_to_page(17.0, 12.0),
        local_to_page(21.0, 8.0),
    ], dxfattribs={"layer": "IE_TIERRA"})
    add_north_arrow(msp)
    add_scale_bar(msp)
    add_legend(msp, "IE-04 | PUESTA A TIERRA Y RAYO", [
        ("PAT", "Pozo de puesta a tierra"),
        ("=O", "Pararrayo con radio de proteccion 20 m (h=12 m)"),
        ("----", "Malla de tierra / equipotencialidad"),
        ("CNE", "Resistencia de PAT <= 10 ohm y <= 25 ohm para rayo"),
    ])


def sheet_ie05(doc: ezdxf.document.Drawing, architecture: dict[str, Any], calc: dict[str, Any]) -> None:
    msp = doc.modelspace()
    s = calc["summary"]
    y = 55.0
    text_center(msp, "DIAGRAMA UNIFILAR GENERAL 380/220 V - 3F+N+PE", 40.0, y, 0.55, "IE_TEXTO")
    y -= 2.2
    rows = [
        ("SUMINISTRO", "Electro Puno (por confirmar), punto de entrega por confirmar"),
        ("INTERRUPTOR", f"Principal {s['main_breaker_a']:.0f} A, 4P, Icu >= 25 kA"),
        ("TABLERO TG", f"380/220 V - demanda con reserva {s['service_design_kva_with_reserve']:.2f} kVA"),
        ("TDE", "Emergencia (ATS) - STP, dispensadores, control, POS"),
        ("TDF", "Fuerza normal - compresor, bombas, alumbrado exterior"),
        ("TD-A1", "Edificio administrativo - alumbrado y tomacorrientes"),
    ]
    x = 6.0
    yy = y - 1.0
    for label, description in rows:
        rect(msp, x, yy - 0.8, x + 20.0, yy, "IE_TABLA")
        text_left(msp, label, x + 0.4, yy - 0.55, 0.28, "IE_TEXTO")
        text_left(msp, description, x + 5.5, yy - 0.55, 0.24, "IE_TEXTO")
        yy -= 1.2
    text_left(msp, "Cargas criticas del grifo se mantienen en TDE mediante grupo electrogeno y UPS.", 6.0, yy - 1.2, 0.24, "IE_TEXTO")
    text_left(msp, "Ver cuadro de cargas en build/renzo-industrial/calculos/cuadro-cargas.csv.", 6.0, yy - 1.8, 0.24, "IE_TEXTO")


def sheet_ie06(doc: ezdxf.document.Drawing, architecture: dict[str, Any], calc: dict[str, Any]) -> None:
    msp = doc.modelspace()
    add_architecture(doc, architecture)
    for tanque in architecture["tanques"]:
        cx, cy = local_to_page(*tanque["pos_local"])
        msp.add_circle((cx, cy), 2.2, dxfattribs={"layer": "IE_ZONA_1", "linetype": "DASHED"})
    for punto in architecture["dispensadores_y_surtidores"]["posiciones_local"]:
        cx, cy = local_to_page(*punto)
        msp.add_circle((cx, cy), 3.5, dxfattribs={"layer": "IE_ZONA_2", "linetype": "DASHED"})
    add_north_arrow(msp)
    add_scale_bar(msp)
    add_legend(msp, "IE-06 | CLASIFICACION DE AREAS", [
        ("Zona 1", "Area peligrosa alrededor de tanques y venteos"),
        ("Zona 2", "Area de despacho alrededor de surtidores"),
        ("NOTA", "Limites propuesta academica; trazado segun CNE-U cap. 6 y revision competente"),
        ("CNE", "Equipo electrico de areas clasificadas con proteccion apropiada"),
    ])


SHEET_BUILDERS = {
    "IE-01": sheet_ie01,
    "IE-02": sheet_ie02,
    "IE-03": sheet_ie03,
    "IE-04": sheet_ie04,
    "IE-05": sheet_ie05,
    "IE-06": sheet_ie06,
}


def sheet_stem(sheet: dict[str, str]) -> str:
    return f"IE-{sheet['codigo'].split('-')[1]}_{sheet['titulo'].split()[0]}_{sheet['titulo'].split()[1]}"


def render(doc: ezdxf.document.Drawing, png_path: Path, pdf_path: Path) -> None:
    def render_filter(entity: ezdxf.entities.DXFGraphic) -> bool:
        return entity.dxftype() not in {"HATCH", "SOLID", "TRACE", "IMAGE"}

    from ezdxf.addons.drawing.config import Configuration

    config = Configuration(lineweight_scaling=2.0, min_lineweight=0.18)
    ezdxf_matplotlib.qsave(
        doc.modelspace(),
        png_path,
        bg="#FFFFFF",
        fg="#111111",
        dpi=220,
        size_inches=(16.54, 11.69),
        filter_func=render_filter,
        config=config,
    )
    ezdxf_matplotlib.qsave(
        doc.modelspace(),
        pdf_path,
        bg="#FFFFFF",
        fg="#111111",
        size_inches=(33.11, 23.39),
        filter_func=render_filter,
        config=config,
    )


def main() -> int:
    root = repository_root()
    project = root / "proyectos/renzo-industrial"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=root / "build/renzo-industrial/cad/planos")
    parser.add_argument("--skip-render", action="store_true")
    parser.add_argument("--sheet", action="append", choices=tuple(SHEET_BUILDERS))
    args = parser.parse_args()

    title_data = load_yaml(project / "datos/rotulo-planos.yaml")
    architecture = load_json(project / "arquitectura/datos/layout-grifo.json")
    calculations = load_json(root / "build/renzo-industrial/calculos/resumen-calculos.json")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    if calculations["status"] != "PASS":
        raise SystemExit("El calculo electrico no esta en estado PASS")

    manifest_path = output / "manifest.json"
    previous_manifest = load_json(manifest_path) if manifest_path.is_file() else None
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "generated_on": date.today().isoformat(),
        "title_block_source": "proyectos/renzo-industrial/datos/rotulo-planos.yaml",
        "architecture_source": "proyectos/renzo-industrial/arquitectura/datos/layout-grifo.json",
        "calculation_source_sha256": calculations["source_sha256"],
        "sheets": [],
    }
    all_sheets = title_data["laminas_previstas"]
    sheets = [sheet for sheet in all_sheets if not args.sheet or sheet["codigo"] in args.sheet]
    for sheet in sheets:
        number = next(index for index, item in enumerate(all_sheets, 1) if item["codigo"] == sheet["codigo"])
        code = sheet["codigo"]
        print(f"Generando {code}: {sheet['titulo']}", flush=True)
        doc = new_document()
        msp = doc.modelspace()
        add_frame(msp)
        SHEET_BUILDERS[code](doc, architecture, calculations)
        scale = "1:100 / IND." if code != "IE-05" else "S/E"
        add_title_block(msp, title_data, sheet, number, len(all_sheets), scale)
        stem = sheet_stem(sheet)
        dxf_path = output / f"{stem}.dxf"
        png_path = output / f"{stem}.png"
        pdf_path = output / f"{stem}.pdf"
        doc.saveas(dxf_path)
        if not args.skip_render:
            render(doc, png_path, pdf_path)
        manifest["sheets"].append({
            "code": code,
            "title": sheet["titulo"],
            "dxf": str(dxf_path.relative_to(root)),
            "png": None if args.skip_render else str(png_path.relative_to(root)),
            "pdf": None if args.skip_render else str(pdf_path.relative_to(root)),
            "entity_count": len(msp),
            "title_block": {
                "university": title_data["institucion"]["universidad"],
                "student": title_data["academico"]["estudiante"],
                "teacher": title_data["academico"]["docente"],
                "owner": title_data["proyecto"]["propietario"],
            },
        })
    if not args.skip_render:
        all_pdf_paths = [output / f"{sheet_stem(sheet)}.pdf" for sheet in all_sheets]
        missing = [path.name for path in all_pdf_paths if not path.is_file()]
        if missing:
            raise SystemExit(f"Faltan PDF vectoriales para componer el juego: {', '.join(missing)}")
        combined = output / "planos-electricos-grifo-renzo.pdf"
        temporary = output / ".planos-electricos-grifo-renzo.tmp.pdf"
        if temporary.exists():
            temporary.unlink()
        subprocess.run(["pdfunite", *(str(path) for path in all_pdf_paths), str(temporary)], check=True)
        temporary.replace(combined)
        manifest["combined_pdf"] = str(combined.relative_to(root))
        manifest["pdf_quality"] = "vectorial_directo_A1; PNG_solo_vista_previa_220_dpi"
    if args.sheet and previous_manifest:
        records = {record["code"]: record for record in previous_manifest.get("sheets", [])}
        records.update({record["code"]: record for record in manifest["sheets"]})
        manifest["sheets"] = [records[sheet["codigo"]] for sheet in all_sheets if sheet["codigo"] in records]
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "sheets": len(sheets), "output": str(output)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

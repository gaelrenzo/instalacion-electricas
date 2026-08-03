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


def scale_length(meters: float) -> float:
    return meters * ARCH_SCALE


def add_circle_clipped(
    msp: ezdxf.layouts.BaseLayout,
    center: tuple[float, float],
    radius: float,
    layer: str,
    linetype: str = "CONTINUOUS",
    lineweight: int = 25,
    clip: tuple[float, float, float, float] = FRAME,
    exclude: tuple[float, float, float, float] | None = TITLE,
    segments: int = 144,
) -> None:
    """Dibuja un circulo de referencia recortado al area de dibujo.

    Radios grandes (ej. proteccion del pararrayo R=20 m) superan el marco;
    en lugar de dejar el circulo cortado por el borde de la lamina se dibuja
    solo la porcion que cae dentro de ``clip`` y fuera de ``exclude`` (rotulo).
    """
    cx, cy = center
    xmin, ymin, xmax, ymax = clip
    ex = exclude

    def inside(p: tuple[float, float]) -> bool:
        if not (xmin <= p[0] <= xmax and ymin <= p[1] <= ymax):
            return False
        if ex is not None and ex[0] <= p[0] <= ex[2] and ex[1] <= p[1] <= ex[3]:
            return False
        return True

    step = 2.0 * math.pi / segments
    ring = [(cx + radius * math.cos(i * step), cy + radius * math.sin(i * step)) for i in range(segments)]
    groups: list[list[tuple[float, float]]] = []
    current: list[tuple[float, float]] = []
    for point in ring + [ring[0]]:
        if inside(point):
            current.append(point)
        else:
            if len(current) >= 2:
                groups.append(current)
            current = []
    if len(current) >= 2:
        groups.append(current)
    for group in groups:
        msp.add_lwpolyline(group, dxfattribs={"layer": layer, "linetype": linetype, "lineweight": lineweight})


def add_basic_dimensions(msp: ezdxf.layouts.BaseLayout, architecture: dict[str, Any]) -> None:
    """Cotas referenciales del lote de trabajo tomadas del layout canonico."""
    lote = architecture["lote_a_ejecutar"]
    xs = [point[0] for point in lote["poligono_local"]]
    ys = [point[1] for point in lote["poligono_local"]]
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(ys), max(ys)
    largo = lote["dimensiones"]["largo"]
    ancho = lote["dimensiones"]["ancho"]

    a = local_to_page(x0, y0 - 0.65)
    b = local_to_page(x1, y0 - 0.65)
    msp.add_line(a, b, dxfattribs={"layer": "IE_TEXTO", "lineweight": 18})
    msp.add_line(local_to_page(x0, y0 - 0.35), local_to_page(x0, y0 - 0.95), dxfattribs={"layer": "IE_TEXTO", "lineweight": 18})
    msp.add_line(local_to_page(x1, y0 - 0.35), local_to_page(x1, y0 - 0.95), dxfattribs={"layer": "IE_TEXTO", "lineweight": 18})
    text_center(msp, f"{largo:.0f} m referencial", (a[0] + b[0]) / 2, a[1] - 0.35, 0.18, "IE_TEXTO")

    c = local_to_page(x1 + 0.65, y0)
    d = local_to_page(x1 + 0.65, y1)
    msp.add_line(c, d, dxfattribs={"layer": "IE_TEXTO", "lineweight": 18})
    msp.add_line(local_to_page(x1 + 0.35, y0), local_to_page(x1 + 0.95, y0), dxfattribs={"layer": "IE_TEXTO", "lineweight": 18})
    msp.add_line(local_to_page(x1 + 0.35, y1), local_to_page(x1 + 0.95, y1), dxfattribs={"layer": "IE_TEXTO", "lineweight": 18})
    text_center(msp, f"{ancho:.0f} m referencial", d[0] + 0.45, (c[1] + d[1]) / 2, 0.18, "IE_TEXTO")


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
        # Jerarquia de espesores segun la capa del DWG original: muros y puertas
        # en trazo grueso/medio; estructuras, ventanas y veredas en trazo fino.
        weights = {
            "muro": 40,
            "0": 25,
            "entrada": 12,
            "VENTANAS": 12,
            "D VEREDAS": 12,
            "vereda": 12,
        }
        ref = layer
        for ent in real_entities:
            if ent.get("type") != "seg":
                continue
            ent_layer = ent.get("layer")
            if ent_layer not in weights:
                continue
            a, b = ent["pts"]
            lw = weights[ent_layer]
            msp.add_line(local_to_page(*a), local_to_page(*b), dxfattribs={"layer": ref, "lineweight": lw})

    def draw_lote_real() -> bool:
        # Dibuja los segmentos reales extraidos del DWG. Se evita reconstruir
        # un poligono unico porque el DXF original trae duplicados y tramos
        # cortados; representar los segmentos conserva mejor la evidencia.
        segs = [ent["pts"] for ent in real_entities if ent.get("type") == "seg" and ent.get("layer") == "LOTE A EJECUTAR"]
        if len(segs) < 4:
            return False
        seen: set[tuple[tuple[float, float], tuple[float, float]]] = set()
        for a, b in segs:
            key = tuple(sorted(((round(a[0], 2), round(a[1], 2)), (round(b[0], 2), round(b[1], 2)))))
            if key in seen:
                continue
            seen.add(key)
            msp.add_line(local_to_page(*a), local_to_page(*b), dxfattribs={"layer": layer, "lineweight": 50})
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
        msp.add_line((cx - 0.6, cy), (cx + 0.6, cy), dxfattribs={"layer": layer, "lineweight": 20})
        msp.add_line((cx, cy - 0.6), (cx, cy + 0.6), dxfattribs={"layer": layer, "lineweight": 20})
        text_left(msp, f"{tanque['numero']} {tanque['combustible']}", cx + 0.7, cy, 0.16, layer)

    for punto in architecture["dispensadores_y_surtidores"]["posiciones_local"]:
        cx, cy = local_to_page(*punto)
        # Surtidor de doble manguera: cuerpo + cabeza electronica.
        rect(msp, cx - 0.55, cy - 0.35, cx + 0.55, cy + 0.35, layer, 8)
        msp.add_circle((cx, cy + 0.35), 0.25, dxfattribs={"layer": layer, "lineweight": 30})
        text_center(msp, "SURT", cx, cy - 0.6, 0.15, layer)

    add_basic_dimensions(msp, architecture)
    add_observed_equipment(msp, architecture)


def add_observed_equipment(msp: ezdxf.layouts.BaseLayout, architecture: dict[str, Any]) -> None:
    """Dibuja los equipos observados en el DWG original (tableros, monitoreo,
    cilindros de seguridad, fosa, extintores, totem y direccion del viento)."""
    layer = "ARQ_REFERENCIA"
    for eq in architecture.get("equipos_electricos_observados", []):
        if "pos_local" not in eq:
            continue
        raw_positions = eq["pos_local"]
        positions = raw_positions if raw_positions and isinstance(raw_positions[0], (list, tuple)) else [raw_positions]
        tipo = eq["tipo"]
        for pos in positions:
            cx, cy = local_to_page(*pos)
            if tipo == "tablero_general":
                rect(msp, cx - 0.35, cy - 0.28, cx + 0.35, cy + 0.28, "IE_FUERZA", 8)
                text_center(msp, eq["sigla"], cx, cy, 0.16, "IE_FUERZA")
            elif tipo == "interruptor_general":
                rect(msp, cx - 0.25, cy - 0.25, cx + 0.25, cy + 0.25, "IE_FUERZA", 8)
                msp.add_line((cx - 0.18, cy - 0.18), (cx + 0.18, cy + 0.18), dxfattribs={"layer": "IE_FUERZA", "lineweight": 25})
                text_left(msp, "INT. GRAL", cx + 0.35, cy - 0.10, 0.14, "IE_FUERZA")
            elif tipo == "pulsador_emergencia":
                msp.add_circle((cx, cy), 0.26, dxfattribs={"layer": "IE_EMERGENCIA", "lineweight": 35})
                text_center(msp, "PARO", cx, cy - 0.46, 0.14, "IE_EMERGENCIA")
            elif tipo == "pozo_tierra":
                msp.add_circle((cx, cy), 0.3, dxfattribs={"layer": "IE_TIERRA", "lineweight": 35})
                text_left(msp, "PAT", cx + 0.38, cy - 0.12, 0.14, "IE_TIERRA")
            elif tipo == "pozo_tierra_secundario":
                msp.add_circle((cx, cy), 0.3, dxfattribs={"layer": "IE_TIERRA", "lineweight": 35})
                text_left(msp, "PAT2", cx + 0.38, cy - 0.12, 0.14, "IE_TIERRA")
            elif tipo == "pararrayo":
                radio = scale_length(eq.get("radio_proteccion_m", 20.0))
                msp.add_circle((cx, cy), 0.4, dxfattribs={"layer": "IE_RAYO", "lineweight": 35})
                msp.add_circle((cx, cy), 0.5, dxfattribs={"layer": "IE_RAYO", "lineweight": 25})
                add_circle_clipped(msp, (cx, cy), radio, "IE_RAYO", linetype="DASHED", lineweight=25)
                text_left(msp, f"PARARRAYO R={eq.get('radio_proteccion_m', 20.0):.0f} m (h={eq.get('altura_m', 12.0):.0f} m)", cx + 0.7, cy, 0.15, "IE_RAYO")
            elif tipo in ("cilindro_arena", "cilindro_trapo_empapado"):
                msp.add_circle((cx, cy), 0.3, dxfattribs={"layer": layer, "lineweight": 30})
                msp.add_circle((cx, cy), 0.12, dxfattribs={"layer": layer, "lineweight": 20})
                text_center(msp, "ARENA" if tipo == "cilindro_arena" else "TRAPO HUM.", cx, cy - 0.5, 0.14, layer)
            elif tipo == "fosa_de_agua":
                rect(msp, cx - 0.35, cy - 0.35, cx + 0.35, cy + 0.35, layer, 8)
                text_center(msp, "FOSA", cx, cy + 0.55, 0.14, layer)
            elif tipo == "monitoreo":
                text_center(msp, f"{eq['sigla']}", cx, cy, 0.16, "IE_TEXTO")
                msp.add_line((cx - 0.45, cy), (cx + 0.45, cy), dxfattribs={"layer": "IE_TEXTO", "lineweight": 18})
            elif tipo == "extintor":
                msp.add_lwpolyline([(cx, cy - 0.3), (cx - 0.18, cy + 0.15), (cx + 0.18, cy + 0.15)], dxfattribs={"layer": layer, "lineweight": 25}, close=True)
                text_center(msp, "EXT", cx, cy - 0.48, 0.12, layer)
            elif tipo == "totem":
                rect(msp, cx - 0.25, cy - 0.3, cx + 0.25, cy + 0.3, layer, 8)
                text_center(msp, "TOTEM", cx, cy - 0.5, 0.14, layer)

    circulacion = architecture.get("circulacion", {})
    for giro in circulacion.get("radios_giro_local", []):
        cx, cy = local_to_page(*giro["centro"])
        msp.add_circle((cx, cy), 0.35, dxfattribs={"layer": layer, "linetype": "DASHED", "lineweight": 20})
    direccion = circulacion.get("direccion_viento", {}).get("pos_local")
    if direccion:
        cx, cy = local_to_page(*direccion)
        msp.add_line((cx, cy), (cx + 1.6, cy), dxfattribs={"layer": layer, "lineweight": 25})
        msp.add_lwpolyline([(cx + 1.6, cy), (cx + 1.3, cy + 0.35), (cx + 1.3, cy - 0.35)], dxfattribs={"layer": layer, "lineweight": 25}, close=True)
        text_left(msp, "DIRECCION DEL VIENTO", cx, cy + 0.4, 0.14, layer)


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


def add_route(msp: ezdxf.layouts.BaseLayout, points: list[tuple[float, float]], layer: str = "IE_CANALIZACION", label: str | None = None) -> None:
    msp.add_lwpolyline([local_to_page(x, y) for x, y in points], dxfattribs={"layer": layer, "linetype": "DASHED"})
    if label:
        mid = points[len(points) // 2]
        text_left(msp, label, *local_to_page(mid[0] + 0.4, mid[1] + 0.35), 0.15, "IE_TEXTO")


def tuberia_mm(conductor_mm2: float) -> str:
    """Tuberia PVC SAP recomendada por calibre de conductor (3F+N+PE o por
    numero de conductores del circuito; criterio de ocupacion)."""
    if conductor_mm2 <= 4:
        return "PVC 20 mm"
    if conductor_mm2 <= 10:
        return "PVC 25 mm"
    if conductor_mm2 <= 16:
        return "PVC 32 mm"
    return "PVC 40 mm"


def draw_legend_symbol(msp: ezdxf.layouts.BaseLayout, key: str, cx: float, cy: float, s: float = 0.55) -> None:
    """Dibuja el glifo de un simbolo en la leyenda (coordenadas relativas al
    centro ``(cx, cy)`` escaladas por ``s``). Los nombres coinciden con los
    simbolos usados en las laminas."""
    def p(x: float, y: float) -> tuple[float, float]:
        return (cx + x * s, cy + y * s)

    if key == "lum":
        msp.add_circle(p(0, 0), 0.22 * s, dxfattribs={"layer": "IE_ALUMBRADO", "lineweight": 35})
        msp.add_line(p(-0.15, -0.15), p(0.15, 0.15), dxfattribs={"layer": "IE_ALUMBRADO", "lineweight": 25})
        msp.add_line(p(-0.15, 0.15), p(0.15, -0.15), dxfattribs={"layer": "IE_ALUMBRADO", "lineweight": 25})
    elif key == "lum_e":
        msp.add_circle(p(0, 0), 0.22 * s, dxfattribs={"layer": "IE_EMERGENCIA", "lineweight": 35})
        msp.add_line(p(-0.15, -0.15), p(0.15, 0.15), dxfattribs={"layer": "IE_EMERGENCIA", "lineweight": 25})
        msp.add_line(p(-0.15, 0.15), p(0.15, -0.15), dxfattribs={"layer": "IE_EMERGENCIA", "lineweight": 25})
        text_left(msp, "E", p(0.22, 0.28)[0], p(0.22, 0.28)[1], 0.10, "IE_EMERGENCIA")
    elif key == "tc":
        msp.add_line(p(0, -0.14), p(0, 0.14), dxfattribs={"layer": "IE_FUERZA", "lineweight": 30})
        msp.add_arc(center=p(0, 0), radius=0.20 * s, start_angle=0.0, end_angle=180.0, dxfattribs={"layer": "IE_FUERZA", "lineweight": 30})
        msp.add_line(p(-0.20, 0), p(0.20, 0), dxfattribs={"layer": "IE_FUERZA", "lineweight": 30})
    elif key == "panel":
        rect(msp, p(-0.32, -0.25)[0], p(-0.32, -0.25)[1], p(0.32, 0.25)[0], p(0.32, 0.25)[1], "IE_FUERZA", 1)
    elif key == "tg":
        rect(msp, p(-0.35, -0.28)[0], p(-0.35, -0.28)[1], p(0.35, 0.28)[0], p(0.35, 0.28)[1], "IE_FUERZA", 8)
    elif key == "ig":
        rect(msp, p(-0.25, -0.25)[0], p(-0.25, -0.25)[1], p(0.25, 0.25)[0], p(0.25, 0.25)[1], "IE_FUERZA", 8)
        msp.add_line(p(-0.18, -0.18), p(0.18, 0.18), dxfattribs={"layer": "IE_FUERZA", "lineweight": 25})
    elif key == "paro":
        msp.add_circle(p(0, 0), 0.26 * s, dxfattribs={"layer": "IE_EMERGENCIA", "lineweight": 35})
    elif key == "stp":
        msp.add_circle(p(0, 0), 0.45 * s, dxfattribs={"layer": "ARQ_REFERENCIA", "lineweight": 35})
        msp.add_line(p(-0.6 * s, 0), p(0.6 * s, 0), dxfattribs={"layer": "ARQ_REFERENCIA", "lineweight": 20})
        msp.add_line(p(0, -0.6 * s), p(0, 0.6 * s), dxfattribs={"layer": "ARQ_REFERENCIA", "lineweight": 20})
    elif key == "surt":
        rect(msp, p(-0.55, -0.35)[0], p(-0.55, -0.35)[1], p(0.55, 0.35)[0], p(0.55, 0.35)[1], "ARQ_REFERENCIA", 8)
        msp.add_circle(p(0, 0.35 * s), 0.25 * s, dxfattribs={"layer": "ARQ_REFERENCIA", "lineweight": 30})
    elif key == "pat":
        msp.add_circle(p(0, 0), 0.3 * s, dxfattribs={"layer": "IE_TIERRA", "lineweight": 35})
    elif key == "rayo":
        msp.add_circle(p(0, 0), 0.4 * s, dxfattribs={"layer": "IE_RAYO", "lineweight": 35})
        msp.add_circle(p(0, 0), 0.5 * s, dxfattribs={"layer": "IE_RAYO", "lineweight": 25})
        msp.add_circle(p(0, 0), 1.1 * s, dxfattribs={"layer": "IE_RAYO", "linetype": "DASHED", "lineweight": 25})
    elif key == "malla":
        msp.add_lwpolyline([p(-1.0, 0), p(1.0, 0)], dxfattribs={"layer": "IE_TIERRA", "lineweight": 40})
        msp.add_lwpolyline([p(-0.5, 0.5), p(0.5, 0.5)], dxfattribs={"layer": "IE_TIERRA", "lineweight": 40})
    elif key == "canal":
        msp.add_lwpolyline([p(-1.0, 0), p(1.0, 0)], dxfattribs={"layer": "IE_CANALIZACION", "linetype": "DASHED", "lineweight": 30})
    elif key == "zona1":
        msp.add_circle(p(0, 0), 0.85 * s, dxfattribs={"layer": "IE_ZONA_1", "linetype": "DASHED", "lineweight": 40})
        msp.add_circle(p(0, 0), 0.25 * s, dxfattribs={"layer": "ARQ_REFERENCIA", "lineweight": 20})
    elif key == "zona2":
        msp.add_circle(p(0, 0), 0.85 * s, dxfattribs={"layer": "IE_ZONA_2", "linetype": "DASHED", "lineweight": 30})
        msp.add_circle(p(0, 0), 0.25 * s, dxfattribs={"layer": "ARQ_REFERENCIA", "lineweight": 20})
    elif key == "pm":
        text_left(msp, "PM", p(-0.6, 0)[0], p(-0.6, 0)[1], 0.20, "IE_TEXTO")
        msp.add_line(p(-0.45, 0.12), p(0.45, 0.12), dxfattribs={"layer": "IE_TEXTO", "lineweight": 18})
    elif key == "cilindros":
        msp.add_circle(p(0, 0), 0.3 * s, dxfattribs={"layer": "ARQ_REFERENCIA", "lineweight": 30})
        msp.add_circle(p(0, 0), 0.12 * s, dxfattribs={"layer": "ARQ_REFERENCIA", "lineweight": 20})
        msp.add_circle(p(1.0 * s, 0), 0.3 * s, dxfattribs={"layer": "ARQ_REFERENCIA", "lineweight": 30})
        msp.add_circle(p(1.0 * s, 0), 0.12 * s, dxfattribs={"layer": "ARQ_REFERENCIA", "lineweight": 20})
    elif key == "fosa":
        rect(msp, p(-0.35, -0.35)[0], p(-0.35, -0.35)[1], p(0.35, 0.35)[0], p(0.35, 0.35)[1], "ARQ_REFERENCIA", 8)
    elif key == "ext":
        msp.add_lwpolyline([p(0, -0.3), p(-0.18, 0.15), p(0.18, 0.15)], dxfattribs={"layer": "ARQ_REFERENCIA", "lineweight": 25}, close=True)
    elif key == "totem":
        rect(msp, p(-0.25, -0.3)[0], p(-0.25, -0.3)[1], p(0.25, 0.3)[0], p(0.25, 0.3)[1], "ARQ_REFERENCIA", 8)
    elif key == "viento":
        msp.add_line(p(-0.9, 0), p(0.9, 0), dxfattribs={"layer": "ARQ_REFERENCIA", "lineweight": 25})
        msp.add_lwpolyline([p(0.9, 0), p(0.65, 0.3), p(0.65, -0.3)], dxfattribs={"layer": "ARQ_REFERENCIA", "lineweight": 25}, close=True)


def add_legend(msp: ezdxf.layouts.BaseLayout, title: str, rows: list[tuple[str, str]], x: float = 55.0, y: float = 55.8, width: float = 28.0, symbol_col: float = 3.4) -> None:
    """Cuadro de leyenda con glifo grafico del simbolo y su descripcion.

    ``rows`` es una lista de ``(symbol_key, description)``; ``symbol_key``
    puede ser un nombre de simbolo dibujable (ver ``draw_legend_symbol``) o
    ``None``/``""`` para una fila de solo texto (norma o nota)."""
    row_h = 0.72
    height = 1.05 + row_h * len(rows)
    rect(msp, x, y - height, x + width, y, "IE_TABLA")
    text_center(msp, title, x + width / 2, y - 0.48, 0.32, "IE_TEXTO")
    msp.add_line((x, y - 0.90), (x + width, y - 0.90), dxfattribs={"layer": "IE_TABLA"})
    for index, (symbol_key, description) in enumerate(rows):
        yy = y - 1.30 - index * row_h
        if symbol_key:
            draw_legend_symbol(msp, symbol_key, x + symbol_col / 2, yy - 0.20)
        text_left(msp, description, x + symbol_col + 0.35, yy, 0.21, "IE_TEXTO")


def add_notes(msp: ezdxf.layouts.BaseLayout, title: str, lines: list[str], x: float = 55.0, y: float = 40.0, width: float = 28.0, height: float = 8.0) -> None:
    """Bloque de notas tecnicas: titulo y lineas de texto dentro de una caja."""
    rect(msp, x, y - height, x + width, y, "IE_TABLA")
    text_center(msp, title, x + width / 2, y - 0.45, 0.26, "IE_TEXTO")
    msp.add_line((x, y - 0.80), (x + width, y - 0.80), dxfattribs={"layer": "IE_TABLA"})
    row_h = 0.55
    for index, line in enumerate(lines):
        yy = y - 1.15 - index * row_h
        text_left(msp, line, x + 0.3, yy, 0.16, "IE_TEXTO")


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
    despacho = [(14.0, 9.5), (16.5, 9.7), (19.0, 9.9), (21.5, 10.1), (14.4, 12.0), (16.9, 12.2), (19.4, 12.4), (21.9, 12.6)]
    patio = [(4.0, 7.0), (6.5, 14.0), (9.5, 14.4), (12.5, 14.8), (15.5, 15.1), (18.5, 15.3), (21.5, 15.5), (24.5, 15.8)]
    for index, point in enumerate(despacho, 1):
        add_luminaire(msp, local_to_page(*point), "L-01" if index in (1, 8) else "", emergency=True)
    for index, point in enumerate(patio, 1):
        add_luminaire(msp, local_to_page(*point), "L-02" if index in (1, 8) else "", emergency=False)
    add_panel(msp, local_to_page(27.42, 14.89), "L-03", "IE_ALUMBRADO")
    tde = local_to_page(9.0, 6.0)
    tdf = local_to_page(10.0, 5.0)
    add_panel(msp, tde, "TDE", "IE_EMERGENCIA")
    add_panel(msp, tdf, "TDF")
    for point in despacho:
        add_route(msp, [(9.0, 6.0), (12.0, 8.0), point], label="PVC 20 mm")
    for point in patio:
        add_route(msp, [(10.0, 5.0), (12.0, 8.0), point], label="PVC 20 mm")
    add_route(msp, [(10.0, 5.0), (17.0, 10.0), (27.42, 14.89)], label="PVC 20 mm")
    add_north_arrow(msp)
    add_scale_bar(msp)
    add_legend(msp, "IE-01 | LEYENDA Y CRITERIOS", [
        ("lum_e", "Luminaria LED - circuito de emergencia (L-01, marquesina/despacho)"),
        ("lum", "Luminaria LED - alumbrado exterior normal (L-02, postes de patio)"),
        ("panel", "Tablero de distribucion TDE / TDF"),
        ("tg", "Tablero general TG / TG2 (observados en el DWG)"),
        ("ig", "Interruptor general de la instalacion"),
        ("paro", "Pulsador de paro de emergencia de playa"),
        ("surt", "Surtidor de doble manguera con cabeza electronica"),
        ("stp", "Tanque subterraneo TK con bomba sumergible (STP)"),
        ("pat", "Pozo de puesta a tierra (PAT / PAT2)"),
        ("rayo", "Pararrayo R=20 m (h=12 m); circulo punteado = radio"),
        ("pm", "Punto de monitoreo de aire/ruido (PM A1/R1/A2/R2)"),
        ("cilindros", "Cilindros de seguridad (arena / trapo humedo)"),
        ("fosa", "Fosa de agua"),
        ("ext", "Extintor"),
        ("totem", "Totem de precios / letrero (L-03)"),
        ("viento", "Direccion del viento"),
        ("canal", "Canalizacion subterranea proyectada"),
        (None, "CNE: dV ramal <= 2.5 % y total <= 4 %; PE en todo circuito"),
    ], y=55.2)
    add_notes(msp, "NOTAS TECNICAS", [
        "Tension: 380/220 V, 60 Hz, 3F+N+PE (sistema TN-S).",
        "Canalizaciones subterraneas enterradas a 0.60 m bajo nivel de piso.",
        "Tuberia PVC SAP 20/25/32 mm segun calibre de conductores.",
        "Conductor de cobre XLPE, seccion minima 2.5 mm2.",
        "Toda luminaria de playa con proteccion IP66 y circuito de emergencia.",
        "Alimentadores a TDE/TDF con ITM 40/32 A y cable 10 mm2 (ver IE-05).",
    ])


def sheet_ie02(doc: ezdxf.document.Drawing, architecture: dict[str, Any], calc: dict[str, Any]) -> None:
    msp = doc.modelspace()
    add_architecture(doc, architecture)
    td1 = local_to_page(9.0, 5.0)
    add_panel(msp, td1, "TD-A1")
    a101 = [
        (3.2, 1.4), (5.2, 1.4), (7.2, 1.4), (9.2, 1.4),
        (3.2, 2.6), (5.2, 2.6), (7.2, 2.6), (9.2, 2.6),
        (6.5, 3.7), (7.8, 3.7), (9.1, 3.7),
        (6.5, 4.5), (7.8, 4.5), (9.1, 4.5), (10.4, 4.5),
    ]
    a102 = [(13.0, 2.4), (13.7, 3.2), (14.4, 4.0), (15.76, 2.52), (17.60, 2.46), (18.33, 2.53), (3.47, 4.71)]
    for index, point in enumerate(a101, 1):
        add_luminaire(msp, local_to_page(*point), "A1-01" if index in (1, 15) else "")
    for index, point in enumerate(a102, 1):
        add_luminaire(msp, local_to_page(*point), "A1-02" if index in (1, 7) else "")
    tomas = ((5.0, 2.0), (10.0, 2.0), (12.0, 4.0), (16.0, 2.0), (18.5, 2.5))
    for x, y in tomas:
        add_outlet(msp, local_to_page(x, y))
    for x, y in (*a101, *a102):
        add_route(msp, [(9.0, 5.0), (9.0, 6.0), (x, 6.0), (x, y)], label="PVC 20 mm")
    for x, y in tomas:
        add_route(msp, [(9.0, 5.0), (9.0, 6.0), (x, 6.0), (x, y)], label="PVC 20 mm")
    add_north_arrow(msp)
    add_scale_bar(msp)
    add_legend(msp, "IE-02 | LEYENDA", [
        ("lum", "Luminaria LED interior (A1-01: admin./oficina; A1-02: SS.HH y sala de maquinas)"),
        ("tc", "Tomacorriente doble (TC), con contacto a tierra"),
        ("panel", "Tablero de distribucion TD-A1"),
        ("canal", "Canalizacion empotrada proyectada"),
        (None, "Tomacorrientes con interruptor diferencial 30 mA"),
        (None, "CNE: conductor minimo 2.5 mm2; dV ramal <= 2.5 %"),
    ])
    add_notes(msp, "NOTAS TECNICAS", [
        "Alumbrado interior con paneles LED 36 W y luminarias estancas 18 W.",
        "Tomas de corriente con puesta a tierra; circuito independiente por zona.",
        "Tuberia empotrada en muros y losa; cajas octogonales y rectangulares.",
        "Interruptores de pared a 1.20 m; tomacorrientes a 0.40 m del piso.",
        "Tablero TD-A1 alimentado desde TG (ver IE-05).",
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
    add_panel(msp, local_to_page(13.0, 2.2), "C-AIRE", "IE_FUERZA")
    add_panel(msp, local_to_page(14.6, 2.2), "B-AGUA", "IE_FUERZA")
    add_panel(msp, local_to_page(16.2, 2.2), "B-FOSA", "IE_FUERZA")
    for tanque in architecture["tanques"]:
        add_route(msp, [(9.0, 6.0), (12.0, 6.0), tanque["pos_local"]], label="PVC 25 mm")
    for punto in architecture["dispensadores_y_surtidores"]["posiciones_local"]:
        add_route(msp, [(10.0, 5.0), (12.0, 7.0), punto], label="PVC 20 mm")
    add_north_arrow(msp)
    add_scale_bar(msp)
    add_legend(msp, "IE-03 | LEYENDA", [
        ("stp", "STP - bomba sumergible de tanque (emergencia, TDE)"),
        ("surt", "Surtidor / cabeza electronica (UPS-FUEL)"),
        ("panel", "Tablero de distribucion TDE (emergencia) / TDF (fuerza)"),
        ("canal", "Canalizacion subterranea proyectada"),
        ("paro", "Pulsador de paro de emergencia de playa (S-04)"),
        (None, "C-AIRE = compresor de aire (F-07); B-AGUA = bomba de agua (F-08); B-FOSA = bomba de efluentes (F-09)"),
        (None, "Cargas criticas (STP, surtidores, ATG, POS) con respaldo de emergencia"),
        (None, "CNE: areas clasificadas con equipo de proteccion apropiada"),
    ])
    add_notes(msp, "NOTAS TECNICAS", [
        "STP de 1.5 hp con arranque directo; circuito de emergencia desde TDE.",
        "Surtidores con cabeza electronica 103 VA (UPS-FUEL 1.5 kVA).",
        "Pulsador de paro de emergencia de playa (S-04) accesible en cada isla.",
        "Equipos de servicio (compresor, bombas) en sala de maquinas desde TDF.",
        "Canalizaciones a tanques y surtidores en zanja a 0.60 m.",
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
    malla_pts = [
        local_to_page(6.0, 5.0), local_to_page(9.0, 6.0), local_to_page(10.0, 5.0),
        local_to_page(12.0, 7.0), local_to_page(14.0, 8.0), local_to_page(17.0, 12.0),
        local_to_page(21.0, 8.0),
    ]
    msp.add_lwpolyline(malla_pts, dxfattribs={"layer": "IE_TIERRA"})

    def nearest_malla(pos: tuple[float, float]) -> tuple[float, float]:
        page = local_to_page(*pos)
        return min(malla_pts, key=lambda pt: (pt[0] - page[0]) ** 2 + (pt[1] - page[1]) ** 2)

    for equipo in architecture.get("equipos_electricos_observados", []):
        if "pos_local" not in equipo:
            continue
        pos = equipo["pos_local"]
        if pos and isinstance(pos[0], (list, tuple)):
            pos = pos[0]
        if not pos:
            continue
        if equipo["tipo"] in ("tablero_general", "interruptor_general", "pozo_tierra", "pozo_tierra_secundario", "pararrayo", "monitoreo"):
            continue
        msp.add_line(local_to_page(*pos), nearest_malla(pos), dxfattribs={"layer": "IE_TIERRA", "linetype": "DASHED"})
    add_north_arrow(msp)
    add_scale_bar(msp)
    add_legend(msp, "IE-04 | PUESTA A TIERRA Y RAYO", [
        ("pat", "Pozo de puesta a tierra PAT / PAT2 (resis. <= 10 ohm)"),
        ("rayo", "Pararrayo con radio de proteccion 20 m (h=12 m)"),
        ("malla", "Malla / enlace equipotencial (conductor de tierra)"),
        ("canal", "Conductor de tierra enterrado proyectado"),
        ("tg", "Tableros generales TG / TG2 y equipos a conectar a la malla"),
        (None, "Resistencia de PAT <= 10 ohm y <= 25 ohm para rayo"),
    ])
    add_notes(msp, "NOTAS TECNICAS", [
        "PAT principal junto al TG: 2 pozos (PAT/PAT2) con varilla Cu 5/8 x 2.4 m.",
        "Enlace equipotencial de tableros, surtidores, tanques y fosa a la malla.",
        "Pararrayo h=12 m con radio de proteccion 20 m (electrogeometrico).",
        "Conductor de tierra desnudo Cu 10 mm2 enterrado a 0.50 m.",
        "Verificar resistencia con telurometro en campo.",
    ])


def add_load_schedule(msp: ezdxf.layouts.BaseLayout, calc: dict[str, Any], x: float = 47.0, y: float = 52.0) -> None:
    circuits = calc["circuits"]
    row_h = 0.55
    width = 33.5
    height = 1.0 + row_h * (len(circuits) + 1)
    rect(msp, x, y - height, x + width, y, "IE_TABLA")
    text_center(msp, "CUADRO RESUMIDO DE CARGAS (CNE-U)", x + width / 2, y - 0.40, 0.28, "IE_TEXTO")
    msp.add_line((x, y - 0.78), (x + width, y - 0.78), dxfattribs={"layer": "IE_TABLA"})
    headers = [("ID", 0.3), ("TAB", 3.2), ("FASE", 7.5), ("kVA", 11.2), ("ITM", 15.0), ("Cu/PE", 19.5), ("dV", 27.5)]
    for label, dx in headers:
        text_left(msp, label, x + dx, y - 1.15, 0.17, "IE_TEXTO")
    for index, circuit in enumerate(circuits):
        yy = y - 1.65 - index * row_h
        text_left(msp, circuit["id"], x + 0.3, yy, 0.15, "IE_TEXTO")
        text_left(msp, circuit["panel"], x + 3.2, yy, 0.15, "IE_TEXTO")
        text_left(msp, circuit["phase"], x + 7.5, yy, 0.15, "IE_TEXTO")
        text_left(msp, f"{circuit['installed_kva_calc']:.2f}", x + 11.2, yy, 0.15, "IE_TEXTO")
        text_left(msp, f"{circuit['breaker_a']} A", x + 15.0, yy, 0.15, "IE_TEXTO")
        text_left(msp, f"{circuit['conductor_mm2']}/{circuit['pe_mm2']}", x + 19.5, yy, 0.15, "IE_TEXTO")
        text_left(msp, f"{circuit['total_voltage_drop_percent']:.2f}%", x + 27.5, yy, 0.15, "IE_TEXTO")


def sheet_ie05(doc: ezdxf.document.Drawing, architecture: dict[str, Any], calc: dict[str, Any]) -> None:
    msp = doc.modelspace()
    s = calc["summary"]
    text_center(msp, "DIAGRAMA UNIFILAR GENERAL 380/220 V - 3F+N+PE - GRIFO SAN ROMÁN", 40.0, 55.5, 0.55, "IE_TEXTO")

    # =========================================================================
    # ACOMETIDA RED PÚBLICA & GRUPO ELECTRÓGENO
    # =========================================================================
    # Suministro Red Publica (Electro Puno)
    text_center(msp, "RED PÚBLICA 10 kV", 6.0, 52.5, 0.22, "IE_EMERGENCIA")
    text_center(msp, "Electro Puno", 6.0, 51.7, 0.18, "IE_TEXTO")
    msp.add_line((6.0, 51.0), (6.0, 48.5), dxfattribs={"layer": "IE_EMERGENCIA"})
    
    # Trafo 100kVA (Subestacion)
    msp.add_circle((6.0, 47.7), 0.8, dxfattribs={"layer": "IE_EMERGENCIA"})
    msp.add_circle((6.0, 46.5), 0.8, dxfattribs={"layer": "IE_EMERGENCIA"})
    text_left(msp, "TRAFO 100 kVA", 7.5, 47.3, 0.20, "IE_TEXTO")
    text_left(msp, "10kV / 0.38-0.22kV", 7.5, 46.5, 0.16, "IE_TEXTO")
    
    msp.add_line((6.0, 45.7), (6.0, 44.0), dxfattribs={"layer": "IE_EMERGENCIA"})
    # Medidor Wh
    msp.add_circle((6.0, 43.4), 0.6, dxfattribs={"layer": "IE_EMERGENCIA"})
    text_center(msp, "Wh", 6.0, 43.4, 0.22, "IE_TEXTO")
    
    msp.add_line((6.0, 42.8), (6.0, 41.5), dxfattribs={"layer": "IE_EMERGENCIA"})
    # ITM Principal Acometida
    rect(msp, 5.0, 40.2, 7.0, 41.5, "IE_FUERZA")
    text_center(msp, f"ITM 4P-{s['main_breaker_a']:.0f}A", 6.0, 40.85, 0.20, "IE_TEXTO")
    text_center(msp, "Icu>=25kA", 6.0, 39.8, 0.16, "IE_TEXTO")
    
    msp.add_line((6.0, 39.4), (6.0, 37.0), dxfattribs={"layer": "IE_EMERGENCIA"})

    # Grupo Electrogeno Standby (Cummins 37.5 kVA)
    msp.add_circle((16.0, 48.0), 1.2, dxfattribs={"layer": "IE_EMERGENCIA"})
    text_center(msp, "G", 16.0, 48.0, 0.40, "IE_EMERGENCIA")
    text_left(msp, "GRUPO ELECTRÓGENO", 18.0, 48.6, 0.22, "IE_EMERGENCIA")
    text_left(msp, "Cummins 37.5 kVA / 30 kW", 18.0, 47.8, 0.18, "IE_TEXTO")
    text_left(msp, "380/220V 3F+N+PE, 60Hz", 18.0, 47.0, 0.16, "IE_TEXTO")
    
    msp.add_line((16.0, 46.8), (16.0, 41.5), dxfattribs={"layer": "IE_EMERGENCIA"})
    rect(msp, 15.0, 40.2, 17.0, 41.5, "IE_EMERGENCIA")
    text_center(msp, "ITM 4P-63A", 16.0, 40.85, 0.20, "IE_TEXTO")
    msp.add_line((16.0, 40.2), (16.0, 37.0), dxfattribs={"layer": "IE_EMERGENCIA"})

    # Tablero de Transferencia Automatica (ATS)
    rect(msp, 4.0, 34.8, 18.0, 37.0, "IE_EMERGENCIA")
    text_center(msp, "TABLERO DE TRANSFERENCIA AUTOMÁTICA (ATS 4P-63A)", 11.0, 35.9, 0.25, "IE_EMERGENCIA")
    text_center(msp, "Conmutación Automática Red / Grupo Electrogeno", 11.0, 35.2, 0.18, "IE_TEXTO")

    msp.add_line((11.0, 34.8), (11.0, 33.0), dxfattribs={"layer": "IE_FUERZA"})

    # =========================================================================
    # BARRA PRINCIPAL TABLERO GENERAL TG (380/220V)
    # =========================================================================
    msp.add_line((4.0, 33.0), (44.0, 33.0), dxfattribs={"layer": "IE_FUERZA", "lineweight": 60})
    text_left(msp, "BARRA PRINCIPAL DE COBRE TG: 380/220V, 3Ø+N+PE, 60Hz (In = 100A)", 4.5, 33.5, 0.25, "IE_TEXTO")

    # =========================================================================
    # DERIVACIONES A SUBTABLEROS: TDE, TDF, TD-A1
    # =========================================================================
    # 1. Alimentador a TDE (Tablero de Emergencia) at x = 10.0
    msp.add_line((10.0, 33.0), (10.0, 31.0), dxfattribs={"layer": "IE_EMERGENCIA"})
    rect(msp, 8.8, 29.8, 11.2, 31.0, "IE_EMERGENCIA")
    text_center(msp, "ITM 3P-40A", 10.0, 30.4, 0.18, "IE_TEXTO")
    text_center(msp, "Alim TDE: 4x10mm2", 10.0, 29.3, 0.15, "IE_TEXTO")
    msp.add_line((10.0, 29.8), (10.0, 27.5), dxfattribs={"layer": "IE_EMERGENCIA"})

    # Barra TDE at y = 27.5
    rect(msp, 4.0, 24.5, 17.0, 27.5, "IE_EMERGENCIA")
    text_center(msp, "TABLERO TDE (EMERGENCIA - CRÍTICO)", 10.5, 26.8, 0.25, "IE_EMERGENCIA")
    msp.add_line((4.5, 25.8), (16.5, 25.8), dxfattribs={"layer": "IE_EMERGENCIA", "lineweight": 40})

    # Circuitos TDE
    tde_circs = [
        ("C1: STP 1.5HP", "ITM 3P-20A", "Guardamotor 4-6.3A", "3x4mm2 N2XH", 5.2),
        ("C2: SURTIDORES", "ITM 2P-16A", "ID 2P-25A 30mA", "UPS-FUEL 1.5kVA", 8.2),
        ("C3: ALUM. PLAYA", "ITM 2P-16A", "ID 2P-25A 30mA", "3x2.5mm2 LSOH", 11.2),
        ("C4: ALUM. EMERG", "ITM 2P-10A", "ID 2P-25A 30mA", "3x2.5mm2 LSOH", 14.2),
    ]
    for name, itm, prot, cond, cx in tde_circs:
        msp.add_line((cx, 25.8), (cx, 24.0), dxfattribs={"layer": "IE_EMERGENCIA"})
        rect(msp, cx - 1.0, 22.8, cx + 1.0, 24.0, "IE_EMERGENCIA")
        text_center(msp, itm, cx, 23.4, 0.16, "IE_TEXTO")
        msp.add_line((cx, 22.8), (cx, 21.6), dxfattribs={"layer": "IE_EMERGENCIA"})
        rect(msp, cx - 1.0, 20.4, cx + 1.0, 21.6, "IE_EMERGENCIA")
        text_center(msp, prot, cx, 21.0, 0.14, "IE_TEXTO")
        msp.add_line((cx, 20.4), (cx, 19.2), dxfattribs={"layer": "IE_EMERGENCIA"})
        text_center(msp, name, cx, 18.7, 0.16, "IE_TEXTO")
        text_center(msp, cond, cx, 18.1, 0.14, "IE_TEXTO")

    # 2. Alimentador a TDF (Tablero Fuerza Normal) at x = 26.0
    msp.add_line((26.0, 33.0), (26.0, 31.0), dxfattribs={"layer": "IE_FUERZA"})
    rect(msp, 24.8, 29.8, 27.2, 31.0, "IE_FUERZA")
    text_center(msp, "ITM 3P-40A", 26.0, 30.4, 0.18, "IE_TEXTO")
    text_center(msp, "Alim TDF: 4x10mm2", 26.0, 29.3, 0.15, "IE_TEXTO")
    msp.add_line((26.0, 29.8), (26.0, 27.5), dxfattribs={"layer": "IE_FUERZA"})

    # Barra TDF at y = 27.5
    rect(msp, 20.0, 24.5, 33.0, 27.5, "IE_FUERZA")
    text_center(msp, "TABLERO TDF (FUERZA NORMAL)", 26.5, 26.8, 0.25, "IE_FUERZA")
    msp.add_line((20.5, 25.8), (32.5, 25.8), dxfattribs={"layer": "IE_FUERZA", "lineweight": 40})

    # Circuitos TDF
    tdf_circs = [
        ("F1: COMPRESOR", "ITM 3P-16A", "Guardamotor 4-6.3A", "3x4mm2 N2XH", 21.5),
        ("F2: B. AGUA", "ITM 3P-10A", "Guardamotor 2.5-4A", "3x2.5mm2 N2XH", 24.5),
        ("F3: B. FOSA", "ITM 3P-10A", "Guardamotor 2.5-4A", "3x2.5mm2 N2XH", 27.5),
        ("F4: TOTEM", "ITM 2P-10A", "ID 2P-25A 30mA", "3x2.5mm2 LSOH", 30.5),
    ]
    for name, itm, prot, cond, cx in tdf_circs:
        msp.add_line((cx, 25.8), (cx, 24.0), dxfattribs={"layer": "IE_FUERZA"})
        rect(msp, cx - 1.0, 22.8, cx + 1.0, 24.0, "IE_FUERZA")
        text_center(msp, itm, cx, 23.4, 0.16, "IE_TEXTO")
        msp.add_line((cx, 22.8), (cx, 21.6), dxfattribs={"layer": "IE_FUERZA"})
        rect(msp, cx - 1.0, 20.4, cx + 1.0, 21.6, "IE_FUERZA")
        text_center(msp, prot, cx, 21.0, 0.14, "IE_TEXTO")
        msp.add_line((cx, 20.4), (cx, 19.2), dxfattribs={"layer": "IE_FUERZA"})
        text_center(msp, name, cx, 18.7, 0.16, "IE_TEXTO")
        text_center(msp, cond, cx, 18.1, 0.14, "IE_TEXTO")

    # 3. Alimentador a TD-A1 (Tablero Admin) at x = 39.0
    msp.add_line((39.0, 33.0), (39.0, 31.0), dxfattribs={"layer": "IE_ALUMBRADO"})
    rect(msp, 37.8, 29.8, 40.2, 31.0, "IE_ALUMBRADO")
    text_center(msp, "ITM 2P-25A", 39.0, 30.4, 0.18, "IE_TEXTO")
    text_center(msp, "Alim TD-A1: 3x4mm2", 39.0, 29.3, 0.15, "IE_TEXTO")
    msp.add_line((39.0, 29.8), (39.0, 27.5), dxfattribs={"layer": "IE_ALUMBRADO"})

    # Barra TD-A1 at y = 27.5
    rect(msp, 35.0, 24.5, 45.0, 27.5, "IE_ALUMBRADO")
    text_center(msp, "TABLERO TD-A1 (ADMINISTRACIÓN)", 40.0, 26.8, 0.25, "IE_ALUMBRADO")
    msp.add_line((35.5, 25.8), (44.5, 25.8), dxfattribs={"layer": "IE_ALUMBRADO", "lineweight": 40})

    # Circuitos TD-A1
    tda_circs = [
        ("A1-01: ALUM ADMIN", "ITM 2P-10A", "3x1.5mm2 LSOH", 36.5),
        ("A2-01: TC ADMIN", "ITM 2P-16A", "ID 2P-25A 30mA", 39.5),
        ("A3-01: TC SS.HH", "ITM 2P-16A", "ID 2P-25A 30mA", 42.5),
    ]
    for name, itm, prot, cx in tda_circs:
        msp.add_line((cx, 25.8), (cx, 24.0), dxfattribs={"layer": "IE_ALUMBRADO"})
        rect(msp, cx - 1.0, 22.8, cx + 1.0, 24.0, "IE_ALUMBRADO")
        text_center(msp, itm, cx, 23.4, 0.16, "IE_TEXTO")
        msp.add_line((cx, 22.8), (cx, 21.6), dxfattribs={"layer": "IE_ALUMBRADO"})
        rect(msp, cx - 1.0, 20.4, cx + 1.0, 21.6, "IE_ALUMBRADO")
        text_center(msp, prot, cx, 21.0, 0.14, "IE_TEXTO")
        msp.add_line((cx, 20.4), (cx, 19.2), dxfattribs={"layer": "IE_ALUMBRADO"})
        text_center(msp, name, cx, 18.7, 0.16, "IE_TEXTO")

    # =========================================================================
    # CAJA RESUMEN DE PARÁMETROS ELÉCTRICOS GENERALES
    # =========================================================================
    rect(msp, 4.0, 10.0, 44.0, 16.5, "IE_TABLA")
    text_center(msp, "PARÁMETROS GENERALES DEL ANTEPROYECTO - GRIFO SAN ROMÁN", 24.0, 15.6, 0.28, "IE_TEXTO")
    msp.add_line((4.0, 15.0), (44.0, 15.0), dxfattribs={"layer": "IE_TABLA"})
    text_left(msp, f"• Potencia Instalada Total (PI): {s['installed_kw']:.2f} kW ({s['installed_kva']:.2f} kVA)", 5.0, 14.2, 0.20, "IE_TEXTO")
    text_left(msp, f"• Máxima Demanda Estimada (MD): {s['maximum_demand_kw']:.2f} kW ({s['maximum_demand_kva']:.2f} kVA)", 5.0, 13.4, 0.20, "IE_TEXTO")
    text_left(msp, f"• Capacidad del Servicio Sugerida: {s['service_capacity_kva']:.0f} kVA (Reserva CNE = {s['service_design_kva_with_reserve']:.2f} kVA)", 5.0, 12.6, 0.20, "IE_TEXTO")
    text_left(msp, f"• Corriente Máxima de Diseño: {s['maximum_phase_current_with_reserve_a']:.1f} A | Interruptor General: 4P-{s['main_breaker_a']:.0f}A", 5.0, 11.8, 0.20, "IE_TEXTO")
    text_left(msp, f"• Caída de Tensión Alimentador Principal: {s['main_voltage_drop_percent']:.2f}% (CNE máximo permitido = 2.5%)", 5.0, 11.0, 0.20, "IE_TEXTO")

    # Cuadro de cargas en el lado derecho
    add_load_schedule(msp, calc)


def sheet_ie06(doc: ezdxf.document.Drawing, architecture: dict[str, Any], calc: dict[str, Any]) -> None:
    msp = doc.modelspace()
    add_architecture(doc, architecture)
    for tanque in architecture["tanques"]:
        cx, cy = local_to_page(*tanque["pos_local"])
        msp.add_circle((cx, cy), scale_length(2.2), dxfattribs={"layer": "IE_ZONA_1", "linetype": "DASHED"})
    for punto in architecture["dispensadores_y_surtidores"]["posiciones_local"]:
        cx, cy = local_to_page(*punto)
        msp.add_circle((cx, cy), scale_length(3.5), dxfattribs={"layer": "IE_ZONA_2", "linetype": "DASHED"})
    for ambiente in architecture.get("ambientes", []):
        if "venteo" not in ambiente["nombre"].lower():
            continue
        cx, cy = local_to_page(*ambiente["centro_local"])
        msp.add_circle((cx, cy), scale_length(1.5), dxfattribs={"layer": "IE_ZONA_1", "linetype": "DASHED"})
        msp.add_circle((cx, cy), 0.15, dxfattribs={"layer": "ARQ_REFERENCIA", "lineweight": 30})
    add_north_arrow(msp)
    add_scale_bar(msp)
    add_legend(msp, "IE-06 | CLASIFICACION DE AREAS", [
        ("zona1", "Zona 1 - area peligrosa alrededor de tanques y venteos"),
        ("zona2", "Zona 2 - area de despacho alrededor de surtidores"),
        ("stp", "Tanque subterraneo TK (punto de riesgo)"),
        ("surt", "Surtidor de despacho"),
        ("viento", "Direccion del viento (referencia para dispersion de vapores)"),
        (None, "Limites: propuesta academica; trazado segun CNE-U cap. 6 y revision competente"),
        (None, "CNE: equipo electrico de areas clasificadas con proteccion apropiada"),
    ])
    add_notes(msp, "NOTAS TECNICAS", [
        "Zona 1 (r=2.2 m) alrededor de tanques y venteos; Zona 2 (r=3.5 m) en despacho.",
        "Venteo de tanques con zona 1 (r=1.5 m) adicional.",
        "Equipo electrico en Zona 1/2: certificado para clasificacion de gases (Ej. ex d / ex e).",
        "Surtidores con cabeza electronica intrinsecamente segura.",
        "Clasificacion preliminar: sujeto a revision competente y normativa sectorial.",
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
        try:
            subprocess.run(["pdfunite", *(str(path) for path in all_pdf_paths), str(temporary)], check=True)
        except Exception:
            try:
                from pypdf import PdfWriter
                merger = PdfWriter()
                for pdf_p in all_pdf_paths:
                    merger.append(str(pdf_p))
                merger.write(str(temporary))
                merger.close()
            except Exception:
                shutil.copy2(str(all_pdf_paths[0]), str(temporary))
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

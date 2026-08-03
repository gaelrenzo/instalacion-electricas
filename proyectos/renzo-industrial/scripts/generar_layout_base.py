#!/usr/bin/env python3
"""Genera la vista esquematica de la geometria base del grifo (planos originales).

Reconstruye la planta a partir de ``arquitectura/datos/layout-grifo.json`` en
formato SVG (vectorial), que luego se convierte a PDF para incluir en el
expediente como ``\IlustracionLayout``. Es una representacion academica de la
geometria extraida del DWG original, no un plano electrico.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def svg_from_layout(layout: dict, real_entities: list[dict] | None, out_svg: Path) -> None:
    scale = 28.0
    pad = 12.0

    def content_extent() -> tuple[float, float, float, float]:
        xs: list[float] = []
        ys: list[float] = []
        if real_entities:
            for ent in real_entities:
                if ent.get("type") == "seg":
                    for p in ent["pts"]:
                        xs.append(p[0]); ys.append(p[1])
        else:
            bbox = layout["edificio"]["bbox_local"]
            xs += [bbox[0], bbox[2]]
            ys += [bbox[1], bbox[3]]
        lote = layout["lote_a_ejecutar"]["poligono_local"]
        for p in lote:
            xs.append(p[0]); ys.append(p[1])
        for tk in layout["tanques"]:
            xs.append(tk["pos_local"][0]); ys.append(tk["pos_local"][1])
        for p in layout["dispensadores_y_surtidores"]["posiciones_local"]:
            xs.append(p[0]); ys.append(p[1])
        for eq in layout.get("equipos_electricos_observados", []):
            if "pos_local" not in eq:
                continue
            pos = eq["pos_local"]
            if pos and isinstance(pos[0], (list, tuple)):
                pos = pos[0]
            xs.append(pos[0]); ys.append(pos[1])
        return min(xs), min(ys), max(xs), max(ys)

    x0, y0, x1, y1 = content_extent()
    span_x = x1 - x0
    span_y = y1 - y0

    def pt(x: float, y: float) -> tuple[float, float]:
        return (pad + (x - x0) * scale, pad + (y1 - y) * scale)

    width = 2 * pad + span_x * scale
    height = 2 * pad + span_y * scale

    lines: list[str] = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}">')
    lines.append('<rect width="100%" height="100%" fill="#ffffff"/>')

    lote = layout["lote_a_ejecutar"]["poligono_local"]

    if real_entities:
        # Lote a ejecutar fiel al DWG: se dibujan los segmentos reales de la
        # capa LOTE A EJECUTAR (el DXF trae duplicados y tramos cortados, por
        # eso se evita reconstruir un poligono unico que pueda "cortar" la
        # figura con una forma simplificada).
        lote_edges = [ent["pts"] for ent in real_entities if ent.get("type") == "seg" and ent.get("layer") == "LOTE A EJECUTAR"]
        seen: set[tuple[tuple[float, float], tuple[float, float]]] = set()
        for a, b in lote_edges:
            key = tuple(sorted(((round(a[0], 2), round(a[1], 2)), (round(b[0], 2), round(b[1], 2)))))
            if key in seen:
                continue
            seen.add(key)
            pa, pb = pt(*a), pt(*b)
            lines.append(f'<line x1="{pa[0]:.1f}" y1="{pa[1]:.1f}" x2="{pb[0]:.1f}" y2="{pb[1]:.1f}" stroke="#243F60" stroke-width="3"/>')
    else:
        pts = " ".join(f"{pt(x, y)[0]:.1f},{pt(x, y)[1]:.1f}" for x, y in lote)
        lines.append(f'<polygon points="{pts}" fill="none" stroke="#243F60" stroke-width="3"/>')

    if real_entities:
        weights = {
            "muro": ("#000000", 2.0),
            "0": ("#808080", 1.0),
            "entrada": ("#B0B0B0", 0.8),
            "VENTANAS": ("#404040", 0.8),
            "D VEREDAS": ("#C0C0C0", 0.6),
            "vereda": ("#C0C0C0", 0.6),
        }
        for ent in real_entities:
            if ent.get("type") != "seg":
                continue
            style = weights.get(ent.get("layer"))
            if style is None:
                continue
            color, lw = style
            a, b = ent["pts"]
            pa, pb = pt(*a), pt(*b)
            lines.append(f'<line x1="{pa[0]:.1f}" y1="{pa[1]:.1f}" x2="{pb[0]:.1f}" y2="{pb[1]:.1f}" stroke="{color}" stroke-width="{lw}"/>')
    else:
        edificio = layout["edificio"]["bbox_local"]
        ex0, ey0, ex1, ey1 = edificio
        p0, p1 = pt(ex0, ey0), pt(ex1, ey1)
        lines.append(
            f'<rect x="{p0[0]:.1f}" y="{p1[1]:.1f}" width="{p1[0]-p0[0]:.1f}" height="{p0[1]-p1[1]:.1f}" '
            'fill="none" stroke="#2E74B5" stroke-width="2.5"/>'
        )

    for ent in real_entities or []:
        if ent.get("type") == "text" and ent.get("layer") in ("TEXT-AMB", "TEXTO-AMB"):
            cx, cy = pt(*ent["pos"])
            lines.append(f'<text x="{cx:.1f}" y="{cy:.1f}" font-family="Arial" font-size="10" fill="#243F60" text-anchor="middle">{ent["text"]}</text>')

    for tanque in layout["tanques"]:
        cx, cy = pt(*tanque["pos_local"])
        lines.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="none" stroke="#C00000" stroke-width="2"/>')
        lines.append(f'<text x="{cx:.1f}" y="{cy - 6:.1f}" font-family="Arial" font-size="9" fill="#C00000" text-anchor="middle">{tanque["numero"]}</text>')

    for px, py in layout["dispensadores_y_surtidores"]["posiciones_local"]:
        cx, cy = pt(px, py)
        lines.append(f'<rect x="{cx-4:.1f}" y="{cy-4:.1f}" width="8" height="8" fill="none" stroke="#000000" stroke-width="1.5"/>')
        lines.append(f'<text x="{cx:.1f}" y="{cy + 14:.1f}" font-family="Arial" font-size="9" fill="#000000" text-anchor="middle">SURT</text>')

    for eq in layout["equipos_electricos_observados"]:
        if "pos_local" not in eq:
            continue
        pos = eq["pos_local"]
        if pos and isinstance(pos[0], (list, tuple)):
            pos = pos[0]
        cx, cy = pt(*pos)
        if eq["tipo"] in ("pozo_tierra", "pozo_tierra_secundario"):
            lines.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="none" stroke="#007000" stroke-width="2"/>')
            lines.append(f'<text x="{cx:.1f}" y="{cy - 6:.1f}" font-family="Arial" font-size="8" fill="#007000" text-anchor="middle">PAT</text>')
        elif eq["tipo"] == "pararrayo":
            lines.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="12" fill="none" stroke="#B00000" stroke-width="1" stroke-dasharray="3,3"/>')
            lines.append(f'<polygon points="{cx-5:.1f},{cy+6:.1f} {cx+5:.1f},{cy+6:.1f} {cx:.1f},{cy-7:.1f}" fill="none" stroke="#000000" stroke-width="1.5"/>')
            lines.append(f'<text x="{cx:.1f}" y="{cy + 16:.1f}" font-family="Arial" font-size="8" fill="#000000" text-anchor="middle">PARARRAYO</text>')
        elif eq["tipo"] == "pulsador_emergencia":
            lines.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3" fill="#C00000"/>')
        elif eq["tipo"] == "tablero_general":
            lines.append(f'<text x="{cx:.1f}" y="{cy:.1f}" font-family="Arial" font-size="9" font-weight="bold" fill="#243F60" text-anchor="middle">{eq["sigla"]}</text>')
        elif eq["tipo"] in ("cilindro_arena", "cilindro_trapo_empapado"):
            lines.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="none" stroke="#C08000" stroke-width="1.5"/>')
            lines.append(f'<text x="{cx:.1f}" y="{cy + 12:.1f}" font-family="Arial" font-size="7" fill="#C08000" text-anchor="middle">ARENA/TRAPO</text>')
        elif eq["tipo"] == "monitoreo":
            lines.append(f'<text x="{cx:.1f}" y="{cy:.1f}" font-family="Arial" font-size="8" font-weight="bold" fill="#800080" text-anchor="middle">{eq["sigla"]}</text>')
        elif eq["tipo"] == "totem":
            lines.append(f'<text x="{cx:.1f}" y="{cy:.1f}" font-family="Arial" font-size="8" fill="#000000" text-anchor="middle">TOTEM</text>')

    # Norte
    lines.append(f'<text x="{width-14:.1f}" y="18" font-family="Arial" font-size="12" font-weight="bold" fill="#000000">N &#8593;</text>')

    # Leyenda
    ly = height - 30
    legend = [
        ("#243F60", 3.0, "Lote a ejecutar"),
        ("#2E74B5", 2.5, "Edificio (bbox)"),
        ("#C00000", 2.0, "Tanques TK-1..TK-3"),
        ("#000000", 1.5, "Surtidores / islas"),
        ("#007000", 2.0, "Pozos de tierra"),
        ("#000000", 1.5, "Pararrayo / tableros"),
    ]
    lx = 14
    for color, sw, label in legend:
        lines.append(f'<line x1="{lx:.1f}" y1="{ly:.1f}" x2="{lx+14:.1f}" y2="{ly:.1f}" stroke="{color}" stroke-width="{sw}"/>')
        lines.append(f'<text x="{lx+18:.1f}" y="{ly+3:.1f}" font-family="Arial" font-size="9" fill="#000000">{label}</text>')
        lx += 110

    lines.append('</svg>')
    out_svg.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    root = repo_root()
    project = root / "proyectos/renzo-industrial"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layout", type=Path, default=project / "arquitectura/datos/layout-grifo.json")
    parser.add_argument("--architecture", type=Path, default=project / "arquitectura/datos/arquitectura-dwg.json")
    parser.add_argument("--output", type=Path, default=root / "build/renzo-industrial/expediente/assets")
    args = parser.parse_args()

    layout = json.loads(args.layout.read_text(encoding="utf-8"))
    real_entities: list[dict] | None = None
    if args.architecture.exists():
        real_entities = json.loads(args.architecture.read_text(encoding="utf-8"))
    args.output.mkdir(parents=True, exist_ok=True)
    svg_path = args.output / "layout-base.svg"
    pdf_path = args.output / "layout-base.pdf"
    png_path = args.output / "layout-base.png"

    svg_from_layout(layout, real_entities, svg_path)
    try:
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPDF
        drawing = svg2rlg(str(svg_path))
        renderPDF.drawToFile(drawing, str(pdf_path))
    except Exception as exc:
        print(f"SVG->PDF no disponible ({exc}); se conserva solo SVG")

    try:
        subprocess.run(["rsvg-convert", "-f", "png", "-o", str(png_path), str(svg_path)], check=True)
    except Exception:
        pass

    print(json.dumps({"status": "PASS", "svg": str(svg_path), "pdf": str(pdf_path)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

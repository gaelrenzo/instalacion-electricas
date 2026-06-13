#!/usr/bin/env python3
"""
Generacion automatica de rutas ortogonales de canalizacion electrica.

Toma un JSON electrico con componentes (luminarias, interruptores, tomacorrientes,
tableros) y genera rutas ortogonales optimizadas que conectan los componentes
de cada circuito, viajando paralelo a muros (ejes X/Y).

Uso:
  python3 auto_routing.py --electrical electrico.json --output electrico_ruteado.json
  python3 auto_routing.py --electrical electrico.json --output electrico_ruteado.json --clearance 0.3
"""

import argparse
import json
import math
import os
import sys
from itertools import groupby


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def orthogonal_route(p1, p2, clearance=0.3):
    """
    Genera una ruta ortogonal (L-shaped) entre dos puntos.
    Elige automaticamente si va primero horizontal o vertical
    basado en la posicion relativa y la distancia.
    """
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) < 0.01 and abs(dy) < 0.01:
        return [p1]

    if abs(dx) > abs(dy):
        mid_x = x2
        mid_y = y1
    else:
        mid_x = x1
        mid_y = y2

    mid = (mid_x, mid_y)

    puntos = [p1, mid, p2]

    simplified = [puntos[0]]
    for p in puntos[1:]:
        last = simplified[-1]
        if abs(p[0] - last[0]) > 0.01 or abs(p[1] - last[1]) > 0.01:
            simplified.append(p)

    return simplified


def route_group(elements, grupo_centro, clearance=0.3):
    """
    Enruta un grupo de elementos conectandolos en estrella desde un punto central.
    """
    rutas = []
    for elem in elements:
        origen = grupo_centro
        destino = (elem["x"], elem["y"])
        puntos = orthogonal_route(origen, destino, clearance)
        rutas.append({
            "points": puntos,
            "element": elem
        })
    return rutas


def find_center(elements):
    """Encuentra el centro geometrico de un conjunto de elementos."""
    if not elements:
        return (0, 0)
    xs = [e["x"] for e in elements if "x" in e]
    ys = [e["y"] for e in elements if "y" in e]
    if not xs or not ys:
        return (0, 0)
    return (sum(xs) / len(xs), sum(ys) / len(ys))


def auto_route_electrical(data, clearance=0.3):
    """
    Genera rutas automaticas para todos los circuitos.
    Para cada circuito, conecta todos sus componentes al tablero (TG)
    usando rutas ortogonales.
    """
    circuitos = {}

    tableros = data.get("tableros", [])
    tg = tableros[0] if tableros else {"x": 2.0, "y": 2.0}
    tg_pos = (tg["x"], tg["y"])

    for elem_type in ["luminarias", "interruptores", "tomacorrientes", "equipos"]:
        for elem in data.get(elem_type, []):
            circuit = elem.get("circuit", "C1")
            if circuit not in circuitos:
                circuitos[circuit] = []
            circuitos[circuit].append({
                "x": float(elem["x"]),
                "y": float(elem["y"]),
                "type": elem_type,
                "id": elem.get("id", ""),
                "label": f"{circuit}"
            })

    rutas = []
    ruta_id = 1

    for circuit, elements in sorted(circuitos.items()):
        if not elements:
            continue

        sorted_elems = sorted(elements, key=lambda e: math.hypot(e["x"] - tg_pos[0], e["y"] - tg_pos[1]))

        puntos_maestros = [tg_pos]
        for elem in sorted_elems:
            dest = (elem["x"], elem["y"])
            last = puntos_maestros[-1]
            segmentos = orthogonal_route(last, dest, clearance)
            for pt in segmentos[1:]:
                puntos_maestros.append(pt)

        ruta = {
            "id": f"R{ruta_id}",
            "circuit": circuit,
            "label": circuit,
            "points": [(round(p[0], 4), round(p[1], 4)) for p in puntos_maestros],
            "linetype": "DASHED"
        }
        rutas.append(ruta)
        ruta_id += 1

    data["rutas"] = rutas
    return data


def parse_args():
    parser = argparse.ArgumentParser(
        description="Genera rutas ortogonales de canalizacion electrica"
    )
    parser.add_argument("--electrical", required=True,
                       help="JSON electrico de entrada")
    parser.add_argument("--output", required=True,
                       help="JSON electrico de salida con rutas")
    parser.add_argument("--clearance", type=float, default=0.3,
                       help="Distancia de separacion de muros (m)")
    return parser.parse_args()


def main():
    args = parse_args()

    if not os.path.exists(args.electrical):
        print(f"Error: No existe {args.electrical}")
        sys.exit(1)

    data = load_json(args.electrical)
    result = auto_route_electrical(data, args.clearance)
    save_json(result, args.output)

    n_rutas = len(result.get("rutas", []))
    n_puntos = sum(len(r["points"]) for r in result.get("rutas", []))
    print(f"Rutas generadas: {n_rutas}")
    print(f"Puntos totales:  {n_puntos}")
    print(f"Salida:          {args.output}")


if __name__ == "__main__":
    main()

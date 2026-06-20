#!/usr/bin/env python3
"""
Generacion automatica de rutas ortogonales de canalizacion electrica
usando A* (A-Star) con deteccion de obstaculos.

Toma un JSON electrico y un JSON de layout arquitectonico (con muros)
y genera rutas optimizadas evitando obstaculos, viajando paralelo a muros.

Uso:
  python3 auto_routing.py --electrical electrico.json --layout layout.json --output electrico_ruteado.json
  python3 auto_routing.py --electrical electrico.json --layout layout.json --output electrico_ruteado.json --clearance 0.3 --grid-res 0.1
"""

import argparse
import json
import math
import os
import sys
from heapq import heappush, heappop
from itertools import groupby
from typing import Any, Optional


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: dict, path: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _build_obstacle_grid(
    walls: list[dict],
    rooms: list[dict],
    x_min: float,
    y_min: float,
    x_max: float,
    y_max: float,
    resolution: float = 0.1,
    wall_thickness: float = 0.15,
) -> tuple[list[list[bool]], int, int, int, int]:
    """
    Construye una grilla booleana donde True = obstaculo (muro).
    Usa Point-in-Polygon para detectar si un punto esta dentro de un muro.
    """
    cols = max(1, int(math.ceil((x_max - x_min) / resolution)))
    rows = max(1, int(math.ceil((y_max - y_min) / resolution)))

    grid = [[False] * cols for _ in range(rows)]
    half_thick = wall_thickness / 2.0

    for wall in walls:
        x1, y1 = wall.get("x1", 0), wall.get("y1", 0)
        x2, y2 = wall.get("x2", 0), wall.get("y2", 0)
        thick = wall.get("thickness", wall_thickness)
        half_t = thick / 2.0

        # Expandir el bounding box del muro
        min_gx = max(0, int((min(x1, x2) - half_t - x_min) / resolution))
        max_gx = min(cols, int((max(x1, x2) + half_t - x_min) / resolution) + 1)
        min_gy = max(0, int((min(y1, y2) - half_t - y_min) / resolution))
        max_gy = min(rows, int((max(y1, y2) + half_t - y_min) / resolution) + 1)

        for gy in range(min_gy, max_gy):
            for gx in range(min_gx, max_gx):
                px = x_min + gx * resolution
                py = y_min + gy * resolution
                # Distancia punto a segmento de recta
                d = _point_segment_distance(px, py, x1, y1, x2, y2)
                if d <= half_t:
                    grid[gy][gx] = True

    return grid, cols, rows, int(x_min / resolution), int(y_min / resolution)


def _point_segment_distance(px: float, py: float, x1: float, y1: float, x2: float, y2: float) -> float:
    """Distancia minima de un punto a un segmento."""
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)
    t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
    proj_x = x1 + t * dx
    proj_y = y1 + t * dy
    return math.hypot(px - proj_x, py - proj_y)


def _grid_to_world(gx: int, gy: int, x_min: float, y_min: float, resolution: float) -> tuple[float, float]:
    return (x_min + gx * resolution, y_min + gy * resolution)


def _world_to_grid(wx: float, wy: float, x_min: float, y_min: float, resolution: float) -> tuple[int, int]:
    return (int(round((wx - x_min) / resolution)), int(round((wy - y_min) / resolution)))


def _astar(
    grid: list[list[bool]],
    start: tuple[int, int],
    goal: tuple[int, int],
    cols: int,
    rows: int,
    clearance_cells: int = 3,
) -> Optional[list[tuple[int, int]]]:
    """
    A* pathfinding sobre grilla booleana.
    Retorna la ruta como lista de (gx, gy) o None si no hay camino.
    """
    if not (0 <= start[0] < cols and 0 <= start[1] < rows):
        return None
    if not (0 <= goal[0] < cols and 0 <= goal[1] < rows):
        return None
    if grid[start[1]][start[0]] or grid[goal[1]][goal[0]]:
        return None

    def heuristic(a: tuple[int, int], b: tuple[int, int]) -> float:
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def neighbors(node: tuple[int, int]) -> list[tuple[int, int]]:
        x, y = node
        result = []
        # Movimientos ortogonales y diagonales
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and not grid[ny][nx]:
                # Verificar clearance alrededor
                blocked = False
                for cy in range(max(0, ny - clearance_cells), min(rows, ny + clearance_cells + 1)):
                    for cx in range(max(0, nx - clearance_cells), min(cols, nx + clearance_cells + 1)):
                        if grid[cy][cx]:
                            blocked = True
                            break
                    if blocked:
                        break
                if not blocked:
                    result.append((nx, ny))
        return result

    open_set: list = []
    heappush(open_set, (0, start))
    came_from: dict[tuple[int, int], Optional[tuple[int, int]]] = {start: None}
    g_score: dict[tuple[int, int], float] = {start: 0}
    f_score: dict[tuple[int, int], float] = {start: heuristic(start, goal)}

    while open_set:
        current = heappop(open_set)[1]
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for neighbor in neighbors(current):
            dx = neighbor[0] - current[0]
            dy = neighbor[1] - current[1]
            move_cost = 1.0 if dx == 0 or dy == 0 else 1.414  # ortogonal = 1, diagonal = sqrt(2)
            tentative_g = g_score[current] + move_cost

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)
                f_score[neighbor] = f
                heappush(open_set, (f, neighbor))

    return None


def _simplify_path(world_path: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Simplifica ruta eliminando vertices colineales y puntos intermedios redundantes."""
    if len(world_path) <= 2:
        return world_path

    simplified = [world_path[0]]
    for i in range(1, len(world_path) - 1):
        prev = simplified[-1]
        curr = world_path[i]
        nxt = world_path[i + 1]

        # Si el angulo entre segmentos es ~180 grados, es colineal
        v1 = (curr[0] - prev[0], curr[1] - prev[1])
        v2 = (nxt[0] - curr[0], nxt[1] - curr[1])
        dot = v1[0] * v2[0] + v1[1] * v2[1]
        mag1 = math.hypot(*v1)
        mag2 = math.hypot(*v2)
        if mag1 > 0 and mag2 > 0:
            cos_angle = dot / (mag1 * mag2)
            if abs(cos_angle) < 0.999:  # no colineal
                simplified.append(curr)

    simplified.append(world_path[-1])
    return simplified


def _snap_to_grid(value: float, resolution: float = 0.05) -> float:
    """Redondea a la rejilla."""
    return round(value / resolution) * resolution


def auto_route_electrical(
    electrical_data: dict,
    layout_data: Optional[dict] = None,
    clearance: float = 0.3,
    resolution: float = 0.1,
) -> dict:
    """
    Genera rutas automaticas para todos los circuitos usando A*.
    Si hay datos de layout, usa los muros como obstaculos.
    """
    # Extraer paredes del layout
    walls = []
    rooms = []
    if layout_data:
        walls = layout_data.get("walls", []) or layout_data.get("muros", [])
        rooms = layout_data.get("rooms", []) or layout_data.get("ambientes", [])

    # Calcular bounding box del layout
    all_x, all_y = [], []
    if walls:
        for w in walls:
            all_x.extend([w.get("x1", 0), w.get("x2", 0)])
            all_y.extend([w.get("y1", 0), w.get("y2", 0)])
    if rooms:
        for r in rooms:
            pts = r.get("points", []) or r.get("puntos", [])
            for p in pts:
                all_x.append(p[0] if isinstance(p, (list, tuple)) else p.get("x", 0))
                all_y.append(p[1] if isinstance(p, (list, tuple)) else p.get("y", 0))

    # Desde los componentes electricos
    for elem_type in ["luminarias", "interruptores", "tomacorrientes", "equipos", "tableros", "medidores"]:
        for elem in electrical_data.get(elem_type, []):
            all_x.append(float(elem.get("x", 0)))
            all_y.append(float(elem.get("y", 0)))

    if not all_x:
        all_x, all_y = [0, 10], [0, 10]

    x_min, x_max = min(all_x) - 1.0, max(all_x) + 1.0
    y_min, y_max = min(all_y) - 1.0, max(all_y) + 1.0

    # Construir grilla de obstaculos
    grid, cols, rows, ox, oy = _build_obstacle_grid(
        walls, rooms, x_min, y_min, x_max, y_max, resolution
    )
    clearance_cells = max(1, int(clearance / resolution))

    # Encontrar TG
    tableros = electrical_data.get("tableros", [])
    tg = tableros[0] if tableros else {"x": 2.0, "y": 2.0}
    tg_pos = (float(tg["x"]), float(tg["y"]))

    # Agrupar componentes por circuito
    circuitos: dict[str, list[dict]] = {}
    for elem_type in ["luminarias", "interruptores", "tomacorrientes", "equipos"]:
        for elem in electrical_data.get(elem_type, []):
            circuit = elem.get("circuit", "C1")
            if circuit not in circuitos:
                circuitos[circuit] = []
            circuitos[circuit].append({
                "x": float(elem["x"]),
                "y": float(elem["y"]),
                "type": elem_type,
                "id": elem.get("id", ""),
                "label": f"{circuit}",
                "z": float(elem.get("z", 0)),
            })

    rutas = []
    ruta_id = 1

    for circuit, elements in sorted(circuitos.items()):
        if not elements:
            continue

        # Ordenar por distancia al TG (mas cercano primero)
        sorted_elems = sorted(
            elements,
            key=lambda e: math.hypot(e["x"] - tg_pos[0], e["y"] - tg_pos[1]),
        )

        # Generar ruta principal que visita todos los puntos en orden
        puntos_ruta = [tg_pos]
        for elem in sorted_elems:
            dest = (elem["x"], elem["y"])
            origin = puntos_ruta[-1]

            # A* entre el ultimo punto y el destino
            sx, sy = _world_to_grid(origin[0], origin[1], x_min, y_min, resolution)
            gx, gy = _world_to_grid(dest[0], dest[1], x_min, y_min, resolution)
            sx = max(0, min(cols - 1, sx))
            sy = max(0, min(rows - 1, sy))
            gx = max(0, min(cols - 1, gx))
            gy = max(0, min(rows - 1, gy))

            astar_path = _astar(grid, (sx, sy), (gx, gy), cols, rows, clearance_cells)

            if astar_path:
                world_segment = []
                for px, py in astar_path[1:]:
                    wx = _snap_to_grid(x_min + px * resolution)
                    wy = _snap_to_grid(y_min + py * resolution)
                    world_segment.append((wx, wy))
                puntos_ruta.extend(world_segment)
            else:
                # Fallback: ruta ortogonal simple
                puntos_ruta.append(dest)

        # Optimizar ruta: eliminar colineales
        puntos_ruta = _simplify_path(puntos_ruta)

        ruta = {
            "id": f"R{ruta_id}",
            "circuit": circuit,
            "label": circuit,
            "points": [(round(p[0], 4), round(p[1], 4)) for p in puntos_ruta],
            "linetype": "DASHED",
            "total_length_m": round(sum(
                math.hypot(puntos_ruta[i][0] - puntos_ruta[i - 1][0],
                           puntos_ruta[i][1] - puntos_ruta[i - 1][1])
                for i in range(1, len(puntos_ruta))
            ), 2),
        }
        rutas.append(ruta)
        ruta_id += 1

    electrical_data["rutas"] = rutas
    electrical_data["_routing_metadata"] = {
        "grid_cols": cols,
        "grid_rows": rows,
        "x_min": round(x_min, 2),
        "y_min": round(y_min, 2),
        "x_max": round(x_max, 2),
        "y_max": round(y_max, 2),
        "resolution": resolution,
        "clearance": clearance,
        "obstacle_cells": sum(row.count(True) for row in grid),
        "total_cells": cols * rows,
        "algorithm": "A*",
    }
    return electrical_data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera rutas ortogonales de canalizacion electrica con A* evitando obstaculos"
    )
    parser.add_argument("--electrical", required=True, help="JSON electrico de entrada")
    parser.add_argument("--layout", default=None, help="JSON de layout arquitectonico (opcional, para obstaculos)")
    parser.add_argument("--output", required=True, help="JSON electrico de salida con rutas")
    parser.add_argument("--clearance", type=float, default=0.3, help="Distancia de separacion de muros (m)")
    parser.add_argument("--grid-res", type=float, default=0.1, help="Resolucion de la grilla A* (m)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not os.path.exists(args.electrical):
        print(f"Error: No existe {args.electrical}")
        sys.exit(1)

    electrical_data = load_json(args.electrical)
    layout_data = None
    if args.layout:
        if os.path.exists(args.layout):
            layout_data = load_json(args.layout)
            print(f"Layout cargado: {args.layout}")
        else:
            print(f"Advertencia: No existe layout {args.layout}, se usara A* sin obstaculos")

    result = auto_route_electrical(electrical_data, layout_data, args.clearance, args.grid_res)
    save_json(result, args.output)

    n_rutas = len(result.get("rutas", []))
    n_puntos = sum(len(r["points"]) for r in result.get("rutas", []))
    total_length = sum(r.get("total_length_m", 0) for r in result.get("rutas", []))
    meta = result.get("_routing_metadata", {})

    print(f"Rutas generadas:          {n_rutas}")
    print(f"Puntos totales:           {n_puntos}")
    print(f"Longitud total de rutas:  {total_length:.2f} m")
    print(f"Grilla:                   {meta.get('grid_cols', 0)}x{meta.get('grid_rows', 0)}")
    print(f"Celdas obstaculo:         {meta.get('obstacle_cells', 0)}/{meta.get('total_cells', 0)}")
    print(f"Algoritmo:                {meta.get('algorithm', 'N/A')}")
    print(f"Salida:                   {args.output}")


if __name__ == "__main__":
    main()

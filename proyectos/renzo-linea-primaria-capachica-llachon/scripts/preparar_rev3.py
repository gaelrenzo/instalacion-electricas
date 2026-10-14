"""Conciliación geométrica y sitios de replanteo Rev. 3; nunca postes aprobados."""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

from lxml import etree
from pyproj import Geod, Transformer
from shapely.geometry import LineString, Point

ROOT = Path(__file__).resolve().parents[1]
KML = ROOT / "sources/ruta topografica capachica llachon.kml"
GIS = ROOT / "derived/route.json"
STRUCTURES = ROOT / "sources/gisem_mt_estructuras.geojson"
OSM = ROOT / "sources/osm_roads.json"
TO_UTM = Transformer.from_crs(4326, 32719, always_xy=True)
TO_GEO = Transformer.from_crs(32719, 4326, always_xy=True)
GEOD = Geod(ellps="WGS84")
SIMPLIFY_M = 10.0  # Filtro cartográfico, no criterio de vano.
TURN_DEG = 20.0  # Filtro de búsqueda de vértices, no selección de estructura.
GIS_SEARCH_M = 25.0  # Radio de cotejo cartográfico, no tolerancia topográfica.


def read_kml(path: Path = KML) -> list[dict]:
    if not path.is_file():
        raise FileNotFoundError(f"KML obligatorio ausente: {path}")
    tree = etree.parse(str(path))
    ns = {"k": "http://www.opengis.net/kml/2.2"}
    lines = []
    for mark in tree.xpath("//k:Placemark", namespaces=ns):
        name = mark.findtext("{http://www.opengis.net/kml/2.2}name") or "sin nombre"
        for node in mark.xpath(".//k:LineString/k:coordinates", namespaces=ns):
            geo = [tuple(float(x) for x in token.split(",")[:2]) for token in node.text.split()]
            if len(geo) < 2 or any(not (math.isfinite(lon) and math.isfinite(lat)
                    and -180 <= lon <= 180 and -90 <= lat <= 90) for lon, lat in geo):
                raise ValueError(f"Coordenadas KML inválidas en {name}")
            xy = [TO_UTM.transform(*p) for p in geo]
            line = LineString(xy)
            if line.length <= 0 or not line.is_simple:
                raise ValueError(f"Geometría inválida en {name}")
            lines.append({"name": name, "geo": geo, "xy": xy, "line": line})
    if len(lines) != 4:
        raise ValueError(f"Se esperaban 4 segmentos KML, hay {len(lines)}")
    return lines


def signed_turn(a, b, c) -> float:
    u = (b[0]-a[0], b[1]-a[1]); v = (c[0]-b[0], c[1]-b[1])
    if min(math.hypot(*u), math.hypot(*v)) < .01:
        return 0.0
    return math.degrees(math.atan2(u[0]*v[1]-u[1]*v[0], u[0]*v[0]+u[1]*v[1]))


def geometry_audit(lines: list[dict], gis: dict) -> tuple[dict, list[dict]]:
    axis = LineString(gis["route_utm_xy"])
    if not axis.is_simple or axis.length <= 0:
        raise ValueError("Corredor GIS derivado inválido")
    if abs(axis.length-float(gis["route_length_m"])) > .05:
        raise ValueError("Longitud GIS declarada no coincide con su geometría")
    segments, gaps, cumulative = [], [], 0.0
    for i, item in enumerate(lines, 1):
        line = item["line"]
        start, end = Point(item["xy"][0]), Point(item["xy"][-1])
        offsets = sorted(axis.distance(Point(p)) for p in item["xy"])
        segments.append({"segmento": i, "nombre": item["name"], "vertices": len(item["xy"]),
                         "longitud_kml_utm_m": round(line.length, 6),
                         "longitud_kml_geodesica_m": round(GEOD.line_length(*zip(*item["geo"])), 6),
                         "estacion_inicio_kml_m": round(cumulative, 6),
                         "estacion_fin_kml_m": round(cumulative+line.length, 6),
                         "proyeccion_inicio_gis_m": round(axis.project(start), 6),
                         "proyeccion_fin_gis_m": round(axis.project(end), 6),
                         "separacion_inicio_gis_m": round(axis.distance(start), 6),
                         "separacion_fin_gis_m": round(axis.distance(end), 6),
                         "separacion_mediana_vertices_gis_m": round(offsets[len(offsets)//2], 6),
                         "separacion_max_vertices_gis_m": round(offsets[-1], 6)})
        cumulative += line.length
        if i < len(lines):
            p, q = end, Point(lines[i]["xy"][0])
            crossing = line.intersection(lines[i]["line"])
            gaps.append({"id": f"GAP-{i}", "segmento_origen": i,
                         "estacion_fin_origen_m": round(cumulative, 6),
                         "lon_fin_origen": item["geo"][-1][0], "lat_fin_origen": item["geo"][-1][1],
                         "lon_inicio_siguiente": lines[i]["geo"][0][0],
                         "lat_inicio_siguiente": lines[i]["geo"][0][1],
                         "distancia_recta_m": round(p.distance(q), 6),
                         "avance_proyectado_gis_m": round(axis.project(q)-axis.project(p), 6),
                         "interseccion_puntual": crossing.geom_type == "Point",
                         "sobrante_hasta_cruce_origen_m": (round(line.length-line.project(crossing), 6)
                                                           if crossing.geom_type == "Point" else ""),
                         "avance_desde_inicio_a_cruce_siguiente_m": (round(lines[i]["line"].project(crossing), 6)
                                                                     if crossing.geom_type == "Point" else ""),
                         "estado": "trazo entre extremos no levantado; verificar continuidad y sentido"})
    total_gap = sum(g["distancia_recta_m"] for g in gaps)
    delta = cumulative-axis.length
    published_delta = round(cumulative, 3)-float(gis["route_length_m"])
    published_gap = sum(round(g["distancia_recta_m"], 3) for g in gaps)
    report = {"crs_entrada": "KML WGS84 longitud,latitud; altitud 0 no usada",
              "crs_metrico": "EPSG:32719", "kml_sha256": hashlib.sha256(KML.read_bytes()).hexdigest(),
              "gis_sha256": hashlib.sha256(GIS.read_bytes()).hexdigest(),
              "longitud_kml_sin_empalmes_m": round(cumulative, 6),
              "longitud_gis_m": round(axis.length, 6),
              "diferencia_ejes_m": round(delta, 6),
              "diferencia_publicada_rev2_m": round(published_delta, 3),
              "suma_brechas_rectas_m": round(total_gap, 6),
              "suma_brechas_publicada_rev2_m": round(published_gap, 3),
              "resta_publicada_rev2_no_atribuible_m": round(published_delta-published_gap, 3),
              "resta_aritmetica_no_atribuible_m": round(delta-total_gap, 6),
              "kml_mas_uniones_rectas_no_validado_m": round(cumulative+total_gap, 6),
              "diferencia_hipotetica_con_uniones_rectas_m": round(delta+total_gap, 6),
              "metodo": "Sumas UTM; brechas son cuerdas rectas, no eje verificado",
              "segmentos": segments, "brechas": gaps}
    return report, gaps


def site_candidates(lines: list[dict], features: list[dict]) -> list[dict]:
    structures = [(Point(TO_UTM.transform(*f["geometry"]["coordinates"][:2])),
                   f["properties"].get("CODESTRUCTURA", "")) for f in features]
    result, offset = [], 0.0
    for segment, item in enumerate(lines, 1):
        source = item["line"]
        simplified = list(source.simplify(SIMPLIFY_M, preserve_topology=True).coords)
        if any(p not in set(item["xy"]) for p in simplified):
            raise ValueError("La simplificación creó coordenadas ajenas al KML")
        for j, xy in enumerate(simplified):
            turn = signed_turn(*simplified[j-1:j+2]) if 0 < j < len(simplified)-1 else 0.0
            if 0 < j < len(simplified)-1 and abs(turn) < TURN_DEG:
                continue
            if segment == 1 and j == 0:
                role = "inicio de corredor; conexión candidata no aprobada"
            elif segment == len(lines) and j == len(simplified)-1:
                role = "fin de corredor; terminal por confirmar"
            elif j in (0, len(simplified)-1):
                role = "extremo de segmento; empalme a replantear"
            else:
                role = "cambio de dirección geométrico"
            p = Point(xy)
            nearest, code = min(structures, key=lambda s: s[0].distance(p))
            distance = nearest.distance(p)
            lon, lat = TO_GEO.transform(*xy)
            relationship = ("estructura GIS cercana; cotejar reutilización" if distance <= GIS_SEARCH_M
                            else "sin estructura GIS cercana en filtro cartográfico")
            result.append({"id": "", "clase_registro": "sitio geométrico para evaluar apoyo nuevo",
                           "segmento": segment, "progresiva_kml_m": round(offset+source.project(p), 3),
                           "latitud": round(lat, 9), "longitud": round(lon, 9),
                           "este_utm19s_m": round(xy[0], 3), "norte_utm19s_m": round(xy[1], 3),
                           "funcion_preliminar": role,
                           "deflexion_geometrica_grados": round(turn, 2) if turn else "",
                           "justificacion": f"vértice KML retenido con simplificación {SIMPLIFY_M:g} m; giro ≥{TURN_DEG:g}° o extremo",
                           "estructura_gis_mas_cercana": code, "separacion_gis_m": round(distance, 3),
                           "relacion_gis": relationship,
                           "restricciones": "empalmes; topografía; vanos/flecha; despejes; acceso; suelo; servidumbre; titularidad",
                           "fuente": KML.name + "; " + STRUCTURES.name,
                           "confianza": "baja (solo gabinete)",
                           "estado_validacion": "no replanteado; no instalar",
                           "observaciones_campo": ""})
        offset += source.length
    result.sort(key=lambda x: (x["progresiva_kml_m"], x["segmento"]))
    for i, row in enumerate(result, 1):
        row["id"] = f"PN-{i:03d}"
    return result


def road_crossings(lines: list[dict], osm: dict) -> list[dict]:
    result, offset = [], 0.0
    from shapely.geometry import MultiPoint
    for segment, item in enumerate(lines, 1):
        for way in osm.get("elements", []):
            if way.get("type") != "way" or len(way.get("geometry", [])) < 2:
                continue
            road = LineString([TO_UTM.transform(p["lon"], p["lat"]) for p in way["geometry"]])
            hit = item["line"].intersection(road)
            points = [hit] if hit.geom_type == "Point" else (
                list(hit.geoms) if hit.geom_type == "MultiPoint" else [])
            for point in points:
                lon, lat = TO_GEO.transform(point.x, point.y)
                tags = way.get("tags", {})
                result.append({"id": "", "segmento": segment,
                               "progresiva_kml_m": round(offset+item["line"].project(point), 3),
                               "latitud": round(lat, 9), "longitud": round(lon, 9),
                               "este_utm19s_m": round(point.x, 3),
                               "norte_utm19s_m": round(point.y, 3),
                               "osm_way_id": way["id"], "highway_osm": tags.get("highway", ""),
                               "nombre_osm": tags.get("name", ""),
                               "fuente": "sources/osm_roads.json; geometría comunitaria",
                               "medir_en_campo": "tipo/anchura de vía, cotas, cruce real, gálibo, servidumbre y permiso",
                               "estado": "indicio geométrico; no verificado"})
        offset += item["line"].length
    result.sort(key=lambda x: (x["progresiva_kml_m"], x["osm_way_id"]))
    for i, row in enumerate(result, 1):
        row["id"] = f"CV-{i:03d}"
    return result


def write_csv(path: Path, rows: list[dict]):
    if path.exists():
        raise FileExistsError(f"Salida Rev. 3 existente: {path}")
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)


def data_register(report: dict, candidates: list[dict], crossings: list[dict]) -> dict:
    pending = json.loads((ROOT/"datos/parametros_diseno_pendientes.json").read_text(encoding="utf-8"))
    with (ROOT/"datos/ubicaciones_postes_preliminares.csv").open(encoding="utf-8-sig", newline="") as f:
        gis_count = len(list(csv.DictReader(f)))
    def item(value, unit, source, note):
        return {"valor": value, "unidad": unit, "fuente": source, "nota": note}
    return {
        "confirmados": {
            "kml_sha256": item(report["kml_sha256"], None, KML.name, "identidad documental; sin validación de campo"),
            "segmentos_kml": item(4, "líneas", KML.name, "estructura del archivo"),
            "vertices_kml": item(sum(s["vertices"] for s in report["segmentos"]), "vértices",
                                KML.name, "estructura del archivo"),
            "codigo_tmt": item("TMT001868169", None, "sources/gisem_mt_tramos.geojson",
                               "capa de tramos; no conexión aprobada"),
        },
        "calculados": {
            key: item(report[key], "m", "derived/reconciliacion_corredores_rev3.json",
                      "geometría cartográfica UTM 19S; no metrado de obra")
            for key in ("longitud_kml_sin_empalmes_m", "longitud_gis_m",
                        "diferencia_ejes_m", "suma_brechas_rectas_m")
        },
        "estimados": {
            "sitios_geometricos_replanteo": item(len(candidates), "sitios",
                "datos/candidatos_nuevos_replanteo_rev3.csv",
                "filtros de gabinete de 10 m y 20 grados; no postes aprobados"),
            "estructuras_gis_proximas": item(gis_count, "puntos",
                "datos/ubicaciones_postes_preliminares.csv",
                "inventario cartográfico con radio de 25 m"),
            "intersecciones_viales_osm": item(len(crossings), "alertas",
                "datos/cruces_viales_rev3.csv",
                "intersecciones geométricas no verificadas en campo"),
        },
        "pendientes_validacion": {
            key: item(None, None, "datos/parametros_diseno_pendientes.json",
                      "solicitar a Electro Puno o levantar en campo")
            for key in pending["design_inputs_required"]
        },
    }


def main():
    lines = read_kml()
    report, gaps = geometry_audit(lines, json.loads(GIS.read_text(encoding="utf-8")))
    features = json.loads(STRUCTURES.read_text(encoding="utf-8"))["features"]
    candidates = site_candidates(lines, features)
    crossings = road_crossings(lines, json.loads(OSM.read_text(encoding="utf-8")))
    outputs = [ROOT/"derived/reconciliacion_corredores_rev3.json",
               ROOT/"datos/empalmes_kml_rev3.csv", ROOT/"datos/candidatos_nuevos_replanteo_rev3.csv",
               ROOT/"datos/registro_datos_rev3.json", ROOT/"datos/cruces_viales_rev3.csv"]
    if any(p.exists() for p in outputs):
        raise FileExistsError("Salidas Rev. 3 presentes; archívelas antes de regenerar")
    outputs[0].write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    write_csv(outputs[1], gaps)
    write_csv(outputs[2], candidates)
    outputs[3].write_text(json.dumps(data_register(report, candidates, crossings), ensure_ascii=False, indent=2)+"\n",
                          encoding="utf-8")
    write_csv(outputs[4], crossings)
    print(json.dumps({"diferencia_m": report["diferencia_ejes_m"],
                      "brechas_m": report["suma_brechas_rectas_m"],
                      "residuo_aritmetico_m": report["resta_aritmetica_no_atribuible_m"],
                      "sitios_geometricos": len(candidates),
                      "indicios_viales_osm": len(crossings)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

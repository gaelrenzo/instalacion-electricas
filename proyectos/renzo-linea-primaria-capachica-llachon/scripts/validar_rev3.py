"""Validación de software Rev. 3; no certifica condiciones eléctricas ni de campo."""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import yaml
from shapely.geometry import Point

from preparar_rev3 import ROOT, GIS, KML, OSM, STRUCTURES, TO_UTM, read_kml


def rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def validate_payload(lines: list[dict], report: dict, gaps: list[dict],
                     candidates: list[dict], register: dict, codes: set[str]) -> list[str]:
    errors = []
    def require(condition: bool, message: str):
        if not condition: errors.append(message)
    length = sum(x["line"].length for x in lines)
    require(abs(float(report.get("longitud_kml_sin_empalmes_m", -1))-length) < .005,
            "longitud KML inconsistente")
    require(report.get("kml_sha256") == hashlib.sha256(KML.read_bytes()).hexdigest(),
            "SHA KML no coincide")
    require(report.get("gis_sha256") == hashlib.sha256(GIS.read_bytes()).hexdigest(),
            "SHA GIS no coincide")
    require(len(gaps) == len(lines)-1, "tabla de empalmes incompleta")
    for i, (left, right) in enumerate(zip(lines, lines[1:]), 1):
        if i > len(gaps): break
        gap = gaps[i-1]
        actual = Point(left["xy"][-1]).distance(Point(right["xy"][0]))
        require(gap.get("id") == f"GAP-{i}" and abs(float(gap["distancia_recta_m"])-actual) < .005,
                f"empalme {i} inconsistente")
        require(actual > 0, f"empalme {i} cambió a continuidad; revisar revisión")
    ids = [p.get("id") for p in candidates]
    require(len(ids) == len(set(ids)) and all(x and x.startswith("PN-") for x in ids),
            "identificadores de candidatos incompletos/duplicados")
    require(len(candidates) > 0, "tabla de sitios vacía")
    previous = -math.inf
    required_columns = {"id", "segmento", "progresiva_kml_m", "latitud", "longitud",
                        "este_utm19s_m", "norte_utm19s_m", "funcion_preliminar",
                        "justificacion", "restricciones", "estado_validacion",
                        "estructura_gis_mas_cercana", "fuente"}
    for p in candidates:
        require(required_columns <= p.keys() and all(p.get(k) not in ("", None) for k in required_columns),
                f"fila {p.get('id')} incompleta")
        try:
            segment = int(p["segmento"])
            station = float(p["progresiva_kml_m"])
            lon, lat = float(p["longitud"]), float(p["latitud"])
            x, y = float(p["este_utm19s_m"]), float(p["norte_utm19s_m"])
        except (ValueError, KeyError):
            errors.append(f"fila {p.get('id')} con números inválidos")
            continue
        require(1 <= segment <= len(lines), f"segmento inválido en {p['id']}")
        require(station >= previous, f"progresiva no monótona en {p['id']}")
        previous = station
        require(-70 < lon < -69 and -16 < lat < -15, f"coordenadas geográficas fuera de zona en {p['id']}")
        px, py = TO_UTM.transform(lon, lat)
        require(math.hypot(px-x, py-y) < .02, f"coordenadas UTM/geográficas inconsistentes en {p['id']}")
        if 1 <= segment <= len(lines):
            require(lines[segment-1]["line"].distance(Point(x,y)) < .02,
                    f"sitio fuera del KML en {p['id']}")
        require(p["estructura_gis_mas_cercana"] in codes, f"código GIS no referenciado en {p['id']}")
        require(p["estado_validacion"] == "no replanteado; no instalar",
                f"estado de ingeniería indebidamente avanzado en {p['id']}")
    require(set(register) == {"confirmados", "calculados", "estimados", "pendientes_validacion"},
            "clasificación de datos incompleta")
    require(all(v.get("valor") is None for v in register.get("pendientes_validacion", {}).values()),
            "parámetro pendiente con valor ficticio")
    require(all(v.get("fuente") for group in register.values() for v in group.values()),
            "dato sin procedencia")
    return errors


def validate_references(config: dict, root: Path = ROOT) -> list[str]:
    errors = []
    for key in ("memoria", "calculos", "matriz_normativa", "parametros_diseno",
                "metodologia_postes", "solicitud_operador", "plan_campo",
                "auditoria_planos", "bloqueos", "informe_revision",
                "registro_datos", "reconciliacion_corredores"):
        value = config.get(key)
        if not isinstance(value, str) or not (root/value).is_file():
            errors.append(f"referencia proyecto.yaml ausente: {key}={value}")
    for key in ("planos", "vistas"):
        for value in config.get(key, []):
            if not (root/value).is_file():
                errors.append(f"referencia proyecto.yaml ausente: {value}")
    return errors


def validate_crossings(lines: list[dict], crossings: list[dict], osm_ids: set[int]) -> list[str]:
    errors = []
    ids = [c.get("id") for c in crossings]
    if len(ids) != len(set(ids)) or not all(x and x.startswith("CV-") for x in ids):
        errors.append("identificadores de cruces incompletos/duplicados")
    previous = -math.inf
    for c in crossings:
        try:
            segment, station = int(c["segmento"]), float(c["progresiva_kml_m"])
            x, y = float(c["este_utm19s_m"]), float(c["norte_utm19s_m"])
            lon, lat = float(c["longitud"]), float(c["latitud"])
            way = int(c["osm_way_id"])
        except (ValueError, KeyError):
            errors.append(f"cruce {c.get('id')} incompleto")
            continue
        if not 1 <= segment <= len(lines):
            errors.append(f"segmento de cruce inválido: {c['id']}")
            continue
        if station < previous: errors.append(f"progresiva de cruce no monótona: {c['id']}")
        previous = station
        if way not in osm_ids: errors.append(f"vía OSM no referenciada: {c['id']}")
        if lines[segment-1]["line"].distance(Point(x, y)) > .02:
            errors.append(f"cruce fuera del KML: {c['id']}")
        px, py = TO_UTM.transform(lon, lat)
        if math.hypot(px-x, py-y) > .02:
            errors.append(f"coordenadas de cruce inconsistentes: {c['id']}")
        if c.get("estado") != "indicio geométrico; no verificado":
            errors.append(f"cruce afirmado como verificado: {c['id']}")
    return errors


def validate_files() -> dict:
    lines = read_kml()
    base = ROOT/"derived/reconciliacion_corredores_rev3.json"
    report = json.loads(base.read_text(encoding="utf-8"))
    gaps = rows(ROOT/"datos/empalmes_kml_rev3.csv")
    candidates = rows(ROOT/"datos/candidatos_nuevos_replanteo_rev3.csv")
    crossings = rows(ROOT/"datos/cruces_viales_rev3.csv")
    register = json.loads((ROOT/"datos/registro_datos_rev3.json").read_text(encoding="utf-8"))
    codes = {f["properties"]["CODESTRUCTURA"] for f in
             json.loads(STRUCTURES.read_text(encoding="utf-8"))["features"]}
    errors = validate_payload(lines, report, gaps, candidates, register, codes)
    osm_ids = {e["id"] for e in json.loads(OSM.read_text(encoding="utf-8"))["elements"]
               if e.get("type") == "way"}
    errors.extend(validate_crossings(lines, crossings, osm_ids))
    if register["estimados"]["intersecciones_viales_osm"]["valor"] != len(crossings):
        errors.append("registro de datos no coincide con cruces")
    config = yaml.safe_load((ROOT/"proyecto.yaml").read_text(encoding="utf-8"))
    errors.extend(validate_references(config))
    if errors:
        raise ValueError("Validación de software Rev. 3 falló:\n- " + "\n- ".join(errors))
    return {"kml_m": report["longitud_kml_sin_empalmes_m"], "gaps": len(gaps),
            "sitios": len(candidates), "cruces_osm": len(crossings),
            "entradas_pendientes": len(register["pendientes_validacion"]),
            "software_validado": True, "ingenieria_validada": False}


if __name__ == "__main__":
    print(json.dumps(validate_files(), ensure_ascii=False))

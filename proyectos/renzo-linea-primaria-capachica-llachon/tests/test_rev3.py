import copy
import csv
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"scripts"))
from preparar_rev3 import GIS, OSM, STRUCTURES, geometry_audit, read_kml, road_crossings, site_candidates
from validar_rev3 import validate_crossings, validate_files, validate_payload, validate_references


def samples():
    lines = read_kml()
    report, gaps = geometry_audit(lines, json.loads(GIS.read_text(encoding="utf-8")))
    features = json.loads(STRUCTURES.read_text(encoding="utf-8"))["features"]
    sites = site_candidates(lines, features)
    register = {
        "confirmados": {"source": {"valor": "KML", "fuente": "source"}},
        "calculados": {"length": {"valor": report["longitud_kml_sin_empalmes_m"], "fuente": "KML"}},
        "estimados": {"sites": {"valor": len(sites), "fuente": "KML"}},
        "pendientes_validacion": {"voltage": {"valor": None, "fuente": "Electro Puno"}},
    }
    codes = {f["properties"]["CODESTRUCTURA"] for f in features}
    return lines, report, gaps, sites, register, codes


def test_discontinuidades_y_restas_no_son_tramos():
    lines, report, gaps, sites, register, codes = samples()
    assert len(gaps) == 3
    assert report["diferencia_publicada_rev2_m"] == pytest.approx(105.482, abs=.001)
    assert report["resta_publicada_rev2_no_atribuible_m"] == pytest.approx(40.405, abs=.001)
    assert report["diferencia_hipotetica_con_uniones_rectas_m"] > report["diferencia_ejes_m"]
    assert gaps[-1]["interseccion_puntual"] is True
    assert validate_payload(lines, report, gaps, sites, register, codes) == []
    assert any("tabla de empalmes incompleta" in x for x in
               validate_payload(lines, report, gaps[:-1], sites, register, codes))


@pytest.mark.parametrize("mutation,expected", [
    (lambda d: d[1].update(longitud_kml_sin_empalmes_m=1), "longitud KML inconsistente"),
    (lambda d: d[3][0].update(longitud="-68.0"), "coordenadas geográficas fuera de zona"),
    (lambda d: d[3][0].update(este_utm19s_m="0"), "coordenadas UTM/geográficas inconsistentes"),
    (lambda d: d[3][0].update(justificacion=""), "incompleta"),
    (lambda d: d[3][0].update(estructura_gis_mas_cercana="NMT_NO_EXISTE"), "código GIS no referenciado"),
    (lambda d: d[4]["pendientes_validacion"]["voltage"].update(valor=22.9), "valor ficticio"),
])
def test_detecta_corrupciones(mutation, expected):
    data = list(copy.deepcopy(samples()))
    mutation(data)
    assert any(expected in error for error in validate_payload(*data))


def test_archivos_y_referencias_rev3():
    result = validate_files()
    assert result["software_validado"] and not result["ingenieria_validada"]
    assert result["gaps"] == 3 and result["sitios"] >= 8
    with (ROOT/"datos/candidatos_nuevos_replanteo_rev3.csv").open(encoding="utf-8-sig", newline="") as f:
        new = list(csv.DictReader(f))
    with (ROOT/"datos/ubicaciones_postes_preliminares.csv").open(encoding="utf-8-sig", newline="") as f:
        existing = list(csv.DictReader(f))
    assert not ({p["id"] for p in new} & {p["id"] for p in existing})
    assert all(p["clase_registro"] == "sitio geométrico para evaluar apoyo nuevo" for p in new)
    assert "inicio de corredor" in new[0]["funcion_preliminar"]
    assert "fin de corredor" in new[-1]["funcion_preliminar"]


def test_referencia_cruzada_incorrecta():
    import yaml
    config = yaml.safe_load((ROOT/"proyecto.yaml").read_text(encoding="utf-8"))
    config["memoria"] = "documentacion/no_existe.md"
    assert any("memoria" in error for error in validate_references(config))


def test_cruces_osm_y_coordenadas():
    lines = read_kml()
    osm = json.loads(OSM.read_text(encoding="utf-8"))
    crossings = road_crossings(lines, osm)
    codes = {e["id"] for e in osm["elements"] if e.get("type") == "way"}
    assert len(crossings) == 44
    assert validate_crossings(lines, crossings, codes) == []
    bad = copy.deepcopy(crossings)
    bad[0]["osm_way_id"] = -1
    assert any("no referenciada" in e for e in validate_crossings(lines, bad, codes))

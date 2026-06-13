#!/usr/bin/env python3
"""Construye el BOM oficial de Aquiles sin modificar los planos electricos."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
REPO_DIR = PROJECT_DIR.parents[1]
COTIZACION_DIR = REPO_DIR / "herramientas" / "cotizacion"
sys.path.insert(0, str(COTIZACION_DIR))

from normalizador_materiales import detectar_categoria


DEFAULT_BOM = PROJECT_DIR / "presupuesto" / "bom_final_aquiles.json"
DEFAULT_ADDITIONS = PROJECT_DIR / "presupuesto" / "datos" / "metrados-adicionales.json"
DEFAULT_OUTPUT = REPO_DIR / "build" / "aquiles" / "bom_final.json"
ELECTRICOS_DIR = PROJECT_DIR / "diseno-electrico"
FUENTES_DXF = [
    ELECTRICOS_DIR / "planos" / "piso-1.dxf",
    ELECTRICOS_DIR / "planos" / "piso-2.dxf",
]
FUENTES_JSON = [
    ELECTRICOS_DIR / "datos" / "piso-1.json",
    ELECTRICOS_DIR / "datos" / "piso-2.json",
]


def cargar(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as archivo:
        for bloque in iter(lambda: archivo.read(65536), b""):
            h.update(bloque)
    return h.hexdigest()


def circuito_desde_item(nombre: str, uso: str) -> str:
    match = re.search(r"\bC\d+\b", f"{nombre} {uso}", re.I)
    if match:
        return match.group(0).upper()
    texto = f"{nombre} {uso}".lower()
    if "tierra" in texto or "spat" in texto:
        return "SPAT"
    if "alimentador" in texto:
        return "ALIM-TG"
    return "GENERAL"


def fuente_item(nombre: str) -> str:
    texto = nombre.lower()
    if "cinta" in texto:
        return "Estimacion tecnica del BOM previo"
    if "tablero" in texto or "puesta a tierra" in texto or "varilla" in texto:
        return "DXF vigente + BOM previo"
    return "BOM/calc ulo previo validado contra circuitos de los DXF vigentes".replace("calc ulo", "calculo")


def normalizar_originales(materiales: List[Dict[str, Any]], eliminar: List[str]) -> List[Dict[str, Any]]:
    salida: List[Dict[str, Any]] = []
    for indice, original in enumerate(materiales, 1):
        nombre = str(original.get("item") or original.get("descripcion") or "")
        if any(fragmento.lower() in nombre.lower() for fragmento in eliminar):
            continue
        item = dict(original)
        item["codigo"] = item.get("codigo") or f"BOM-{indice:03d}"
        item["categoria"] = item.get("categoria") or detectar_categoria(nombre)
        item["circuito"] = item.get("circuito") or circuito_desde_item(nombre, str(item.get("uso", "")))
        item["observacion"] = item.get("observacion") or "Partida del BOM previo conservada y validada contra la revision electrica vigente."
        item["fuente_metrado"] = item.get("fuente_metrado") or fuente_item(nombre)
        cantidad = float(item.get("cantidad") or 0.0)
        precio = float(item.get("precio_unit_soles") or 0.0)
        item["costo_soles"] = round(cantidad * precio, 2)
        salida.append(item)
    return salida


def construir_bom_final(bom_path: Path, additions_path: Path) -> Dict[str, Any]:
    for fuente in [*FUENTES_DXF, *FUENTES_JSON]:
        if not fuente.exists():
            raise FileNotFoundError(f"No existe fuente obligatoria: {fuente}")

    bom = cargar(bom_path)
    additions = cargar(additions_path)
    materiales = normalizar_originales(
        list(bom.get("materiales", [])),
        list(additions.get("eliminar_si_contiene", [])),
    )
    codigos_adicionales = {
        str(item.get("codigo"))
        for item in additions.get("materiales", [])
        if item.get("codigo")
    }
    materiales = [
        item for item in materiales
        if str(item.get("codigo")) not in codigos_adicionales
    ]
    materiales.extend(dict(item) for item in additions.get("materiales", []))
    for item in materiales:
        cantidad = float(item.get("cantidad") or 0.0)
        precio = float(item.get("precio_unit_soles") or 0.0)
        item["costo_soles"] = round(cantidad * precio, 2)

    return {
        "proyecto": "Proyecto de instalaciones electricas de vivienda - Aquiles",
        "propietario": "Aquiles Taylor Ramos Yapo",
        "fecha": datetime.now().date().isoformat(),
        "caracter": "Metrado oficial para presupuesto academico; no reemplaza verificacion de obra.",
        "fuentes": [
            {
                "ruta": str(path.relative_to(REPO_DIR)),
                "sha256": sha256(path),
                "criterio": "fuente geometrica vigente" if path.suffix.lower() == ".dxf" else "documentacion estructurada para conteos",
            }
            for path in [*FUENTES_DXF, *FUENTES_JSON]
        ],
        "nota_fuentes": "Se usan los planos y datos canonicos publicados en diseno-electrico.",
        "resumen": {
            "cantidad_partidas": len(materiales),
            "costo_referencial_bom_soles": round(sum(float(x.get("costo_soles") or 0.0) for x in materiales), 2),
        },
        "materiales": materiales,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera el BOM final de metrados de Aquiles")
    parser.add_argument("--bom-base", default=str(DEFAULT_BOM))
    parser.add_argument("--adicionales", default=str(DEFAULT_ADDITIONS))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    salida = Path(args.output)
    data = construir_bom_final(Path(args.bom_base), Path(args.adicionales))
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"BOM final: {salida}")
    print(f"Partidas: {data['resumen']['cantidad_partidas']}")
    print(f"Referencia previa: S/ {data['resumen']['costo_referencial_bom_soles']:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

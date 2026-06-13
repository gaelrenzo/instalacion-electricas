#!/usr/bin/env python3
"""Normalizacion y matching tecnico de materiales electricos."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:
    from rapidfuzz import fuzz
except Exception:  # pragma: no cover - fallback para entornos minimos
    fuzz = None


BASE_DIR = Path(__file__).resolve().parent


STOPWORDS = {
    "proteccion", "proteccion", "general", "alimentador", "trifasico",
    "escenario", "confirmar", "piso", "primer", "segundo", "tercer",
    "1er", "2do", "3er", "exterior", "auxiliar", "verde", "amarillo",
}


CATEGORY_PATTERNS = [
    ("interruptores diferenciales", [r"\bdiferencial\b", r"\brccb\b", r"\bid\b"]),
    ("interruptores termomagneticos", [r"\bitm\b", r"termomagnet", r"\bmcb\b"]),
    ("cables", [r"\bcable\b", r"\bconductor\b", r"\bthw\b", r"\btw\b", r"\blsoh\b"]),
    ("accesorios", [r"\bcinta\b", r"\bcurva\b", r"\bunion\b", r"\bconector\b", r"\baccesorio\b"]),
    ("ductos/tuberias", [r"\btubo\b", r"\btuber", r"\bconduit\b", r"\bsap\b"]),
    ("cajas electricas", [r"\bcaja\b", r"octogonal", r"rectangular", r"pase"]),
    ("tableros electricos", [r"\btablero\b", r"\bgabinete\b"]),
    ("tomacorrientes", [r"tomacorriente", r"\btoma\b", r"\bgfci\b"]),
    ("interruptores simples/dobles/conmutados", [r"interruptor simple", r"conmutad", r"\bs3\b"]),
    ("luminarias", [r"luminaria", r"\bled\b", r"panel"]),
    ("puesta a tierra", [r"puesta a tierra", r"\bvarilla\b", r"\btierra\b", r"\bspat\b"]),
]


def quitar_acentos(texto: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(c)
    )


def limpiar_texto(texto: str) -> str:
    texto = quitar_acentos(texto or "").lower()
    texto = texto.replace("²", "2")
    texto = re.sub(r"(?<=\d),(?=\d)", ".", texto)
    texto = re.sub(r"[-_]", " ", texto)
    texto = re.sub(r"[()]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def quitar_sufijos_circuito(texto: str) -> str:
    texto = re.sub(r"\s*-\s*c\d+\b", "", texto, flags=re.I)
    texto = re.sub(r"\bc\d+\b", "", texto, flags=re.I)
    texto = re.sub(r"\btg[- ]?\d*\b", "", texto, flags=re.I)
    texto = re.sub(r"\btd[- ]?\d*\b", "", texto, flags=re.I)
    texto = re.sub(r"\s+", " ", texto).strip(" -")
    return texto


def extraer_especificaciones(nombre: str) -> Dict[str, Any]:
    n = limpiar_texto(nombre)
    specs: Dict[str, Any] = {}

    mm2 = re.search(r"(\d+(?:\.\d+)?)\s*mm\s*2\b", n)
    if not mm2:
        mm2 = re.search(r"(\d+(?:\.\d+)?)\s*mm2\b", n)
    if mm2:
        specs["seccion_mm2"] = float(mm2.group(1))

    diam = re.search(r"(\d+(?:\.\d+)?)\s*mm\b", n)
    if diam and "seccion_mm2" not in specs:
        specs["diametro_mm"] = float(diam.group(1))
    elif re.search(r"\b(?:tubo|tuber|conduit|sap)\b", n):
        pulgadas_nominales = [
            (r"\b1\s+1\s*/\s*4\s*(?:\"|pulg)", 40.0),
            (r"\b1\s*(?:\"|pulg)", 32.0),
            (r"\b3\s*/\s*4\s*(?:\"|pulg)", 25.0),
            (r"\b1\s*/\s*2\s*(?:\"|pulg)", 20.0),
        ]
        for patron, diametro_nominal in pulgadas_nominales:
            if re.search(patron, n):
                specs["diametro_mm"] = diametro_nominal
                break

    polos = re.search(r"\b([1234])\s*p\b|\b([1234])\s*polos?\b", n)
    if polos:
        specs["polos"] = int(next(g for g in polos.groups() if g))

    amp = re.search(r"\b(\d+(?:\.\d+)?)\s*a\b", n)
    if amp:
        val = float(amp.group(1))
        specs["amperaje_a"] = int(val) if val.is_integer() else val

    ma = re.search(r"\b(\d+(?:\.\d+)?)\s*ma\b", n)
    if ma:
        val = float(ma.group(1))
        specs["sensibilidad_ma"] = int(val) if val.is_integer() else val

    watts = re.search(r"\b(\d+(?:\.\d+)?)\s*w\b", n)
    if watts:
        val = float(watts.group(1))
        specs["potencia_w"] = int(val) if val.is_integer() else val

    polos_tablero = re.search(r"\b(\d+)\s*(?:circuitos|polos)\b", n)
    if polos_tablero:
        specs["capacidad_polos"] = int(polos_tablero.group(1))

    if re.search(r"\b(thw|tw)\b", n):
        specs["tipo_conductor"] = "THW/TW"
    if "sap" in n:
        specs["tipo_tuberia"] = "SAP"
    if "gfci" in n:
        specs["proteccion"] = "GFCI"

    return specs


def detectar_categoria(nombre: str) -> str:
    n = limpiar_texto(nombre)
    for categoria, patrones in CATEGORY_PATTERNS:
        if any(re.search(p, n) for p in patrones):
            return categoria
    return "accesorios"


def cargar_equivalencias(path: Optional[Path] = None) -> Dict[str, Any]:
    path = path or BASE_DIR / "data" / "equivalencias_materiales.json"
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def normalizar_nombre_material(nombre: str, equivalencias: Optional[Dict[str, Any]] = None) -> str:
    """Convierte un nombre de BOM a una consulta tecnica limpia."""
    equivalencias = equivalencias if equivalencias is not None else cargar_equivalencias()
    original_limpio = quitar_sufijos_circuito(nombre)
    n = limpiar_texto(original_limpio)
    specs = extraer_especificaciones(n)
    categoria = detectar_categoria(n)

    if categoria == "accesorios" and any(palabra in n for palabra in ("union", "curva")):
        diam = specs.get("diametro_mm")
        tipo = "union" if "union" in n else "curva"
        if diam:
            return f"{tipo} pvc sap electrica {fmt_num(diam)} mm"
        return f"{tipo} pvc sap electrica"

    # Reglas explicitas para materiales electricos residenciales frecuentes.
    if categoria == "cables":
        seccion = specs.get("seccion_mm2")
        if seccion:
            return f"cable electrico thw {fmt_num(seccion)} mm2 cobre"
        return "cable electrico thw cobre"

    if categoria == "ductos/tuberias":
        diam = specs.get("diametro_mm")
        if diam:
            return f"tubo pvc sap electrico {fmt_num(diam)} mm"
        return "tubo pvc sap electrico"

    if categoria == "interruptores termomagneticos":
        polos = specs.get("polos")
        amp = specs.get("amperaje_a")
        partes = ["interruptor termomagnetico"]
        if polos:
            partes.append(f"{polos} polos")
        if amp:
            partes.append(f"{fmt_num(amp)}A")
        return " ".join(partes)

    if categoria == "interruptores diferenciales":
        polos = specs.get("polos")
        amp = specs.get("amperaje_a")
        ma = specs.get("sensibilidad_ma")
        partes = ["interruptor diferencial"]
        if polos:
            partes.append(f"{polos} polos")
        if amp:
            partes.append(f"{fmt_num(amp)}A")
        if ma:
            partes.append(f"{fmt_num(ma)}mA")
        return " ".join(partes)

    if categoria == "cajas electricas":
        if "estanca" in n or "ip55" in n:
            return "caja electrica estanca ip55"
        if "registro" in n and "tierra" in n:
            return "caja registro puesta a tierra"
        if "rectangular" in n and "octogonal" in n:
            return "caja electrica rectangular octogonal"
        if "octogonal" in n:
            return "caja electrica octogonal"
        if "rectangular" in n:
            return "caja electrica rectangular"
        return "caja electrica"

    if categoria == "tableros electricos":
        polos = specs.get("capacidad_polos") or specs.get("polos")
        if polos:
            return f"tablero electrico {polos} polos empotrable"
        return "tablero electrico empotrable"

    if categoria == "puesta a tierra":
        if "conector" in n or "abrazadera" in n:
            return "conector abrazadera para varilla puesta a tierra"
        if "varilla" in n:
            return "varilla puesta a tierra cobre 5/8 2.4 m"
        return "kit puesta a tierra electrica"

    if "cinta" in n:
        return "cinta aislante electrica"

    # Equivalencias configurables por token/frase.
    for patron, reemplazo in equivalencias.get("frases", {}).items():
        if patron in n:
            n = n.replace(patron, reemplazo)

    tokens = [t for t in n.split() if t not in STOPWORDS]
    return " ".join(tokens).strip()


def fmt_num(valor: Any) -> str:
    try:
        v = float(valor)
        return str(int(v)) if v.is_integer() else str(v).rstrip("0").rstrip(".")
    except Exception:
        return str(valor)


def tokenizar(texto: str) -> List[str]:
    n = limpiar_texto(texto)
    return [t for t in n.split() if len(t) > 1 and t not in STOPWORDS]


def similitud_texto(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    if fuzz:
        return fuzz.token_set_ratio(a, b) / 100.0
    sa, sb = set(tokenizar(a)), set(tokenizar(b))
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def comparar_specs(material_specs: Dict[str, Any], producto_texto: str) -> Tuple[float, List[str]]:
    """Calcula coincidencia tecnica entre specs BOM y texto de producto."""
    prod_specs = extraer_especificaciones(producto_texto)
    total = 0
    ok = 0
    notas: List[str] = []

    for key, label in [
        ("seccion_mm2", "seccion"),
        ("diametro_mm", "diametro"),
        ("amperaje_a", "amperaje"),
        ("polos", "polos"),
        ("sensibilidad_ma", "sensibilidad"),
        ("capacidad_polos", "capacidad"),
    ]:
        if key in material_specs:
            total += 1
            if key in prod_specs and str(prod_specs[key]) == str(material_specs[key]):
                ok += 1
                notas.append(f"{label} coincide")
            elif key in prod_specs:
                notas.append(f"{label} difiere")
            else:
                notas.append(f"{label} no visible")

    if total == 0:
        return 0.65, ["sin specs criticas detectadas"]
    return ok / total, notas


def score_tecnico(material_nombre: str, material_specs: Dict[str, Any], producto: str) -> Tuple[float, str]:
    sim = similitud_texto(material_nombre, producto)
    spec_score, notas = comparar_specs(material_specs, producto)
    score = 0.45 * sim + 0.55 * spec_score
    return max(0.0, min(1.0, score)), "; ".join(notas)

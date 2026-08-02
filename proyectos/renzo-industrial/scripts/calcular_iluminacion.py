#!/usr/bin/env python3
"""Memoria de calculo de iluminacion por el metodo de lumanes.

Lee ``diseno-electrico/datos/iluminacion-ambientes.yaml`` y la geometria de
``arquitectura/datos/layout-grifo.json``, calcula el indice de local, el flujo
requerido, la cantidad de luminarias, la potencia instalada, la densidad de
potencia (LPD) y la iluminancia resultante por ambiente. Escribe:

* ``build/renzo-industrial/calculos/iluminacion-resumen.json``
* ``build/renzo-industrial/expediente/generated/iluminacion-datos``
  (tabla LaTeX resumen + macros del ejemplo de calculo)

Los factores de utilizacion se estiman por interpolacion de tablas tipicas de
luminarias LED segun el indice de local y las reflectancias del ambiente. El
resultado es un criterio academico; la seleccion final de luminaria se define
con catalogo vigente y verificacion de campo.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import yaml


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


# Factor de utilizacion (interior) segun indice de local K, para reflectancias
# tipicas 70/50/20 (tabla estandar de luminarias LED de alumbrado general).
FU_INTERIOR = [
    (0.60, 0.42),
    (0.80, 0.50),
    (1.00, 0.56),
    (1.25, 0.62),
    (1.50, 0.66),
    (2.00, 0.72),
    (2.50, 0.76),
    (3.00, 0.79),
]

# Factor de utilizacion exterior (iluminacion de area/patio).
FU_EXTERIOR = [
    (0.50, 0.35),
    (0.80, 0.45),
    (1.00, 0.50),
    (1.50, 0.58),
    (2.00, 0.63),
    (3.00, 0.68),
]


def interpolate(table: list[tuple[float, float]], k: float) -> float:
    if k <= table[0][0]:
        return table[0][1]
    if k >= table[-1][0]:
        return table[-1][1]
    for (k0, fu0), (k1, fu1) in zip(table, table[1:]):
        if k0 <= k <= k1:
            return fu0 + (fu1 - fu0) * (k - k0) / (k1 - k0)
    return table[-1][1]


def esc_tex(text: str) -> str:
    return (
        text.replace("\\", r"\textbackslash{}")
        .replace("{", "\\{")
        .replace("}", "\\}")
        .replace("%", "\\%")
        .replace("#", "\\#")
        .replace("&", "\\&")
    )


def fmt(v: float) -> str:
    return f"{v:.2f}".replace(".", ",")


def main() -> int:
    root = repo_root()
    project = root / "proyectos/renzo-industrial"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--datos", type=Path, default=project / "diseno-electrico/datos/iluminacion-ambientes.yaml")
    parser.add_argument("--output-calc", type=Path, default=root / "build/renzo-industrial/calculos")
    parser.add_argument("--output-latex", type=Path, default=root / "build/renzo-industrial/expediente/generated")
    args = parser.parse_args()

    spec = yaml.safe_load(args.datos.read_text(encoding="utf-8"))
    lums = spec["luminarias"]
    results = []
    latex_rows = []

    for amb in spec["ambientes"]:
        lum = lums[amb["luminaria"]]
        largo, ancho, altura = amb["largo_m"], amb["ancho_m"], amb["altura_m"]
        area = largo * ancho
        hm = altura - amb["plano_trabajo_m"]
        k = largo * ancho / (hm * (largo + ancho)) if hm > 0 else 0.0
        exterior = amb["reflectancias"] == ["exterior"]
        fu = interpolate(FU_EXTERIOR if exterior else FU_INTERIOR, k)
        fm = amb["factor_mantenimiento"]
        lux_req = amb["iluminancia_lux"]
        flujo_requerido = lux_req * area / (fu * fm)
        n = max(1, math.ceil(flujo_requerido / lum["flujo_lm"]))
        potencia = n * lum["potencia_w"]
        lpd = potencia / area
        lux_result = n * lum["flujo_lm"] * fu * fm / area

        record = {
            "id": amb["id"],
            "nombre": amb["nombre"],
            "uso": amb["uso"],
            "largo_m": largo,
            "ancho_m": ancho,
            "altura_m": altura,
            "area_m2": round(area, 2),
            "iluminancia_lux": lux_req,
            "iluminancia_fuente": amb["iluminancia_fuente"],
            "indice_local": round(k, 2),
            "factor_utilizacion": round(fu, 2),
            "factor_mantenimiento": fm,
            "flujo_requerido_lm": round(flujo_requerido),
            "luminaria_tipo": lum["tipo"],
            "luminaria_potencia_w": lum["potencia_w"],
            "luminaria_flujo_lm": lum["flujo_lm"],
            "n_luminarias": n,
            "distribucion": amb["distribucion"],
            "potencia_instalada_w": potencia,
            "lpd_w_m2": round(lpd, 2),
            "iluminancia_resultado_lux": round(lux_result),
            "cumple": lux_result >= lux_req,
            "estado": amb["estado"],
        }
        results.append(record)
        latex_rows.append(
            f"{esc_tex(amb['nombre'])} & {amb['largo_m']:.1f}~m $\\times$ {amb['ancho_m']:.1f}~m & "
            f"{fmt(area)} & {amb['iluminancia_lux']} & {fmt(k)} & {fmt(fu)} & {fm} & "
            f"{n} & {lum['potencia_w']} & {fmt(potencia)} & {fmt(lpd)} & {round(lux_result)} \\\\"
        )

    adquis = next(r for r in results if r["id"] == "ADM")
    total_luminarias = sum(r["n_luminarias"] for r in results)
    total_potencia_w = sum(r["potencia_instalada_w"] for r in results)
    total_area_m2 = sum(r["area_m2"] for r in results)
    total_lpd = total_potencia_w / total_area_m2

    macros = [
        "\\providecommand{\\IllumTitulo}{Memoria de calculo de iluminacion}",
        "\\providecommand{\\IllumEjNombre}{" + esc_tex(adquis["nombre"]) + "}",
        f"\\providecommand{{\\IllumEjLargo}}{{{adquis['largo_m']:.1f}}}",
        f"\\providecommand{{\\IllumEjAncho}}{{{adquis['ancho_m']:.1f}}}",
        f"\\providecommand{{\\IllumEjAltura}}{{{adquis['altura_m']:.1f}}}",
        f"\\providecommand{{\\IllumEjArea}}{{{fmt(adquis['area_m2'])}}}",
        f"\\providecommand{{\\IllumEjLux}}{{{adquis['iluminancia_lux']}}}",
        f"\\providecommand{{\\IllumEjK}}{{{fmt(adquis['indice_local'])}}}",
        f"\\providecommand{{\\IllumEjFu}}{{{fmt(adquis['factor_utilizacion'])}}}",
        f"\\providecommand{{\\IllumEjFm}}{{{adquis['factor_mantenimiento']}}}",
        f"\\providecommand{{\\IllumEjFlujoReq}}{{{fmt(adquis['flujo_requerido_lm'])}}}",
        f"\\providecommand{{\\IllumEjLumFlujo}}{{{adquis['luminaria_flujo_lm']}}}",
        f"\\providecommand{{\\IllumEjLumPot}}{{{adquis['luminaria_potencia_w']}}}",
        f"\\providecommand{{\\IllumEjN}}{{{adquis['n_luminarias']}}}",
        f"\\providecommand{{\\IllumEjPot}}{{{fmt(adquis['potencia_instalada_w'])}}}",
        f"\\providecommand{{\\IllumEjLpd}}{{{fmt(adquis['lpd_w_m2'])}}}",
        f"\\providecommand{{\\IllumEjResult}}{{{adquis['iluminancia_resultado_lux']}}}",
        f"\\providecommand{{\\IllumTotalN}}{{{total_luminarias}}}",
        f"\\providecommand{{\\IllumTotalW}}{{{total_potencia_w}}}",
        f"\\providecommand{{\\IllumTotalKW}}{{{total_potencia_w / 1000:.3f}}}",
        f"\\providecommand{{\\IllumTotalLPD}}{{{total_lpd:.2f}}}",
    ]

    tabla = "\n".join(latex_rows)
    payload = "\n".join([
        "% Archivo de datos generado: iluminacion (renzo-industrial)",
        "\\providecommand{\\ILLUMTAB}{}",
        *macros,
        f"\\providecommand{{\\ILLUMTAB}}{{\\setlength{{\\tabcolsep}}{{3pt}}\\begin{{longtable}}{{p{{3.1cm}} c c c c c c c c c c c}}\\toprule",
        "Ambiente & Dimensiones & \\'Area (m\\textsuperscript{2}) & E (lux) & K & FU & FM & N\\textsuperscript{*} & W/lum. & W inst. & LPD (W/m\\textsuperscript{2}) & E resultante \\\\\\midrule",
        tabla,
        "\\bottomrule\\end{longtable}}",
        "\\providecommand{\\IllumNotaN}{\\textsuperscript{*}N: numero de luminarias por ambiente}",
    ])
    (args.output_latex / "iluminacion-datos").write_text(payload, encoding="utf-8")

    args.output_calc.mkdir(parents=True, exist_ok=True)
    (args.output_calc / "iluminacion-resumen.json").write_text(
        json.dumps({
            "schema_version": 1,
            "method": "lumanes_con_indice_de_local",
            "source": str(args.datos),
            "status": "PASS" if all(r["cumple"] for r in results) else "REVISION",
            "ambientes": results,
            "totales": {
                "n_luminarias": total_luminarias,
                "potencia_instalada_w": total_potencia_w,
                "area_m2": round(total_area_m2, 2),
                "lpd_promedio_w_m2": round(total_lpd, 2),
            },
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "status": "PASS" if all(r["cumple"] for r in results) else "REVISION",
        "ambientes": len(results),
        "totales": {
            "n_luminarias": total_luminarias,
            "potencia_instalada_w": total_potencia_w,
            "lpd_promedio_w_m2": round(total_lpd, 2),
        },
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

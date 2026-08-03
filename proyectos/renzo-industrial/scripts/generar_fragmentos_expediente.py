#!/usr/bin/env python3
"""Genera fragmentos LaTeX de datos del expediente a partir de los resultados
PASS del calculo electrico de renzo-industrial.

Lee ``build/renzo-industrial/calculos/resumen-calculos.json`` y escribe
``build/renzo-industrial/expediente/generated/datos`` (macros LaTeX) mas las
tablas ``alimentadores``, ``circuitos`` y ``resumen`` para inyectar en los
capitulos. Los valores provienen exclusivamente del proyecto Renzo.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def fmt(value: float) -> str:
    return f"{value:.2f}"


def fmt_size(value: float | int) -> str:
    number = float(value)
    if number.is_integer():
        return f"{number:.0f}"
    return f"{number:.1f}"


def main() -> int:
    root = repo_root()
    project = root / "proyectos/renzo-industrial"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resumen", type=Path, default=root / "build/renzo-industrial/calculos/resumen-calculos.json")
    parser.add_argument("--cargas", type=Path, default=project / "diseno-electrico/datos/cargas.yaml")
    parser.add_argument("--output", type=Path, default=root / "build/renzo-industrial/expediente/generated")
    args = parser.parse_args()

    result = json.loads(args.resumen.read_text(encoding="utf-8"))
    if result["status"] != "PASS":
        raise SystemExit("El calculo electrico no esta en estado PASS; no se generan fragmentos")

    cargas = yaml.safe_load(args.cargas.read_text(encoding="utf-8"))
    s = result["summary"]
    g = result["generator"]
    system = cargas["system"]
    worst_vd = max(result["circuits"], key=lambda c: c["total_voltage_drop_percent"])
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    # --- Archivo de macros de resumen ---
    macros = [
        "\\providecommand{\\PI}{0}%",
        f"\\renewcommand{{\\PI}}{{{fmt(s['installed_kw'])} \\,kW instalados ({fmt(s['installed_kva'])} \\,kVA)}}",
        f"\\renewcommand{{\\MD}}{{{fmt(s['maximum_demand_kw'])} \\,kW / {fmt(s['maximum_demand_kva'])} \\,kVA}}",
        f"\\renewcommand{{\\MDReserva}}{{{fmt(s['service_design_kva_with_reserve'])} \\,kVA}}",
        f"\\renewcommand{{\\ServCap}}{{{fmt(s['service_capacity_kva'])} \\,kVA}}",
        f"\\renewcommand{{\\IPrincipal}}{{{fmt(s['main_breaker_a'])} \\,A, 4P}}",
        f"\\renewcommand{{\\Desb}}{{{fmt(s['phase_unbalance_percent'])}\\%}}",
        f"\\renewcommand{{\\dVAlim}}{{{fmt(s['main_voltage_drop_percent'])}\\%}}",
        f"\\renewcommand{{\\MDkw}}{{{fmt(s['maximum_demand_kw'])}}}",
        f"\\renewcommand{{\\MDkva}}{{{fmt(s['maximum_demand_kva'])}}}",
        f"\\renewcommand{{\\Ipase}}{{{fmt(s['maximum_phase_current_with_reserve_a'])}}}",
        f"\\renewcommand{{\\EmergKVA}}{{{fmt(g['emergency_running_kva'])}}}",
        f"\\renewcommand{{\\ArranqueKVA}}{{{fmt(g['starting_scenario_kva'])}}}",
        f"\\renewcommand{{\\ArranqueMargen}}{{{fmt(g['starting_with_margin_kva'])}}}",
        f"\\renewcommand{{\\AltFactor}}{{{fmt(g['altitude_factor'])}}}",
        f"\\renewcommand{{\\GrupoDisp}}{{{fmt(g['available_standby_kva_at_site'])}}}",
        f"\\renewcommand{{\\GrupoNom}}{{{fmt(g['selected_nameplate_kva'])}}}",
        f"\\renewcommand{{\\GrupoModelo}}{{Cummins C30D6}}",
        f"\\renewcommand{{\\IccAsumido}}{{10}}",
        f"\\renewcommand{{\\Icu}}{{{fmt(system.get('main_breaker_icu_ka_min', 25))}}}",
        f"\\providecommand{{\\dVMaxCircuit}}{{{worst_vd['id']}}}",
        f"\\providecommand{{\\dVMaxTotal}}{{{fmt(worst_vd['total_voltage_drop_percent'])}\\%}}",
    ]

    feeder_breaker = {fdr["id"]: fdr["breaker_a"] for fdr in result["feeders"]}

    def esc(text: str) -> str:
        return (
            text.replace("\\", r"\textbackslash{}")
            .replace("{", "\\{")
            .replace("}", "\\}")
            .replace("%", "\\%")
            .replace("#", "\\#")
            .replace("&", "\\&")
        )

    # --- Tabla alimentadores ---
    feeder_rows = []
    for fdr in result["feeders"]:
        feeder_rows.append(
            f"{fdr['id']} & {fdr['panel']} & {fdr['breaker_a']:.0f} A & "
            f"{fmt_size(fdr['phase_mm2'])}/{fmt_size(fdr['neutral_mm2'])}/{fmt_size(fdr['pe_mm2'])} & "
            f"{fdr['corrected_ampacity_a']:.1f} & {fdr['max_phase_current_a']:.2f} & "
            f"{fdr['voltage_drop_percent']:.2f}\\% \\\\"
        )
    alimentadores = "\n".join(feeder_rows)

    # --- Tabla circuitos ---
    circuit_rows = []
    for c in result["circuits"]:
        circuit_rows.append(
            f"{c['id']} & {esc(c['description'])} & {c['panel']} & {c['phase']} & "
            f"{fmt(c['installed_kva_calc'])} & {fmt(c['demand_kva'])} & "
            f"{fmt(c['design_current_a'])} & {c['breaker_a']} & "
            f"{c['conductor_mm2']}/{c['pe_mm2']} & "
            f"{fmt(c['branch_voltage_drop_percent'])}\\% / {fmt(c['total_voltage_drop_percent'])}\\% \\\\"
        )
    circuitos = "\n".join(circuit_rows)

    # --- Archivo datos (todo junto) ---
    payload = "\n".join([
        "% Archivo de datos generado: renzo-industrial",
        "\\providecommand{\\PI}{}",
        "\\providecommand{\\MD}{}",
        "\\providecommand{\\MDReserva}{}",
        "\\providecommand{\\ServCap}{}",
        "\\providecommand{\\IPrincipal}{}",
        "\\providecommand{\\Desb}{}",
        "\\providecommand{\\dVAlim}{}",
        "\\providecommand{\\MDkw}{}",
        "\\providecommand{\\MDkva}{}",
        "\\providecommand{\\Ipase}{}",
        "\\providecommand{\\EmergKVA}{}",
        "\\providecommand{\\ArranqueKVA}{}",
        "\\providecommand{\\ArranqueMargen}{}",
        "\\providecommand{\\AltFactor}{}",
        "\\providecommand{\\GrupoDisp}{}",
        "\\providecommand{\\GrupoNom}{}",
        "\\providecommand{\\GrupoModelo}{}",
        "\\providecommand{\\IccAsumido}{}",
        "\\providecommand{\\Icu}{}",
        "\\providecommand{\\dVMaxCircuit}{}",
        "\\providecommand{\\dVMaxTotal}{}",
        f"\\providecommand{{\\ITMAlTDE}}{{{feeder_breaker.get('AL-TDE', 40)}}}",
        f"\\providecommand{{\\ITMAlTDF}}{{{feeder_breaker.get('AL-TDF', 32)}}}",
        f"\\providecommand{{\\ITMAlTDA}}{{{feeder_breaker.get('AL-TD-A1', 20)}}}",
        "\\providecommand{\\CIRCUITOS}{}",
        "\\providecommand{\\ALIMENTADORES}{}",
        *macros,
        f"\\providecommand{{\\CIRCUITOSTAB}}{{\\setlength{{\\tabcolsep}}{{1pt}}\\begin{{longtable}}{{l >{{\\raggedright\\arraybackslash}}p{{3.0cm}} c c c c c c c c}}\\toprule",
        "ID & Descripcion & Tablero & Fase & kVA inst. & kVA MD & Ib (A) & ITM & Cu/PE & dV ramal/total \\\\\\midrule",
        circuitos,
        "\\bottomrule\\end{longtable}}",
        f"\\providecommand{{\\ALIMENTADORESTAB}}{{\\begin{{tabularx}}{{\\linewidth}}{{l c c c c c c}}\\toprule",
        "ID & Tablero & ITM & Cu/N/PE & Iz corr. & Imax & dV \\\\\\midrule",
        alimentadores,
        "\\bottomrule\\end{tabularx}}",
    ])
    (output / "datos").write_text(payload, encoding="utf-8")
    (output / "datos.tex").write_text(payload, encoding="utf-8")

    print(json.dumps({
        "status": "PASS",
        "output": str(output),
        "macros": len(macros),
        "circuitos": len(result["circuits"]),
        "alimentadores": len(result["feeders"]),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

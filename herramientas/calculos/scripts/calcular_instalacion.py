#!/usr/bin/env python3
import argparse
import copy
import json
import math
import os


STANDARDS_ITM = [10, 16, 20, 25, 32, 40, 50, 63, 80, 100]

# Ampacidad preliminar de conductores de cobre en ducto a 30 C. La tabla debe
# validarse contra la tabla CNE aplicable antes del cierre definitivo.
AMPACITIES_CU = {
    1.5: 15,
    2.5: 20,
    4.0: 28,
    6.0: 36,
    10.0: 50,
    16.0: 66,
    25.0: 88,
    35.0: 109,
    50.0: 134,
    70.0: 167,
    95.0: 202,
}


def load_data(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def write_text(filepath, content):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def find_appropriate_itm(ib, max_capacity):
    """
    Selecciona una llave comercial bajo el criterio Ib <= In_ITM <= Iz.
    Ib es la corriente de empleo o carga, no la corriente de diseno con margen.
    """
    for rating in STANDARDS_ITM:
        if rating >= ib and rating <= max_capacity:
            return rating
    for rating in STANDARDS_ITM:
        if rating >= ib:
            return rating
    return STANDARDS_ITM[-1]


def select_conductor_for_design(id_current, minimum_section=2.5):
    for section, ampacity in sorted(AMPACITIES_CU.items()):
        if section >= minimum_section and ampacity >= id_current:
            return section, ampacity
    section = max(AMPACITIES_CU)
    return section, AMPACITIES_CU[section]


def get_ampacity(section):
    return AMPACITIES_CU.get(float(section), 0)


def cne_050_200_basic_load(area_m2):
    if area_m2 is None:
        return 0
    if area_m2 <= 90:
        return 2500
    return 2500 + 1000 * math.ceil((area_m2 - 90) / 90)


def apply_scenario(base_circuits, scenario):
    circuits = copy.deepcopy(base_circuits)
    overrides = scenario.get("circuito_overrides", {})
    for circuit in circuits:
        override = overrides.get(circuit["id"])
        if override:
            circuit.update(override)
    return circuits


def calculate_circuit(circ, params):
    v_nominal = params["tension_v"]
    cosphi = params["factor_potencia_cosphi"]
    rho = params["resistividad_cobre_rho"]
    factor_diseno = params["factor_diseno_conductor"]

    pi = circ["potencia_instalada_w"]
    fd = circ["factor_demanda"]
    md = pi * fd
    ib = md / (v_nominal * cosphi)
    id_current = ib * factor_diseno
    section = float(circ["seccion_conductor_mm2"])
    ampacity = get_ampacity(section)
    length = circ["longitud_m"]
    dv = (2.0 * length * ib * rho) / section
    dv_porc = (dv / v_nominal) * 100.0
    itm = find_appropriate_itm(ib, ampacity)

    descripcion = circ.get("descripcion", "").lower()
    requires_diff = circ.get("requiere_diferencial")
    if requires_diff is None:
        requires_diff = any(
            termino in descripcion
            for termino in ("tomacorriente", "cocina", "lavadora", "bomba", "baño")
        )
    requires_ground = circ.get("requiere_tierra", True)
    diff_rating = 25 if itm <= 20 else (40 if itm <= 32 else 63)
    diff_str = f"2P-{diff_rating}A-30mA" if requires_diff else "Ver diferencial general"

    cumple_conductor = id_current <= ampacity
    cumple_coord = ib <= itm <= ampacity
    cumple_caida = dv_porc <= params["caida_tension_max_derivados_porc"]

    return {
        "id": circ["id"],
        "descripcion": circ["descripcion"],
        "estado": circ.get("estado", "preliminar"),
        "fuente": circ.get("fuente", "por confirmar"),
        "potencia_instalada_w": round(pi, 2),
        "factor_demanda": fd,
        "maxima_demanda_w": round(md, 2),
        "corriente_empleo_ib_a": round(ib, 3),
        "corriente_diseno_id_a": round(id_current, 3),
        "seccion_conductor_mm2": section,
        "ampacidad_conductor_iz_a": ampacity,
        "longitud_m": length,
        "caida_tension_v": round(dv, 3),
        "caida_tension_porc": round(dv_porc, 3),
        "itm_a": itm,
        "itm_sugerido": f"2P-{itm}A",
        "diferencial_sugerido": diff_str,
        "requiere_diferencial": bool(requires_diff),
        "requiere_tierra": bool(requires_ground),
        "diametro_tubo_pvc_mm": circ["diametro_tubo_mm"],
        "cumple_conductor": "CUMPLE" if cumple_conductor else "SOBRECARGADO",
        "cumple_coordinacion": "CUMPLE" if cumple_coord else "REVISAR ITM",
        "cumple_caida": "CUMPLE" if cumple_caida else "EXCEDE LIMITE",
    }


def run_scenario(data, scenario):
    params = data["parametros_electricos"]
    area_total = data["areas"]["techada_total_calculo_m2"]["valor"]
    circuits = apply_scenario(data["circuitos_base"], scenario)
    calculated_circuits = [calculate_circuit(circ, params) for circ in circuits]

    total_pi = sum(c["potencia_instalada_w"] for c in calculated_circuits)
    md_circuitos = sum(c["maxima_demanda_w"] for c in calculated_circuits)

    cne_info = scenario.get("cne_050_200", {})
    cne_area = cne_050_200_basic_load(area_total) if cne_info.get("aplicar", True) else 0
    cne_cocina = cne_info.get("cocina_electrica_normativa_w", 0)
    md_cne = cne_area + cne_cocina

    md_adoptada = max(md_circuitos, md_cne)
    metodo = "CNE-U 050-200" if md_cne >= md_circuitos else "Circuitos derivados"

    v_nominal = params["tension_v"]
    cosphi = params["factor_potencia_cosphi"]
    rho = params["resistividad_cobre_rho"]
    factor_diseno = params["factor_diseno_conductor"]
    ib_total = md_adoptada / (v_nominal * cosphi)
    id_total = ib_total * factor_diseno

    alim_section, alim_ampacity = select_conductor_for_design(id_total, minimum_section=10.0)
    alim_length = data["alimentacion_principal"]["longitud_m"]
    alim_dv = (2.0 * alim_length * ib_total * rho) / alim_section
    alim_dv_porc = (alim_dv / v_nominal) * 100.0
    alim_itm = find_appropriate_itm(ib_total, alim_ampacity)

    return {
        "id": scenario["id"],
        "nombre": scenario["nombre"],
        "estado": scenario.get("estado", "preliminar"),
        "descripcion": scenario.get("descripcion", ""),
        "cocina_electrica": scenario.get("cocina_electrica", False),
        "resumen_general": {
            "potencia_instalada_total_w": round(total_pi, 2),
            "maxima_demanda_circuitos_w": round(md_circuitos, 2),
            "cne_050_200_area_w": round(cne_area, 2),
            "cne_050_200_cocina_w": round(cne_cocina, 2),
            "maxima_demanda_cne_w": round(md_cne, 2),
            "maxima_demanda_adoptada_w": round(md_adoptada, 2),
            "metodo_gobernante": metodo,
            "corriente_empleo_ib_total_a": round(ib_total, 2),
            "corriente_diseno_id_total_a": round(id_total, 2),
            "alimentador_seccion_mm2": alim_section,
            "alimentador_ampacidad_iz_a": alim_ampacity,
            "alimentador_longitud_m": alim_length,
            "alimentador_caida_tension_v": round(alim_dv, 3),
            "alimentador_caida_tension_porc": round(alim_dv_porc, 3),
            "alimentador_itm_a": alim_itm,
            "alimentador_itm_sugerido": f"2P-{alim_itm}A",
            "cumple_conductor_alimentador": "CUMPLE" if id_total <= alim_ampacity else "SOBRECARGADO",
            "cumple_coordinacion_alimentador": "CUMPLE" if ib_total <= alim_itm <= alim_ampacity else "REVISAR ITM",
            "cumple_caida_alimentador": "CUMPLE"
            if alim_dv_porc <= params["caida_tension_max_alimentador_porc"]
            else "EXCEDE LIMITE",
        },
        "circuitos_calculados": calculated_circuits,
    }


def run_calculations(data):
    scenarios = {}
    for scenario in data["escenarios"]:
        scenarios[scenario["id"]] = run_scenario(data, scenario)

    design_id = data.get("escenario_dimensionamiento_id") or data["escenarios"][0]["id"]
    return {
        "proyecto": data["proyecto"],
        "propietario": data["propietario"],
        "ubicacion": data["ubicacion"],
        "areas": data["areas"],
        "parametros_electricos": data["parametros_electricos"],
        "alimentacion_principal": data["alimentacion_principal"],
        "escenario_dimensionamiento_id": design_id,
        "escenario_dimensionamiento": scenarios[design_id],
        "escenarios": scenarios,
    }


def tex_escape(value):
    text = str(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def fmt_num(value, digits=0):
    if value is None:
        return "Por confirmar"
    if digits == 0:
        return f"{value:,.0f}"
    return f"{value:,.{digits}f}"


def generate_area_table(data, output_dir):
    labels = [
        ("terreno_m2", "Area de terreno"),
        ("techada_primer_piso_m2", "Area techada primer piso"),
        ("techada_segundo_piso_m2", "Area techada segundo piso"),
        ("techada_total_calculo_m2", "Area techada total de calculo"),
    ]
    lines = [
        r"\begin{table}[H]",
        r"\centering",
        r"\caption{Datos base de areas usados para calculo preliminar.}",
        r"\label{tab:areas_base_calculo}",
        r"\begin{small}",
        r"\begin{tabularx}{\textwidth}{l c l L}",
        r"\toprule",
        r"\textbf{Dato} & \textbf{Valor (m$^2$)} & \textbf{Estado} & \textbf{Fuente / observacion} \\",
        r"\midrule",
    ]
    for key, label in labels:
        item = data["areas"][key]
        value = item.get("valor")
        value_tex = "Por confirmar" if value is None else fmt_num(float(value), 2)
        lines.append(
            f"{tex_escape(label)} & {value_tex} & {tex_escape(item.get('estado', 'preliminar'))} & {tex_escape(item.get('fuente', ''))} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabularx}", r"\end{small}", r"\end{table}"])
    write_text(os.path.join(output_dir, "tabla_areas.tex"), "\n".join(lines))


def generate_scenarios_table(results, output_dir):
    lines = [
        r"\begin{table}[H]",
        r"\centering",
        r"\caption{Comparacion de escenarios de maxima demanda preliminar.}",
        r"\label{tab:escenarios_demanda}",
        r"\begin{scriptsize}",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}{l c c c c c c c c}",
        r"\toprule",
        r"\textbf{Escenario} & \textbf{P.I. (W)} & \textbf{MD circ. (W)} & \textbf{MD CNE (W)} & \textbf{MD adopt. (W)} & \textbf{Ib (A)} & \textbf{Cond. (mm$^2$)} & \textbf{ITM} & \textbf{dV alim. (\%)} \\",
        r"\midrule",
    ]
    for scenario in results["escenarios"].values():
        res = scenario["resumen_general"]
        lines.append(
            f"{tex_escape(scenario['nombre'])} & "
            f"{fmt_num(res['potencia_instalada_total_w'])} & "
            f"{fmt_num(res['maxima_demanda_circuitos_w'])} & "
            f"{fmt_num(res['maxima_demanda_cne_w'])} & "
            f"{fmt_num(res['maxima_demanda_adoptada_w'])} & "
            f"{fmt_num(res['corriente_empleo_ib_total_a'], 2)} & "
            f"{fmt_num(res['alimentador_seccion_mm2'], 1)} & "
            f"{tex_escape(res['alimentador_itm_sugerido'])} & "
            f"{fmt_num(res['alimentador_caida_tension_porc'], 3)} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}%", r"}", r"\end{scriptsize}", r"\end{table}"])
    write_text(os.path.join(output_dir, "tabla_escenarios.tex"), "\n".join(lines))


def generate_cargas_table(scenario_result, output_dir, filename):
    label_id = scenario_result["id"].replace("_", "-")
    lines = [
        r"\begin{table}[H]",
        r"\centering",
        rf"\caption{{Cuadro de cargas preliminar - {tex_escape(scenario_result['nombre'])}.}}",
        rf"\label{{tab:cuadro-cargas-{label_id}}}",
        r"\begin{small}",
        r"\begin{tabular}{l l c c c}",
        r"\toprule",
        r"\textbf{Circuito} & \textbf{Descripcion (Uso)} & \textbf{P.I. (W)} & \textbf{F.D.} & \textbf{M.D. (W)} \\",
        r"\midrule",
    ]
    for circ in scenario_result["circuitos_calculados"]:
        lines.append(
            f"{tex_escape(circ['id'])} & {tex_escape(circ['descripcion'])} & "
            f"{fmt_num(circ['potencia_instalada_w'])} & {circ['factor_demanda']:.2f} & "
            f"{fmt_num(circ['maxima_demanda_w'], 1)} \\\\"
        )
    res = scenario_result["resumen_general"]
    lines.extend(
        [
            r"\midrule",
            f"\\multicolumn{{2}}{{l}}{{\\textbf{{Total instalado / MD circuitos}}}} & "
            f"\\textbf{{{fmt_num(res['potencia_instalada_total_w'])}}} & & "
            f"\\textbf{{{fmt_num(res['maxima_demanda_circuitos_w'], 1)}}} \\\\",
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{small}",
            r"\end{table}",
        ]
    )
    write_text(os.path.join(output_dir, filename), "\n".join(lines))


def generate_conductores_table(scenario_result, output_dir, filename):
    res = scenario_result["resumen_general"]
    label_id = scenario_result["id"].replace("_", "-")
    lines = [
        r"\begin{table}[H]",
        r"\centering",
        rf"\caption{{Seleccion preliminar de conductores y protecciones - {tex_escape(scenario_result['nombre'])}.}}",
        rf"\label{{tab:conductores-protecciones-{label_id}}}",
        r"\begin{scriptsize}",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}{l c c c c c l c c c}",
        r"\toprule",
        r"\textbf{Circ.} & \textbf{P.I. (W)} & \textbf{M.D. (W)} & \textbf{Ib (A)} & \textbf{Id (A)} & \textbf{Cond.} & \textbf{ITM} & \textbf{Iz (A)} & \textbf{dV (\%)} & \textbf{Estado} \\",
        r"\midrule",
        f"Alim. & {fmt_num(res['potencia_instalada_total_w'])} & {fmt_num(res['maxima_demanda_adoptada_w'])} & "
        f"{fmt_num(res['corriente_empleo_ib_total_a'], 2)} & {fmt_num(res['corriente_diseno_id_total_a'], 2)} & "
        f"{fmt_num(res['alimentador_seccion_mm2'], 1)} mm$^2$ & {tex_escape(res['alimentador_itm_sugerido'])} & "
        f"{fmt_num(res['alimentador_ampacidad_iz_a'])} & {fmt_num(res['alimentador_caida_tension_porc'], 3)} & "
        f"{tex_escape(res['cumple_conductor_alimentador'])} \\\\",
        r"\midrule",
    ]
    for circ in scenario_result["circuitos_calculados"]:
        estado = f"{circ['cumple_conductor']}/{circ['cumple_coordinacion']}/{circ['cumple_caida']}"
        lines.append(
            f"{tex_escape(circ['id'])} & {fmt_num(circ['potencia_instalada_w'])} & "
            f"{fmt_num(circ['maxima_demanda_w'], 1)} & {fmt_num(circ['corriente_empleo_ib_a'], 2)} & "
            f"{fmt_num(circ['corriente_diseno_id_a'], 2)} & {fmt_num(circ['seccion_conductor_mm2'], 1)} mm$^2$ & "
            f"{tex_escape(circ['itm_sugerido'])} & {fmt_num(circ['ampacidad_conductor_iz_a'])} & "
            f"{fmt_num(circ['caida_tension_porc'], 3)} & {tex_escape(estado)} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}%", r"}", r"\end{scriptsize}", r"\end{table}"])
    write_text(os.path.join(output_dir, filename), "\n".join(lines))


def generate_tex_tables(results, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    generate_area_table(results, output_dir)
    generate_scenarios_table(results, output_dir)

    design = results["escenario_dimensionamiento"]
    generate_cargas_table(design, output_dir, "tabla_cargas.tex")
    generate_conductores_table(design, output_dir, "tabla_conductores.tex")

    for scenario in results["escenarios"].values():
        suffix = scenario["id"]
        generate_cargas_table(scenario, output_dir, f"tabla_cargas_{suffix}.tex")
        generate_conductores_table(scenario, output_dir, f"tabla_conductores_{suffix}.tex")

    print(f"\nTablas LaTeX exportadas correctamente a: {output_dir}")


def generate_markdown_report(results, output_filepath):
    lines = [
        "# Reporte Tecnico de Calculos Electricos",
        f"**Propietario:** {results['propietario']}",
        f"**Proyecto:** {results['proyecto']}",
        "**Estado de los Calculos:** Preliminar / Sujeto a validacion",
        "",
        "## 1. Comparacion de Escenarios",
        "",
        "| Escenario | P.I. (W) | MD circuitos (W) | MD CNE (W) | MD adoptada (W) | Ib (A) | Id (A) | Alimentador | ITM | dV alim. (%) | Metodo |",
        "|---|---:|---:|---:|---:|---:|---:|---|---|---:|---|",
    ]
    for scenario in results["escenarios"].values():
        res = scenario["resumen_general"]
        lines.append(
            f"| {scenario['nombre']} | {res['potencia_instalada_total_w']:.0f} | "
            f"{res['maxima_demanda_circuitos_w']:.0f} | {res['maxima_demanda_cne_w']:.0f} | "
            f"{res['maxima_demanda_adoptada_w']:.0f} | {res['corriente_empleo_ib_total_a']:.2f} | "
            f"{res['corriente_diseno_id_total_a']:.2f} | {res['alimentador_seccion_mm2']:.1f} mm2 | "
            f"{res['alimentador_itm_sugerido']} | {res['alimentador_caida_tension_porc']:.3f} | "
            f"{res['metodo_gobernante']} |"
        )

    design = results["escenario_dimensionamiento"]
    res = design["resumen_general"]
    lines.extend(
        [
            "",
            f"## 2. Escenario de dimensionamiento preliminar: {design['nombre']}",
            "",
            f"- Potencia instalada total: {res['potencia_instalada_total_w']:.0f} W",
            f"- Maxima demanda adoptada: {res['maxima_demanda_adoptada_w']:.0f} W",
            f"- Corriente de empleo del alimentador: {res['corriente_empleo_ib_total_a']:.2f} A",
            f"- Corriente de diseno preliminar del conductor: {res['corriente_diseno_id_total_a']:.2f} A",
            f"- Alimentador sugerido: {res['alimentador_seccion_mm2']:.1f} mm2",
            f"- Interruptor general sugerido: {res['alimentador_itm_sugerido']}",
            f"- Caida de tension del alimentador: {res['alimentador_caida_tension_porc']:.3f}%",
            "",
            "## 3. Notas",
            "",
            "- Los escenarios alternativos son comparativos y deben confirmarse con el propietario.",
            "- El factor 1.25 se mantiene como criterio preliminar de dimensionamiento del conductor; REVISAR sustento normativo final.",
            "- Los circuitos de alumbrado se actualizaron a conductor minimo 2.5 mm2 conforme auditoria CNE-U 030-002.",
        ]
    )
    write_text(output_filepath, "\n".join(lines))
    print(f"Reporte en Markdown exportado correctamente a: {output_filepath}")


def parse_args():
    parser = argparse.ArgumentParser(description="Calcula escenarios electricos residenciales preliminares.")
    parser.add_argument(
        "--input",
        required=True,
        help="Ruta del JSON de entrada.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directorio de salida.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    data = load_data(args.input)
    results = run_calculations(data)

    print("\n--- RESUMEN DE ESCENARIOS ---")
    for scenario in results["escenarios"].values():
        res = scenario["resumen_general"]
        print(
            f"{scenario['id']}: PI={res['potencia_instalada_total_w']:.0f} W, "
            f"MD_circ={res['maxima_demanda_circuitos_w']:.0f} W, "
            f"MD_CNE={res['maxima_demanda_cne_w']:.0f} W, "
            f"MD_adoptada={res['maxima_demanda_adoptada_w']:.0f} W, "
            f"Ib={res['corriente_empleo_ib_total_a']:.2f} A, "
            f"Id={res['corriente_diseno_id_total_a']:.2f} A, "
            f"Cond={res['alimentador_seccion_mm2']:.1f} mm2, "
            f"ITM={res['alimentador_itm_sugerido']}, "
            f"dV={res['alimentador_caida_tension_porc']:.3f}%"
        )

    output_json = os.path.join(args.output_dir, "resultados.json")
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResultados JSON exportados correctamente a: {output_json}")

    generate_tex_tables(results, args.output_dir)
    generate_markdown_report(results, os.path.join(args.output_dir, "reporte_calculos.md"))


if __name__ == "__main__":
    main()

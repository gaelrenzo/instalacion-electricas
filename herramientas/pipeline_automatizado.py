#!/usr/bin/env python3
"""
Pipeline automatizado completo: desde configuracion del proyecto hasta
planos DXF/PDF, tablas LaTeX, lista de materiales y diagrama unifilar.

Uso:
  python3 pipeline_automatizado.py --config proyecto.yaml
  python3 pipeline_automatizado.py --config proyecto.yaml --skip-cad

Flujo:
  1. Lee configuracion YAML/JSON del proyecto
  2. Genera JSON de calculo y ejecuta motor de calculos
  3. Genera JSON electrico con superposicion de simbologia
  4. Genera plano DXF arquitectonico + superposicion electrica
  5. Exporta a PDF via QCAD o matplotlib
  6. Genera tablas LaTeX actualizadas
  7. Genera lista de materiales (BOM)
  8. Genera diagrama unifilar
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import math
from pathlib import Path
from datetime import date
from typing import Any, Optional


REPO_ROOT = Path(__file__).resolve().parent.parent
HERRAMIENTAS = REPO_ROOT / "herramientas"
PROJECTS_DIR = REPO_ROOT / "proyectos"
CALCULOS_DIR = HERRAMIENTAS / "calculos"
CAD_DIR = HERRAMIENTAS / "cad"


def log(msg: str) -> None:
    print(f"[pipeline] {msg}")


def load_config(path: str) -> dict:
    import yaml
    with open(path, "r", encoding="utf-8") as f:
        if str(path).endswith((".yaml", ".yml")):
            return yaml.safe_load(f)
        return json.load(f)


def resolve_path(config_path: Path, value: Any) -> Optional[Path]:
    if not value:
        return None
    path = Path(str(value)).expanduser()
    if path.is_absolute():
        return path
    project_path = config_path.parent / path
    if project_path.exists():
        return project_path
    return REPO_ROOT / path


def config_input(config: dict, key: str) -> Any:
    return config.get("entradas", {}).get(key) or config.get(key)


def generar_json_calculo(config: dict, output_path: str) -> str:
    """Genera el JSON de entrada para el motor de calculo a partir de una config simplificada."""
    pisos = config.get("pisos", [])
    circuitos = []
    idx = 1
    for piso in pisos:
        for c in piso.get("circuitos", []):
            circuito = {
                "id": c.get("id", f"C{idx}"),
                "descripcion": f"{c['uso']} - {piso['nombre']}",
                "potencia_instalada_w": c["potencia_w"],
                "factor_demanda": c.get("factor_demanda", 1.0),
                "longitud_m": c.get("longitud_m", 15.0),
                "seccion_conductor_mm2": c.get("seccion_mm2", 2.5),
                "diametro_tubo_mm": c.get("tubo_mm", 20),
                "estado": "definitivo",
                "fuente": "configuracion del proyecto"
            }
            circuitos.append(circuito)
            idx += 1

    escenarios = config.get("escenarios", [
        {
            "id": "escenario_base",
            "nombre": "Escenario base",
            "estado": "definitivo",
            "descripcion": "Escenario generado automaticamente",
            "cocina_electrica": config.get("cocina_electrica", False),
            "circuito_overrides": {},
            "cne_050_200": {
                "aplicar": True,
                "cocina_electrica_normativa_w": config.get("cocina_electrica_w", 0)
            }
        }
    ])

    data = {
        "proyecto": config.get("proyecto", "Proyecto"),
        "propietario": config.get("propietario", "Estudiante"),
        "ubicacion": {
            "distrito": config.get("distrito", ""),
            "provincia": config.get("provincia", ""),
            "departamento": config.get("departamento", ""),
            "direccion": config.get("direccion", ""),
            "estado": "definitivo",
            "fuente": "configuracion del proyecto"
        },
        "areas": {
            "terreno_m2": {"valor": config.get("area_terreno_m2"), "estado": "definitivo", "fuente": "config"},
            "techada_primer_piso_m2": {"valor": config.get("area_techada_m2", {}).get("piso_1"), "estado": "definitivo", "fuente": "config"},
            "techada_segundo_piso_m2": {"valor": config.get("area_techada_m2", {}).get("piso_2"), "estado": "definitivo", "fuente": "config"},
            "techada_total_calculo_m2": {"valor": config.get("area_techada_total_m2"), "estado": "definitivo", "fuente": "config"}
        },
        "parametros_electricos": {
            "tension_v": config.get("tension_v", 220),
            "fases": config.get("fases", 1),
            "frecuencia_hz": 60,
            "factor_potencia_cosphi": config.get("factor_potencia", 0.90),
            "factor_diseno_conductor": config.get("factor_diseno", 1.25),
            "factor_diseno_estado": "criterio preliminar conservador",
            "resistividad_cobre_rho": config.get("resistividad_rho", 0.0175),
            "resistividad_cobre_fuente": "tabla CNE-U",
            "caida_tension_max_alimentador_porc": config.get("caida_alimentador_porc", 1.5),
            "caida_tension_max_alimentador_estado": "criterio del proyecto",
            "caida_tension_max_derivados_porc": config.get("caida_derivados_porc", 2.5),
            "caida_tension_total_max_cne_porc": 4.0
        },
        "alimentacion_principal": {
            "origen": "Medidor Concesionaria",
            "destino": "Tablero General (TG)",
            "longitud_m": config.get("longitud_alimentador_m", 10.0),
            "estado": "definitivo",
            "fuente": "configuracion del proyecto"
        },
        "escenario_dimensionamiento_id": escenarios[0]["id"],
        "circuitos_base": circuitos,
        "escenarios": escenarios
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    log(f"JSON de calculo generado: {output_path}")
    return output_path


def ejecutar_calculos(json_path: str, output_dir: str) -> Optional[str]:
    """Ejecuta el motor de calculos existente."""
    script = CALCULOS_DIR / "scripts" / "calcular_instalacion.py"
    cmd = [
        sys.executable, str(script),
        "--input", str(json_path),
        "--output-dir", str(output_dir)
    ]
    log(f"Ejecutando calculos: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        log(f"ERROR en calculos: {result.stderr}")
        return None
    log(result.stdout.strip())
    return output_dir


def generar_json_electrico(calculo_json_path: str, config: dict, output_path: str) -> Optional[str]:
    """Genera el JSON electrico para superposicion a partir de los resultados de calculo y config."""
    with open(calculo_json_path, "r", encoding="utf-8") as f:
        calculo = json.load(f)

    pisos_config = config.get("pisos", [])
    if not pisos_config:
        log("ADVERTENCIA: No hay configuracion de pisos para generar plano electrico")
        return None

    design = calculo["escenario_dimensionamiento"]
    circuitos_calc = {c["id"]: c for c in design["circuitos_calculados"]}

    resultado = calculo.get("resultados_electricos", design)
    ib_total = resultado["resumen_general"]["corriente_empleo_ib_total_a"]

    electric_data = {
        "title": {
            "text": f"PLANO ELECTRICO - {config.get('proyecto', 'PROYECTO').upper()}",
            "subtitle": f"Maxima Demanda: {resultado['resumen_general']['maxima_demanda_adoptada_w']:.0f} W  |  Ib: {ib_total:.2f} A",
            "x": 7.5, "y": 10.7, "height": 0.28
        },
        "luminarias": [],
        "interruptores": [],
        "tomacorrientes": [],
        "tableros": [],
        "medidores": [],
        "equipos": [],
        "rutas": [],
        "circuit_summary": [],
        "notes": [],
        "legend": {
            "x": 16.7, "y": 9.2, "width": 5.2, "height": 6.0,
            "title": "LEYENDA ELECTRICA",
            "show_meter": True
        }
    }

    for c in design["circuitos_calculados"]:
        electric_data["circuit_summary"].append({
            "id": c["id"],
            "label": f"{c['descripcion']} | {c['maxima_demanda_w']:.0f}W | {c['seccion_conductor_mm2']:.1f}mm2"
        })

    tg_pos = config.get("tablero_general", {"x": 2.0, "y": 2.0})
    electric_data["tableros"].append({
        "id": 0, "x": tg_pos["x"], "y": tg_pos["y"],
        "label": "TG", "note": f"ITM: {resultado['resumen_general']['alimentador_itm_sugerido']}"
    })

    med_pos = config.get("medidor", {"x": 0.5, "y": 0.5})
    electric_data["medidores"].append({
        "id": 0, "x": med_pos["x"], "y": med_pos["y"],
        "label": "M"
    })

    for piso_idx, piso in enumerate(pisos_config):
        for elem_type in ["luminarias", "interruptores", "tomacorrientes"]:
            for elem in piso.get(elem_type, []):
                entry = {
                    "id": elem.get("id", len(electric_data[elem_type])),
                    "x": elem["x"],
                    "y": elem["y"],
                    "circuit": elem.get("circuit", "C1"),
                    "label": f"{elem.get('circuit', 'C1')}"
                }
                if elem_type == "interruptores":
                    entry["kind"] = elem.get("kind", "simple")
                elif elem_type == "tomacorrientes":
                    entry["kind"] = elem.get("kind", "doble")
                electric_data[elem_type].append(entry)

    for elem in config.get("equipos", []):
        electric_data["equipos"].append({
            "id": elem.get("id", 0),
            "kind": elem.get("kind", "equipo"),
            "x": elem["x"], "y": elem["y"],
            "circuit": elem.get("circuit", "C1"),
            "label": elem.get("label", "")
        })

    electric_data["rutas"] = config.get("rutas", [])
    electric_data["notes"] = config.get("notas", [])

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(str(output_path), "w", encoding="utf-8") as f:
        json.dump(electric_data, f, indent=2, ensure_ascii=False)
    log(f"JSON electrico generado: {output_path}")
    return output_path


def generar_plano_dxf(layout_json_path: Optional[str], electrico_json_path: Optional[str], output_dxf: str) -> Optional[str]:
    """Genera plano DXF arquitectonico + superposicion electrica."""
    generator = CAD_DIR / "scripts" / "dxf_generator.py"
    overlay = CAD_DIR / "scripts" / "electrical_overlay.py"

    temp_dxf = output_dxf.replace(".dxf", "_arq.dxf")

    if layout_json_path and os.path.exists(layout_json_path):
        cmd_arq = [
            sys.executable, str(generator),
            "--input", str(layout_json_path),
            "--output", str(temp_dxf)
        ]
        log(f"Generando plano arquitectonico DXF...")
        result = subprocess.run(cmd_arq, capture_output=True, text=True)
        if result.returncode != 0:
            log(f"ERROR: {result.stderr}")
            return None
        base_dxf = temp_dxf
    else:
        log("ADVERTENCIA: No hay layout del proyecto; se usara el ejemplo")
        example_layout = CAD_DIR / "examples" / "layout.json"
        if not example_layout.exists():
            log("No se encontro layout de ejemplo, omitiendo CAD")
            return None
        cmd_arq = [
            sys.executable, str(generator),
            "--input", str(example_layout),
            "--output", str(temp_dxf),
        ]
        result = subprocess.run(cmd_arq, capture_output=True, text=True)
        if result.returncode != 0:
            log(f"ERROR: {result.stderr}")
            return None
        base_dxf = temp_dxf

    if electrico_json_path and os.path.exists(electrico_json_path):
        cmd_elec = [
            sys.executable, str(overlay),
            "--base", str(base_dxf),
            "--electrical", str(electrico_json_path),
            "--output", str(output_dxf)
        ]
        log(f"Superponiendo simbologia electrica...")
        result = subprocess.run(cmd_elec, capture_output=True, text=True)
        if result.returncode == 0:
            log(f"DXF final: {output_dxf}")
            return output_dxf
        else:
            log(f"ERROR: {result.stderr}")
            return None

    return base_dxf


def generar_pdf(dxf_path: Optional[str], output_pdf: str) -> Optional[str]:
    """Genera PDF a partir de DXF usando QCAD o matplotlib."""
    if not dxf_path or not os.path.exists(dxf_path):
        return None

    try:
        import matplotlib.pyplot as plt
        from ezdxf.addons.drawing import RenderContext, Frontend
        from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
        import ezdxf

        doc = ezdxf.readfile(dxf_path)
        msp = doc.modelspace()
        fig = plt.figure(figsize=(11.69, 8.27))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis("off")
        ctx = RenderContext(doc)
        out = MatplotlibBackend(ax)
        Frontend(ctx, out).draw_layout(msp, finalize=True)
        fig.savefig(output_pdf, dpi=300, bbox_inches="tight", pad_inches=0)
        plt.close(fig)
        log(f"PDF generado: {output_pdf}")
        return output_pdf
    except Exception as e:
        log(f"No se pudo generar PDF con matplotlib: {e}")
        try:
            qcad_script = CAD_DIR / "cad-scripts" / "dxf2pdf.js"
            if qcad_script.exists():
                cmd = [
                    "qcad", "-no-gui", "-platform", "offscreen", "-quit",
                    "-autostart", str(qcad_script.resolve()),
                    "-input", str(Path(dxf_path).resolve()),
                    "-output", str(Path(output_pdf).resolve())
                ]
                subprocess.run(cmd, capture_output=True, text=True)
                if os.path.exists(output_pdf):
                    log(f"PDF generado con QCAD: {output_pdf}")
                    return output_pdf
        except Exception:
            pass
        return None


def ejecutar_cad_personalizado(config_path: Path, cad_config: dict, output_dxf: str, output_pdf: str) -> Optional[str]:
    """Ejecuta un generador CAD declarado por el manifiesto del proyecto."""
    script = resolve_path(config_path, cad_config.get("script"))
    electrical = resolve_path(config_path, cad_config.get("electrical"))
    if not script or not script.exists():
        log(f"ERROR: No existe el generador CAD personalizado: {script}")
        return None
    if not electrical or not electrical.exists():
        log(f"ERROR: No existe la entrada CAD personalizada: {electrical}")
        return None

    cmd = [
        sys.executable,
        str(script),
        "--electrical", str(electrical),
        "--view", cad_config.get("view", "todo"),
        "--output", str(output_dxf),
        "--pdf", str(output_pdf),
    ]
    log(f"Ejecutando CAD personalizado: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        log(f"ERROR en CAD personalizado: {result.stderr or result.stdout}")
        return None
    log(result.stdout.strip())
    if not Path(output_dxf).exists() or not Path(output_pdf).exists():
        log("ERROR: El generador CAD no produjo todos los archivos esperados")
        return None
    return output_dxf


def generar_bom(calculo_json_path: str, config: dict, output_path: str) -> str:
    """Genera lista de materiales (BOM)."""
    with open(calculo_json_path, "r", encoding="utf-8") as f:
        calculo = json.load(f)

    design = calculo["escenario_dimensionamiento"]
    circuitos = design["circuitos_calculados"]
    resumen = design["resumen_general"]

    materiales = []
    total_cond = 0.0
    total_tubo = 0.0

    # Alimentador general
    long_alim = resumen.get("alimentador_longitud_m", 10)
    seccion_alim = resumen.get("alimentador_seccion_mm2", 10)
    materiales.append({
        "item": f"Cable TW THW {seccion_alim:.0f} mm2 (alimentador)",
        "unidad": "m",
        "cantidad": round(long_alim * 2 * 1.1),  # 2 fases + 10% desperdicio
        "uso": "Alimentador principal"
    })
    materiales.append({
        "item": f"Tubo PVC SAP {seccion_alim * 2 + 4:.0f} mm (alimentador)",
        "unidad": "m",
        "cantidad": round(long_alim * 1.1),
        "uso": "Alimentador principal"
    })
    materiales.append({
        "item": f"Interruptor termomagnetico {resumen['alimentador_itm_sugerido']}",
        "unidad": "und",
        "cantidad": 1,
        "uso": "Proteccion general"
    })

    for c in circuitos:
        long = c["longitud_m"]
        seccion = c["seccion_conductor_mm2"]
        cond_m = round(long * 2 * 1.1)
        tubo_m = round(long * 1.1)

        materiales.append({
            "item": f"Cable TW THW {seccion:.0f} mm2 - {c['id']}",
            "unidad": "m",
            "cantidad": cond_m,
            "uso": f"{c['descripcion']}"
        })
        materiales.append({
            "item": f"Tubo PVC SAP {c.get('diametro_tubo_mm', 20)} mm - {c['id']}",
            "unidad": "m",
            "cantidad": tubo_m,
            "uso": f"{c['descripcion']}"
        })
        materiales.append({
            "item": f"ITM {c['itm_sugerido']} - {c['id']}",
            "unidad": "und",
            "cantidad": 1,
            "uso": f"Proteccion {c['id']}"
        })
        materiales.append({
            "item": c["diferencial_sugerido"],
            "unidad": "und",
            "cantidad": 1,
            "uso": f"Diferencial {c['id']}"
        } if "Ver" not in c["diferencial_sugerido"] else {
            "item": "Diferencial general 2P-40A-30mA",
            "unidad": "und",
            "cantidad": 1,
            "uso": "Proteccion diferencial general"
        })
        total_cond += cond_m
        total_tubo += tubo_m

    # Tablero
    n_circuitos = len(circuitos)
    materiales.append({
        "item": f"Tablero general para {n_circuitos} circuitos",
        "unidad": "und",
        "cantidad": 1,
        "uso": "Distribucion"
    })

    # Puesta a tierra
    materiales.append({
        "item": "Varilla de puesta a tierra 5/8 x 2.4 m",
        "unidad": "und",
        "cantidad": 1,
        "uso": "SPAT"
    })
    materiales.append({
        "item": "Cable de tierra TW 10 mm2 (verde/amarillo)",
        "unidad": "m",
        "cantidad": round(total_tubo * 0.3),
        "uso": "SPAT y conexiones"
    })

    bom = {
        "proyecto": calculo["proyecto"],
        "propietario": calculo["propietario"],
        "fecha": str(date.today()),
        "resumen": {
            "potencia_instalada_w": resumen["potencia_instalada_total_w"],
            "maxima_demanda_w": resumen["maxima_demanda_adoptada_w"],
            "total_cable_m": round(total_cond),
            "total_tubo_m": round(total_tubo)
        },
        "materiales": materiales
    }

    with open(str(output_path), "w", encoding="utf-8") as f:
        json.dump(bom, f, indent=2, ensure_ascii=False)

    md_lines = [
        f"# Lista de Materiales - {bom['proyecto']}",
        f"**Propietario:** {bom['propietario']}",
        f"**Fecha:** {bom['fecha']}",
        "",
        "## Resumen",
        f"- Potencia instalada: {bom['resumen']['potencia_instalada_w']:.0f} W",
        f"- Maxima demanda: {bom['resumen']['maxima_demanda_w']:.0f} W",
        f"- Total cable: {bom['resumen']['total_cable_m']} m",
        f"- Total tuberia: {bom['resumen']['total_tubo_m']} m",
        "",
        "## Materiales",
        "",
        "| Item | Unidad | Cantidad | Uso |",
        "|---|---|---:|---|",
    ]
    for m in materiales:
        md_lines.append(f"| {m['item']} | {m['unidad']} | {m['cantidad']} | {m['uso']} |")

    bom_md = str(output_path).replace(".json", ".md")
    with open(bom_md, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    log(f"BOM generado: {output_path}")
    log(f"BOM Markdown: {bom_md}")
    return output_path


def generar_config_ejemplo(output_path: str) -> str:
    """Genera un archivo de configuracion YAML de ejemplo."""
    ejemplo = """# Configuracion de proyecto de instalaciones electricas
# Generado por pipeline_automatizado.py

proyecto: "Vivienda Unifamiliar - Ejemplo"
propietario: "Juan Perez"
distrito: "San Miguel"
provincia: "San Roman"
departamento: "Puno"
direccion: "Av. Principal 123"

# Datos electricos generales
tension_v: 220
fases: 1
factor_potencia: 0.90
factor_diseno: 1.25
resistividad_rho: 0.0175
caida_alimentador_porc: 1.5
caida_derivados_porc: 2.5

# Areas
area_terreno_m2: 120.0
area_techada_total_m2: 100.0
area_techada_m2:
  piso_1: 60.0
  piso_2: 40.0

# Longitud del alimentador (medidor -> TG)
longitud_alimentador_m: 12.0

# Cocina electrica (opcional)
cocina_electrica: false
cocina_electrica_w: 0

# Posicion del tablero general y medidor en el plano
tablero_general:
  x: 2.0
  y: 2.0
medidor:
  x: 0.5
  y: 0.5

# Definicion de pisos y sus circuitos/elementos
pisos:
  - nombre: "Primer Piso"
    circuitos:
      - id: C1
        uso: "Alumbrado 1er Piso"
        potencia_w: 120
        factor_demanda: 1.0
        longitud_m: 15.0
        seccion_mm2: 2.5
        tubo_mm: 20
      - id: C2
        uso: "Tomacorrientes 1er Piso"
        potencia_w: 1800
        factor_demanda: 0.70
        longitud_m: 20.0
        seccion_mm2: 2.5
        tubo_mm: 20
      - id: C3
        uso: "Cocina 1er Piso"
        potencia_w: 500
        factor_demanda: 0.80
        longitud_m: 10.0
        seccion_mm2: 4.0
        tubo_mm: 25

    # Elementos electricos en el plano (coordenadas en metros)
    luminarias:
      - id: L1
        x: 3.0
        y: 3.0
        circuit: C1
      - id: L2
        x: 5.0
        y: 3.0
        circuit: C1

    interruptores:
      - id: S1
        x: 2.2
        y: 2.8
        circuit: C1
        kind: simple

    tomacorrientes:
      - id: T1
        x: 2.5
        y: 1.5
        circuit: C2
        kind: doble
      - id: T2
        x: 4.5
        y: 1.5
        circuit: C2
        kind: tierra

  - nombre: "Segundo Piso"
    circuitos:
      - id: C4
        uso: "Alumbrado 2do Piso"
        potencia_w: 100
        factor_demanda: 1.0
        longitud_m: 12.0
        seccion_mm2: 2.5
        tubo_mm: 20
      - id: C5
        uso: "Tomacorrientes 2do Piso"
        potencia_w: 1500
        factor_demanda: 0.70
        longitud_m: 18.0
        seccion_mm2: 2.5
        tubo_mm: 20

    luminarias:
      - id: L3
        x: 3.0
        y: 7.0
        circuit: C4

    interruptores:
      - id: S2
        x: 2.2
        y: 6.8
        circuit: C4
        kind: simple

    tomacorrientes:
      - id: T3
        x: 2.5
        y: 5.5
        circuit: C5
        kind: doble

# Rutas de canalizacion (conexiones entre elementos)
rutas:
  - id: R1
    circuit: C1
    label: C1
    points: [[2.0, 2.0], [3.0, 2.8], [3.0, 3.0], [5.0, 3.0]]
    linetype: DASHED
  - id: R2
    circuit: C2
    label: C2
    points: [[2.0, 2.0], [2.5, 1.5], [4.5, 1.5]]
    linetype: DASHED

# Notas en el plano
notas:
  - text: "NOTAS:\\n1. Todas las canalizaciones son empotradas.\\n2. Altura de interruptores: 1.20 m.\\n3. Altura de tomacorrientes: 0.40 m."
    x: 0.5
    y: 1.0
    height: 0.13

# Escenarios de calculo
escenarios:
  - id: escenario_base
    nombre: "Escenario base"
    estado: "definitivo"
    descripcion: "Escenario generado automaticamente"
    cocina_electrica: false
    circuito_overrides: {}
    cne_050_200:
      aplicar: true
      cocina_electrica_normativa_w: 0
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ejemplo)
    log(f"Configuracion de ejemplo generada: {output_path}")
    return output_path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Pipeline automatizado de instalaciones electricas"
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--config", help="Archivo YAML/JSON de configuracion del proyecto")
    source.add_argument("--proyecto", help="ID de una carpeta dentro de proyectos/")
    parser.add_argument("--generar-ejemplo", action="store_true",
                       help="Generar archivo de configuracion de ejemplo")
    parser.add_argument("--output-dir", help="Directorio de salida; por defecto build/<proyecto>")
    parser.add_argument("--skip-cad", action="store_true",
                       help="Saltar generacion de planos CAD")
    parser.add_argument("--skip-bom", action="store_true",
                       help="Saltar generacion de lista de materiales")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.generar_ejemplo:
        output_dir = Path(args.output_dir or REPO_ROOT / "build" / "ejemplo")
        ejemplo_path = output_dir / "proyecto_ejemplo.yaml"
        output_dir.mkdir(parents=True, exist_ok=True)
        generar_config_ejemplo(ejemplo_path)
        print(f"\nConfiguracion de ejemplo creada en: {ejemplo_path}")
        print("Ejecuta: python3 pipeline_automatizado.py --config " + ejemplo_path)
        return

    if not args.config and not args.proyecto:
        print("ERROR: Debes especificar --proyecto, --config o --generar-ejemplo")
        print("Usa: python3 pipeline_automatizado.py --generar-ejemplo")
        sys.exit(1)

    if args.proyecto:
        config_path = PROJECTS_DIR / args.proyecto / "proyecto.yaml"
    else:
        config_path = Path(args.config)

    if not config_path.exists():
        print(f"ERROR: No existe el archivo: {config_path}")
        sys.exit(1)

    log(f"Iniciando pipeline para: {config_path.name}")
    print("=" * 60)

    # 1. Cargar configuracion
    config = load_config(config_path)
    if config.get("automatizacion", {}).get("pipeline_habilitado") is False:
        log("ERROR: El manifiesto marca este pipeline como pendiente de migracion")
        sys.exit(2)

    script_nativo = config.get("automatizacion", {}).get("script_nativo")
    if script_nativo:
        script_path = resolve_path(config_path, script_nativo)
        if not script_path or not script_path.exists():
            log(f"ERROR: No existe el pipeline nativo: {script_path}")
            sys.exit(1)
        log(f"Ejecutando pipeline nativo: {script_path}")
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(config_path.parent),
        )
        sys.exit(result.returncode)

    project_id = args.proyecto or config_path.parent.name or config_path.stem
    out = Path(args.output_dir or REPO_ROOT / "build" / project_id)
    out.mkdir(parents=True, exist_ok=True)

    # 2. Generar JSON de calculo
    calculo_json = out / "calculo.json"
    calculos_source = resolve_path(config_path, config_input(config, "calculos_json"))
    if calculos_source:
        if not calculos_source.exists():
            log(f"ERROR: No existe la entrada de calculos: {calculos_source}")
            sys.exit(1)
        shutil.copy2(calculos_source, calculo_json)
        log(f"Entrada de calculo copiada desde: {calculos_source}")
    else:
        generar_json_calculo(config, calculo_json)

    # 3. Ejecutar calculos
    calculos_out = out / "calculos"
    if ejecutar_calculos(calculo_json, calculos_out) is None:
        sys.exit(1)

    # Leer resultados
    resultados_json = calculos_out / "resultados.json"
    if not resultados_json.exists():
        log("ERROR: No se generaron los resultados de calculo")
        sys.exit(1)

    # Mostrar resumen
    with open(resultados_json) as f:
        resultados = json.load(f)
    r = resultados["escenario_dimensionamiento"]["resumen_general"]
    print(f"\n--- RESUMEN DEL PROYECTO ---")
    print(f"  Potencia instalada: {r['potencia_instalada_total_w']:.0f} W")
    print(f"  Maxima demanda:     {r['maxima_demanda_adoptada_w']:.0f} W")
    print(f"  Corriente total:    {r['corriente_empleo_ib_total_a']:.2f} A")
    print(f"  Alimentador:        {r['alimentador_seccion_mm2']:.1f} mm2")
    print(f"  ITM general:        {r['alimentador_itm_sugerido']}")
    print(f"  Caida de tension:   {r['alimentador_caida_tension_porc']:.3f}%")

    # 4. Generar JSON electrico
    electrico_json = out / "electrico.json"
    electrico_source = resolve_path(config_path, config_input(config, "electrico_json"))
    if electrico_source:
        if not electrico_source.exists():
            log(f"ERROR: No existe la entrada electrica: {electrico_source}")
            sys.exit(1)
        shutil.copy2(electrico_source, electrico_json)
        log(f"Entrada electrica copiada desde: {electrico_source}")
    else:
        generar_json_electrico(resultados_json, config, electrico_json)

    # 5. Generar plano CAD
    layout_json = None
    layout_path = config_input(config, "layout_json")
    if layout_path:
        layout_json = resolve_path(config_path, layout_path)
        if not layout_json.exists():
            layout_json = None

    dxf_output = None
    cad_ok = True
    if not args.skip_cad:
        dxf_output = str(out / "plano_electrico.dxf")
        pdf_output = str(out / "plano_electrico.pdf")
        cad_personalizado = config.get("automatizacion", {}).get("cad_personalizado")
        if cad_personalizado:
            result = ejecutar_cad_personalizado(
                config_path, cad_personalizado, dxf_output, pdf_output
            )
        else:
            result = generar_plano_dxf(layout_json, electrico_json, dxf_output)
            if result:
                pdf_result = generar_pdf(result, pdf_output)
                cad_ok = bool(pdf_result and Path(dxf_output).exists())
            else:
                cad_ok = False
        if cad_personalizado:
            cad_ok = bool(result)

    # 6. Generar BOM
    if not args.skip_bom:
        bom_json = out / "bom.json"
        generar_bom(resultados_json, config, bom_json)

    # 7. Copiar tablas LaTeX
    tex_src = calculos_out
    tex_dst = out / "latex"
    os.makedirs(tex_dst, exist_ok=True)
    for f_name in os.listdir(tex_src):
        if f_name.endswith(".tex"):
            shutil.copy2(os.path.join(tex_src, f_name), os.path.join(tex_dst, f_name))

    print(f"\n{'=' * 60}")
    log(f"Pipeline completado exitosamente!")
    print(f"  Resultados:  {out}")
    print(f"  Calculos:    {calculos_out}")
    print(f"  Tablas LaTeX: {tex_dst}")
    if not args.skip_cad and cad_ok:
        print(f"  Plano DXF:   {dxf_output}")
        print(f"  Plano PDF:   {pdf_output}")
    if not args.skip_bom:
        print(f"  BOM:         {out / 'bom.json'}")
    print("=" * 60)
    if not cad_ok:
        log("Pipeline incompleto: fallo la etapa CAD")
        sys.exit(2)


if __name__ == "__main__":
    main()

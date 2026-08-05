#!/usr/bin/env python3
"""
Generador de proyectos QElectroTech (.qet) a partir de resultados JSON.

Transforma los resultados de cálculo eléctrico (circuitos, alimentador, ITM, ID)
en un proyecto de diagrama unifilar en formato XML para QElectroTech (QET).

Uso:
  python3 qet_generator.py --resultados build/proyecto/calculos/resultados.json --output build/proyecto/unifilar.qet
"""

import argparse
import json
import os
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_qet_xml(data):
    """
    Construye la estructura XML estándar de QElectroTech para el Diagrama Unifilar.
    """
    qet = ET.Element("qet-project", {
        "version": "0.90",
        "title": "Diagrama Unifilar Tablero General TD - Norma DGE/MEM Perú"
    })
    
    # Extraer información del proyecto
    nombre_proyecto = data.get("proyecto", "Instalaciones Eléctricas Unifamiliares")
    if isinstance(nombre_proyecto, dict):
        nombre_proyecto = nombre_proyecto.get("nombre", "Instalaciones Eléctricas")
        
    propietario = data.get("propietario", "Diego Jefferson Charaja Mamani")
    if isinstance(propietario, dict):
        propietario = propietario.get("nombre", "Diego Jefferson Charaja Mamani")
        
    # Extraer alimentador y resumen
    escenario = data.get("escenario_dimensionamiento", {})
    if isinstance(escenario, dict):
        resumen = escenario.get("resumen_general", {})
        circuitos = escenario.get("circuitos_calculados", [])
    else:
        resumen = data.get("resumen_general", {})
        circuitos = data.get("circuitos", [])
        
    itm_general = resumen.get("alimentador_itm_sugerido") or resumen.get("alimentador_itm_a", "ITM Tripolar 3x40A (10 kA)")
    alimentador_cable = f"3-1x{resumen.get('alimentador_seccion_mm2', 10.0)} mm² NH-80 en PVC-P {resumen.get('alimentador_tuberia_mm', 25)} mmØ"
    
    # Propiedades del Proyecto
    props = ET.SubElement(qet, "properties")
    ET.SubElement(props, "property", {"name": "propietario", "value": str(propietario)})
    ET.SubElement(props, "property", {"name": "proyecto", "value": str(nombre_proyecto)})
    ET.SubElement(props, "property", {"name": "docente", "value": "Ing. Villanueva Cornejo Marcos Jose"})
    ET.SubElement(props, "property", {"name": "asignatura", "value": "Instalaciones Eléctricas (Grupo B)"})
    ET.SubElement(props, "property", {"name": "escuela", "value": "EPIME - FIMEES - UNAP"})
    
    # Diagrama principal
    diagram = ET.SubElement(qet, "diagram", {
        "width": "1050",
        "height": "1485",
        "title": "Diagrama Unifilar Tablero General (TD)",
        "order": "1"
    })
    
    # Rótulo / Cartouche
    inset = ET.SubElement(diagram, "inset")
    ET.SubElement(inset, "title").text = "DIAGRAMA UNIFILAR TABLERO GENERAL (TD)"
    ET.SubElement(inset, "author").text = str(propietario)
    ET.SubElement(inset, "date").text = "2026-06-15"
    ET.SubElement(inset, "folio").text = "IE-01"
    ET.SubElement(inset, "plant").text = "Vivienda Unifamiliar 3 Niveles - Puno"
    
    # Elementos del Esquema Unifilar
    elements = ET.SubElement(diagram, "elements")

    # Acometida / Red Concesionaria
    ET.SubElement(elements, "element", {
        "type": "acometida_red",
        "x": "100", "y": "100",
        "label": "RED SECUNDARIA 220V 3Ø 60Hz - ELECTRO PUNO S.A.A."
    })
    
    # Medidor M-1
    ET.SubElement(elements, "element", {
        "type": "medidor_kwh",
        "x": "100", "y": "200",
        "label": "MEDIDOR M-1 (Caja LT de Cobre)"
    })
    
    # Alimentador General
    ET.SubElement(elements, "element", {
        "type": "alimentador_general",
        "x": "100", "y": "300",
        "label": f"Alimentador General: {alimentador_cable}"
    })
    
    # ITM General
    ET.SubElement(elements, "element", {
        "type": "itm_tripolar",
        "x": "100", "y": "400",
        "label": f"ITM General: {itm_general}"
    })
    
    # Barras R-S-T
    ET.SubElement(elements, "element", {
        "type": "barras_colectoras",
        "x": "100", "y": "500",
        "label": "BARRAS COLECTORAS CU 100A (FASES R - S - T)"
    })
    
    # Circuitos Derivados C-1 a C-N
    x_pos = 100
    for circ in circuitos:
        c_id = circ.get("id", "C-?")
        c_desc = circ.get("descripcion", "")
        c_itm = circ.get("itm_a") or circ.get("itm", "2x16A")
        c_id_diff = circ.get("diferencial_sugerido") or circ.get("id_diferencial", "ID 2x25A 30mA")
        c_cable = f"2x{circ.get('seccion_conductor_mm2', 2.5)} mm² NH-80"
        
        ET.SubElement(elements, "element", {
            "type": "circuito_derivado",
            "x": str(x_pos),
            "y": "600",
            "id": c_id,
            "label": f"{c_id}: {c_desc} | ITM {c_itm} | {c_id_diff} | {c_cable}"
        })
        x_pos += 120
        
    return qet


def save_pretty_xml(element, filepath):
    raw_str = ET.tostring(element, encoding="utf-8")
    reparsed = minidom.parseString(raw_str)
    pretty_str = reparsed.toprettyxml(indent="  ")
    
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(pretty_str)


def main():
    parser = argparse.ArgumentParser(description="Generador de proyectos QElectroTech (.qet) desde JSON")
    parser.add_argument("--resultados", required=True, help="Ruta al archivo JSON de resultados de cálculo")
    parser.add_argument("--output", required=True, help="Ruta de salida del archivo .qet")
    args = parser.parse_args()
    
    if not os.path.exists(args.resultados):
        print(f"Error: No existe el archivo {args.resultados}")
        sys.exit(1)
        
    data = load_json(args.resultados)
    qet_tree = build_qet_xml(data)
    save_pretty_xml(qet_tree, args.output)
    print(f"Proyecto QElectroTech (.qet) generado exitosamente en: {args.output}")


if __name__ == "__main__":
    main()

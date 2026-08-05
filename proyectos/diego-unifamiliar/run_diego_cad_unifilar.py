import json
import os
import subprocess

TARGET_DIR = "/storage/emulated/0/universida-datos/instalacion-electricas/proyectos/diego-unifamiliar"
os.makedirs(TARGET_DIR, exist_ok=True)

# Build calculation results JSON matching ezdxf CAD engine schema
resultados_diego = {
    "proyecto": "Instalaciones Eléctricas Interiores - Vivienda Unifamiliar de 3 Niveles",
    "propietario": "CHARAJA MAMANI DIEGO JEFFERSON (Cód. 214254)",
    "escenario_dimensionamiento": {
        "resumen_general": {
            "maxima_demanda_adoptada_w": 13500.0,
            "potencia_instalada_total_w": 18250.0,
            "corriente_empleo_ib_total_a": 39.36,
            "corriente_diseno_id_a": 49.20,
            "alimentador_seccion_mm2": 10.0,
            "alimentador_itm_a": "3x40A (10 kA)",
            "alimentador_itm_sugerido": "ITM Tripolar 3x40A",
            "alimentador_tuberia_mm": 25,
            "caida_tension_alimentador_porc": 0.81
        },
        "circuitos_calculados": [
            {
                "id": "C-1",
                "descripcion": "Alumbrado y Tomacorrientes Generales (1er Piso)",
                "potencia_instalada_w": 2500,
                "maxima_demanda_w": 2500,
                "ib_a": 12.63,
                "itm_a": "2x16A (6 kA)",
                "diferencial_sugerido": "ID 2x25A 30mA",
                "seccion_conductor_mm2": 2.5,
                "tuberia_mm": 20,
                "caida_tension_porc": 0.95,
                "cumple_conductor": "CUMPLE",
                "requiere_tierra": True
            },
            {
                "id": "C-2",
                "descripcion": "Alumbrado y Tomacorrientes (2do Piso y Azotea)",
                "potencia_instalada_w": 2000,
                "maxima_demanda_w": 700,
                "ib_a": 3.54,
                "itm_a": "2x16A (6 kA)",
                "diferencial_sugerido": "ID 2x25A 30mA",
                "seccion_conductor_mm2": 2.5,
                "tuberia_mm": 20,
                "caida_tension_porc": 0.42,
                "cumple_conductor": "CUMPLE",
                "requiere_tierra": True
            },
            {
                "id": "C-3",
                "descripcion": "Cocina Eléctrica (Primer Piso - 3Ø)",
                "potencia_instalada_w": 6000,
                "maxima_demanda_w": 4800,
                "ib_a": 13.99,
                "itm_a": "3x25A (6 kA)",
                "diferencial_sugerido": "ID 3x32A 30mA",
                "seccion_conductor_mm2": 6.0,
                "tuberia_mm": 25,
                "caida_tension_porc": 0.68,
                "cumple_conductor": "CUMPLE",
                "requiere_tierra": True
            },
            {
                "id": "C-4",
                "descripcion": "Terma Eléctrica (Segundo Piso)",
                "potencia_instalada_w": 1500,
                "maxima_demanda_w": 1500,
                "ib_a": 7.58,
                "itm_a": "2x16A (6 kA)",
                "diferencial_sugerido": "ID 2x25A 30mA",
                "seccion_conductor_mm2": 4.0,
                "tuberia_mm": 20,
                "caida_tension_porc": 0.55,
                "cumple_conductor": "CUMPLE",
                "requiere_tierra": True
            },
            {
                "id": "C-5",
                "descripcion": "Electrobomba de Agua (0.75 HP Cisterna)",
                "potencia_instalada_w": 750,
                "maxima_demanda_w": 750,
                "ib_a": 3.79,
                "itm_a": "2x16A (6 kA)",
                "diferencial_sugerido": "ID 2x25A 30mA",
                "seccion_conductor_mm2": 2.5,
                "tuberia_mm": 20,
                "caida_tension_porc": 0.45,
                "cumple_conductor": "CUMPLE",
                "requiere_tierra": True
            },
            {
                "id": "C-6",
                "descripcion": "Tomacorrientes Especiales Cocina",
                "potencia_instalada_w": 1500,
                "maxima_demanda_w": 750,
                "ib_a": 3.79,
                "itm_a": "2x20A (6 kA)",
                "diferencial_sugerido": "ID 2x25A 30mA",
                "seccion_conductor_mm2": 4.0,
                "tuberia_mm": 20,
                "caida_tension_porc": 0.38,
                "cumple_conductor": "CUMPLE",
                "requiere_tierra": True
            },
            {
                "id": "C-7",
                "descripcion": "Lavadora y Secadora de Ropa (Azotea)",
                "potencia_instalada_w": 2500,
                "maxima_demanda_w": 1750,
                "ib_a": 8.84,
                "itm_a": "2x20A (6 kA)",
                "diferencial_sugerido": "ID 2x25A 30mA",
                "seccion_conductor_mm2": 4.0,
                "tuberia_mm": 20,
                "caida_tension_porc": 0.72,
                "cumple_conductor": "CUMPLE",
                "requiere_tierra": True
            },
            {
                "id": "C-8",
                "descripcion": "Cargas Especiales de Reserva",
                "potencia_instalada_w": 1500,
                "maxima_demanda_w": 750,
                "ib_a": 3.79,
                "itm_a": "2x20A (6 kA)",
                "diferencial_sugerido": "Reserva equipada",
                "seccion_conductor_mm2": 4.0,
                "tuberia_mm": 20,
                "caida_tension_porc": 0.38,
                "cumple_conductor": "CUMPLE",
                "requiere_tierra": True
            }
        ]
    }
}

json_path = os.path.join(TARGET_DIR, "resultados_diego.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(resultados_diego, f, indent=2, ensure_ascii=False)

print(f"JSON resultados salvado en {json_path}")

# Run generar_unifilar.py tool from repo
gen_script = "/storage/emulated/0/universida-datos/instalacion-electricas/herramientas/cad/scripts/generar_unifilar.py"
output_dxf = os.path.join(TARGET_DIR, "plano_unifilar_diego_cad.dxf")
output_pdf = os.path.join(TARGET_DIR, "plano_unifilar_diego_cad.pdf")

subprocess.run(["python3", gen_script, "--resultados", json_path, "--output", output_dxf], check=True)
print("DXF generated successfully!")

subprocess.run(["python3", gen_script, "--resultados", json_path, "--output", output_pdf], check=True)
print("PDF generated successfully!")


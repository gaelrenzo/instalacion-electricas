#!/usr/bin/env python3
"""
Script generador de catalogo y biblioteca de simbologia DGE en formato DXF.
Lee las definiciones vectoriales de simbologia_normativa_dge.json, crea bloques
y genera una lamina catalogo ordenada en grilla por categorias.
"""

import os
import json
import sys
from pathlib import Path

# Intentar importar ezdxf
try:
    import ezdxf
    from ezdxf.enums import TextEntityAlignment
except ImportError:
    print("Error: ezdxf no esta instalado. Instalandolo...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "ezdxf"])
    import ezdxf
    from ezdxf.enums import TextEntityAlignment

# Intentar importar matplotlib para el renderizado PDF
try:
    import matplotlib.pyplot as plt
    from ezdxf.addons.drawing import RenderContext, Frontend
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Advertencia: matplotlib no esta disponible. No se generara el PDF automaticamente.")

# Rutas de archivos
BASE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = BASE_DIR / "simbologia_normativa_dge.json"
OUTPUT_DXF = BASE_DIR / "salidas" / "simbologia_dge_completa.dxf"
OUTPUT_PDF = BASE_DIR / "salidas" / "simbologia_dge_completa.pdf"

# Definicion de colores AutoCAD ACI
COLOR_ROJO = 1
COLOR_AMARILLO = 2
COLOR_VERDE = 3
COLOR_CYAN = 4
COLOR_AZUL = 5
COLOR_VIOLETA = 6
COLOR_BLANCO_NEGRO = 7
COLOR_GRIS_OSCURO = 8
COLOR_GRIS_CLARO = 9

def cargar_biblioteca_json():
    if not JSON_PATH.exists():
        print(f"Error: No existe el archivo JSON de simbologia en: {JSON_PATH}")
        sys.exit(1)
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def crear_capas(doc):
    capas = [
        ("SIMBOLOS_DGE", COLOR_AMARILLO, 25),
        ("TEXTOS_CODIGOS", COLOR_ROJO, 18),
        ("TEXTOS_NOMBRES", COLOR_BLANCO_NEGRO, 13),
        ("CELDAS_GUIA", COLOR_GRIS_OSCURO, 9),
        ("OBSERVACIONES", COLOR_GRIS_CLARO, 9),
        ("TITULOS", COLOR_CYAN, 30),
        ("MARCOS", COLOR_BLANCO_NEGRO, 35)
    ]
    for name, color, lw in capas:
        if name not in doc.layers:
            doc.layers.new(name, dxfattribs={
                "color": color,
                "lineweight": lw
            })

def crear_bloque_simbolo(doc, simbolo):
    block_name = simbolo["block_name"]
    # Si el bloque ya existe, lo eliminamos o lo omitimos para evitar duplicados
    if block_name in doc.blocks:
        return doc.blocks.get(block_name)
    
    block = doc.blocks.new(name=block_name)
    layer = "SIMBOLOS_DGE"
    
    for prim in simbolo["primitivas"]:
        tipo = prim["tipo"]
        try:
            if tipo == "linea":
                block.add_line(
                    (float(prim["x1"]), float(prim["y1"])),
                    (float(prim["x2"]), float(prim["y2"])),
                    dxfattribs={"layer": layer}
                )
            elif tipo == "circulo":
                block.add_circle(
                    (float(prim["cx"]), float(prim["cy"])),
                    float(prim["r"]),
                    dxfattribs={"layer": layer}
                )
            elif tipo == "circulo_relleno":
                r = float(prim["r"])
                cx = float(prim["cx"])
                cy = float(prim["cy"])
                # Dibujar el contorno del circulo
                block.add_circle((cx, cy), r, dxfattribs={"layer": layer})
                # Rellenar con Hatch solido
                hatch = block.add_hatch(dxfattribs={"layer": layer})
                hatch.set_solid_fill()
                # ezdxf requiere un path cerrado para el hatch
                # Usamos una aproximacion de circulo con un spline o arco cerrado,
                # pero para maxima compatibilidad en QCAD usamos una polilinea circular
                edge_path = hatch.paths.add_edge_path()
                edge_path.add_arc((cx, cy), r, 0, 360)
            elif tipo == "rectangulo":
                x = float(prim["x"])
                y = float(prim["y"])
                w = float(prim["w"])
                h = float(prim["h"])
                pts = [(x, y), (x+w, y), (x+w, y+h), (x, y+h), (x, y)]
                block.add_lwpolyline(pts, dxfattribs={"layer": layer})
            elif tipo == "rectangulo_relleno":
                x = float(prim["x"])
                y = float(prim["y"])
                w = float(prim["w"])
                h = float(prim["h"])
                # Rellenar con un solido ACI (ezdxf requiere puntos en orden de triangulacion 0,1,3,2)
                block.add_solid(
                    [(x, y), (x+w, y), (x, y+h), (x+w, y+h)],
                    dxfattribs={"layer": layer}
                )
            elif tipo == "arco":
                cx = float(prim["cx"])
                cy = float(prim["cy"])
                r = float(prim["r"])
                start = float(prim["ang_ini"])
                end = float(prim["ang_fin"])
                block.add_arc(
                    (cx, cy), r, start, end,
                    dxfattribs={"layer": layer}
                )
            elif tipo == "texto":
                text_entity = block.add_text(
                    str(prim["contenido"]),
                    dxfattribs={"layer": layer, "height": float(prim["h"])}
                )
                text_entity.set_placement(
                    (float(prim["x"]), float(prim["y"])),
                    align=TextEntityAlignment.MIDDLE_CENTER
                )
            elif tipo == "punto":
                block.add_circle(
                    (float(prim["x"]), float(prim["y"])),
                    float(prim["r"]),
                    dxfattribs={"layer": layer}
                )
        except Exception as e:
            print(f"Error procesando primitiva {prim} en simbolo {simbolo['id']}: {e}")
            
    return block

def dibujar_lamina_catalogo(doc, data):
    msp = doc.modelspace()
    simbolos = data["simbolos"]
    
    # Agrupar simbolos por categoria
    categorias = {}
    for sim in simbolos:
        cat = sim.get("categoria", "OTROS SIMBOLOS DGE").upper()
        if cat not in categorias:
            categorias[cat] = []
        categorias[cat].append(sim)
        
    # Parametros de grilla
    celda_w = 60.0
    celda_h = 35.0
    cols_por_fila = 3
    separacion_y = 15.0
    
    start_x = 0.0
    start_y = 0.0
    
    current_y = start_y
    
    for cat, sim_list in categorias.items():
        # Escribir titulo de la categoria
        current_y -= 10.0
        msp.add_text(
            f"=== CATEGORIA: {cat} ===",
            dxfattribs={"layer": "TITULOS", "height": 3.5}
        ).set_placement((start_x, current_y), align=TextEntityAlignment.MIDDLE_LEFT)
        current_y -= 12.0
        
        # Dibujar grilla de celdas para esta categoria
        for i, sim in enumerate(sim_list):
            col = i % cols_por_fila
            row = i // cols_por_fila
            
            x = start_x + col * (celda_w + 10.0)
            y = current_y - row * (celda_h + 10.0)
            
            # 1. Dibujar celda guia (capa CELDAS_GUIA)
            rect_pts = [(x, y), (x + celda_w, y), (x + celda_w, y - celda_h), (x, y - celda_h), (x, y)]
            msp.add_lwpolyline(rect_pts, dxfattribs={"layer": "CELDAS_GUIA"})
            
            # 2. Crear bloque e insertar simbolo
            crear_bloque_simbolo(doc, sim)
            # Centro del simbolo en X: x+15, Y: y-17.5
            sym_x = x + 15.0
            sym_y = y - 17.5
            scale_factor = 45.0  # Escalar para que el simbolo sea muy legible en la celda 60x35
            
            msp.add_blockref(
                sim["block_name"],
                insert=(sym_x, sym_y),
                dxfattribs={
                    "layer": "SIMBOLOS_DGE",
                    "xscale": scale_factor,
                    "yscale": scale_factor,
                    "zscale": scale_factor
                }
            )
            
            # 3. Escribir metadatos a la derecha (X: x+30)
            text_x = x + 30.0
            
            # Codigo DGE
            msp.add_text(
                f"COD: {sim['codigo_dge']}",
                dxfattribs={"layer": "TEXTOS_CODIGOS", "height": 1.8}
            ).set_placement((text_x, y - 8.0), align=TextEntityAlignment.MIDDLE_LEFT)
            
            # Nombre del Simbolo (soporte para multilinea simple si es largo)
            nombre = sim["nombre"]
            if len(nombre) > 28:
                # Partir en dos lineas si es muy largo
                partes = nombre.split(" ")
                mitad = len(partes) // 2
                nombre_l1 = " ".join(partes[:mitad])
                nombre_l2 = " ".join(partes[mitad:])
                msp.add_text(
                    nombre_l1,
                    dxfattribs={"layer": "TEXTOS_NOMBRES", "height": 1.4}
                ).set_placement((text_x, y - 15.0), align=TextEntityAlignment.MIDDLE_LEFT)
                msp.add_text(
                    nombre_l2,
                    dxfattribs={"layer": "TEXTOS_NOMBRES", "height": 1.4}
                ).set_placement((text_x, y - 20.0), align=TextEntityAlignment.MIDDLE_LEFT)
                y_offset_obs = -26.0
            else:
                msp.add_text(
                    nombre,
                    dxfattribs={"layer": "TEXTOS_NOMBRES", "height": 1.5}
                ).set_placement((text_x, y - 16.0), align=TextEntityAlignment.MIDDLE_LEFT)
                y_offset_obs = -24.0
                
            # Observaciones
            obs = sim.get("observaciones", "")
            if len(obs) > 30:
                obs = obs[:28] + "..."
            if obs:
                msp.add_text(
                    f"* {obs}",
                    dxfattribs={"layer": "OBSERVACIONES", "height": 1.0}
                ).set_placement((text_x, y + y_offset_obs), align=TextEntityAlignment.MIDDLE_LEFT)
                
        # Calcular el Y para la siguiente categoria
        filas = (len(sim_list) - 1) // cols_por_fila + 1
        current_y -= filas * (celda_h + 10.0) + separacion_y
        
    # Dibujar un marco exterior general a la lamina
    extents_min_x = start_x - 5.0
    extents_max_x = start_x + cols_por_fila * (celda_w + 10.0)
    extents_min_y = current_y + separacion_y
    extents_max_y = start_y + 10.0
    
    marco_pts = [
        (extents_min_x, extents_max_y),
        (extents_max_x, extents_max_y),
        (extents_max_x, extents_min_y),
        (extents_min_x, extents_min_y),
        (extents_min_x, extents_max_y)
    ]
    msp.add_lwpolyline(marco_pts, dxfattribs={"layer": "MARCOS"})
    
    # Escribir titulo principal del plano
    msp.add_text(
        "BIBLIOTECA COMPLETA DE SIMBOLOGIA ELECTRICA - NORMA DGE (SECCION 9)",
        dxfattribs={"layer": "TITULOS", "height": 4.5}
    ).set_placement((start_x + 10.0, start_y + 5.0), align=TextEntityAlignment.MIDDLE_LEFT)

def exportar_a_pdf():
    if not HAS_MATPLOTLIB:
        print("No se exportara a PDF porque matplotlib o dependencias de dibujo no estan disponibles.")
        return False
        
    print(f"Exportando {OUTPUT_DXF} a PDF en {OUTPUT_PDF}...")
    try:
        doc = ezdxf.readfile(OUTPUT_DXF)
        msp = doc.modelspace()
        
        # Configurar lienzo de matplotlib para una hoja de catalogo
        fig = plt.figure(figsize=(22, 34), dpi=150)
        ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
        ax.set_aspect("equal")
        ax.axis("off")
        
        ctx = RenderContext(doc)
        
        out = MatplotlibBackend(ax)
        Frontend(ctx, out).draw_layout(msp, finalize=True)
        
        # Guardar lamina
        OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(OUTPUT_PDF, dpi=200, bbox_inches="tight", pad_inches=0.1)
        plt.close(fig)
        print(f"PDF generado exitosamente en: {OUTPUT_PDF}")
        return True
    except Exception as e:
        print(f"Error renderizando PDF: {e}")
        return False

def main():
    print("Iniciando Generador de Catalogo DXF de Simbologia DGE...")
    data = cargar_biblioteca_json()
    
    # Crear un nuevo dibujo DXF R2010
    doc = ezdxf.new("R2010")
    
    # Configurar capas
    crear_capas(doc)
    
    # Dibujar la lamina
    dibujar_lamina_catalogo(doc, data)
    
    # Guardar DXF
    OUTPUT_DXF.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(OUTPUT_DXF)
    print(f"Archivo DXF del catalogo guardado en: {OUTPUT_DXF}")
    
    # Exportar a PDF
    exportar_a_pdf()
    
    print("¡Proceso finalizado con exito!")

if __name__ == "__main__":
    main()

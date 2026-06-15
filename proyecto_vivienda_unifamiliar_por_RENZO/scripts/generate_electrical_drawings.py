import os
import json
import shutil
import math
import sys

try:
    import ezdxf
    from ezdxf.enums import TextEntityAlignment
except ImportError:
    print("ezdxf is required. Please install it using pip.")
    sys.exit(1)

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
layouts_dir = os.path.join(base_dir, "datos_diseno", "layouts")
planos_cad_dir = os.path.join(base_dir, "06_planos", "fuentes")
planos_electricos_dir = os.path.join(base_dir, "06_planos", "entregables", "dxf")
diagramas_dir = os.path.join(base_dir, "06_planos", "diagramas")
planos_report_dir = os.path.join(base_dir, "06_planos", "entregables", "pdf")

os.makedirs(planos_electricos_dir, exist_ok=True)
os.makedirs(diagramas_dir, exist_ok=True)
os.makedirs(planos_report_dir, exist_ok=True)

# Helper to render PDF/SVG using Matplotlib
def render_dxf_to_pdf_and_svg(dxf_path):
    pdf_path = dxf_path.replace('.dxf', '.pdf')
    svg_path = dxf_path.replace('.dxf', '.svg')
    try:
        import matplotlib.pyplot as plt
        from ezdxf.addons.drawing import RenderContext, Frontend
        from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
        
        print(f"Renderizando PDF/SVG para: {dxf_path} ...")
        doc = ezdxf.readfile(dxf_path)
        msp = doc.modelspace()
        
        # Save PDF
        fig = plt.figure(figsize=(11.69, 8.27))  # A4 landscape
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        
        ctx = RenderContext(doc)
        out = MatplotlibBackend(ax)
        Frontend(ctx, out).draw_layout(msp, finalize=True)
        
        fig.savefig(pdf_path, dpi=300, bbox_inches='tight', pad_inches=0)
        # Save SVG
        fig.savefig(svg_path, format='svg', bbox_inches='tight', pad_inches=0)
        plt.close(fig)
        print(f"SUCCESS: Renderizado PDF y SVG completado para {dxf_path}")
    except Exception as e:
        print(f"Advertencia: No se pudo renderizar {dxf_path} a PDF/SVG: {e}")

# Helper to draw a standard architectural layout on modelspace from layout data
def draw_base_architecture(msp, data):
    wall_thickness = 0.15
    walls = set()
    
    # 1. Collect walls
    for room in data["rooms"]:
        rx, ry = room["x"], room["y"]
        rw, rh = room["width"], room["height"]
        
        seg_bottom = tuple(sorted([(rx, ry), (rx + rw, ry)]))
        seg_top = tuple(sorted([(rx, ry + rh), (rx + rw, ry + rh)]))
        seg_left = tuple(sorted([(rx, ry), (rx, ry + rh)]))
        seg_right = tuple(sorted([(rx + rw, ry), (rx + rw, ry + rh)]))
        
        walls.add(seg_bottom)
        walls.add(seg_top)
        walls.add(seg_left)
        walls.add(seg_right)
        
        # Room label
        x_center = rx + rw / 2
        y_center = ry + rh / 2
        
        if "escalera" in room["name"].lower():
            # Draw standard stair steps
            landing_depth = 1.2
            msp.add_line((x_center, ry), (x_center, ry + rh - landing_depth), dxfattribs={'layer': 'ESCALERAS', 'color': 8})
            msp.add_line((rx, ry + rh - landing_depth), (rx + rw, ry + rh - landing_depth), dxfattribs={'layer': 'ESCALERAS', 'color': 8})
            num_steps = 8
            tread_depth = (rh - landing_depth) / num_steps
            for i in range(1, num_steps):
                y_step = ry + i * tread_depth
                msp.add_line((rx, y_step), (x_center, y_step), dxfattribs={'layer': 'ESCALERAS', 'color': 8})
                msp.add_line((x_center, y_step), (rx + rw, y_step), dxfattribs={'layer': 'ESCALERAS', 'color': 8})
            text_y = ry + rh - (landing_depth / 2)
            dim_y = text_y - 0.25
        else:
            text_y = y_center
            dim_y = y_center - 0.25
            
        if room["name"] and not room["name"].startswith("_"):
            msp.add_text(room["name"].upper(), dxfattribs={'layer': 'TEXTOS', 'height': 0.18, 'color': 8}).set_placement((x_center, text_y), align=TextEntityAlignment.MIDDLE_CENTER)
            dim_text = f"{rw:.2f} x {rh:.2f} m"
            msp.add_text(dim_text, dxfattribs={'layer': 'TEXTOS', 'height': 0.12, 'color': 8}).set_placement((x_center, dim_y), align=TextEntityAlignment.MIDDLE_CENTER)

    # Ignored walls (removes lines where spaces merge)
    ignored_walls = set()
    if "ignored_walls" in data:
        for p in data["ignored_walls"]:
            p1, p2 = p
            seg = tuple(sorted([tuple(p1), tuple(p2)]))
            ignored_walls.add(seg)
            
    walls = walls - ignored_walls
    
    # Draw walls in light gray or white/black layer
    for start, end in walls:
        x1, y1 = start
        x2, y2 = end
        if abs(x1 - x2) < 1e-5:  # vertical
            msp.add_line((x1 - wall_thickness/2, y1), (x1 - wall_thickness/2, y2), dxfattribs={'layer': 'MUROS', 'color': 8})
            msp.add_line((x1 + wall_thickness/2, y1), (x1 + wall_thickness/2, y2), dxfattribs={'layer': 'MUROS', 'color': 8})
        elif abs(y1 - y2) < 1e-5:  # horizontal
            msp.add_line((x1, y1 - wall_thickness/2), (x2, y1 - wall_thickness/2), dxfattribs={'layer': 'MUROS', 'color': 8})
            msp.add_line((x1, y1 + wall_thickness/2), (x2, y1 + wall_thickness/2), dxfattribs={'layer': 'MUROS', 'color': 8})
        else:
            msp.add_line(start, end, dxfattribs={'layer': 'MUROS', 'color': 8})
            
    # 2. Draw doors (yellow / color 2)
    if "doors" in data:
        for door in data["doors"]:
            x, y = door["x"], door["y"]
            w = door["width"]
            ori = door["orientation"]
            swing = door["swing"]
            layer = "PUERTAS"
            
            if ori == "horizontal":
                if swing == "top-right":
                    msp.add_line((x, y), (x, y + w), dxfattribs={'layer': layer, 'color': 2})
                    msp.add_arc((x, y), w, 0, 90, dxfattribs={'layer': layer, 'color': 2})
                elif swing == "top-left":
                    msp.add_line((x + w, y), (x + w, y + w), dxfattribs={'layer': layer, 'color': 2})
                    msp.add_arc((x + w, y), w, 90, 180, dxfattribs={'layer': layer, 'color': 2})
                elif swing == "bottom-right":
                    msp.add_line((x, y), (x, y - w), dxfattribs={'layer': layer, 'color': 2})
                    msp.add_arc((x, y), w, 270, 360, dxfattribs={'layer': layer, 'color': 2})
                elif swing == "bottom-left":
                    msp.add_line((x + w, y), (x + w, y - w), dxfattribs={'layer': layer, 'color': 2})
                    msp.add_arc((x + w, y), w, 180, 270, dxfattribs={'layer': layer, 'color': 2})
            else:  # vertical
                if swing == "top-right":
                    msp.add_line((x, y), (x + w, y), dxfattribs={'layer': layer, 'color': 2})
                    msp.add_arc((x, y), w, 0, 90, dxfattribs={'layer': layer, 'color': 2})
                elif swing == "top-left":
                    msp.add_line((x, y), (x - w, y), dxfattribs={'layer': layer, 'color': 2})
                    msp.add_arc((x, y), w, 90, 180, dxfattribs={'layer': layer, 'color': 2})
                elif swing == "bottom-right":
                    msp.add_line((x, y + w), (x + w, y + w), dxfattribs={'layer': layer, 'color': 2})
                    msp.add_arc((x, y + w), w, 270, 360, dxfattribs={'layer': layer, 'color': 2})
                elif swing == "bottom-left":
                    msp.add_line((x, y + w), (x - w, y + w), dxfattribs={'layer': layer, 'color': 2})
                    msp.add_arc((x, y + w), w, 180, 270, dxfattribs={'layer': layer, 'color': 2})

    # 3. Draw windows (cyan / color 4)
    if "windows" in data:
        for win in data["windows"]:
            x, y = win["x"], win["y"]
            w = win["width"]
            ori = win["orientation"]
            layer = "VENTANAS"
            thick = 0.15
            if ori == "horizontal":
                msp.add_line((x, y - thick/2), (x + w, y - thick/2), dxfattribs={'layer': layer, 'color': 4})
                msp.add_line((x + w, y - thick/2), (x + w, y + thick/2), dxfattribs={'layer': layer, 'color': 4})
                msp.add_line((x + w, y + thick/2), (x, y + thick/2), dxfattribs={'layer': layer, 'color': 4})
                msp.add_line((x, y + thick/2), (x, y - thick/2), dxfattribs={'layer': layer, 'color': 4})
                msp.add_line((x, y), (x + w, y), dxfattribs={'layer': layer, 'color': 4})
            else:
                msp.add_line((x - thick/2, y), (x + thick/2, y), dxfattribs={'layer': layer, 'color': 4})
                msp.add_line((x + thick/2, y), (x + thick/2, y + w), dxfattribs={'layer': layer, 'color': 4})
                msp.add_line((x + thick/2, y + w), (x - thick/2, y + w), dxfattribs={'layer': layer, 'color': 4})
                msp.add_line((x - thick/2, y + w), (x - thick/2, y), dxfattribs={'layer': layer, 'color': 4})
                msp.add_line((x, y), (x, y + w), dxfattribs={'layer': layer, 'color': 4})

    # 4. Marco and Cajetín
    limit_w = data["dimensions"]["width"]
    limit_h = data["dimensions"]["height"]
    margin = data.get("dimensions", {}).get("margin", 1.5)
    
    mx1, my1 = -margin, -margin
    mx2, my2 = limit_w + margin, limit_h + margin
    
    # Outer frame
    msp.add_line((mx1, my1), (mx2, my1), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((mx2, my1), (mx2, my2), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((mx2, my2), (mx1, my2), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((mx1, my2), (mx1, my1), dxfattribs={'layer': 'MARCO', 'color': 7})
    
    # Inner decorative frame
    o = 0.08
    msp.add_line((mx1+o, my1+o), (mx2-o, my1+o), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((mx2-o, my1+o), (mx2-o, my2-o), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((mx2-o, my2-o), (mx1+o, my2-o), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((mx1+o, my2-o), (mx1+o, my1+o), dxfattribs={'layer': 'MARCO', 'color': 7})
    
    # Title Block
    c_w = 4.8
    c_h = 1.6
    cx1 = mx2 - o - c_w
    cy1 = my1 + o
    cx2 = mx2 - o
    cy2 = my1 + o + c_h
    
    msp.add_line((cx1, cy1), (cx1, cy2), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((cx1, cy2), (cx2, cy2), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((cx1, cy1 + 0.4), (cx2, cy1 + 0.4), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((cx1, cy1 + 0.8), (cx2, cy1 + 0.8), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((cx1, cy1 + 1.2), (cx2, cy1 + 1.2), dxfattribs={'layer': 'MARCO', 'color': 7})
    
    author = data.get("author", " Mamani Galindo Renzo Gabriel")
    project_name = data.get("project", "INSTALACIONES ELECTRICAS")
    date_str = data.get("date", "2026-06-03")
    
    msp.add_text("UNAP - ESCUELA INGENIERIA MECANICA ELECTRICA", dxfattribs={'layer': 'TEXTOS', 'height': 0.11, 'color': 7}).set_placement((cx1 + 0.1, cy1 + 1.35))
    msp.add_text(f"PROY: {project_name.upper()}", dxfattribs={'layer': 'TEXTOS', 'height': 0.11, 'color': 7}).set_placement((cx1 + 0.1, cy1 + 0.95))
    msp.add_text(f"ALUM: {author.upper()}", dxfattribs={'layer': 'TEXTOS', 'height': 0.11, 'color': 7}).set_placement((cx1 + 0.1, cy1 + 0.55))
    msp.add_text(f"FECHA: {date_str}  |  ESC: 1:50", dxfattribs={'layer': 'TEXTOS', 'height': 0.09, 'color': 7}).set_placement((cx1 + 0.1, cy1 + 0.15))

# Helper to draw a circle center symbol
def draw_electric_center(msp, x, y, symbol_text="X", layer="ELEC", color=3, radius=0.15):
    # Draw circle
    msp.add_circle((x, y), radius, dxfattribs={'layer': layer, 'color': color})
    # Draw text inside
    msp.add_text(symbol_text, dxfattribs={'layer': layer, 'height': radius * 1.2, 'color': color}).set_placement((x, y), align=TextEntityAlignment.MIDDLE_CENTER)

def draw_switch(msp, x, y, label="S", layer="ELEC", color=3, radius=0.08):
    msp.add_circle((x, y), radius, dxfattribs={'layer': layer, 'color': color})
    # Lollipop line
    msp.add_line((x, y + radius), (x, y + radius + 0.12), dxfattribs={'layer': layer, 'color': color})
    msp.add_line((x, y + radius + 0.12), (x + 0.10, y + radius + 0.12), dxfattribs={'layer': layer, 'color': color})
    msp.add_text(label, dxfattribs={'layer': layer, 'height': 0.10, 'color': color}).set_placement((x + 0.15, y + radius + 0.10))

def draw_conduit(msp, p1, p2, layer="ELEC_CONDUIT", color=3):
    # Curve conduit represented by a dashed line
    msp.add_line(p1, p2, dxfattribs={'layer': layer, 'color': color, 'linetype': 'DASHED'})

# Unified Legend Drawer
def draw_unified_legend(msp, leg_x, leg_y):
    # Outer box for Legend
    msp.add_lwpolyline([(leg_x, leg_y - 0.7), (leg_x + 2.5, leg_y - 0.7), (leg_x + 2.5, leg_y + 1.8), (leg_x, leg_y + 1.8)], close=True, dxfattribs={'layer': 'TEXTOS', 'color': 8})
    
    # Legend header
    msp.add_text("LEYENDA ELÉCTRICA", dxfattribs={'layer': 'TEXTOS', 'height': 0.11, 'color': 7}).set_placement((leg_x + 0.1, leg_y + 1.6))
    
    # Light symbol
    draw_electric_center(msp, leg_x + 0.2, leg_y + 1.25, symbol_text="L", layer="TEXTOS", color=3, radius=0.09)
    msp.add_text("Pto. Luz LED (12W)", dxfattribs={'layer': 'TEXTOS', 'height': 0.08, 'color': 7}).set_placement((leg_x + 0.5, leg_y + 1.2))
    
    # Switch
    draw_switch(msp, leg_x + 0.2, leg_y + 0.95, label="S", layer="TEXTOS", color=3, radius=0.05)
    msp.add_text("Interruptor Simple", dxfattribs={'layer': 'TEXTOS', 'height': 0.08, 'color': 7}).set_placement((leg_x + 0.5, leg_y + 0.90))
    
    # Conmutación S3
    draw_switch(msp, leg_x + 0.2, leg_y + 0.65, label="S3", layer="TEXTOS", color=3, radius=0.05)
    msp.add_text("Interruptor Conmutado", dxfattribs={'layer': 'TEXTOS', 'height': 0.08, 'color': 7}).set_placement((leg_x + 0.5, leg_y + 0.60))
    
    # TC
    draw_electric_center(msp, leg_x + 0.2, leg_y + 0.35, symbol_text="TC", layer="TEXTOS", color=6, radius=0.09)
    msp.add_text("T/C Doble Gral (H=0.3m)", dxfattribs={'layer': 'TEXTOS', 'height': 0.08, 'color': 7}).set_placement((leg_x + 0.5, leg_y + 0.30))
    
    # TD / TG box
    msp.add_lwpolyline([(leg_x + 0.1, leg_y + 0.0), (leg_x + 0.3, leg_y + 0.0), (leg_x + 0.3, leg_y + 0.2), (leg_x + 0.1, leg_y + 0.2)], close=True, dxfattribs={'layer': 'TEXTOS', 'color': 1})
    msp.add_text("Tablero General/Dist.", dxfattribs={'layer': 'TEXTOS', 'height': 0.08, 'color': 7}).set_placement((leg_x + 0.5, leg_y + 0.05))
    
    # Conduit Alumbrado (Dashed green)
    msp.add_line((leg_x + 0.1, leg_y - 0.2), (leg_x + 0.3, leg_y - 0.2), dxfattribs={'layer': 'TEXTOS', 'color': 3, 'linetype': 'DASHED'})
    msp.add_text("Canaliz. Techo (Alum)", dxfattribs={'layer': 'TEXTOS', 'height': 0.08, 'color': 7}).set_placement((leg_x + 0.5, leg_y - 0.25))
    
    # Conduit Tomacorriente (Dashed magenta)
    msp.add_line((leg_x + 0.1, leg_y - 0.5), (leg_x + 0.3, leg_y - 0.5), dxfattribs={'layer': 'TEXTOS', 'color': 6, 'linetype': 'DASHED'})
    msp.add_text("Canaliz. Piso (T/C)", dxfattribs={'layer': 'TEXTOS', 'height': 0.08, 'color': 7}).set_placement((leg_x + 0.5, leg_y - 0.55))


# ====================================================
# FLOOR 1: ALUMBRADO Y TOMACORRIENTES (IE-02)
# ====================================================
def build_floor1_electrical():
    layout_path = os.path.join(layouts_dir, "primer_piso_v3.json")
    with open(layout_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    data["project"] = "Plano Elec. 1er Piso (IE-02)"
    doc = ezdxf.new("R2010", setup=True)
    msp = doc.modelspace()
    
    # Layers
    doc.layers.new("MUROS", dxfattribs={'color': 8})
    doc.layers.new("PUERTAS", dxfattribs={'color': 8})
    doc.layers.new("VENTANAS", dxfattribs={'color': 8})
    doc.layers.new("TEXTOS", dxfattribs={'color': 8})
    doc.layers.new("MARCO", dxfattribs={'color': 7})
    doc.layers.new("ESCALERAS", dxfattribs={'color': 8})
    doc.layers.new("COTAS", dxfattribs={'color': 8})
    doc.layers.new("ELEC_ALUMBRADO", dxfattribs={'color': 3}) # Green
    doc.layers.new("ELEC_TOMACORRIENTES", dxfattribs={'color': 6}) # Magenta
    doc.layers.new("ELEC_CONDUIT", dxfattribs={'color': 3})
    
    # Base layout
    draw_base_architecture(msp, data)
    
    # Add Tablero General TG-01 on the right wall of pasadizo
    tg_x, tg_y = 4.3, 1.2
    msp.add_lwpolyline([(tg_x - 0.1, tg_y - 0.2), (tg_x + 0.1, tg_y - 0.2), (tg_x + 0.1, tg_y + 0.2), (tg_x - 0.1, tg_y + 0.2)], close=True, dxfattribs={'layer': 'ELEC_ALUMBRADO', 'color': 1}) # Red TG-01
    msp.add_text("TG-01", dxfattribs={'layer': 'ELEC_ALUMBRADO', 'height': 0.11, 'color': 1}).set_placement((tg_x - 0.4, tg_y - 0.05))
    
    # 5 Lights (Centro de Luz)
    lights = {
        "Tienda": (1.5, 1.75),
        "Cocina": (1.5, 5.25),
        "Pasadizo_1": (3.75, 2.0),
        "Pasadizo_2": (3.75, 5.0),
        "Escalera": (1.25, 7.75)
    }
    
    for l_name, (lx, ly) in lights.items():
        draw_electric_center(msp, lx, ly, symbol_text="L", layer="ELEC_ALUMBRADO", color=3, radius=0.14)
        
    # Switches
    switches = {
        "S_Tienda": ((2.8, 2.3), "S"),
        "S_Cocina": ((2.8, 5.8), "S"),
        "S3_Pasa1": ((3.2, 0.5), "S3"),
        "S3_Pasa2": ((3.2, 6.5), "S3"),
        "S3_Escalera": ((2.2, 7.2), "S3")
    }
    
    for sw_name, (pos, lbl) in switches.items():
        draw_switch(msp, pos[0], pos[1], label=lbl, layer="ELEC_ALUMBRADO", color=3)
        
    # Conduits for lighting
    draw_conduit(msp, (tg_x, tg_y), lights["Pasadizo_1"], color=3)
    draw_conduit(msp, lights["Pasadizo_1"], lights["Tienda"], color=3)
    draw_conduit(msp, lights["Tienda"], (2.8, 2.3), color=3)
    draw_conduit(msp, lights["Pasadizo_1"], lights["Pasadizo_2"], color=3)
    draw_conduit(msp, lights["Pasadizo_2"], lights["Cocina"], color=3)
    draw_conduit(msp, lights["Cocina"], (2.8, 5.8), color=3)
    draw_conduit(msp, lights["Pasadizo_2"], lights["Escalera"], color=3)
    draw_conduit(msp, lights["Escalera"], (2.2, 7.2), color=3)
    draw_conduit(msp, lights["Pasadizo_1"], (3.2, 0.5), color=3)
    draw_conduit(msp, lights["Pasadizo_2"], (3.2, 6.5), color=3)
    
    # 6 Outlets
    tcs = {
        "Tienda_TC1": (0.5, 1.0),
        "Tienda_TC2": (2.5, 1.0),
        "Cocina_TC1": (0.5, 4.5),
        "Cocina_TC2": (0.5, 6.0),
        "Cocina_TC3": (2.5, 4.5),
        "Cocina_TC4": (2.5, 6.0)
    }
    
    for tc_name, (tx, ty) in tcs.items():
        draw_electric_center(msp, tx, ty, symbol_text="TC", layer="ELEC_TOMACORRIENTES", color=6, radius=0.13)
        
    # Conduits for general outlets (C2) - Ring layout loop
    draw_conduit(msp, (tg_x, tg_y), tcs["Tienda_TC2"], color=6)
    draw_conduit(msp, tcs["Tienda_TC2"], tcs["Tienda_TC1"], color=6)
    draw_conduit(msp, tcs["Tienda_TC1"], (tg_x, tg_y), color=6)
    
    # Conduits for kitchen outlets (C3) - Ring layout loop
    draw_conduit(msp, (tg_x, tg_y), tcs["Cocina_TC1"], color=6)
    draw_conduit(msp, tcs["Cocina_TC1"], tcs["Cocina_TC2"], color=6)
    draw_conduit(msp, tcs["Cocina_TC2"], tcs["Cocina_TC4"], color=6)
    draw_conduit(msp, tcs["Cocina_TC4"], tcs["Cocina_TC3"], color=6)
    draw_conduit(msp, tcs["Cocina_TC3"], (tg_x, tg_y), color=6)
    
    # Legend
    draw_unified_legend(msp, -1.2, 0.5)

    out_dxf = os.path.join(planos_electricos_dir, "plano_electrico_primer_piso.dxf")
    doc.saveas(out_dxf)
    render_dxf_to_pdf_and_svg(out_dxf)
    
    # Copy to report directory
    shutil.copy2(out_dxf.replace('.dxf', '.pdf'), os.path.join(planos_report_dir, "IE-02-primer-piso.pdf"))
    print("Primer Piso Electrical compiled.")

# ====================================================
# FLOOR 2: ALUMBRADO Y TOMACORRIENTES (IE-03)
# ====================================================
def build_floor2_electrical():
    layout_path = os.path.join(layouts_dir, "segundo_piso_v3.json")
    with open(layout_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    data["project"] = "Plano Elec. 2do Piso (IE-03)"
    doc = ezdxf.new("R2010", setup=True)
    msp = doc.modelspace()
    
    # Layers
    doc.layers.new("MUROS", dxfattribs={'color': 8})
    doc.layers.new("PUERTAS", dxfattribs={'color': 8})
    doc.layers.new("VENTANAS", dxfattribs={'color': 8})
    doc.layers.new("TEXTOS", dxfattribs={'color': 8})
    doc.layers.new("MARCO", dxfattribs={'color': 7})
    doc.layers.new("ESCALERAS", dxfattribs={'color': 8})
    doc.layers.new("COTAS", dxfattribs={'color': 8})
    doc.layers.new("ELEC_ALUMBRADO", dxfattribs={'color': 3})
    doc.layers.new("ELEC_TOMACORRIENTES", dxfattribs={'color': 6})
    doc.layers.new("ELEC_CONDUIT", dxfattribs={'color': 6})
    
    draw_base_architecture(msp, data)
    
    # Add Tablero de Distribución TD-01 on the right wall of Hall
    td_x, td_y = 4.3, 4.5
    msp.add_lwpolyline([(td_x - 0.1, td_y - 0.2), (td_x + 0.1, td_y - 0.2), (td_x + 0.1, td_y + 0.2), (td_x - 0.1, td_y + 0.2)], close=True, dxfattribs={'layer': 'ELEC_TOMACORRIENTES', 'color': 1}) # Red TD-01
    msp.add_text("TD-01", dxfattribs={'layer': 'ELEC_TOMACORRIENTES', 'height': 0.11, 'color': 1}).set_placement((td_x - 0.4, td_y - 0.05))
    
    # 6 Lights (Centro de Luz)
    lights = {
        "Dorm_Prin_1": (1.5, 2.0),
        "Dorm_Prin_2": (3.0, 2.0),
        "Dorm_3": (1.5, 5.75),
        "Sala": (3.75, 5.75),
        "Bano": (3.75, 8.25),
        "Escalera": (1.25, 8.25)
    }
    for l_name, (lx, ly) in lights.items():
        draw_electric_center(msp, lx, ly, symbol_text="L", layer="ELEC_ALUMBRADO", color=3, radius=0.14)
        
    # Switches
    switches = {
        "S_DormPrin": ((0.8, 3.8), "S"),
        "S_Dorm3": ((0.8, 4.2), "S"),
        "S_Sala": ((3.2, 4.2), "S"),
        "S_Bano": ((3.2, 7.2), "S"),
        "S3_Escalera": ((2.2, 7.7), "S3")
    }
    for sw_name, (pos, lbl) in switches.items():
        draw_switch(msp, pos[0], pos[1], label=lbl, layer="ELEC_ALUMBRADO", color=3)
        
    # Conduits for lighting
    draw_conduit(msp, (td_x, td_y), lights["Sala"], color=3)
    draw_conduit(msp, lights["Sala"], lights["Bano"], color=3)
    draw_conduit(msp, lights["Sala"], lights["Dorm_3"], color=3)
    draw_conduit(msp, lights["Dorm_3"], lights["Dorm_Prin_2"], color=3)
    draw_conduit(msp, lights["Dorm_Prin_2"], lights["Dorm_Prin_1"], color=3)
    draw_conduit(msp, lights["Bano"], lights["Escalera"], color=3)
    draw_conduit(msp, lights["Escalera"], (2.2, 7.7), color=3)
    draw_conduit(msp, lights["Dorm_Prin_1"], (0.8, 3.8), color=3)
    draw_conduit(msp, lights["Dorm_3"], (0.8, 4.2), color=3)
    draw_conduit(msp, lights["Sala"], (3.2, 4.2), color=3)
    draw_conduit(msp, lights["Bano"], (3.2, 7.2), color=3)

    # 11 Outlets (Dorm principal 4, Dorm 3 4, Sala 3)
    tcs = {
        "Dorm_Prin_1": (0.5, 1.0),
        "Dorm_Prin_2": (4.0, 1.0),
        "Dorm_Prin_3": (1.5, 0.5),
        "Dorm_Prin_4": (3.0, 3.5),
        "Dorm_3_1": (0.5, 4.5),
        "Dorm_3_2": (0.5, 6.5),
        "Dorm_3_3": (2.5, 4.5),
        "Dorm_3_4": (2.5, 6.5),
        "Sala_1": (4.0, 4.5),
        "Sala_2": (4.0, 6.5),
        "Sala_3": (3.2, 5.5)
    }
    
    for tc_name, (tx, ty) in tcs.items():
        draw_electric_center(msp, tx, ty, symbol_text="TC", layer="ELEC_TOMACORRIENTES", color=6, radius=0.13)
        
    # Conduits for tomacorrientes (C5) - Ring layout loop
    draw_conduit(msp, (td_x, td_y), tcs["Sala_3"], color=6)
    draw_conduit(msp, tcs["Sala_3"], tcs["Sala_1"], color=6)
    draw_conduit(msp, tcs["Sala_1"], tcs["Sala_2"], color=6)
    draw_conduit(msp, tcs["Sala_2"], tcs["Dorm_3_4"], color=6)
    draw_conduit(msp, tcs["Dorm_3_4"], tcs["Dorm_3_2"], color=6)
    draw_conduit(msp, tcs["Dorm_3_2"], tcs["Dorm_3_1"], color=6)
    draw_conduit(msp, tcs["Dorm_3_1"], tcs["Dorm_3_3"], color=6)
    draw_conduit(msp, tcs["Dorm_3_3"], tcs["Dorm_Prin_4"], color=6)
    draw_conduit(msp, tcs["Dorm_Prin_4"], tcs["Dorm_Prin_2"], color=6)
    draw_conduit(msp, tcs["Dorm_Prin_2"], tcs["Dorm_Prin_3"], color=6)
    draw_conduit(msp, tcs["Dorm_Prin_3"], tcs["Dorm_Prin_1"], color=6)
    draw_conduit(msp, tcs["Dorm_Prin_1"], (td_x, td_y), color=6)
    
    # Legend
    draw_unified_legend(msp, -1.2, 0.5)

    out_dxf = os.path.join(planos_electricos_dir, "plano_electrico_segundo_piso.dxf")
    doc.saveas(out_dxf)
    render_dxf_to_pdf_and_svg(out_dxf)
    
    # Copy to report directory
    shutil.copy2(out_dxf.replace('.dxf', '.pdf'), os.path.join(planos_report_dir, "IE-03-segundo-piso.pdf"))
    print("Segundo Piso Electrical compiled.")

# ====================================================
# FLOOR 3: ALUMBRADO Y TOMACORRIENTES (IE-04)
# ====================================================
def build_floor3_electrical():
    layout_path = os.path.join(layouts_dir, "tercer_piso_v3.json")
    with open(layout_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    data["project"] = "Plano Elec. 3er Piso (IE-04)"
    doc = ezdxf.new("R2010", setup=True)
    msp = doc.modelspace()
    
    # Layers
    doc.layers.new("MUROS", dxfattribs={'color': 8})
    doc.layers.new("PUERTAS", dxfattribs={'color': 8})
    doc.layers.new("VENTANAS", dxfattribs={'color': 8})
    doc.layers.new("TEXTOS", dxfattribs={'color': 8})
    doc.layers.new("MARCO", dxfattribs={'color': 7})
    doc.layers.new("ESCALERAS", dxfattribs={'color': 8})
    doc.layers.new("COTAS", dxfattribs={'color': 8})
    doc.layers.new("ELEC_ALUMBRADO", dxfattribs={'color': 3})
    doc.layers.new("ELEC_TOMACORRIENTES", dxfattribs={'color': 6})
    doc.layers.new("ELEC_CONDUIT", dxfattribs={'color': 5})
    
    draw_base_architecture(msp, data)
    
    # Add Tablero de Distribución TD-02 on the left wall of Pasadizo
    td_x, td_y = 0.2, 8.0
    msp.add_lwpolyline([(td_x - 0.1, td_y - 0.2), (td_x + 0.1, td_y - 0.2), (td_x + 0.1, td_y + 0.2), (td_x - 0.1, td_y + 0.2)], close=True, dxfattribs={'layer': 'ELEC_ALUMBRADO', 'color': 1}) # Red TD-02
    msp.add_text("TD-02", dxfattribs={'layer': 'ELEC_ALUMBRADO', 'height': 0.11, 'color': 1}).set_placement((td_x + 0.2, td_y - 0.05))
    
    # 7 Lights (Centro de Luz)
    lights = {
        "Dorm_4_1": (1.12, 2.5),
        "Dorm_4_2": (1.12, 5.5),
        "Dorm_5_1": (3.37, 2.5),
        "Dorm_5_2": (3.37, 5.5),
        "Pasadizo": (1.0, 8.25),
        "Bano": (3.37, 8.25),
        "Escalera": (1.0, 7.75)
    }
    
    for l_name, (lx, ly) in lights.items():
        draw_electric_center(msp, lx, ly, symbol_text="L", layer="ELEC_ALUMBRADO", color=3, radius=0.14)
        
    # Switches
    switches = {
        "S_Dorm4": ((0.8, 7.2), "S"),
        "S_Dorm5": ((2.5, 7.2), "S"),
        "S_Bano": ((3.0, 7.2), "S"),
        "S_Pasa": ((1.5, 8.2), "S"),
        "S3_Esc": ((0.8, 7.7), "S3")
    }
    for sw_name, (pos, lbl) in switches.items():
        draw_switch(msp, pos[0], pos[1], label=lbl, layer="ELEC_ALUMBRADO", color=3)
        
    # Conduits for lighting
    draw_conduit(msp, (td_x, td_y), lights["Pasadizo"], color=3)
    draw_conduit(msp, lights["Pasadizo"], lights["Bano"], color=3)
    draw_conduit(msp, lights["Pasadizo"], lights["Escalera"], color=3)
    draw_conduit(msp, lights["Pasadizo"], lights["Dorm_4_2"], color=3)
    draw_conduit(msp, lights["Dorm_4_2"], lights["Dorm_4_1"], color=3)
    draw_conduit(msp, lights["Bano"], lights["Dorm_5_2"], color=3)
    draw_conduit(msp, lights["Dorm_5_2"], lights["Dorm_5_1"], color=3)
    
    # 10 Outlets (Dorm 4 has 5, Dorm 5 has 5)
    tcs = {
        "Dorm_4_1": (0.5, 1.5),
        "Dorm_4_2": (0.5, 3.5),
        "Dorm_4_3": (0.5, 5.5),
        "Dorm_4_4": (1.8, 2.0),
        "Dorm_4_5": (1.8, 5.0),
        "Dorm_5_1": (4.0, 1.5),
        "Dorm_5_2": (4.0, 3.5),
        "Dorm_5_3": (4.0, 5.5),
        "Dorm_5_4": (2.7, 2.0),
        "Dorm_5_5": (2.7, 5.0)
    }
    
    for name, (tx, ty) in tcs.items():
        draw_electric_center(msp, tx, ty, symbol_text="TC", layer="ELEC_TOMACORRIENTES", color=6, radius=0.13)
            
    # Conduits for outlets (C7) - Ring layout loop
    draw_conduit(msp, (td_x, td_y), tcs["Dorm_4_3"], color=6)
    draw_conduit(msp, tcs["Dorm_4_3"], tcs["Dorm_4_2"], color=6)
    draw_conduit(msp, tcs["Dorm_4_2"], tcs["Dorm_4_1"], color=6)
    draw_conduit(msp, tcs["Dorm_4_1"], tcs["Dorm_4_4"], color=6)
    draw_conduit(msp, tcs["Dorm_4_4"], tcs["Dorm_4_5"], color=6)
    draw_conduit(msp, tcs["Dorm_4_5"], tcs["Dorm_5_5"], color=6)
    draw_conduit(msp, tcs["Dorm_5_5"], tcs["Dorm_5_4"], color=6)
    draw_conduit(msp, tcs["Dorm_5_4"], tcs["Dorm_5_1"], color=6)
    draw_conduit(msp, tcs["Dorm_5_1"], tcs["Dorm_5_2"], color=6)
    draw_conduit(msp, tcs["Dorm_5_2"], tcs["Dorm_5_3"], color=6)
    draw_conduit(msp, tcs["Dorm_5_3"], (td_x, td_y), color=6)
    
    # Legend
    draw_unified_legend(msp, -1.2, 0.5)

    out_dxf = os.path.join(planos_electricos_dir, "plano_electrico_tercer_piso.dxf")
    doc.saveas(out_dxf)
    render_dxf_to_pdf_and_svg(out_dxf)
    
    # Copy to report directory
    shutil.copy2(out_dxf.replace('.dxf', '.pdf'), os.path.join(planos_report_dir, "IE-04-tercer-piso.pdf"))
    print("Tercer Piso Electrical compiled.")

# ====================================================
# DIAGRAMA UNIFILAR (IE-05-unifilar-cuadro-cargas)
# ====================================================
def build_diagrama_unifilar():
    doc = ezdxf.new("R2010", setup=True)
    msp = doc.modelspace()
    
    # Set up some layers
    doc.layers.new("DIAGRAMA", dxfattribs={'color': 7})
    doc.layers.new("TEXTOS", dxfattribs={'color': 7})
    doc.layers.new("TABLAS", dxfattribs={'color': 8})
    doc.layers.new("MARCO", dxfattribs={'color': 7})
    
    # Frame and title block
    mx1, my1 = -1.5, -1.5
    mx2, my2 = 14.5, 9.5
    
    msp.add_line((mx1, my1), (mx2, my1), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((mx2, my1), (mx2, my2), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((mx2, my2), (mx1, my2), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((mx1, my2), (mx1, my1), dxfattribs={'layer': 'MARCO', 'color': 7})
    
    o = 0.08
    msp.add_line((mx1+o, my1+o), (mx2-o, my1+o), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((mx2-o, my1+o), (mx2-o, my2-o), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((mx2-o, my2-o), (mx1+o, my2-o), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((mx1+o, my2-o), (mx1+o, my1+o), dxfattribs={'layer': 'MARCO', 'color': 7})
    
    c_w, c_h = 4.8, 1.6
    cx1, cy1 = mx2 - o - c_w, my1 + o
    cx2, cy2 = mx2 - o, my1 + o + c_h
    msp.add_line((cx1, cy1), (cx1, cy2), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((cx1, cy2), (cx2, cy2), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((cx1, cy1 + 0.4), (cx2, cy1 + 0.4), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((cx1, cy1 + 0.8), (cx2, cy1 + 0.8), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((cx1, cy1 + 1.2), (cx2, cy1 + 1.2), dxfattribs={'layer': 'MARCO', 'color': 7})
    
    msp.add_text("UNAP - ESCUELA INGENIERIA MECANICA ELECTRICA", dxfattribs={'layer': 'TEXTOS', 'height': 0.11, 'color': 7}).set_placement((cx1 + 0.1, cy1 + 1.35))
    msp.add_text("PROY: DIAGRAMA UNIFILAR Y CARGAS (IE-05)", dxfattribs={'layer': 'TEXTOS', 'height': 0.11, 'color': 7}).set_placement((cx1 + 0.1, cy1 + 0.95))
    msp.add_text("ALUM: MAMANI GALINDO RENZO GABRIEL", dxfattribs={'layer': 'TEXTOS', 'height': 0.11, 'color': 7}).set_placement((cx1 + 0.1, cy1 + 0.55))
    msp.add_text("FECHA: 2026-06-03  |  ESC: S/E (MTS)", dxfattribs={'layer': 'TEXTOS', 'height': 0.09, 'color': 7}).set_placement((cx1 + 0.1, cy1 + 0.15))
    
    # 1. Title
    msp.add_text("DIAGRAMA UNIFILAR GENERAL - TG-01", dxfattribs={'layer': 'TEXTOS', 'height': 0.28, 'color': 7}).set_placement((0.0, 8.5))
    
    # 2. Draw single line tree
    # Draw incoming line
    msp.add_line((1.0, 7.5), (1.0, 7.0), dxfattribs={'layer': 'DIAGRAMA', 'color': 7})
    msp.add_text("Suministro Monofásico 220V, 60Hz (Desde Red)", dxfattribs={'layer': 'TEXTOS', 'height': 0.12, 'color': 7}).set_placement((1.2, 7.3))
    
    # KWH Meter
    msp.add_circle((1.0, 6.7), 0.3, dxfattribs={'layer': 'DIAGRAMA', 'color': 7})
    msp.add_text("kWh", dxfattribs={'layer': 'TEXTOS', 'height': 0.11, 'color': 7}).set_placement((1.0, 6.7), align=TextEntityAlignment.MIDDLE_CENTER)
    
    # Connect meter to main breaker
    msp.add_line((1.0, 6.4), (1.0, 5.8), dxfattribs={'layer': 'DIAGRAMA', 'color': 7})
    
    # Main Breaker Symbol (box/termomagnetic)
    msp.add_lwpolyline([(0.85, 5.4), (1.15, 5.4), (1.15, 5.8), (0.85, 5.8)], close=True, dxfattribs={'layer': 'DIAGRAMA', 'color': 7})
    msp.add_text("ITM General", dxfattribs={'layer': 'TEXTOS', 'height': 0.10, 'color': 7}).set_placement((1.3, 5.65))
    msp.add_text("2P, 40A, 10kA", dxfattribs={'layer': 'TEXTOS', 'height': 0.10, 'color': 7}).set_placement((1.3, 5.5))
    
    # Connect Main Breaker to Differential Breaker
    msp.add_line((1.0, 5.4), (1.0, 4.8), dxfattribs={'layer': 'DIAGRAMA', 'color': 7})
    
    # Differential Breaker Symbol (box with ID label)
    msp.add_lwpolyline([(0.85, 4.4), (1.15, 4.4), (1.15, 4.8), (0.85, 4.8)], close=True, dxfattribs={'layer': 'DIAGRAMA', 'color': 7})
    msp.add_text("ID General", dxfattribs={'layer': 'TEXTOS', 'height': 0.10, 'color': 7}).set_placement((1.3, 4.65))
    msp.add_text("2P, 40A, 30mA", dxfattribs={'layer': 'TEXTOS', 'height': 0.10, 'color': 7}).set_placement((1.3, 4.50))
    
    # Connect to TG Busbar (horizontal thick line)
    msp.add_line((1.0, 4.4), (1.0, 3.8), dxfattribs={'layer': 'DIAGRAMA', 'color': 7})
    msp.add_line((0.5, 3.8), (14.0, 3.8), dxfattribs={'layer': 'DIAGRAMA', 'color': 7, 'lineweight': 50})
    msp.add_text("BARRA DE COBRE TABLERO GENERAL TG-01", dxfattribs={'layer': 'TEXTOS', 'height': 0.12, 'color': 7}).set_placement((0.5, 4.0))
    
    # Branch feeders: C1 to C7
    ctos = [
        {"x": 1.5, "lbl": "C1", "name": "Alum. 1er Piso", "itm": "2P, 10A", "cond": "3x1.5mm2", "desc": "Luz LED (500 W)"},
        {"x": 3.4, "lbl": "C2", "name": "T/C 1er Piso", "itm": "2P, 16A", "cond": "3x2.5mm2", "desc": "Tomacorrientes (1000 W)"},
        {"x": 5.3, "lbl": "C3", "name": "Cocin. 1er Piso", "itm": "2P, 20A", "cond": "3x2.5mm2", "desc": "Cocina (1500 W)"},
        {"x": 7.2, "lbl": "C4", "name": "Alum. 2do Piso", "itm": "2P, 10A", "cond": "3x1.5mm2", "desc": "Luz LED (500 W)"},
        {"x": 9.1, "lbl": "C5", "name": "T/C 2do Piso", "itm": "2P, 16A", "cond": "3x2.5mm2", "desc": "Tomacorrientes (1500 W)"},
        {"x": 11.0, "lbl": "C6", "name": "Alum. 3er Piso", "itm": "2P, 10A", "cond": "3x1.5mm2", "desc": "Luz LED (500 W)"},
        {"x": 12.9, "lbl": "C7", "name": "T/C 3er Piso", "itm": "2P, 16A", "cond": "3x2.5mm2", "desc": "Tomacorrientes (1500 W)"}
    ]
    
    for c in ctos:
        cx = c["x"]
        # Vertical branch line from busbar
        msp.add_line((cx, 3.8), (cx, 3.2), dxfattribs={'layer': 'DIAGRAMA', 'color': 7})
        
        # Individual branch breaker
        msp.add_lwpolyline([(cx - 0.15, 2.8), (cx + 0.15, 2.8), (cx + 0.15, 3.2), (cx - 0.15, 3.2)], close=True, dxfattribs={'layer': 'DIAGRAMA', 'color': 7})
        msp.add_text(c["itm"], dxfattribs={'layer': 'TEXTOS', 'height': 0.09, 'color': 7}).set_placement((cx + 0.25, 3.0), align=TextEntityAlignment.LEFT)
        
        # Connected to circuit details
        msp.add_line((cx, 2.8), (cx, 2.0), dxfattribs={'layer': 'DIAGRAMA', 'color': 7})
        
        # Text details below
        msp.add_text(f"{c['lbl']}: {c['name'].upper()}", dxfattribs={'layer': 'TEXTOS', 'height': 0.10, 'color': 7}).set_placement((cx, 1.8), align=TextEntityAlignment.MIDDLE_CENTER)
        msp.add_text(f"Cond: {c['cond']}", dxfattribs={'layer': 'TEXTOS', 'height': 0.08, 'color': 7}).set_placement((cx, 1.6), align=TextEntityAlignment.MIDDLE_CENTER)
        msp.add_text(c["desc"], dxfattribs={'layer': 'TEXTOS', 'height': 0.08, 'color': 7}).set_placement((cx, 1.4), align=TextEntityAlignment.MIDDLE_CENTER)

    # 3. Load Schedule Table (Cuadro de Cargas) at the bottom
    ty1, ty2 = -1.5, 0.8
    tx1, tx2 = 0.0, 11.5
    
    # Outer box
    msp.add_lwpolyline([(tx1, ty1), (tx2, ty1), (tx2, ty2), (tx1, ty2)], close=True, dxfattribs={'layer': 'TABLAS', 'color': 8})
    
    # Title of table
    msp.add_text("CUADRO DE CARGAS DE INSTALACIÓN ELÉCTRICA (C1 - C7)", dxfattribs={'layer': 'TEXTOS', 'height': 0.13, 'color': 7}).set_placement((tx1 + 0.2, ty2 + 0.1))
    
    # Headers
    cols = [
        {"w": 0.8, "name": "Cto"},
        {"w": 2.5, "name": "Descripción de Carga"},
        {"w": 1.4, "name": "Pot. Inst. (W)"},
        {"w": 1.4, "name": "F. Demanda"},
        {"w": 1.4, "name": "Máx. Dem. (W)"},
        {"w": 1.2, "name": "Int. ITM"},
        {"w": 2.8, "name": "Conductor Alimentador"}
    ]
    
    # Draw horizontal header line
    msp.add_line((tx1, ty2 - 0.35), (tx2, ty2 - 0.35), dxfattribs={'layer': 'TABLAS', 'color': 8})
    
    x_curr = tx1
    for c in cols:
        msp.add_text(c["name"], dxfattribs={'layer': 'TEXTOS', 'height': 0.09, 'color': 7}).set_placement((x_curr + c["w"]/2, ty2 - 0.22), align=TextEntityAlignment.MIDDLE_CENTER)
        x_curr += c["w"]
        if x_curr < tx2 - 0.01:
            msp.add_line((x_curr, ty1), (x_curr, ty2), dxfattribs={'layer': 'TABLAS', 'color': 8})
            
    # Table rows
    rows_data = [
        ["C1", "Alumbrado 1er Piso (LED)", "500", "1.00", "500", "2P-10A", "3 x 1.5 mm2 Cu (PVC 3/4\")"],
        ["C2", "Tomacorrientes 1er Piso", "1,000", "1.00", "1,000", "2P-16A", "3 x 2.5 mm2 Cu (PVC 3/4\")"],
        ["C3", "Tomacorrientes Cocina", "1,500", "1.00", "1,500", "2P-20A", "3 x 2.5 mm2 Cu (PVC 3/4\")"],
        ["C4", "Alumbrado 2do Piso (LED)", "500", "1.00", "500", "2P-10A", "3 x 1.5 mm2 Cu (PVC 3/4\")"],
        ["C5", "Tomacorrientes 2do Piso", "1,500", "0.70", "1,050", "2P-16A", "3 x 2.5 mm2 Cu (PVC 3/4\")"],
        ["C6", "Alumbrado 3er Piso (LED)", "500", "1.00", "500", "2P-10A", "3 x 1.5 mm2 Cu (PVC 3/4\")"],
        ["C7", "Tomacorrientes 3er Piso", "1,500", "0.70", "1,050", "2P-16A", "3 x 2.5 mm2 Cu (PVC 3/4\")"],
        ["Total", "MÁXIMA DEMANDA ESTIMADA", "7,000", "-", "6,100 W", "Idem: 30.81 A", "Llave Gral: 2P-40A"]
    ]
    
    y_curr = ty2 - 0.35
    row_height = 0.22
    for r in rows_data:
        y_curr -= row_height
        msp.add_line((tx1, y_curr), (tx2, y_curr), dxfattribs={'layer': 'TABLAS', 'color': 8})
        
        # Put values
        x_cell = tx1
        for idx, val in enumerate(r):
            col_width = cols[idx]["w"]
            msp.add_text(val, dxfattribs={'layer': 'TEXTOS', 'height': 0.08, 'color': 7}).set_placement((x_cell + col_width/2, y_curr + 0.07), align=TextEntityAlignment.MIDDLE_CENTER)
            x_cell += col_width

    out_dxf = os.path.join(diagramas_dir, "diagrama_unifilar.dxf")
    doc.saveas(out_dxf)
    render_dxf_to_pdf_and_svg(out_dxf)
    
    # Copy to report directory
    shutil.copy2(out_dxf.replace('.dxf', '.pdf'), os.path.join(planos_report_dir, "IE-05-unifilar-cuadro-cargas.pdf"))
    print("Diagrama Unifilar General compiled.")

# ====================================================
# PUESTA A TIERRA (IE-06-puesta-tierra)
# ====================================================
def build_puesta_a_tierra():
    doc = ezdxf.new("R2010", setup=True)
    msp = doc.modelspace()
    
    doc.layers.new("POZO", dxfattribs={'color': 7})
    doc.layers.new("TEXTOS", dxfattribs={'color': 7})
    doc.layers.new("MARCO", dxfattribs={'color': 7})
    
    # Frame and title block
    mx1, my1 = -1.5, -1.5
    mx2, my2 = 14.5, 9.5
    
    msp.add_line((mx1, my1), (mx2, my1), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((mx2, my1), (mx2, my2), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((mx2, my2), (mx1, my2), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((mx1, my2), (mx1, my1), dxfattribs={'layer': 'MARCO', 'color': 7})
    
    o = 0.08
    msp.add_line((mx1+o, my1+o), (mx2-o, my1+o), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((mx2-o, my1+o), (mx2-o, my2-o), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((mx2-o, my2-o), (mx1+o, my2-o), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((mx1+o, my2-o), (mx1+o, my1+o), dxfattribs={'layer': 'MARCO', 'color': 7})
    
    c_w, c_h = 4.8, 1.6
    cx1, cy1 = mx2 - o - c_w, my1 + o
    cx2, cy2 = mx2 - o, my1 + o + c_h
    msp.add_line((cx1, cy1), (cx1, cy2), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((cx1, cy2), (cx2, cy2), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((cx1, cy1 + 0.4), (cx2, cy1 + 0.4), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((cx1, cy1 + 0.8), (cx2, cy1 + 0.8), dxfattribs={'layer': 'MARCO', 'color': 7})
    msp.add_line((cx1, cy1 + 1.2), (cx2, cy1 + 1.2), dxfattribs={'layer': 'MARCO', 'color': 7})
    
    msp.add_text("UNAP - ESCUELA INGENIERIA MECANICA ELECTRICA", dxfattribs={'layer': 'TEXTOS', 'height': 0.11, 'color': 7}).set_placement((cx1 + 0.1, cy1 + 1.35))
    msp.add_text("PROY: DETALLE PUESTA A TIERRA (IE-06)", dxfattribs={'layer': 'TEXTOS', 'height': 0.11, 'color': 7}).set_placement((cx1 + 0.1, cy1 + 0.95))
    msp.add_text("ALUM: MAMANI GALINDO RENZO GABRIEL", dxfattribs={'layer': 'TEXTOS', 'height': 0.11, 'color': 7}).set_placement((cx1 + 0.1, cy1 + 0.55))
    msp.add_text("FECHA: 2026-06-03  |  ESC: S/E (MTS)", dxfattribs={'layer': 'TEXTOS', 'height': 0.09, 'color': 7}).set_placement((cx1 + 0.1, cy1 + 0.15))
    
    # Title
    msp.add_text("DETALLE CONSTRUCTIVO DE POZO DE PUESTA A TIERRA", dxfattribs={'layer': 'TEXTOS', 'height': 0.28, 'color': 7}).set_placement((0.0, 8.5))
    
    # Draw concrete cover (Tapa de registro) at top
    msp.add_lwpolyline([(2.0, 6.8), (4.0, 6.8), (4.0, 7.2), (2.0, 7.2)], close=True, dxfattribs={'layer': 'POZO', 'color': 7})
    msp.add_text("TAPA DE CONCRETO 0.40 x 0.40 m", dxfattribs={'layer': 'TEXTOS', 'height': 0.11, 'color': 7}).set_placement((4.2, 7.0))
    
    # Draw pit main body
    msp.add_line((2.2, 6.8), (2.2, 2.0), dxfattribs={'layer': 'POZO', 'color': 8})
    msp.add_line((3.8, 6.8), (3.8, 2.0), dxfattribs={'layer': 'POZO', 'color': 8})
    msp.add_line((2.2, 2.0), (3.8, 2.0), dxfattribs={'layer': 'POZO', 'color': 8})
    
    # Labeled dimension of the pit
    msp.add_text("Diámetro del Pozo: 0.80 m / Altura: 2.40 m", dxfattribs={'layer': 'TEXTOS', 'height': 0.10, 'color': 7}).set_placement((4.2, 4.5))
    
    # Draw copper electrode
    msp.add_line((3.0, 1.0), (3.0, 7.0), dxfattribs={'layer': 'POZO', 'color': 1, 'lineweight': 40}) # Red for copper rod
    msp.add_text("ELECTRODO DE COBRE 3/4\" x 2.40 m", dxfattribs={'layer': 'TEXTOS', 'height': 0.11, 'color': 7}).set_placement((3.2, 3.5))
    
    # Split-bolt copper connector
    msp.add_circle((3.0, 6.9), 0.08, dxfattribs={'layer': 'POZO', 'color': 1})
    msp.add_text("Conector Split-Bolt de Bronce", dxfattribs={'layer': 'TEXTOS', 'height': 0.10, 'color': 7}).set_placement((3.2, 6.8))
    
    # Copper wire
    msp.add_line((3.0, 6.9), (1.5, 7.8), dxfattribs={'layer': 'POZO', 'color': 1, 'linetype': 'DASHED'})
    msp.add_text("Cable de Cobre de Protección (10 mm2)", dxfattribs={'layer': 'TEXTOS', 'height': 0.10, 'color': 7}).set_placement((0.2, 7.5))
    
    # Soil filling
    msp.add_text("Relleno: Tierra de cultivo tratada", dxfattribs={'layer': 'TEXTOS', 'height': 0.10, 'color': 7}).set_placement((4.2, 2.8))
    msp.add_text("con aditivos de conductividad (Bentonita/Gel)", dxfattribs={'layer': 'TEXTOS', 'height': 0.10, 'color': 7}).set_placement((4.2, 2.5))
    
    # Specifications list on the right
    spec_x, spec_y = 8.5, 3.5
    msp.add_text("ESPECIFICACIONES TÉCNICAS", dxfattribs={'layer': 'TEXTOS', 'height': 0.13, 'color': 7}).set_placement((spec_x, spec_y + 3.0))
    specs = [
        "1. Resistencia final del pozo: < 15 Ohms.",
        "2. Electrodo de cobre puro electrolítico al 99.9%.",
        "3. Conductor de tierra embutido en tubo PVC-SAP 3/4\".",
        "4. Tratamiento del terreno con sales higroscópicas.",
        "5. Caja de registro de concreto H=0.30 m.",
        "6. Conexión franca a barra de tierra en TG-01."
    ]
    for i, s in enumerate(specs):
        msp.add_text(s, dxfattribs={'layer': 'TEXTOS', 'height': 0.09, 'color': 7}).set_placement((spec_x, spec_y + 2.5 - i * 0.4))

    out_dxf = os.path.join(diagramas_dir, "puesta_a_tierra.dxf")
    doc.saveas(out_dxf)
    render_dxf_to_pdf_and_svg(out_dxf)
    
    # Copy to report directory
    shutil.copy2(out_dxf.replace('.dxf', '.pdf'), os.path.join(planos_report_dir, "IE-06-puesta-tierra.pdf"))
    print("Detalle Puesta a Tierra compiled.")

if __name__ == "__main__":
    print("Generando todos los planos eléctricos y diagramas...")
    build_floor1_electrical()
    build_floor2_electrical()
    build_floor3_electrical()
    build_diagrama_unifilar()
    build_puesta_a_tierra()
    print("¡Todos los entregables CAD generados con éxito!")

#!/usr/bin/env python3
import argparse
import json
import os
import sys

try:
    from ezdxf.enums import TextEntityAlignment
except ImportError:
    TextEntityAlignment = None


DEFAULT_WALL_THICKNESS = 0.15


def point_key(point):
    return (round(float(point[0]), 5), round(float(point[1]), 5))


def segment_key(start, end):
    return tuple(sorted([point_key(start), point_key(end)]))


def draw_multiline_text(msp, text, x, y, height=0.22, layer="TEXTOS", rotation=0):
    lines = str(text).splitlines() or [""]
    spacing = height * 1.35
    start_y = y + spacing * (len(lines) - 1) / 2
    for i, line in enumerate(lines):
        msp.add_text(
            line,
            dxfattribs={"layer": layer, "height": height, "rotation": rotation},
        ).set_placement((x, start_y - i * spacing), align=TextEntityAlignment.MIDDLE_CENTER)


def draw_wall_segment(msp, start, end, thickness=DEFAULT_WALL_THICKNESS, layer="MUROS"):
    x1, y1 = float(start[0]), float(start[1])
    x2, y2 = float(end[0]), float(end[1])
    thickness = float(thickness)

    if abs(x1 - x2) < 1e-5:
        msp.add_line((x1 - thickness / 2, y1), (x2 - thickness / 2, y2), dxfattribs={"layer": layer})
        msp.add_line((x1 + thickness / 2, y1), (x2 + thickness / 2, y2), dxfattribs={"layer": layer})
    elif abs(y1 - y2) < 1e-5:
        msp.add_line((x1, y1 - thickness / 2), (x2, y2 - thickness / 2), dxfattribs={"layer": layer})
        msp.add_line((x1, y1 + thickness / 2), (x2, y2 + thickness / 2), dxfattribs={"layer": layer})
    else:
        msp.add_line((x1, y1), (x2, y2), dxfattribs={"layer": layer})


def validate_layout(data):
    if not isinstance(data, dict):
        raise ValueError("El archivo JSON debe contener un objeto/diccionario raíz.")
    if "dimensions" not in data:
        raise ValueError("Falta la sección 'dimensions' en el JSON.")
    if "rooms" not in data or not isinstance(data["rooms"], list):
        raise ValueError("Falta la lista 'rooms' en el JSON.")
    
    # Validar dimensiones
    dims = data["dimensions"]
    if "width" not in dims or "height" not in dims:
        raise ValueError("La sección 'dimensions' debe tener 'width' y 'height'.")
        
    # Validar habitaciones
    for i, room in enumerate(data["rooms"]):
        required = ["name", "x", "y", "width", "height"]
        for field in required:
            if field not in room:
                raise ValueError(f"Habitación en índice {i} no tiene el campo requerido '{field}'.")
                
    # Validar puertas si existen
    if "doors" in data:
        if not isinstance(data["doors"], list):
            raise ValueError("La sección 'doors' debe ser una lista.")
        for i, door in enumerate(data["doors"]):
            required = ["x", "y", "width", "orientation", "swing"]
            for field in required:
                if field not in door:
                    raise ValueError(f"Puerta en índice {i} no tiene el campo requerido '{field}'.")
                    
    # Validar ventanas si existen
    if "windows" in data:
        if not isinstance(data["windows"], list):
            raise ValueError("La sección 'windows' debe ser una lista.")
        for i, window in enumerate(data["windows"]):
            required = ["x", "y", "width", "orientation"]
            for field in required:
                if field not in window:
                    raise ValueError(f"Ventana en índice {i} no tiene el campo requerido '{field}'.")

    # Validar escaleras si existen
    if "stairs" in data:
        if not isinstance(data["stairs"], list):
            raise ValueError("La sección 'stairs' debe ser una lista.")
        for i, stair in enumerate(data["stairs"]):
            required = ["x1", "y1", "x2", "y2"]
            for field in required:
                if field not in stair:
                    raise ValueError(f"Escalera en índice {i} no tiene el campo requerido '{field}'.")

    if "walls" in data:
        if not isinstance(data["walls"], list):
            raise ValueError("La sección 'walls' debe ser una lista.")
        for i, wall in enumerate(data["walls"]):
            required = ["x1", "y1", "x2", "y2"]
            for field in required:
                if field not in wall:
                    raise ValueError(f"Muro en índice {i} no tiene el campo requerido '{field}'.")

    if "hatches" in data:
        if not isinstance(data["hatches"], list):
            raise ValueError("La sección 'hatches' debe ser una lista.")
        for i, hatch in enumerate(data["hatches"]):
            required = ["x", "y", "width", "height"]
            for field in required:
                if field not in hatch:
                    raise ValueError(f"Trama en índice {i} no tiene el campo requerido '{field}'.")

    if "texts" in data:
        if not isinstance(data["texts"], list):
            raise ValueError("La sección 'texts' debe ser una lista.")
        for i, text in enumerate(data["texts"]):
            required = ["text", "x", "y"]
            for field in required:
                if field not in text:
                    raise ValueError(f"Texto en índice {i} no tiene el campo requerido '{field}'.")

    if "custom_dimensions" in data:
        if not isinstance(data["custom_dimensions"], list):
            raise ValueError("La sección 'custom_dimensions' debe ser una lista.")
        for i, dim in enumerate(data["custom_dimensions"]):
            required = ["start", "end", "offset", "label", "direction"]
            for field in required:
                if field not in dim:
                    raise ValueError(f"Cota en índice {i} no tiene el campo requerido '{field}'.")

def draw_dimension(msp, start, end, offset, label, direction="horizontal"):
    """
    Dibuja una cota arquitectónica simple con líneas de extensión y marcas oblicuas (ticks).
    """
    layer = "COTAS"
    x1, y1 = start
    x2, y2 = end
    
    if direction == "horizontal":
        y_dim = y1 + offset
        # Línea de cota principal
        msp.add_line((x1, y_dim), (x2, y_dim), dxfattribs={'layer': layer})
        # Líneas de extensión
        msp.add_line((x1, y1), (x1, y_dim + (0.1 if offset > 0 else -0.1)), dxfattribs={'layer': layer})
        msp.add_line((x2, y2), (x2, y_dim + (0.1 if offset > 0 else -0.1)), dxfattribs={'layer': layer})
        # Marcas oblicuas (ticks)
        tick_len = 0.12
        msp.add_line((x1 - tick_len, y_dim - tick_len), (x1 + tick_len, y_dim + tick_len), dxfattribs={'layer': layer})
        msp.add_line((x2 - tick_len, y_dim - tick_len), (x2 + tick_len, y_dim + tick_len), dxfattribs={'layer': layer})
        # Texto de cota
        text_y = y_dim + 0.15 if offset > 0 else y_dim - 0.35
        msp.add_text(label, dxfattribs={'layer': layer, 'height': 0.18}).set_placement(((x1 + x2)/2, text_y), align=TextEntityAlignment.MIDDLE_CENTER)
    else: # vertical
        x_dim = x1 + offset
        # Línea de cota principal
        msp.add_line((x_dim, y1), (x_dim, y2), dxfattribs={'layer': layer})
        # Líneas de extensión
        msp.add_line((x1, y1), (x_dim + (0.1 if offset > 0 else -0.1), y1), dxfattribs={'layer': layer})
        msp.add_line((x2, y2), (x_dim + (0.1 if offset > 0 else -0.1), y2), dxfattribs={'layer': layer})
        # Marcas oblicuas
        tick_len = 0.12
        msp.add_line((x_dim - tick_len, y1 - tick_len), (x_dim + tick_len, y1 + tick_len), dxfattribs={'layer': layer})
        msp.add_line((x_dim - tick_len, y2 - tick_len), (x_dim + tick_len, y2 + tick_len), dxfattribs={'layer': layer})
        # Texto de cota (rotado 90 grados)
        text_x = x_dim + 0.15 if offset > 0 else x_dim - 0.35
        msp.add_text(label, dxfattribs={'layer': layer, 'height': 0.18, 'rotation': 90}).set_placement((text_x, (y1 + y2)/2), align=TextEntityAlignment.MIDDLE_CENTER)

def draw_door(msp, door):
    """
    Dibuja una puerta con su hoja abierta y la trayectoria del arco de giro.
    """
    layer = "PUERTAS"
    x = door["x"]
    y = door["y"]
    w = door["width"]
    ori = door["orientation"]
    swing = door["swing"]
    
    if ori == "horizontal":
        if swing == "top-right":
            # Hinge at (x, y), leaf goes up, arc starts at (x + w, y) to (x, y + w)
            msp.add_line((x, y), (x, y + w), dxfattribs={'layer': layer})
            msp.add_arc((x, y), w, 0, 90, dxfattribs={'layer': layer})
        elif swing == "top-left":
            # Hinge at (x + w, y), leaf goes up, arc starts at (x + w, y + w) to (x, y)
            msp.add_line((x + w, y), (x + w, y + w), dxfattribs={'layer': layer})
            msp.add_arc((x + w, y), w, 90, 180, dxfattribs={'layer': layer})
        elif swing == "bottom-right":
            # Hinge at (x, y), leaf goes down, arc starts at (x, y - w) to (x + w, y)
            msp.add_line((x, y), (x, y - w), dxfattribs={'layer': layer})
            msp.add_arc((x, y), w, 270, 360, dxfattribs={'layer': layer})
        elif swing == "bottom-left":
            # Hinge at (x + w, y), leaf goes down, arc starts at (x, y) to (x + w, y - w)
            msp.add_line((x + w, y), (x + w, y - w), dxfattribs={'layer': layer})
            msp.add_arc((x + w, y), w, 180, 270, dxfattribs={'layer': layer})
    else: # vertical
        if swing == "top-right":
            # Hinge at (x, y), leaf goes right, arc starts at (x + w, y) to (x, y + w)
            msp.add_line((x, y), (x + w, y), dxfattribs={'layer': layer})
            msp.add_arc((x, y), w, 0, 90, dxfattribs={'layer': layer})
        elif swing == "top-left":
            # Hinge at (x, y), leaf goes left, arc starts at (x, y + w) to (x - w, y)
            msp.add_line((x, y), (x - w, y), dxfattribs={'layer': layer})
            msp.add_arc((x, y), w, 90, 180, dxfattribs={'layer': layer})
        elif swing == "bottom-right":
            # Hinge at (x, y + w), leaf goes right, arc starts at (x, y) to (x + w, y + w)
            msp.add_line((x, y + w), (x + w, y + w), dxfattribs={'layer': layer})
            msp.add_arc((x, y + w), w, 270, 360, dxfattribs={'layer': layer})
        elif swing == "bottom-left":
            # Hinge at (x, y + w), leaf goes left, arc starts at (x - w, y + w) to (x, y)
            msp.add_line((x, y + w), (x - w, y + w), dxfattribs={'layer': layer})
            msp.add_arc((x, y + w), w, 180, 270, dxfattribs={'layer': layer})

def draw_window(msp, window):
    """
    Dibuja una ventana como un rectángulo estrecho con una línea central.
    """
    layer = "VENTANAS"
    x = window["x"]
    y = window["y"]
    w = window["width"]
    ori = window["orientation"]
    thick = 0.15 # Espesor de ventana estándar (espesor del muro)
    
    if ori == "horizontal":
        # Marco exterior de la ventana
        x1, y1 = x, y - thick/2
        x2, y2 = x + w, y + thick/2
        # Dibujar líneas del rectángulo
        msp.add_line((x1, y1), (x2, y1), dxfattribs={'layer': layer})
        msp.add_line((x2, y1), (x2, y2), dxfattribs={'layer': layer})
        msp.add_line((x2, y2), (x1, y2), dxfattribs={'layer': layer})
        msp.add_line((x1, y2), (x1, y1), dxfattribs={'layer': layer})
        # Línea central de vidrio
        msp.add_line((x1, y), (x2, y), dxfattribs={'layer': layer})
    else: # vertical
        x1, y1 = x - thick/2, y
        x2, y2 = x + thick/2, y + w
        # Dibujar líneas del rectángulo
        msp.add_line((x1, y1), (x2, y1), dxfattribs={'layer': layer})
        msp.add_line((x2, y1), (x2, y2), dxfattribs={'layer': layer})
        msp.add_line((x2, y2), (x1, y2), dxfattribs={'layer': layer})
        msp.add_line((x1, y2), (x1, y1), dxfattribs={'layer': layer})
        # Línea central de vidrio
        msp.add_line((x, y1), (x, y2), dxfattribs={'layer': layer})


def draw_rectangle(msp, x, y, width, height, layer="MOBILIARIO"):
    x2 = x + width
    y2 = y + height
    msp.add_line((x, y), (x2, y), dxfattribs={"layer": layer})
    msp.add_line((x2, y), (x2, y2), dxfattribs={"layer": layer})
    msp.add_line((x2, y2), (x, y2), dxfattribs={"layer": layer})
    msp.add_line((x, y2), (x, y), dxfattribs={"layer": layer})


def draw_hatch(msp, hatch):
    layer = hatch.get("layer", "TRAMAS")
    x = float(hatch["x"])
    y = float(hatch["y"])
    width = float(hatch["width"])
    height = float(hatch["height"])
    spacing = float(hatch.get("spacing", 0.35))
    k = -height
    while k <= width:
        t_start = max(0.0, -k)
        t_end = min(height, width - k)
        if t_start < t_end:
            msp.add_line(
                (x + k + t_start, y + t_start),
                (x + k + t_end, y + t_end),
                dxfattribs={"layer": layer},
            )
        k += spacing


def draw_fixture(msp, fixture):
    layer = fixture.get("layer", "MOBILIARIO")
    kind = fixture.get("type", "rect")
    x = float(fixture.get("x", 0.0))
    y = float(fixture.get("y", 0.0))
    width = float(fixture.get("width", 1.0))
    height = float(fixture.get("height", 1.0))

    if kind == "bed":
        draw_rectangle(msp, x, y, width, height, layer)
        draw_rectangle(msp, x + 0.10, y + height - 0.45, width - 0.20, 0.35, layer)
        msp.add_line((x + 0.15, y + height - 0.55), (x + width - 0.15, y + height - 0.55), dxfattribs={"layer": layer})
    elif kind == "sofa":
        draw_rectangle(msp, x, y, width, height, layer)
        draw_rectangle(msp, x + 0.10, y + 0.10, width - 0.20, height - 0.20, layer)
        if width > height:
            msp.add_line((x + width / 2, y + 0.10), (x + width / 2, y + height - 0.10), dxfattribs={"layer": layer})
        else:
            msp.add_line((x + 0.10, y + height / 2), (x + width - 0.10, y + height / 2), dxfattribs={"layer": layer})
    elif kind == "table":
        draw_rectangle(msp, x, y, width, height, layer)
        chair = min(width, height) * 0.22
        draw_rectangle(msp, x + width * 0.25, y - chair * 1.3, chair, chair, layer)
        draw_rectangle(msp, x + width * 0.60, y - chair * 1.3, chair, chair, layer)
        draw_rectangle(msp, x + width * 0.25, y + height + chair * 0.3, chair, chair, layer)
        draw_rectangle(msp, x + width * 0.60, y + height + chair * 0.3, chair, chair, layer)
    elif kind == "stove":
        draw_rectangle(msp, x, y, width, height, layer)
        radius = min(width, height) * 0.12
        for cx, cy in [
            (x + width * 0.30, y + height * 0.30),
            (x + width * 0.70, y + height * 0.30),
            (x + width * 0.30, y + height * 0.70),
            (x + width * 0.70, y + height * 0.70),
        ]:
            msp.add_circle((cx, cy), radius, dxfattribs={"layer": layer})
    elif kind == "sink":
        draw_rectangle(msp, x, y, width, height, layer)
        msp.add_ellipse(
            (x + width / 2, y + height / 2),
            major_axis=(width * 0.32, 0),
            ratio=max(0.2, min(1.0, height / max(width, 0.01) * 0.55)),
            dxfattribs={"layer": layer},
        )
    elif kind == "toilet":
        msp.add_circle((x + width / 2, y + height * 0.35), min(width, height) * 0.25, dxfattribs={"layer": layer})
        draw_rectangle(msp, x + width * 0.20, y + height * 0.62, width * 0.60, height * 0.22, layer)
    elif kind == "shower":
        draw_rectangle(msp, x, y, width, height, layer)
        msp.add_line((x + width * 0.12, y + height * 0.12), (x + width * 0.88, y + height * 0.88), dxfattribs={"layer": layer})
        msp.add_circle((x + width * 0.78, y + height * 0.22), min(width, height) * 0.06, dxfattribs={"layer": layer})
    elif kind == "line":
        msp.add_line((x, y), (float(fixture["x2"]), float(fixture["y2"])), dxfattribs={"layer": layer})
    elif kind == "circle":
        msp.add_circle((x, y), float(fixture.get("radius", 0.25)), dxfattribs={"layer": layer})
    else:
        draw_rectangle(msp, x, y, width, height, layer)

def main():
    global TextEntityAlignment
    parser = argparse.ArgumentParser(description="Generador automático de planos DXF a partir de JSON")
    parser.add_argument("--input", default="layout_example.json", help="Ruta del archivo JSON de entrada")
    parser.add_argument("--output", default="plan_distribucion.dxf", help="Ruta del archivo DXF de salida")
    args = parser.parse_args()
    
    # Resolver rutas relativas al directorio del script si es necesario
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    input_path = args.input
    if not os.path.isabs(input_path) and not os.path.exists(input_path):
        # Intentar rutas relativas al script y a la carpeta data del motor.
        candidates = [
            os.path.join(script_dir, args.input),
            os.path.join(script_dir, "..", "data", args.input),
        ]
        for possible_path in candidates:
            if os.path.exists(possible_path):
                input_path = possible_path
                break
            
    if not os.path.exists(input_path):
        print(f"Error: El archivo de entrada '{args.input}' no existe.", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error al leer/analizar el archivo JSON: {e}", file=sys.stderr)
        sys.exit(1)
        
    try:
        validate_layout(data)
    except ValueError as ve:
        print(f"Error de validación del diseño: {ve}", file=sys.stderr)
        sys.exit(1)
        
    try:
        import ezdxf
        if TextEntityAlignment is None:
            from ezdxf.enums import TextEntityAlignment as _TextEntityAlignment
            TextEntityAlignment = _TextEntityAlignment
    except ImportError:
        print("Error: La librería 'ezdxf' no está instalada. Ejecute 'pip install ezdxf'.", file=sys.stderr)
        sys.exit(1)
        
    print(f"Generando plano CAD para el proyecto: '{data.get('project', 'Sin nombre')}'...")
    output_dir = os.path.dirname(os.path.abspath(args.output))
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # Crear un nuevo dibujo DXF (formato R2010 es compatible con la mayoría de visores)
    doc = ezdxf.new("R2010", setup=True)
    msp = doc.modelspace()
    
    # Crear y configurar capas. Se fija true_color para que PDF/visores en fondo
    # blanco no rendericen muros/textos demasiado claros.
    black = 0x000000
    gray = 0x666666
    light_gray = 0x999999
    doc.layers.new("MUROS", dxfattribs={'color': 7, 'true_color': black, 'lineweight': 35}) # Grosor de línea 0.35 mm
    doc.layers.new("PUERTAS", dxfattribs={'color': 7, 'true_color': black})
    doc.layers.new("VENTANAS", dxfattribs={'color': 7, 'true_color': black})
    doc.layers.new("TEXTOS", dxfattribs={'color': 7, 'true_color': black})
    doc.layers.new("COTAS", dxfattribs={'color': 8, 'true_color': gray})
    doc.layers.new("MARCO", dxfattribs={'color': 7, 'true_color': black, 'lineweight': 50}) # Marco grueso
    doc.layers.new("ESCALERAS", dxfattribs={'color': 7, 'true_color': black})
    doc.layers.new("TRAMAS", dxfattribs={'color': 8, 'true_color': light_gray})
    doc.layers.new("MOBILIARIO", dxfattribs={'color': 8, 'true_color': gray})
    doc.layers.new("ANOTACIONES", dxfattribs={'color': 8, 'true_color': gray})
    
    # 1. Dibujar habitaciones y muros
    # Para evitar dibujar líneas duplicadas entre habitaciones adyacentes,
    # recopilamos todos los segmentos de muro únicos.
    walls = set()
    wall_thickness = float(data.get("wall_thickness", DEFAULT_WALL_THICKNESS))
    draw_room_walls = data.get("draw_room_walls", True)
    show_room_labels = data.get("show_room_labels", True)
    show_room_dimensions = data.get("show_room_dimensions", True)
    
    for room in data["rooms"]:
        rx, ry = room["x"], room["y"]
        rw, rh = room["width"], room["height"]
        
        if draw_room_walls and room.get("draw_walls", True):
            # Segmentos de la habitación (ordenados para evitar duplicados semánticos).
            walls.add(segment_key((rx, ry), (rx + rw, ry)))
            walls.add(segment_key((rx, ry + rh), (rx + rw, ry + rh)))
            walls.add(segment_key((rx, ry), (rx, ry + rh)))
            walls.add(segment_key((rx + rw, ry), (rx + rw, ry + rh)))
        
        # 2. Dibujar detalles de Escalera si corresponde
        x_center = rx + rw / 2
        y_center = ry + rh / 2
        
        if "escalera" in room["name"].lower():
            # Escalera tipo U con descanso al fondo (superior)
            landing_depth = 1.2
            # Línea central divisoria (ojo)
            msp.add_line((x_center, ry), (x_center, ry + rh - landing_depth), dxfattribs={'layer': 'MUROS'})
            # Línea de inicio del descanso
            msp.add_line((rx, ry + rh - landing_depth), (rx + rw, ry + rh - landing_depth), dxfattribs={'layer': 'MUROS'})
            
            # Dibujar escalones (huellas)
            num_steps = 9
            tread_depth = (rh - landing_depth) / num_steps
            for i in range(1, num_steps):
                y_step = ry + i * tread_depth
                # Paso izquierdo
                msp.add_line((rx, y_step), (x_center, y_step), dxfattribs={'layer': 'MUROS'})
                # Paso derecho
                msp.add_line((x_center, y_step), (rx + rw, y_step), dxfattribs={'layer': 'MUROS'})
                
            # Desplazar textos al descanso (landing) para evitar solapamientos
            text_y = ry + rh - (landing_depth / 2)
            dim_y = text_y - 0.25
        else:
            text_y = y_center
            dim_y = y_center - 0.25
        
        # 3. Dibujar etiquetas de textos en el centro de las habitaciones
        # Solo se dibuja si el nombre no está vacío y no empieza con guión bajo (útil para corredores auxiliares o vestíbulos)
        if show_room_labels and room.get("show_label", True) and room["name"] and not room["name"].startswith("_"):
            label = room.get("label", room["name"]).upper()
            label_height = float(room.get("label_height", data.get("room_label_height", 0.22)))
            draw_multiline_text(msp, label, x_center, text_y, height=label_height, layer="TEXTOS", rotation=float(room.get("label_rotation", 0)))
            
            # Dimensiones de la habitación (e.g. 4.00 x 4.00 m)
            if show_room_dimensions and room.get("show_dimensions", True):
                dim_text = f"{rw:.2f} x {rh:.2f} m"
                msp.add_text(
                    dim_text,
                    dxfattribs={'layer': 'TEXTOS', 'height': 0.15}
                ).set_placement((x_center, dim_y), align=TextEntityAlignment.MIDDLE_CENTER)
        
    # Cargar y remover los muros ignorados (ej. uniones libres de pasadizos o arcos de paso)
    ignored_walls = set()
    if "ignored_walls" in data:
        for p in data["ignored_walls"]:
            p1, p2 = p
            ignored_walls.add(segment_key(p1, p2))
            
    # Quitar de la lista de muros
    walls = walls - ignored_walls
        
    # Dibujar los muros derivados de habitaciones en la capa MUROS.
    for start, end in walls:
        draw_wall_segment(msp, start, end, wall_thickness, "MUROS")

    # Dibujar muros manuales opcionales. Permiten calcar croquis con vacíos, puertas
    # y contornos que no son una simple retícula de ambientes rectangulares.
    if "walls" in data:
        for wall in data["walls"]:
            start = (wall["x1"], wall["y1"])
            end = (wall["x2"], wall["y2"])
            draw_wall_segment(msp, start, end, wall.get("thickness", wall_thickness), wall.get("layer", "MUROS"))
        
    # 3. Dibujar Puertas
    if "doors" in data:
        for door in data["doors"]:
            draw_door(msp, door)
            
    # 4. Dibujar Ventanas
    if "windows" in data:
        for window in data["windows"]:
            draw_window(msp, window)

    # 4a. Dibujar tramas y mobiliario/artefactos simples de apoyo visual.
    if "hatches" in data:
        for hatch in data["hatches"]:
            draw_hatch(msp, hatch)

    if "fixtures" in data:
        for fixture in data["fixtures"]:
            draw_fixture(msp, fixture)

    # 4b. Dibujar Escaleras
    if "stairs" in data:
        for stair in data["stairs"]:
            x1, y1 = stair["x1"], stair["y1"]
            x2, y2 = stair["x2"], stair["y2"]
            steps = stair.get("steps", 6)
            
            # Contorno de la escalera
            msp.add_line((x1, y1), (x1, y2), dxfattribs={'layer': 'ESCALERAS'})
            msp.add_line((x2, y1), (x2, y2), dxfattribs={'layer': 'ESCALERAS'})
            msp.add_line((x1, y1), (x2, y1), dxfattribs={'layer': 'ESCALERAS'})
            msp.add_line((x1, y2), (x2, y2), dxfattribs={'layer': 'ESCALERAS'})
            
            # Pasos
            width = x2 - x1
            height = y2 - y1
            step_h = height / steps
            for i in range(1, steps):
                y_curr = y1 + i * step_h
                msp.add_line((x1, y_curr), (x2, y_curr), dxfattribs={'layer': 'ESCALERAS'})
            
    # 5. Dibujar Cotas generales externas
    limit_w = data["dimensions"]["width"]
    limit_h = data["dimensions"]["height"]
    
    # Cota de ancho total (abajo)
    draw_dimension(msp, (0.0, 0.0), (limit_w, 0.0), -1.0, f"ANCHO TOTAL: {limit_w:.2f} m", "horizontal")
    # Cota de alto total (izquierda)
    draw_dimension(msp, (0.0, 0.0), (0.0, limit_h), -1.0, f"ALTO TOTAL: {limit_h:.2f} m", "vertical")

    if "custom_dimensions" in data:
        for dim in data["custom_dimensions"]:
            draw_dimension(
                msp,
                tuple(dim["start"]),
                tuple(dim["end"]),
                dim["offset"],
                dim["label"],
                dim.get("direction", "horizontal"),
            )

    if "texts" in data:
        for item in data["texts"]:
            draw_multiline_text(
                msp,
                item["text"],
                float(item["x"]),
                float(item["y"]),
                height=float(item.get("height", 0.18)),
                layer=item.get("layer", "ANOTACIONES"),
                rotation=float(item.get("rotation", 0)),
            )
    
    # 6. Dibujar Marco y Bloque de Título (Title Block)
    margin = data.get("dimensions", {}).get("margin", 1.5)
    # Línea de marco exterior
    mx1, my1 = -margin, -margin
    mx2, my2 = limit_w + margin, limit_h + margin
    
    # Rectángulo del marco
    msp.add_line((mx1, my1), (mx2, my1), dxfattribs={'layer': 'MARCO'})
    msp.add_line((mx2, my1), (mx2, my2), dxfattribs={'layer': 'MARCO'})
    msp.add_line((mx2, my2), (mx1, my2), dxfattribs={'layer': 'MARCO'})
    msp.add_line((mx1, my2), (mx1, my1), dxfattribs={'layer': 'MARCO'})
    
    # Rectángulo interno del marco (doble línea decorativa)
    offset_m = 0.08
    imx1, imy1 = mx1 + offset_m, my1 + offset_m
    imx2, imy2 = mx2 - offset_m, my2 - offset_m
    msp.add_line((imx1, imy1), (imx2, imy1), dxfattribs={'layer': 'MARCO'})
    msp.add_line((imx2, imy1), (imx2, imy2), dxfattribs={'layer': 'MARCO'})
    msp.add_line((imx2, imy2), (imx1, imy2), dxfattribs={'layer': 'MARCO'})
    msp.add_line((imx1, imy2), (imx1, imy1), dxfattribs={'layer': 'MARCO'})

    if data.get("show_title_block", True):
        # Cajetín de Título (Bottom-Right, del marco interno)
        c_w = 4.8
        c_h = 1.6
        cx1 = imx2 - c_w
        cy1 = imy1
        cx2 = imx2
        cy2 = imy1 + c_h

        # Bordes del cajetín
        msp.add_line((cx1, cy1), (cx1, cy2), dxfattribs={'layer': 'MARCO'})
        msp.add_line((cx1, cy2), (cx2, cy2), dxfattribs={'layer': 'MARCO'})

        # Líneas divisorias internas del cajetín
        msp.add_line((cx1, cy1 + 0.4), (cx2, cy1 + 0.4), dxfattribs={'layer': 'MARCO'})
        msp.add_line((cx1, cy1 + 0.8), (cx2, cy1 + 0.8), dxfattribs={'layer': 'MARCO'})
        msp.add_line((cx1, cy1 + 1.2), (cx2, cy1 + 1.2), dxfattribs={'layer': 'MARCO'})

        # Textos del cajetín
        author = data.get("author", "ESTUDIANTE")
        project_name = data.get("project", "PROYECTO CAD")
        date_str = data.get("date", "2026-06-03")

        # Línea 4 (superior): Universidad
        msp.add_text("UNAP - ESCUELA INGENIERIA MECANICA ELECTRICA", dxfattribs={'layer': 'TEXTOS', 'height': 0.12, 'insert': (cx1 + 0.1, cy1 + 1.35)})
        # Línea 3: Nombre del proyecto
        msp.add_text(f"PROY: {project_name.upper()}", dxfattribs={'layer': 'TEXTOS', 'height': 0.12, 'insert': (cx1 + 0.1, cy1 + 0.95)})
        # Línea 2: Autor / Estudiante
        msp.add_text(f"DIB: {author.upper()}", dxfattribs={'layer': 'TEXTOS', 'height': 0.12, 'insert': (cx1 + 0.1, cy1 + 0.55)})
        # Línea 1: Fecha y Escala
        msp.add_text(f"FECHA: {date_str}   |   ESC: S/E (MTS)", dxfattribs={'layer': 'TEXTOS', 'height': 0.10, 'insert': (cx1 + 0.1, cy1 + 0.15)})
    
    # Guardar archivo DXF
    try:
        doc.saveas(args.output)
        print(f"¡Éxito! Plano guardado en: '{args.output}'")
    except Exception as e:
        print(f"Error al guardar el archivo DXF: {e}", file=sys.stderr)
        sys.exit(1)

    # Renderizar PDF automáticamente usando matplotlib
    pdf_output = args.output.replace('.dxf', '.pdf')
    try:
        import matplotlib.pyplot as plt
        from ezdxf.addons.drawing import RenderContext, Frontend
        from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
        
        print(f"Renderizando PDF con matplotlib: '{pdf_output}'...")
        # Volver a cargar el documento para asegurar consistencia
        doc_render = ezdxf.readfile(args.output)
        msp_render = doc_render.modelspace()
        
        fig = plt.figure(figsize=(11.69, 8.27))  # A4 horizontal en pulgadas
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        
        ctx = RenderContext(doc_render)
        out = MatplotlibBackend(ax)
        Frontend(ctx, out).draw_layout(msp_render, finalize=True)
        
        fig.savefig(pdf_output, dpi=300, bbox_inches='tight', pad_inches=0)
        plt.close(fig)
        print("¡Renderizado PDF completado con éxito!")
    except Exception as re:
        print(f"Advertencia: No se pudo generar el PDF automáticamente: {re}", file=sys.stderr)

if __name__ == "__main__":
    main()

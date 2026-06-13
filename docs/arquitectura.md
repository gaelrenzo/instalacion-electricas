# Arquitectura del repositorio

## Principio central

El repositorio separa tres tipos de información:

- **Fuentes:** croquis, fotografías, normativa y documentos recibidos.
- **Datos canónicos:** JSON/YAML que representan la interpretación vigente.
- **Resultados:** DXF, PDF, tablas, BOM y reportes que pueden regenerarse.

Esta separación permite cambiar el motor de IA o CAD sin perder la evidencia original y evita usar una salida vieja como entrada accidental.

## Proyectos

Cada carpeta en `proyectos/` debe contener:

```text
proyecto.yaml
fuentes/
arquitectura/datos/
diseno-electrico/datos/
datos/
documentacion/
entregables/
scripts/          solo extensiones realmente específicas
```

`proyecto.yaml` es el punto de entrada. Declara identidad, estado, rutas canónicas, automatización disponible y entregables publicados.

## Herramientas

- `pipeline_automatizado.py`: orquestación común.
- `calculos/`: demanda, conductores, protecciones y tablas LaTeX.
- `cad/`: generación arquitectónica, superposición eléctrica y PDF.
- `simbologia/`: biblioteca DGE y generador del catálogo.
- `cotizacion/`: BOM, normalización, proveedores, comparación y reportes.
- `calculadora/`: interfaz HTML independiente.

Las herramientas no deben incluir datos, nombres ni rutas de Aquiles o Renzo.

## Extensiones

Un proyecto con un formato CAD especial puede declarar `automatizacion.cad_personalizado` en su manifiesto. El pipeline conserva así una interfaz común sin forzar todos los diseños a un único esquema interno.

## Salidas

`build/<id>/` contiene la ejecución actual y está ignorado por Git. `entregables/` contiene únicamente resultados revisados que sí se desea versionar.

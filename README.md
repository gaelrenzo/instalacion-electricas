# Automatización de instalaciones eléctricas residenciales

Repositorio para convertir información de una vivienda, idealmente un croquis, en datos estructurados, cálculos eléctricos, planos CAD, metrados, cotizaciones y un expediente técnico revisable.

El objetivo es automatizar el trabajo repetitivo con agentes de IA sin presentar resultados preliminares como diseño definitivo. Toda salida técnica requiere revisión humana y contraste con el Código Nacional de Electricidad, el RNE y las condiciones reales de obra.

## Estructura

```text
.
├── AGENTS.md                 reglas de trabajo para agentes
├── docs/                     arquitectura, flujo y política de datos
├── herramientas/             motores reutilizables, sin datos de un alumno
├── proyectos/
│   ├── aquiles/              proyecto de dos pisos
│   └── renzo/                proyecto de tres pisos
├── referencias/              normativa y fuentes de consulta
└── build/                    resultados regenerables, ignorados por Git
```

Cada proyecto tiene un `proyecto.yaml`, entradas canónicas y un directorio `entregables/`. Las herramientas leen esas entradas y escriben únicamente en `build/`, salvo que un comando indique otra ruta de forma explícita.

## Inicio rápido

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 herramientas/pipeline_automatizado.py --proyecto aquiles
python3 herramientas/pipeline_automatizado.py --proyecto renzo
```

También se puede generar una configuración mínima para un proyecto nuevo:

```bash
python3 herramientas/pipeline_automatizado.py --generar-ejemplo
```

## Flujo esperado

1. Conservar el croquis original en `proyectos/<id>/fuentes/`.
2. Extraer geometría, ambientes, cotas e incertidumbres a JSON.
3. Validar la planta arquitectónica antes de ubicar elementos eléctricos.
4. Definir cargas, circuitos, protecciones, conductores y canalizaciones.
5. Ejecutar cálculos, CAD, BOM y cotización en `build/<id>/`.
6. Registrar observaciones y revisión humana.
7. Publicar únicamente resultados aprobados en `entregables/`.

La arquitectura completa está en [docs/arquitectura.md](docs/arquitectura.md) y el protocolo para agentes en [docs/flujo-agentes.md](docs/flujo-agentes.md).

## Estado actual

- Aquiles: pipeline general activo, con el primer piso como plano primario y el segundo piso conservado como entrada canónica separada.
- Renzo: cálculos generales y generador CAD multipiso integrados mediante una extensión declarada en su manifiesto.
- Cotización: pruebas automatizadas disponibles; las consultas web dependen de disponibilidad de proveedores y siempre deben guardar fecha, URL y nivel de confianza.

## Respaldo

El estado anterior a esta reorganización quedó preservado en la rama `respaldo/pre-reorganizacion-2026-06-13`. No se reescribió el historial de Git.

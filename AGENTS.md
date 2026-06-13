# Reglas para agentes

## Prioridad

Trabaja desde `proyecto.yaml` y las entradas canónicas del proyecto. No deduzcas el estado vigente por el nombre `v1`, `final`, `nuevo` o por la fecha de modificación de un archivo histórico.

## Contrato de directorios

- `fuentes/`: evidencia original; no modificar ni sobrescribir.
- `arquitectura/datos/`: geometría estructurada aprobada para continuar.
- `diseno-electrico/datos/`: elementos y circuitos eléctricos estructurados.
- `datos/`: parámetros de cálculo y otras entradas del pipeline.
- `documentacion/`: decisiones, supuestos y revisión técnica.
- `entregables/`: archivos aprobados para compartir.
- `build/`: resultados regenerables; nunca tratarlos como fuente.
- `referencias/local/`: material pesado o restringido; puede no existir en otro clon.

## Reglas técnicas

1. No inventar cotas, cargas, ubicación de tablero, sistema de puesta a tierra ni datos del propietario. Usar `null`, `por confirmar` o una hipótesis identificada.
2. Separar dato observado, dato calculado, supuesto y decisión humana.
3. Incluir unidad, fuente, estado y nivel de confianza en datos extraídos por IA.
4. No modificar las fuentes para que coincidan con una interpretación.
5. No publicar automáticamente en `entregables/`; primero generar en `build/` y revisar.
6. Mantener las herramientas genéricas. Los nombres, rutas y parámetros de un proyecto pertenecen a `proyectos/<id>/`.
7. Ejecutar pruebas y registrar cualquier parte que no se pudo validar.

## Secuencia mínima

```text
croquis -> extracción -> validación arquitectónica -> diseño eléctrico
        -> cálculos -> CAD -> BOM -> cotización -> expediente -> revisión
```

Si una etapa falla o contiene incertidumbre crítica, detener las etapas dependientes y dejar una observación explícita.

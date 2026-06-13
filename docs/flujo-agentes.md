# Flujo de trabajo con agentes de IA

## 1. Ingesta

Guardar el archivo recibido sin alterarlo y registrar su procedencia. Si es una imagen, conservar resolución y orientación originales.

## 2. Extracción del croquis

El agente debe producir una representación estructurada de muros, puertas, ventanas, escaleras, ambientes y cotas. Cada valor debe indicar si fue leído, inferido o queda por confirmar.

Salida recomendada:

```json
{
  "valor": 3.5,
  "unidad": "m",
  "origen": "cota visible en croquis",
  "confianza": 0.96,
  "estado": "observado"
}
```

## 3. Revisión arquitectónica

Comprobar cierre geométrico, escala, circulación, coherencia entre pisos y correspondencia con el croquis. No iniciar el diseño eléctrico si faltan dimensiones que cambian los recorridos o el metrado.

## 4. Diseño eléctrico

Proponer puntos de utilización y circuitos, pero marcar las decisiones que requieren confirmación: potencia de equipos, tipo de cocina, ubicación de medidor y tablero, diferenciales, SPAT y condiciones especiales.

## 5. Cálculo y generación

Ejecutar:

```bash
python3 herramientas/pipeline_automatizado.py --proyecto <id>
```

El agente debe revisar el código de salida, los mensajes de advertencia y los archivos producidos. La existencia de un PDF no prueba que el diseño sea correcto.

## 6. Cotización

Generar el BOM desde el diseño vigente. Toda oferta debe registrar proveedor, fecha, URL, unidad comercial, conversión y confianza. Un precio estimado nunca debe presentarse como precio verificado.

## 7. Aprobación

Comparar visualmente planos y croquis, revisar cálculos y documentar observaciones. Solo después copiar o regenerar la versión aprobada dentro de `entregables/`.

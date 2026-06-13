# Auditoria visual del PDF

**PDF revisado:** `proyectos/aquiles/expediente/build/main.pdf`
**Fecha:** 2026-06-03
**Metodo:** `pdfinfo`, `pdftoppm` y revision visual de capturas PNG.

## 1. Datos del PDF

- Paginas: 20.
- Tamano: carta (`612 x 792 pts`).
- Generador: `pdfTeX-1.40.29`.
- Compilo sin errores fatales con `pdflatex`.

## 2. Capturas generadas

Carpeta:

`proyectos/aquiles/expediente/docs/capturas_auditoria_pdf/`

Paginas renderizadas:

- `pagina-01.png`: portada.
- `pagina-02.png`: indice, primera pagina.
- `pagina-03.png`: indice, segunda pagina.
- `pagina-04.png`: inicio memoria.
- `pagina-12.png`: cierre de memoria / entorno de 2.12.
- `pagina-13.png`: inicio Capitulo 2.
- `pagina-17.png`: conductores, protecciones y formula de caida.
- `pagina-18.png`: resultados de caida, SPAT e inicio de tabla de cargas.
- `pagina-19.png`: tablas de cargas y conductores.
- `pagina-20.png`: pagina final casi vacia.

## 3. Observaciones visuales

| Elemento | Estado | Observacion |
|---|---|---|
| Portada | Correcta | Mantiene formato visual del modelo. |
| Indice | Correcto pero denso | Muestra Capitulo 2 completo; no incluye 3 y 4. |
| Encabezado | Correcto visualmente | Hay advertencias `Overfull hbox` de 7.8 pt por el ancho del encabezado. |
| Pie de pagina | DUDOSO | En Capitulo 2 sigue diciendo `MEMORIA DESCRIPTIVA - INSTALACIONES ELECTRICAS`; deberia cambiar a `CALCULOS JUSTIFICATIVOS - INSTALACIONES ELECTRICAS` o un pie general. |
| Inicio Capitulo 2 | Correcto | Titulo visible y jerarquia clara. |
| Formulas | Correctas visualmente | La formula de caida de tension se renderiza bien. |
| Tabla de cargas | Correcta | Se lee sin desbordes. |
| Tabla de conductores | Correcta pero ajustada | Se lee completa; podria usar tabla mas compacta o `tabularx` para robustez. |
| Pagina final | Baja calidad de paginacion | Queda casi vacia con una sola linea de texto. |
| Caracteres raros | Parcial | En texto extraido por `pdftotext` aparecen marcas por formulas, pero visualmente no afectan lectura. |
| Markdown literal | Problema textual | El LaTeX contiene `**6,992 W**` y `**NH-80**`; en PDF aparecen asteriscos literales en texto extraido. Debe cambiarse a `\textbf{}`. |

## 4. Advertencias de compilacion relevantes

Se compilo dos veces con:

```bash
pdflatex -interaction=nonstopmode -output-directory=build main.tex
pdflatex -interaction=nonstopmode -output-directory=build main.tex
```

Advertencias principales:

- `Package babel Warning`: no hay patrones de separacion de palabras en espanol precargados.
- Multiples `Overfull \hbox (7.80136pt too wide)` asociados al encabezado.
- `pdfTeX warning (ext4): destination with the same identifier ... duplicate ignored` en secciones 2.1 y 2.2 por reiniciar contadores de seccion sin ajustar anchors de `hyperref`.

## 5. Diagnostico visual general

**APROBADO CON OBSERVACIONES VISUALES.**

El PDF se ve entregable en forma general, pero antes de entrega formal conviene:

1. Corregir pie de pagina para que no diga memoria descriptiva durante calculos.
2. Eliminar asteriscos Markdown en LaTeX.
3. Corregir anchors duplicados de `hyperref`.
4. Ajustar encabezado para eliminar sobreanchos.
5. Evitar la pagina final casi vacia.

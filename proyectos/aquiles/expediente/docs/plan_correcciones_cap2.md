# Plan de correcciones del Capitulo 2

**Estado actual:** NO APROBADO para cierre definitivo.  
**Criterio:** no corregir de golpe; primero atender los puntos criticos que afectan seguridad, norma y resultados.

## CRITICO

1. **Recalcular maxima demanda con CNE-U 050-200.**
   - Archivo afectado: `herramientas/calculos/scripts/calcular_instalacion.py`.
   - Problema: el motor usa solo `PI * FD` por circuito.
   - Correccion: implementar metodo CNE 050-200 por area + cargas especiales y tomar el mayor valor aplicable frente al metodo por circuitos.
   - Impacto: cambia alimentador, interruptor general, caidas y cuadro resumen.

2. **Confirmar cocina electrica o cocina a gas.**
   - Archivo afectado: `data/proyecto_aquiles_base.json` y `capitulos/02-calculos-justificativos.tex`.
   - Problema: el capitulo asume cocina electrica de 3400 W; no esta confirmada.
   - Correccion: si es cocina electrica, usar `6000 W` como primera cocina conforme CNE 050-200; si es gas, retirar carga especial y mantener solo tomacorrientes de cocina/electrodomesticos.
   - Impacto: demanda puede pasar de `6992 W` a por lo menos `9500 W` en el escenario de cocina electrica con area 120 m2.

3. **Corregir seccion minima de alumbrado.**
   - Archivos afectados: JSON, script/output, Capitulo 2.
   - Problema: C1 y C4 usan `1.5 mm2`.
   - Correccion: usar minimo `2.5 mm2` para circuitos derivados de alumbrado, dejando `1.5 mm2` solo para retornos/control.
   - Impacto: cambia tabla de conductores y caida de tension de C1/C4.

4. **Corregir cita del factor 1.25.**
   - Archivo afectado: `capitulos/02-calculos-justificativos.tex` y docs de formulas.
   - Problema: se cita CNE 050-204, pero esa regla corresponde a escuelas.
   - Correccion: buscar regla correcta si existe; si no se verifica, presentar 1.25 como criterio conservador interno y no como exigencia CNE.

## ALTO

5. **Separar `Ib`, `Id`, `In_ITM` e `Iz`.**
   - Problema: la tabla muestra `I.d.` junto al ITM, pero el script selecciona ITM con `In` de carga.
   - Correccion: documentar claramente que `Ib` es corriente de empleo, `Id` es corriente de dimensionamiento termico si se usa, `In_ITM` es el calibre de proteccion e `Iz` es ampacidad.

6. **Marcar estado de cada dato de entrada.**
   - Problema: el JSON no indica si cada potencia, longitud o cantidad es confirmada, preliminar o supuesta.
   - Correccion: agregar campos `estado` y `fuente` por circuito/carga.

7. **Confirmar area techada por piso.**
   - Problema: memoria, cuestionario y capitulo tienen valores distintos.
   - Correccion: actualizar memoria, JSON y Capitulo 2 con un unico valor trazable.

8. **Aclarar criterio de caida de tension.**
   - Problema: capitulo usa 1.5% alimentador y 2.5% derivado; CNE extraido indica 2.5% y total 4%.
   - Correccion: si se mantiene 1.5%, presentarlo como criterio conservador del proyecto, no como exigencia textual.

9. **Revisar proteccion diferencial.**
   - Problema: el script asigna diferencial por circuito de tomacorriente/cocina/bomba, pero no define diferencial general ni agrupamientos.
   - Correccion: decidir esquema de diferenciales conforme CNE-U 020-132 y 150-400.

## MEDIO

10. **Hacer el motor parametrizable.**
    - Problema: rutas fijas de entrada/salida.
    - Correccion: agregar argumentos `--input`, `--output-dir` y posiblemente `--latex-out`.

11. **Mover ampacidades y calibres comerciales al JSON o tabla externa.**
    - Problema: valores hardcodeados en Python.
    - Correccion: usar archivo `data/tablas_normativas.json` con fuente y condiciones.

12. **Corregir LaTeX de tablas.**
    - Problema: rutas relativas fragiles y tabla ancha.
    - Correccion: copiar/centralizar tablas generadas en el proyecto LaTeX o definir ruta en `main.tex`; usar `tabularx` o `scriptsize` si crece.

13. **Corregir `hyperref` y pie de pagina.**
    - Problema: anchors duplicados y pie fijo de memoria.
    - Correccion: cambiar contador/anchor por capitulo o usar `\chapter` numerado; crear pie general o especifico para calculos.

14. **Eliminar Markdown literal en LaTeX.**
    - Problema: `**6,992 W**` y `**NH-80**`.
    - Correccion: reemplazar por `\textbf{6,992 W}` y `\textbf{NH-80}`.

## BAJO

15. **Evitar frases demasiado definitivas.**
    - Ejemplo: "Todos los circuitos cumplen holgadamente".
    - Correccion: "Con los datos preliminares actuales, las caidas calculadas quedan por debajo del limite adoptado; deben verificarse con longitudes definitivas".

16. **Revisar ortografia tecnica y tildes en LaTeX.**
    - Mantener coherencia entre ASCII y UTF-8.

17. **Controlar pagina final casi vacia.**
    - Ajustar salto de pagina o compactar el cierre del capitulo.

## Orden recomendado de ejecucion

1. Preguntar a Aquiles: area, cocina electrica/gas, TG, longitudes, cargas reales.
2. Corregir JSON de datos.
3. Corregir motor con metodo CNE 050-200 y conductores minimos.
4. Regenerar outputs.
5. Actualizar Capitulo 2 con resultados recalculados.
6. Recompilar y repetir auditoria de calculos.

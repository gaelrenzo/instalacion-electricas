# Política de datos y limpieza

- No versionar cachés, archivos temporales, compilaciones LaTeX ni resultados de pruebas.
- No versionar colecciones pesadas de referencia en `referencias/local/`.
- No versionar fuentes privadas o pesadas del proyecto en `proyectos/*/fuentes/local/`.
- Versionar datos canónicos pequeños, código, documentación, normativa permitida y entregables aprobados.
- Conservar una sola versión canónica de cada plano dentro de la estructura activa; mover la historia útil a `archivo/` o confiar en Git.
- Nombrar por función (`piso-1.json`, `expediente.pdf`), no por secuencias ambiguas (`final_v7_nuevo2`).
- Antes de eliminar datos, comprobar que exista respaldo en Git, en una rama de resguardo o fuera del repositorio.

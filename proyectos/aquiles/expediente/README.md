# Proyecto LaTeX de instalaciones electricas interiores

Esta carpeta contiene el nuevo proyecto LaTeX aislado para la vivienda de Aquiles Taylor Ramos Yapo. El entregable formal se organiza como documento tecnico academico y no modifica los proyectos LaTeX antiguos del repositorio.

## Contenido

- `main.tex`: archivo principal compilable.
- `preambulo.tex`: configuracion general del documento.
- `referencias.bib`: referencias normativas basicas.
- `capitulos/00-portada.tex`: portada con formato visual de memoria descriptiva.
- `capitulos/01-memoria-descriptiva.tex`: memoria descriptiva desarrollada en esta fase.
- `capitulos/02-...` a `08-...`: capitulos creados como estructura pendiente.
- `figuras/`: contiene el escudo usado en la cabecera y la referencia catastral de ubicacion.
- `planos/`, `tablas/`: carpetas preparadas para fases posteriores.
- `build/`: salida de compilacion.

Para respetar el formato del modelo indicado por el usuario, `main.tex` compila actualmente solo la memoria descriptiva. Los capitulos restantes permanecen creados como estructura, pero no se insertan en el PDF de esta fase.

## Compilacion

Desde esta carpeta:

```bash
latexmk -pdf -interaction=nonstopmode -output-directory=build main.tex
```

Si `latexmk` no esta disponible:

```bash
pdflatex -interaction=nonstopmode -output-directory=build main.tex
pdflatex -interaction=nonstopmode -output-directory=build main.tex
```

El PDF esperado es:

```text
build/main.pdf
```

## Fuentes revisadas

Fuentes directas del caso Aquiles:

- `proyectos/aquiles/documentacion/capitulo-1-memoria-descriptiva.md`
- `proyectos/aquiles/documentacion/capitulo-2-calculos-justificativos.md`
- `proyectos/aquiles/documentacion/pautas-vivienda-2-pisos.md`
- `proyectos/aquiles/documentacion/plan-de-trabajo.md`
- `proyectos/aquiles/documentacion/respuestas-cuestionario-aquiles.md`
- `proyectos/aquiles/documentacion/apoyo-gemini-matriz-normativa.md`
- `proyectos/aquiles/fuentes/croquis/`
- `proyectos/aquiles/trabajo-cad-casa/`

Modelos de estructura y tono:

- `materiales/INSTALACIONES ELECTRICAS DVD 28.02-23/memoria descriptiva/`
- `materiales/INSTALACIONES ELECTRICAS DVD 28.02-23/especificaciones tecnicas/`
- `materiales/proyecto-guia-red-primaria/capitulo-i-memoria/`
- `materiales/proyecto-guia-red-primaria/capitulo-ii-calculos/`
- `materiales/proyecto-guia-red-primaria/capitulo-vii-planos/`
- `latex/`

Modelo principal adoptado para la memoria descriptiva:

- `materiales/INSTALACIONES ELECTRICAS DVD 28.02-23/memoria descriptiva/memoria descriptiva l.pdf`

La estructura de la memoria se rehizo siguiendo ese modelo: `Generalidades` y `Descripcion del proyecto`, con subapartados de ubicacion, objetivos, alcances, normas, alimentadores, tablero, circuitos, canalizaciones, iluminacion, tomacorrientes, puesta a tierra, pruebas, simbolos y cuadro de cargas. Los datos del proyecto institucional del modelo no fueron copiados.

El formato visual tambien se ajusto al modelo: tamano carta, portada con barra lateral azul, cabecera institucional enmarcada, pie de pagina con linea azul, titulo `CONTENIDO`, titulos rojos subrayados y numeracion por apartados.

## Normativa considerada

- Codigo Nacional de Electricidad -- Utilizacion.
- Reglamento Nacional de Edificaciones.
- Norma Tecnica EM.010 Instalaciones Electricas Interiores.

Los numerales y articulos especificos quedan para revision tecnica antes de cerrar calculos y especificaciones.

## Estado de esta fase

Desarrollado:

- Memoria descriptiva.

Pendiente:

- Calculos justificativos.
- Especificaciones de materiales.
- Especificaciones de montaje.
- Cronograma.
- Metrado.
- Planos.
- Anexos.

## Datos pendientes de confirmacion

- Propietario civil o titular formal del predio.
- Docente responsable del curso.
- Area construida final por piso.
- Punto de suministro, medidor y tipo de acometida.
- Ubicacion definitiva del tablero general.
- Numero definitivo de circuitos derivados.
- Cantidad final de salidas de alumbrado y tomacorrientes.
- Sistema de puesta a tierra y resistencia objetivo.
- Conciliacion definitiva entre los nombres de ambientes del cuestionario y los croquis CAD.

## Siguiente fase recomendada

Desarrollar `capitulos/02-calculos-justificativos.tex` usando los ambientes ya regularizados, los planos CAD vigentes y los criterios normativos verificados.

PYTHON ?= python3

.PHONY: install test test-tools test-renzo test-unidad-2 check-unidad-2 aquiles renzo clean

install:
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m pytest -q herramientas/cotizacion/v0_legacy/tests herramientas/cotizacion/v1/tests proyectos/renzo/tests proyectos/unidad-2-industrial/tests

test-tools:
	$(PYTHON) -m pytest -q herramientas/cotizacion/v0_legacy/tests herramientas/cotizacion/v1/tests

test-renzo:
	$(PYTHON) -m pytest -q proyectos/renzo/tests

test-unidad-2:
	$(PYTHON) -m pytest -q proyectos/unidad-2-industrial/tests

check-unidad-2:
	$(PYTHON) proyectos/unidad-2-industrial/scripts/verificar_preparacion.py

aquiles:
	$(PYTHON) herramientas/pipeline_automatizado.py --proyecto aquiles

renzo:
	$(PYTHON) herramientas/pipeline_automatizado.py --proyecto renzo

renzo-industrial:
	$(PYTHON) herramientas/pipeline_automatizado.py --proyecto renzo-industrial

clean:
	rm -rf build

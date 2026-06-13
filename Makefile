PYTHON ?= python3

.PHONY: install test aquiles renzo clean

install:
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m pytest -q herramientas/cotizacion/tests

aquiles:
	$(PYTHON) herramientas/pipeline_automatizado.py --proyecto aquiles

renzo:
	$(PYTHON) herramientas/pipeline_automatizado.py --proyecto renzo

clean:
	rm -rf build

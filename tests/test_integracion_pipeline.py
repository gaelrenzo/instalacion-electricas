from __future__ import annotations

import json
import math
import os
import tempfile
from pathlib import Path

import pytest
import yaml


# ─── Tests para ampacidades configurables ───────────────────────────────

class TestAmpacidadesConfigurables:
    """Verifica que las tablas de ampacidad se carguen correctamente desde YAML."""

    def test_carga_yaml_cobre(self) -> None:
        from herramientas.calculos.scripts.calcular_instalacion import cargar_ampacidades
        data = cargar_ampacidades()
        assert "cobre" in data
        assert "ducto" in data["cobre"]
        assert 2.5 in data["cobre"]["ducto"]
        assert data["cobre"]["ducto"][2.5] == 20  # 2.5 mm2 Cu = 20A

    def test_carga_yaml_aluminio(self) -> None:
        from herramientas.calculos.scripts.calcular_instalacion import cargar_ampacidades
        data = cargar_ampacidades()
        assert "aluminio" in data
        assert 2.5 in data["aluminio"]["ducto"]

    def test_carga_yaml_itm(self) -> None:
        from herramientas.calculos.scripts.calcular_instalacion import cargar_ampacidades
        data = cargar_ampacidades()
        assert 10 in data["itm_estandar_a"]
        assert 63 in data["itm_estandar_a"]

    def test_get_ampacity_cu(self) -> None:
        from herramientas.calculos.scripts.calcular_instalacion import cargar_ampacidades, get_ampacity
        data = cargar_ampacidades()
        assert get_ampacity(4.0, "cobre", "ducto", data) == 28

    def test_get_ampacity_al(self) -> None:
        from herramientas.calculos.scripts.calcular_instalacion import cargar_ampacidades, get_ampacity
        data = cargar_ampacidades()
        al_amp = get_ampacity(4.0, "aluminio", "ducto", data)
        assert al_amp > 0
        assert al_amp < 28  # Al < Cu para misma seccion

    def test_get_ampacity_unknown_section(self) -> None:
        from herramientas.calculos.scripts.calcular_instalacion import cargar_ampacidades, get_ampacity
        data = cargar_ampacidades()
        assert get_ampacity(999, "cobre", "ducto", data) == 0

    def test_select_conductor_cu(self) -> None:
        from herramientas.calculos.scripts.calcular_instalacion import cargar_ampacidades, select_conductor_for_design
        data = cargar_ampacidades()
        section, amp = select_conductor_for_design(25, 2.5, "cobre", "ducto", data)
        assert section >= 2.5
        assert amp >= 25

    def test_select_conductor_al(self) -> None:
        from herramientas.calculos.scripts.calcular_instalacion import cargar_ampacidades, select_conductor_for_design
        data = cargar_ampacidades()
        section, amp = select_conductor_for_design(25, 2.5, "aluminio", "ducto", data)
        assert section >= 2.5
        assert amp >= 25

    def test_find_itm(self) -> None:
        from herramientas.calculos.scripts.calcular_instalacion import cargar_ampacidades, find_appropriate_itm
        data = cargar_ampacidades()
        assert find_appropriate_itm(15, 50, data) == 16
        assert find_appropriate_itm(30, 50, data) == 32
        assert find_appropriate_itm(5, 10, data) == 10


# ─── Tests para A* routing ──────────────────────────────────────────────

class TestAutoRoutingAStar:
    """Verifica que el nuevo auto_routing con A* funcione correctamente."""

    @pytest.fixture
    def sample_electrical(self) -> dict:
        return {
            "tableros": [{"x": 1.0, "y": 1.0, "label": "TG"}],
            "luminarias": [
                {"id": "L1", "x": 5.0, "y": 5.0, "circuit": "C1"},
                {"id": "L2", "x": 5.0, "y": 3.0, "circuit": "C1"},
            ],
            "interruptores": [
                {"id": "S1", "x": 4.0, "y": 4.0, "circuit": "C1", "kind": "simple"},
            ],
            "tomacorrientes": [],
            "equipos": [],
        }

    @pytest.fixture
    def sample_layout(self) -> dict:
        return {
            "walls": [
                {"x1": 0, "y1": 0, "x2": 8, "y2": 0, "thickness": 0.15},
                {"x1": 8, "y1": 0, "x2": 8, "y2": 8, "thickness": 0.15},
                {"x1": 8, "y1": 8, "x2": 0, "y2": 8, "thickness": 0.15},
                {"x1": 0, "y1": 8, "x2": 0, "y2": 0, "thickness": 0.15},
            ],
            "rooms": [
                {"name": "Sala", "points": [[0, 0], [8, 0], [8, 8], [0, 8]]},
            ],
        }

    def test_astar_basic_routing(self, sample_electrical: dict) -> None:
        from herramientas.cad.scripts.auto_routing import auto_route_electrical
        result = auto_route_electrical(sample_electrical, clearance=0.3, resolution=0.2)
        assert "rutas" in result
        assert len(result["rutas"]) >= 1
        for ruta in result["rutas"]:
            assert len(ruta["points"]) >= 2
            assert "circuit" in ruta

    def test_astar_with_obstacles(self, sample_electrical: dict, sample_layout: dict) -> None:
        from herramientas.cad.scripts.auto_routing import auto_route_electrical
        result = auto_route_electrical(sample_electrical, sample_layout, clearance=0.3, resolution=0.2)
        assert "rutas" in result
        assert "_routing_metadata" in result
        meta = result["_routing_metadata"]
        assert meta["algorithm"] == "A*"
        assert meta["obstacle_cells"] > 0

    def test_astar_path_connects_tg(self, sample_electrical: dict) -> None:
        from herramientas.cad.scripts.auto_routing import auto_route_electrical
        result = auto_route_electrical(sample_electrical)
        tg = (1.0, 1.0)
        for ruta in result["rutas"]:
            first = ruta["points"][0]
            assert abs(first[0] - tg[0]) < 0.1
            assert abs(first[1] - tg[1]) < 0.1

    def test_astar_path_length_reported(self, sample_electrical: dict) -> None:
        from herramientas.cad.scripts.auto_routing import auto_route_electrical
        result = auto_route_electrical(sample_electrical)
        for ruta in result["rutas"]:
            assert ruta["total_length_m"] > 0

    def test_astar_without_layout(self, sample_electrical: dict) -> None:
        """Debe funcionar incluso sin layout (sin obstaculos)."""
        from herramientas.cad.scripts.auto_routing import auto_route_electrical
        result = auto_route_electrical(sample_electrical)
        assert len(result["rutas"]) > 0

    def test_astar_multiple_circuits(self) -> None:
        from herramientas.cad.scripts.auto_routing import auto_route_electrical
        data = {
            "tableros": [{"x": 1.0, "y": 1.0}],
            "luminarias": [
                {"x": 3.0, "y": 3.0, "circuit": "C1"},
                {"x": 5.0, "y": 5.0, "circuit": "C2"},
            ],
            "interruptores": [],
            "tomacorrientes": [],
            "equipos": [],
        }
        result = auto_route_electrical(data)
        circuits = {r["circuit"] for r in result["rutas"]}
        assert "C1" in circuits
        assert "C2" in circuits


# ─── Tests de calculo electrico con ampacidades ──────────────────────────

class TestCalculoConAmpacidades:
    """Verifica que el motor de calculo use correctamente las ampacidades configurables."""

    @pytest.fixture
    def sample_data(self) -> dict:
        return {
            "proyecto": "Test",
            "propietario": "Test",
            "ubicacion": {"distrito": "Test", "provincia": "Test", "departamento": "Test", "direccion": "", "estado": "test", "fuente": "test"},
            "areas": {
                "terreno_m2": {"valor": 100, "estado": "test", "fuente": "test"},
                "techada_primer_piso_m2": {"valor": 50, "estado": "test", "fuente": "test"},
                "techada_segundo_piso_m2": {"valor": 50, "estado": "test", "fuente": "test"},
                "techada_total_calculo_m2": {"valor": 100, "estado": "test", "fuente": "test"},
            },
            "parametros_electricos": {
                "tension_v": 220,
                "fases": 1,
                "frecuencia_hz": 60,
                "factor_potencia_cosphi": 0.90,
                "factor_diseno_conductor": 1.25,
                "material_conductor": "cobre",
                "modo_instalacion": "ducto",
                "resistividad_auto": True,
                "caida_tension_max_derivados_porc": 2.5,
                "caida_tension_max_alimentador_porc": 1.5,
            },
            "alimentacion_principal": {"origen": "M", "destino": "TG", "longitud_m": 10, "estado": "test", "fuente": "test"},
            "escenario_dimensionamiento_id": "base",
            "circuitos_base": [
                {"id": "C1", "descripcion": "Alumbrado", "potencia_instalada_w": 200, "factor_demanda": 1.0, "longitud_m": 20, "seccion_conductor_mm2": 2.5, "diametro_tubo_mm": 20, "requiere_diferencial": False, "requiere_tierra": True, "estado": "test", "fuente": "test"},
                {"id": "C2", "descripcion": "Tomacorrientes", "potencia_instalada_w": 1800, "factor_demanda": 0.7, "longitud_m": 25, "seccion_conductor_mm2": 2.5, "diametro_tubo_mm": 20, "requiere_diferencial": True, "requiere_tierra": True, "estado": "test", "fuente": "test"},
            ],
            "escenarios": [
                {"id": "base", "nombre": "Base", "estado": "test", "descripcion": "", "cocina_electrica": False, "cne_050_200": {"aplicar": True, "cocina_electrica_normativa_w": 0}, "circuito_overrides": {}},
            ],
        }

    def test_calculo_con_cobre(self, sample_data: dict) -> None:
        from herramientas.calculos.scripts.calcular_instalacion import run_calculations, cargar_ampacidades
        amp_data = cargar_ampacidades()
        results = run_calculations(sample_data, amp_data)
        design = results["escenario_dimensionamiento"]
        assert design["resumen_general"]["potencia_instalada_total_w"] == 2000

    def test_calculo_con_aluminio(self, sample_data: dict) -> None:
        from herramientas.calculos.scripts.calcular_instalacion import run_calculations, cargar_ampacidades
        sample_data["parametros_electricos"]["material_conductor"] = "aluminio"
        amp_data = cargar_ampacidades()
        results = run_calculations(sample_data, amp_data)
        design = results["escenario_dimensionamiento"]
        # Aluminio tiene resistividad mayor -> mayor caida de tension
        assert design["circuitos_calculados"][0]["caida_tension_porc"] > 0

    def test_ampacidad_afecta_seleccion_itm(self) -> None:
        from herramientas.calculos.scripts.calcular_instalacion import find_appropriate_itm, cargar_ampacidades
        amp_data = cargar_ampacidades()
        # Corriente alta con capacidad limitada
        itm = find_appropriate_itm(45, 50, amp_data)
        assert itm == 50  # 45A con max 50A -> ITM 50A

    def test_calculo_con_resistividad_manual(self, sample_data: dict) -> None:
        from herramientas.calculos.scripts.calcular_instalacion import run_calculations, cargar_ampacidades
        sample_data["parametros_electricos"]["resistividad_auto"] = False
        sample_data["parametros_electricos"]["resistividad_cobre_rho"] = 0.0200  # mayor resistividad
        amp_data = cargar_ampacidades()
        results = run_calculations(sample_data, amp_data)
        design = results["escenario_dimensionamiento"]
        assert design["circuitos_calculados"][0]["caida_tension_porc"] > 0

    def test_escenarios_multiples(self, sample_data: dict) -> None:
        from herramientas.calculos.scripts.calcular_instalacion import run_calculations, cargar_ampacidades
        sample_data["escenarios"].append({
            "id": "cocina_elec",
            "nombre": "Con cocina electrica",
            "estado": "test", "descripcion": "",
            "cocina_electrica": True,
            "cne_050_200": {"aplicar": True, "cocina_electrica_normativa_w": 3000},
            "circuito_overrides": {},
        })
        amp_data = cargar_ampacidades()
        results = run_calculations(sample_data, amp_data)
        assert len(results["escenarios"]) == 2
        cocina = results["escenarios"]["cocina_elec"]
        assert cocina["resumen_general"]["maxima_demanda_adoptada_w"] > 2000

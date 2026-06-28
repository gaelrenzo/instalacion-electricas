"""CNE Peru norm strategy — voltage drop, grounding, validation, ampacity."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Dict, Optional

from electra_core.modelos.topologia import Cable, Circuito, RedElectrica, Tablero, TipoNormativa

from electra.dominio.calculos.puertos import EstrategiaNormativa


_AMPACIDADES_CACHE: Optional[Dict] = None


def _ampacidades_fallback() -> Dict:
    return {
        "cobre": {
            "conductividad_rho_mohm": 0.0175,
            "ducto": {1.5: 15, 2.5: 20, 4.0: 28, 6.0: 36, 10.0: 50, 16.0: 66, 25.0: 88, 35.0: 109, 50.0: 134, 70.0: 167, 95.0: 202, 120.0: 235},
        },
        "aluminio": {
            "conductividad_rho_mohm": 0.0282,
            "ducto": {2.5: 16, 4.0: 22, 6.0: 28, 10.0: 40, 16.0: 55, 25.0: 72, 35.0: 88, 50.0: 108, 70.0: 135, 95.0: 165, 120.0: 195},
        },
        "itm_estandar_a": [10, 16, 20, 25, 32, 40, 50, 63, 80, 100],
    }


def cargar_ampacidades(path: Optional[str] = None) -> Dict:
    global _AMPACIDADES_CACHE
    if _AMPACIDADES_CACHE is not None:
        return _AMPACIDADES_CACHE

    if path:
        ruta = Path(path)
    else:
        ruta = Path(__file__).resolve().parents[4] / "herramientas" / "calculos" / "datos" / "ampacidades.yaml"

    try:
        import yaml
        if ruta.exists():
            with open(ruta, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            _AMPACIDADES_CACHE = data
            return data
    except ImportError:
        pass

    _AMPACIDADES_CACHE = _ampacidades_fallback()
    return _AMPACIDADES_CACHE


class CNEPeru(EstrategiaNormativa):
    CAIDA_MAX_ALIMENTADOR = 2.5
    CAIDA_MAX_DERIVADO = 1.5
    CAIDA_MAX_ACUMULADA = 4.0
    RESISTENCIA_PST_FUERZA = 25.0
    RESISTENCIA_PST_EQUIPOS = 5.0

    def __init__(self) -> None:
        self._amp_data = cargar_ampacidades()

    def get_ampacity(self, section: float, material: str = "cobre", modo: str = "ducto") -> float:
        return self._amp_data.get(material, {}).get(modo, {}).get(float(section), 0)

    def find_appropriate_itm(self, ib: float, max_capacity: float) -> int:
        itm_list = self._amp_data.get("itm_estandar_a", [10, 16, 20, 25, 32, 40, 50, 63, 80, 100])
        for rating in itm_list:
            if rating >= ib and rating <= max_capacity:
                return rating
        for rating in itm_list:
            if rating >= ib:
                return rating
        return itm_list[-1] if itm_list else 100

    def validar_caida_tension(self, circuito: Circuito) -> list[str]:
        alertas = []
        caida = circuito.caida_tension_max_porcentaje
        if caida > self.CAIDA_MAX_ALIMENTADOR:
            alertas.append(
                f"Alimentador '{circuito.nombre}': caída {caida:.2f}% "
                f"excede límite CNE {self.CAIDA_MAX_ALIMENTADOR}%"
            )
        return alertas

    def validar_tablero(self, tablero: Tablero) -> list[str]:
        alertas = []
        for circuito in tablero.circuitos:
            alertas.extend(self.validar_caida_tension(circuito))
        return alertas

    def validar_red(self, red: RedElectrica) -> list[str]:
        alertas = []
        for tablero in red.tableros:
            alertas.extend(self.validar_tablero(tablero))
        return alertas

    def calcular_resistencia_pst(
        self, resistividad: float, longitud_m: float, diametro_mm: float
    ) -> float:
        d = diametro_mm / 1000
        return (resistividad / (2 * math.pi * longitud_m)) * (
            math.log(4 * longitud_m / d) - 1
        )

    def calcular_caida_tension(
        self, cable: Cable, corriente_a: float, largo_metros: float
    ) -> float:
        R = 0.0172 / cable.seccion_mm2
        return (2 * largo_metros * R * corriente_a * 100) / 220.0

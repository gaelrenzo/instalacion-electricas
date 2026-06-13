import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

from cotizador_multi_proveedor import cargar_bom


def test_cargar_bom_minimo():
    raw, materiales = cargar_bom(BASE / "tests" / "fixtures" / "bom_minimo.json")
    assert raw["propietario"] == "Persona de prueba"
    assert len(materiales) == 2
    assert materiales[0].nombre_normalizado == "cable electrico thw 2.5 mm2 cobre"
    assert materiales[1].categoria == "interruptores termomagneticos"

import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE.parents[1]))  # src/

from electra.infraestructura.presupuestos.cotizador_multi_proveedor import (
    elegir_recomendado,
    puntuar_resultados,
)
from electra.infraestructura.presupuestos.modelos import MaterialBOM, ResultadoProveedor


def test_matching_prefiere_coincidencia_tecnica():
    material = MaterialBOM(
        id="M001",
        nombre_original="ITM 2P-10A - C1",
        nombre_normalizado="interruptor termomagnetico 2 polos 10A",
        categoria="interruptores termomagneticos",
        unidad="und",
        cantidad=1,
        especificaciones={"polos": 2, "amperaje_a": 10},
    )
    barato_malo = ResultadoProveedor(
        proveedor="Proveedor barato",
        consulta=material.nombre_normalizado,
        producto="Interruptor simple decorativo",
        precio=5.0,
        url="https://example.test/malo",
        score_proveedor=0.8,
    )
    tecnico = ResultadoProveedor(
        proveedor="Proveedor tecnico",
        consulta=material.nombre_normalizado,
        producto="Interruptor termomagnetico 2 polos 10A curva C",
        precio=35.0,
        url="https://example.test/bueno",
        score_proveedor=0.8,
    )
    reglas = {
        "pesos": {"precio": 0.5, "tecnico": 0.3, "proveedor": 0.1, "disponibilidad": 0.1},
        "rangos_precio_referenciales": {"interruptores termomagneticos": [10, 500]},
    }
    resultados = [barato_malo, tecnico]
    puntuar_resultados(material, resultados, reglas)
    recomendado, _ = elegir_recomendado(material, resultados)
    assert recomendado is tecnico

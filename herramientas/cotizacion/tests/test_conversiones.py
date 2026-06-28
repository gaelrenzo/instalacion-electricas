#!/usr/bin/env python3
"""Pruebas unitarias para conversion de unidades comerciales."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from electra.infraestructura.presupuestos.conversor_unidades import (
    calcular_compra_comercial,
    detectar_unidad_comercial,
    extraer_contenido_comercial,
    marcar_confianza_conversion,
    normalizar_unidad,
)

def test_cable_85m_rollo_100m():
    # 1. Cable 85 m, rollo 100 m, precio 180
    cant_com, subtotal, sobrante, pr_equiv = calcular_compra_comercial(
        cantidad_bom=85.0,
        unidad_bom="m",
        precio_producto=180.0,
        unidad_comercial="rollo",
        contenido_comercial=100.0
    )
    assert cant_com == 1.0
    assert subtotal == 180.0
    assert sobrante == 15.0
    assert pr_equiv == 1.80

def test_cable_110m_rollo_100m():
    # 2. Cable 110 m, rollo 100 m, precio 180
    cant_com, subtotal, sobrante, pr_equiv = calcular_compra_comercial(
        cantidad_bom=110.0,
        unidad_bom="m",
        precio_producto=180.0,
        unidad_comercial="rollo",
        contenido_comercial=100.0
    )
    assert cant_com == 2.0
    assert subtotal == 360.0
    assert sobrante == 90.0
    assert pr_equiv == 1.80

def test_tubo_26m_tubo_3m():
    # 3. Tubo 26 m, tubo 3 m, precio 8
    cant_com, subtotal, sobrante, pr_equiv = calcular_compra_comercial(
        cantidad_bom=26.0,
        unidad_bom="m",
        precio_producto=8.0,
        unidad_comercial="tubo",
        contenido_comercial=3.0
    )
    assert cant_com == 9.0
    assert subtotal == 72.0
    assert sobrante == 1.0
    assert round(pr_equiv, 4) == round(8.0 / 3.0, 4)

def test_itm_unidad_2():
    # 4. ITM unidad, precio 35, cantidad 2
    cant_com, subtotal, sobrante, pr_equiv = calcular_compra_comercial(
        cantidad_bom=2.0,
        unidad_bom="unidad",
        precio_producto=35.0,
        unidad_comercial="unidad",
        contenido_comercial=1.0
    )
    assert cant_com == 2.0
    assert subtotal == 70.0
    assert sobrante == 0.0
    assert pr_equiv == 35.0

def test_detectar_y_extraer():
    titulo1 = "Cable Indeco THW 2.5 mm2 rojo Rollo 100 metros"
    unidad1 = detectar_unidad_comercial(titulo1, "cables")
    contenido1, und_cont1, confianza1, obs1 = extraer_contenido_comercial(titulo1, "cables")
    
    assert "rollo" in unidad1.lower()
    assert contenido1 == 100.0
    assert und_cont1 == "m"
    assert confianza1 == 1.0
    
    titulo2 = "Tubo PVC SAP 20 mm electrico Pavco"
    # No dice longitud en titulo, debe asumir 3m por regla de ductos
    unidad2 = detectar_unidad_comercial(titulo2, "ductos/tuberias")
    contenido2, und_cont2, confianza2, obs2 = extraer_contenido_comercial(titulo2, "ductos/tuberias")
    
    assert contenido2 == 3.0
    assert und_cont2 == "m"
    assert confianza2 == 0.8  # Se asume longitud


def test_paquete_cajas_x_10():
    titulo = "Paquete x 10 unidades caja rectangular PVC"
    unidad = detectar_unidad_comercial(titulo, "cajas electricas")
    contenido, unidad_contenido, confianza, _ = extraer_contenido_comercial(
        titulo, "cajas electricas"
    )
    assert unidad == "paquete"
    assert contenido == 10
    assert unidad_contenido == "unidad"
    assert confianza == 1.0


def test_alias_und_es_unidad_y_conversion_confiable():
    assert normalizar_unidad("und") == "unidad"
    assert marcar_confianza_conversion("und", "unidad", 1, 1.0) == 1.0

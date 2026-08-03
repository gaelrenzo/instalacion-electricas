#!/usr/bin/env python3
"""Construye todos los entregables y el expediente técnico del proyecto Renzo Industrial (Grifo San Román)."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
REPO_DIR = PROJECT_DIR.parent.parent
EXPEDIENTE_DIR = PROJECT_DIR / "expediente"
BUILD_DIR = REPO_DIR / "build" / "renzo-industrial"
ENTREGABLES_DIR = PROJECT_DIR / "entregables"


def run_script(script_name, *args):
    script_path = SCRIPT_DIR / script_name
    print(f"\n====== Ejecutando: {script_name} ======")
    result = subprocess.run(
        [sys.executable, str(script_path), *args],
        cwd=str(PROJECT_DIR),
    )
    if result.returncode != 0:
        raise SystemExit(f"[ERROR] El script {script_name} falló.")
    print(f"[OK] {script_name} completado.")


def compile_latex():
    print("\n====== Compilando expediente/main.tex ======")
    latex_build_dir = BUILD_DIR / "expediente"
    latex_build_dir.mkdir(parents=True, exist_ok=True)
    command = [
        "pdflatex",
        "-interaction=nonstopmode",
        f"-output-directory={latex_build_dir}",
        "main.tex",
    ]

    for pass_number in (1, 2):
        print(f"-> Pasada {pass_number} de LaTeX")
        result = subprocess.run(command, cwd=str(EXPEDIENTE_DIR))
        if result.returncode != 0:
            print(f"[WARN] Pasada {pass_number} de LaTeX retornó advertencias/errores no fatales.")

    pdf_path = latex_build_dir / "main.pdf"
    if pdf_path.exists():
        ENTREGABLES_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(pdf_path), str(ENTREGABLES_DIR / "expediente-renzo-industrial.pdf"))
        print(f"[OK] Expediente PDF copiado a: {ENTREGABLES_DIR / 'expediente-renzo-industrial.pdf'}")


def sync_entregables():
    print("\n====== Sincronizando Entregables ======")
    ENTREGABLES_DIR.mkdir(parents=True, exist_ok=True)
    
    # Copiar PDF combinado de planos
    planos_combined = BUILD_DIR / "cad" / "planos" / "planos-electricos-grifo-renzo.pdf"
    if planos_combined.exists():
        shutil.copy2(str(planos_combined), str(ENTREGABLES_DIR / "planos-electricos-grifo-renzo.pdf"))
        print(f"[OK] Planos combinados copiados a entregables/planos-electricos-grifo-renzo.pdf")
    
    # Copiar planos individuales PDF
    for i in range(1, 7):
        code = f"IE-0{i}"
        for pdf_file in (BUILD_DIR / "cad" / "planos").glob(f"{code}_*.pdf"):
            shutil.copy2(str(pdf_file), str(ENTREGABLES_DIR / pdf_file.name))
            print(f"[OK] Plano {pdf_file.name} copiado a entregables/")


def main():
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    (BUILD_DIR / "calculos").mkdir(parents=True, exist_ok=True)
    (BUILD_DIR / "expediente" / "generated").mkdir(parents=True, exist_ok=True)
    (BUILD_DIR / "cad" / "planos").mkdir(parents=True, exist_ok=True)
    
    run_script("calcular_proyecto.py")
    run_script("calcular_iluminacion.py")
    run_script("generar_bom_renzo.py")
    run_script("generar_fragmentos_expediente.py")
    run_script("generar_planos_grifo_renzo.py")
    compile_latex()
    sync_entregables()
    print(f"\n[OK] Pipeline renzo-industrial completado exitosamente.")


if __name__ == "__main__":
    main()

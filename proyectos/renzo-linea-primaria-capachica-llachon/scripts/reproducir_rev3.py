"""Pipeline Rev. 3 desde raíz o subcarpeta; protege salidas existentes."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
OUTPUTS = [ROOT/name for name in (
    "derived/reconciliacion_corredores_rev3.json",
    "datos/empalmes_kml_rev3.csv",
    "datos/candidatos_nuevos_replanteo_rev3.csv",
    "datos/registro_datos_rev3.json",
    "datos/cruces_viales_rev3.csv",
    "derived/manifest_rev3.json",
)]
DOCS = [ROOT/name for name in (
    "documentacion/CONCILIACION_CORREDORES_REV3.md",
    "documentacion/SOLICITUD_TECNICA_ELECTRO_PUNO_REV3.md",
    "documentacion/METODOLOGIA_UBICACION_POSTES_REV3.md",
    "documentacion/FLUJO_CALCULOS_REV3.md",
    "documentacion/PLAN_CAMPO_Y_CRUCES_REV3.md",
    "documentacion/AUDITORIA_PLANOS_REV3.md",
    "documentacion/BLOQUEOS_Y_PUERTAS_REV3.md",
    "documentacion/INFORME_REV3.md",
    "expediente/08_preparacion_diseno_rev3.md",
)]
CODE = [ROOT/name for name in (
    "README.md", "proyecto.yaml", "requirements.txt",
    "datos/parametros_diseno_pendientes.json",
    "scripts/preparar_rev3.py", "scripts/validar_rev3.py",
    "scripts/reproducir_rev3.py", "tests/test_rev3.py",
)]


def digest(path: Path):
    return {"bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-existing", action="store_true",
                        help="respalda únicamente las salidas Rev. 3 y las regenera")
    args = parser.parse_args()
    inputs = [ROOT/"sources/ruta topografica capachica llachon.kml",
              ROOT/"derived/route.json", ROOT/"sources/gisem_mt_estructuras.geojson",
              ROOT/"sources/osm_roads.json",
              ROOT/"datos/parametros_diseno_pendientes.json", *DOCS, *CODE]
    missing = [str(p) for p in inputs if not p.is_file()]
    if missing: raise FileNotFoundError("Faltan entradas: " + ", ".join(missing))
    existing = [p for p in OUTPUTS if p.exists()]
    if existing and not args.archive_existing:
        raise FileExistsError("Hay salidas Rev. 3; use --archive-existing para respaldar y regenerar")
    if existing:
        archive = REPO/"build"/ROOT.name/"archive_rev3"/datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        for path in existing:
            rel = path.resolve().relative_to(ROOT.resolve())
            dest = archive/rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(dest))
        print(f"Respaldadas {len(existing)} salidas Rev. 3 en {archive}", flush=True)
    subprocess.run([sys.executable, str(ROOT/"scripts/preparar_rev3.py")], cwd=REPO, check=True)
    subprocess.run([sys.executable, str(ROOT/"scripts/validar_rev3.py")], cwd=REPO, check=True)
    subprocess.run([sys.executable, "-m", "pytest", str(ROOT/"tests"), "-q"], cwd=REPO, check=True)
    manifest = ROOT/"derived/manifest_rev3.json"
    payload = {"revision": 3, "status": "PRELIMINARY_NOT_FOR_CONSTRUCTION",
               "software_tests": "pytest completo aprobado; ver salida de pipeline",
               "engineering_validation": False,
               "files": {p.relative_to(ROOT).as_posix(): digest(p)
                         for p in [*OUTPUTS[:-1], *DOCS, *CODE, *inputs[:4]]}}
    manifest.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    saved = json.loads(manifest.read_text(encoding="utf-8"))
    for relative, expected in saved["files"].items():
        if digest(ROOT/relative) != expected:
            raise ValueError(f"Huella de manifiesto inválida: {relative}")
    print(f"Rev. 3 verificada; manifiesto: {manifest}")


if __name__ == "__main__":
    main()

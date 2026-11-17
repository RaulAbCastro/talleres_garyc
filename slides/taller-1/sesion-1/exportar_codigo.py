"""Exporta R/Python ejecutables y la referencia Stata desde el mismo QMD."""
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent
qmd = (BASE / "index.qmd").read_text(encoding="utf-8")
target = BASE / "codigo"
target.mkdir(exist_ok=True)
for engine, extension in (("webr", "R"), ("pyodide", "py")):
    cells = re.findall(r"^```\{" + engine + r"\}\n(.*?)^```", qmd, re.M | re.S)
    intro = (
        "# Taller 1 / Sesión 1: De la muestra a la inferencia\n"
        "# Generado desde index.qmd por exportar_codigo.py; edita el QMD.\n"
        "# Ejecutar desde slides/taller-1/sesion-1/. Datos sintéticos.\n\n"
    )
    (target / f"sesion-1.{extension}").write_text(
        (intro + "\n\n".join(cells)).rstrip() + "\n", encoding="utf-8"
    )
    print(f"Exportados {len(cells)} laboratorios {extension}")

cells = re.findall(r"^```stata\n(.*?)^```", qmd, re.M | re.S)
intro = (
    "* Taller 1 / Sesión 1: De la muestra a la inferencia\n"
    "* Generado desde index.qmd por exportar_codigo.py; edita el QMD.\n"
    "* Ejecutar desde slides/taller-1/sesion-1/. Datos sintéticos.\n"
    "* Referencia estática: no ejecutada ni validada con Stata en este entorno.\n"
    "set more off\n\n"
)
(target / "sesion-1.do").write_text(
    (intro + "\n\n".join(
        f"* Laboratorio {i}\n{cell}" for i, cell in enumerate(cells, 1)
    )).rstrip() + "\n", encoding="utf-8"
)
print(f"Exportados {len(cells)} laboratorios Stata (referencia)")

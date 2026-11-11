#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
export PATH="$PWD/.venv/bin:$PATH"
export QUARTO_PYTHON="$PWD/.venv/bin/python"

printf 'Python del proyecto: '
.venv/bin/python --version
Rscript -e 'cat(R.version.string, "\n"); packages <- c("tidyverse", "readxl", "haven", "broom", "knitr", "rmarkdown", "reticulate", "IRkernel", "languageserver", "httpgd"); stopifnot(all(vapply(packages, requireNamespace, logical(1), quietly = TRUE))); stopifnot(packageVersion("reticulate") >= "1.40.0", packageVersion("systemfonts") >= "1.3.2"); cat("Paquetes R: OK\n")'
printf 'Quarto: '
quarto --version
pdflatex --version | head -n 1
xelatex --version | head -n 1
latexmk -v
.venv/bin/python - <<'PY'
import importlib
from pathlib import Path
from jupyter_client.kernelspec import KernelSpecManager

for name in ["numpy", "pandas", "scipy", "matplotlib", "seaborn", "statsmodels.api", "sklearn", "openpyxl", "pyreadstat", "jupyterlab", "notebook", "nbconvert", "ipywidgets"]:
    importlib.import_module(name)
print("Paquetes Python: OK")
manager = KernelSpecManager()
kernels = manager.find_kernel_specs()
for name in ["talleres-python", "talleres-r"]:
    if name not in kernels:
        raise RuntimeError("Falta el kernel " + name)
    executable = manager.get_kernel_spec(name).argv[0]
    if not Path(executable).is_file():
        raise RuntimeError("Ejecutable del kernel no encontrado: " + executable)
    print("Kernel {}: {}".format(name, executable))
PY

if [[ -f documents_overleaf/.git ]]; then
  printf 'Overleaf: submódulo descargado; comprobar autenticación con bash scripts/overleaf.sh check.\n'
else
  printf 'Overleaf: pendiente de conectar con tu token privado (ver README).\n'
fi
printf 'Stata: ejecución en el Windows remoto del banco; editor .do configurado aquí.\n'

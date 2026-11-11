#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
project_dir="$PWD"

bash .devcontainer/install-system.sh

# El Python de Ubuntu 24.04 es 3.12; el Python global del Codespace puede ser otro.
if [[ ! -x .venv/bin/python ]]; then
  /usr/bin/python3 -m venv .venv
fi
export PATH="$project_dir/.venv/bin:$PATH"
export QUARTO_PYTHON="$project_dir/.venv/bin/python"
export RETICULATE_PYTHON="$QUARTO_PYTHON"
export R_LIBS_USER="$project_dir/.local/R/library"
mkdir -p "$R_LIBS_USER" outputs

python -m pip install --upgrade pip
if [[ -f requirements.lock.txt ]]; then
  python -m pip install -r requirements.lock.txt
else
  python -m pip install -r requirements.txt
fi

# Los kernels pertenecen al entorno del proyecto y se recrean al reconstruirlo.
python -m ipykernel install --sys-prefix --name talleres-python --display-name 'Python (talleres)'
Rscript .devcontainer/install-r.R
Rscript -e 'IRkernel::installspec(prefix = normalizePath(".venv"), name = "talleres-r", displayname = "R (talleres)")'

bash scripts/check-environment.sh
printf '\nListo. En una terminal nueva: source .venv/bin/activate\n'

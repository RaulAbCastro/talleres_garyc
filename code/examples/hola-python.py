"""Ejecutar desde la raíz: .venv/bin/python code/examples/hola-python.py."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

data = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [2, 4, 5, 4, 6]})
print(smf.ols("y ~ x", data=data).fit().params)
output = Path(__file__).resolve().parents[2] / "outputs"
output.mkdir(exist_ok=True)
data.plot.scatter(x="x", y="y")
plt.savefig(output / "hola-python.png", dpi=150, bbox_inches="tight")
print("Gráfica guardada en outputs/hola-python.png")

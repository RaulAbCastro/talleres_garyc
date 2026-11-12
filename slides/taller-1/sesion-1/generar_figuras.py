"""Figuras de respaldo en Python; solo leen el CSV observado de participantes."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

BASE = Path(__file__).resolve().parent
d = pd.read_csv(BASE / "datos/muestra.csv")
ASSETS = BASE / "assets"
ASSETS.mkdir(exist_ok=True)
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 14, "svg.fonttype": "none",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.labelcolor": "#253347", "text.color": "#1B2A4A",
    "figure.facecolor": "#F7F8FA", "axes.facecolor": "#F7F8FA",
})

fig, ax = plt.subplots(figsize=(11, 4.0))
for uso, color in ((0, "#5D6D7E"), (1, "#007279")):
    y = d.loc[d.usa_agente == uso, "tasa_anual"]
    margen = stats.t.ppf(.975, len(y) - 1) * stats.sem(y)
    ax.errorbar(y.mean(), 1-uso, xerr=margen, fmt="o", color=color,
                markersize=11, elinewidth=3, capsize=6)
    ax.text(y.mean(), 1-uso+.17, f"{y.mean():.2f}% · n={len(y)}",
            ha="center", color=color, fontweight="bold")
ax.set(yticks=[0, 1], yticklabels=["Usa el Agente", "No usa el Agente"],
       xlabel="Tasa anual media (%) · intervalos de confianza del 95%",
       xlim=(17, 25), ylim=(-.5, 1.5))
ax.grid(axis="x", alpha=.18)
fig.tight_layout()
fig.savefig(ASSETS / "tasas-python.svg")
plt.close(fig)

fig, ax = plt.subplots(figsize=(11, 4.0))
for uso, color, etiqueta in ((0, "#9BA5B7", "No usa el Agente"),
                              (1, "#007279", "Usa el Agente")):
    g = d.loc[d.usa_agente == uso]
    ax.scatter(g.ingreso_miles, g.tasa_anual, color=color, s=22,
               alpha=.6, label=etiqueta, edgecolors="none")
modelo = stats.linregress(d.ingreso_miles, d.tasa_anual)
x = np.array([d.ingreso_miles.min(), d.ingreso_miles.max()])
ax.plot(x, modelo.intercept + modelo.slope*x, color="#B26A00", linewidth=3,
        label="Recta descriptiva conjunta")
ax.set(xlabel="Ingreso (miles de áureos al mes)", ylabel="Tasa anual (%)")
ax.legend(frameon=False, fontsize=10, loc="upper right")
ax.grid(alpha=.12)
fig.tight_layout()
fig.savefig(ASSETS / "ingreso-python.svg")
plt.close(fig)
print("Figuras Python: tasas e ingreso en assets/")

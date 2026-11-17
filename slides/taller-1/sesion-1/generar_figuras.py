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
    "svg.hashsalt": "taller-1-sesion-1-202609",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.labelcolor": "#253347", "text.color": "#1B2A4A",
    "figure.facecolor": "#F7F8FA", "axes.facecolor": "#F7F8FA",
})

fig, ax = plt.subplots(figsize=(11, 4))
for nomina, color in ((0, "#5D6D7E"), (1, "#007279")):
    y = d.loc[d.recibe_nomina == nomina, "saldo_promedio_miles"]
    margen = stats.t.ppf(.975, len(y)-1) * stats.sem(y)
    ax.errorbar(y.mean(), 1-nomina, xerr=margen, fmt="o", color=color,
                markersize=11, elinewidth=3, capsize=6)
    ax.text(y.mean(), 1-nomina+.19, f"{y.mean():.2f} · n={len(y)}",
            ha="center", color=color, fontweight="bold")
ax.set(yticks=[0, 1], yticklabels=["Recibe nómina", "No recibe nómina"],
       xlabel="Saldo promedio del mes (miles de MXN) · IC del 95% de cada media",
       xlim=(9, 18), ylim=(-.5, 1.5))
ax.grid(axis="x", alpha=.18)
fig.tight_layout()
fig.savefig(ASSETS / "saldos-python.svg", metadata={"Date": None})
plt.close(fig)

fig, ax = plt.subplots(figsize=(11, 4))
for nomina, color, etiqueta in ((0, "#9BA5B7", "No recibe nómina"),
                                (1, "#007279", "Recibe nómina")):
    g = d.loc[d.recibe_nomina == nomina]
    ax.scatter(g.abonos_miles, g.saldo_promedio_miles, color=color, s=22,
               alpha=.6, label=etiqueta, edgecolors="none")
ax.set(xlabel="Abonos totales del mes (miles de MXN)",
       ylabel="Saldo promedio (miles de MXN)", xlim=(0, 82), ylim=(0, 36))
ax.legend(frameon=False, fontsize=10, loc="upper left")
ax.grid(alpha=.12)
fig.tight_layout()
fig.savefig(ASSETS / "abonos-python.svg", metadata={"Date": None})
plt.close(fig)

# Distribución de referencia bajo la hipótesis nula en el ejemplo bilateral.
fig, ax = plt.subplots(figsize=(11, 2.65))
z = np.arange(-450, 451) / 100
densidad = stats.norm.pdf(z)
extremo = 2
porcentaje_cola = 100 * stats.norm.sf(extremo)
for signo in (-1, 1):
    cola = signo * z >= extremo
    ax.fill_between(z[cola], 0, densidad[cola], color="#E0A33B")
    ax.vlines(signo * extremo, 0, stats.norm.pdf(extremo), color="#805600")
    ax.annotate(f"{porcentaje_cola:.3f}%", (signo * 2.2, 0.017),
                xytext=(signo * 2.95, 0.17), ha="center", color="#805600",
                fontsize=17, fontweight="bold",
                arrowprops={"arrowstyle": "->", "color": "#805600"})
ax.plot(z, densidad, color="#007279", linewidth=2.5)
ax.set(xlim=(-4.5, 4.5), ylim=(0, 0.42), yticks=[],
       xlabel="Valor del estadístico bajo la hipótesis nula")
ax.set_xticks([-extremo, 0, extremo], labels=["−2", "0", "+2"])
ax.spines["left"].set_visible(False)
fig.tight_layout()
fig.savefig(ASSETS / "colas-python.svg", metadata={"Date": None})
plt.close(fig)

for nombre in ("saldos-python.svg", "abonos-python.svg", "colas-python.svg"):
    archivo = ASSETS / nombre
    contenido = archivo.read_text(encoding="utf-8")
    archivo.write_text("\n".join(linea.rstrip() for linea in contenido.splitlines()) + "\n", encoding="utf-8")
print("Figuras Python: saldos-python.svg, abonos-python.svg y colas-python.svg en assets/")

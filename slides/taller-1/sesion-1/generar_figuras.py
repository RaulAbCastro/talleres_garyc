"""Figuras en Python del caso bancario y de los escenarios didácticos."""
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

# Comparar los mismos grupos manteniendo sus tamaños y medias.
pagos = pd.cut(d.n_pagos_debito, [-1, 0, 4, np.inf],
               labels=["0 pagos", "1 a 4 pagos", "5 o más pagos"])
grupos = d.groupby(pagos, observed=True).saldo_promedio_miles
medias, desvios = grupos.mean(), grupos.std()
fig, ejes = plt.subplots(1, 2, figsize=(11, 2.95), sharex=True, sharey=True)
escenarios = [("Muestra del taller", 1), ("Distancias a la mitad", 0.5)]
for eje, (titulo, escala) in zip(ejes, escenarios):
    eje.errorbar(medias, [2, 1, 0], xerr=escala * desvios, fmt="o", markersize=8,
                 color="#1B2A4A", ecolor="#007279", elinewidth=3, capsize=5)
    eje.set(title=titulo, xlim=(7, 20), ylim=(-0.5, 2.5), xticks=[8, 10, 12, 14, 16, 18],
            yticks=[2, 1, 0], yticklabels=medias.index)
    eje.set_axisbelow(True)
    eje.grid(axis="x", color="#D9DDE5")
fig.supxlabel("Saldo promedio del mes (miles de MXN)", y=0.06, fontsize=14)
fig.tight_layout(rect=(0, 0.13, 1, 1))
fig.savefig(ASSETS / "dispersion-anova-python.svg", metadata={"Date": None})
plt.close(fig)

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

# La extensión horizontal del perfil representa densidad, no un cambio en X.
fig, ax = plt.subplots(figsize=(11, 3.15))
abonos = np.array([10, 25, 40])
centros = 5 + 0.4 * abonos
desvios = np.linspace(-3.2, 3.2, 129)
ax.plot([2, 51], [5.8, 25.4], color="#1B2A4A", lw=2,
        label="Saldo medio condicional")
for x, media in zip(abonos, centros):
    saldos = media + 2.2 * desvios
    densidad_horizontal = x + 7 * np.exp(-0.5 * desvios**2)
    ax.vlines(x, saldos[0], saldos[-1], color="#5D6D7E", lw=1, linestyles="dashed")
    ax.fill_betweenx(saldos, x, densidad_horizontal, color="#D4EBE8", zorder=2)
    ax.plot(densidad_horizontal, saldos, color="#007279", lw=2)
    ax.scatter(x, media, color="#1B2A4A", zorder=4)
ax.set(xlim=(2, 51), ylim=(0, 30), xticks=abonos,
       xlabel="Abonos del mes (miles de MXN)", ylabel="Saldo promedio\n(miles de MXN)")
ax.legend(loc="upper left", frameon=False)
fig.tight_layout()
fig.savefig(ASSETS / "supuestos-regresion-python.svg", metadata={"Date": None})
plt.close(fig)

# Seis saldos por nivel ajustado. El centro y la amplitud cambian por separado.
niveles = np.arange(8, 27, 3)
perfil = ((niveles - niveles.mean()) / 9) ** 2
centro_curvo = 5.4 * (perfil - perfil.mean())
abanico = np.linspace(0.5, 4.1, len(niveles))
desvios_relativos = np.array([-1, -0.6, -0.25, 0.25, 0.6, 1])
fig, ejes = plt.subplots(1, 2, figsize=(11.5, 3.5), sharey=True)
for eje, nombre, centros, amplitudes in (
    (ejes[0], "Cartera A", centro_curvo, np.ones_like(niveles)),
    (ejes[1], "Cartera B", np.zeros_like(niveles), abanico),
):
    residuos = centros[:, None] + amplitudes[:, None] * desvios_relativos
    eje.axhline(0, linestyle="--", color="#667788", linewidth=1)
    eje.scatter(np.repeat(niveles, len(desvios_relativos)), residuos.ravel(),
                c="#007279", s=23, zorder=3)
    eje.plot(niveles, centros, color="#A05A00", marker="D", markersize=5, linewidth=1.6)
    eje.set(title=nombre, xlabel="Saldo ajustado (miles de MXN)",
            xlim=(6, 28), ylim=(-5, 5), xticks=niveles[::2], yticks=[-4, -2, 0, 2, 4])
ejes[0].set_ylabel("Residuo (miles de MXN)")
fig.tight_layout()
fig.savefig(ASSETS / "lectura-residuos-python.svg", metadata={"Date": None})
plt.close(fig)

figuras = ("saldos-python.svg", "abonos-python.svg", "colas-python.svg",
           "supuestos-regresion-python.svg", "dispersion-anova-python.svg", "lectura-residuos-python.svg")
for nombre in figuras:
    archivo = ASSETS / nombre
    contenido = archivo.read_text(encoding="utf-8")
    archivo.write_text("\n".join(linea.rstrip() for linea in contenido.splitlines()) + "\n", encoding="utf-8")
print("Figuras Python en assets/:", ", ".join(figuras))

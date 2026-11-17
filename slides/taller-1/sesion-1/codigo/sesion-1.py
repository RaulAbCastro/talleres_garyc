# Taller 1 / Sesión 1: De la muestra a la inferencia
# Generado desde index.qmd por exportar_codigo.py; edita el QMD.
# Ejecutar desde slides/taller-1/sesion-1/. Datos sintéticos.

#| exercise: explorar-py
import pandas as pd
d = pd.read_csv("datos/muestra.csv")
cols = ["id_cliente", "recibe_nomina", "abonos_miles",
        "saldo_promedio_miles", "n_entradas", "n_salidas"]
print(d[cols].head(4).to_string(index=False))
print("Clientes:", len(d))
print(d.recibe_nomina.value_counts().sort_index())
print(d.groupby("recibe_nomina")["saldo_promedio_miles"].mean())


#| exercise: muestreo-py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
pob = pd.read_csv("datos/poblacion_saldos.csv").saldo_promedio_miles.to_numpy()
rng = np.random.default_rng(42)
n = 40  # prueba 200; debe ser menor que len(pob)
medias = [rng.choice(pob, n, replace=False).mean() for _ in range(300)]
print(f"DE de medias: {np.std(medias, ddof=1):.3f} miles de MXN")
fig, ax = plt.subplots(figsize=(9, 3.2))
ax.hist(medias, bins=20, color="#007279", edgecolor="white")
ax.axvline(pob.mean(), color="#B26A00", linewidth=3)
ax.set(xlim=(10, 16), xlabel="Media del saldo (miles de MXN)", ylabel="Frecuencia")
fig.tight_layout()
plt.show()


#| exercise: medias-py
import pandas as pd
from scipy import stats
d = pd.read_csv("datos/muestra.csv")
y1 = d.loc[d.recibe_nomina == 1, "saldo_promedio_miles"]
y0 = d.loc[d.recibe_nomina == 0, "saldo_promedio_miles"]
prueba = stats.ttest_ind(y1, y0, equal_var=False, alternative="two-sided")
ic = prueba.confidence_interval(confidence_level=0.95)
print(f"Diferencia (miles de MXN): {y1.mean() - y0.mean():.4f}")
print(f"IC 95%: [{ic.low:.4f}, {ic.high:.4f}]")
print(f"p bilateral: {prueba.pvalue:.4g}")


#| exercise: proporciones-py
import numpy as np
import pandas as pd
from scipy import stats
d = pd.read_csv("datos/muestra.csv")
a = d.loc[d.recibe_nomina == 1, "pago_debito"]
b = d.loc[d.recibe_nomina == 0, "pago_debito"]
p1, p0, n1, n0 = a.mean(), b.mean(), len(a), len(b)
dif = p1 - p0
se = np.sqrt(p1*(1-p1)/n1 + p0*(1-p0)/n0)
ic = dif + np.array([-1, 1]) * stats.norm.ppf(.975) * se
pool = (a.sum() + b.sum()) / (n1 + n0)
z = dif / np.sqrt(pool*(1-pool)*(1/n1 + 1/n0))
print(f"Proporciones (nómina 1, 0): {p1:.4f}, {p0:.4f}")
print(f"Diferencia: {100*dif:.2f} pp; IC: {100*ic}")
print(f"p bilateral: {2*stats.norm.sf(abs(z)):.4g}")


#| exercise: correlacion-py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
d = pd.read_csv("datos/muestra.csv")
print("r de Pearson:", d.abonos_miles.corr(d.saldo_promedio_miles))
fig, ax = plt.subplots(figsize=(9, 3.2))
colores = np.where(d.recibe_nomina == 1, "#007279", "#9BA5B7")
ax.scatter(d.abonos_miles, d.saldo_promedio_miles, c=colores, alpha=.6, s=14)
ax.set(xlabel="Abonos del mes (miles de MXN)", ylabel="Saldo promedio (miles de MXN)")
fig.tight_layout()
plt.show()


#| exercise: regresion-py
import pandas as pd
import numpy as np
from scipy import stats
d = pd.read_csv("datos/muestra.csv")
modelo = stats.linregress(d.abonos_miles, d.saldo_promedio_miles)
ic = modelo.slope + np.array([-1, 1]) * stats.t.ppf(.975, len(d)-2) * modelo.stderr
print(f"Intercepto: {modelo.intercept:.4f}; pendiente: {modelo.slope:.4f}")
print(f"IC 95% de la pendiente: {ic}")
print(f"p bilateral: {modelo.pvalue:.4g}")
print(f"R cuadrada: {modelo.rvalue**2:.4f}")
ajustado = modelo.intercept + modelo.slope * d.abonos_miles
print(pd.DataFrame({"observado": d.saldo_promedio_miles,
                    "ajustado": ajustado,
                    "residuo": d.saldo_promedio_miles - ajustado}).head(3))

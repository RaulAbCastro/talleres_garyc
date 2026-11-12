#!/usr/bin/env python3
"""Datos sintéticos de Marginalia para Taller 1, sesión 1.

Esta población DIDÁCTICA contiene 12 000 clientes con crédito activo elegibles
para un piloto ficticio del Agente Ciudadano en Capital y Valle, 2031 T1.
La elección de regiones, población y todos los parámetros son supuestos del
ejercicio, no cifras del caso.tex ni estimaciones sobre un país real.

Se observa adopción voluntaria, no asignación aleatoria del uso. La
sofisticación financiera latente afecta ingreso, adopción y tasa. El Agente
reduce la tasa anual de cada persona exactamente 1.5 puntos porcentuales.
La diferencia observada entre usuarios y no usuarios combina ese efecto
con selección. Se generan también resultados potenciales de cambio de banco.
No se modela dependencia entre personas, impago, cumplimiento de invitaciones
ni respuestas estratégicas de bancos. La tasa es una medición por persona.

La muestra es aleatoria simple sin reemplazo: n=480 de N=12 000. Las pruebas
y los intervalos habituales usan la aproximación de observaciones
independientes y no aplican corrección por población finita (fracción 4%).

Salida para participantes: datos/muestra.csv (solo variables observadas) y
datos/poblacion_tasas.csv (una tasa por persona, para simular muestreo).
Salida docente: docente/poblacion.csv (incluye latente y potenciales) y
docente/resumen.json (resultados esperados y supuestos). Ninguna salida
docente debe cargarse en el HTML de las diapositivas.

Ejecutar con .venv/bin/python slides/taller-1/sesion-1/generar_datos.py.
Las rutas se resuelven desde este archivo y se usa una semilla fija.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from scipy.special import expit


SEMILLA = 203101
N_POBLACION = 12_000
N_MUESTRA = 480
EFECTO_TASA_PP = -1.5
BASE = Path(__file__).resolve().parent
OBSERVADAS = [
    "id_persona", "region", "edad", "ingreso_miles", "usa_agente",
    "tasa_anual", "cambio_banco",
]


def resumen_grupo(grupo: pd.DataFrame) -> dict:
    """Resumen de tasas y cambios para un grupo de adopción."""
    return {
        "n": int(len(grupo)),
        "media_tasa": float(grupo.tasa_anual.mean()),
        "desviacion_tasa": float(grupo.tasa_anual.std(ddof=1)),
        "cambios_banco": int(grupo.cambio_banco.sum()),
        "proporcion_cambio": float(grupo.cambio_banco.mean()),
        "ingreso_medio_miles": float(grupo.ingreso_miles.mean()),
    }


def generar() -> dict:
    rng = np.random.default_rng(SEMILLA)
    sofisticacion = rng.normal(size=N_POBLACION)
    region = rng.choice(["Capital", "Valle"], N_POBLACION, p=[0.55, 0.45])
    valle = (region == "Valle").astype(int)
    edad = rng.integers(21, 66, size=N_POBLACION)
    ingreso = np.round(np.exp(3.0 + 0.25 * sofisticacion
                             + rng.normal(0, 0.30, N_POBLACION)), 3)
    p_uso = expit(-0.25 + 0.95 * sofisticacion - 0.10 * valle)
    usa = (rng.random(N_POBLACION) < p_uso).astype(int)
    tasa_0 = np.round(np.clip(
        24.0 - 0.12 * ingreso - 1.80 * sofisticacion + 0.60 * valle
        + rng.normal(0, 2.20, N_POBLACION), 5.0, 45.0,
    ), 4)
    tasa_1 = np.round(tasa_0 + EFECTO_TASA_PP, 4)
    tasa = np.where(usa == 1, tasa_1, tasa_0)
    u_cambio = rng.random(N_POBLACION)
    cambio_0 = (u_cambio < expit(-2.1 + 0.20 * sofisticacion)).astype(int)
    cambio_1 = (u_cambio < expit(-1.1 + 0.20 * sofisticacion)).astype(int)
    cambio = np.where(usa == 1, cambio_1, cambio_0)

    poblacion = pd.DataFrame({
        "id_persona": np.arange(1, N_POBLACION + 1),
        "region": region, "edad": edad, "ingreso_miles": ingreso,
        "usa_agente": usa, "tasa_anual": tasa, "cambio_banco": cambio,
        "sofisticacion_latente": sofisticacion,
        "probabilidad_uso": p_uso,
        "tasa_sin_agente": tasa_0, "tasa_con_agente": tasa_1,
        "cambio_sin_agente": cambio_0, "cambio_con_agente": cambio_1,
    })
    indices = rng.choice(N_POBLACION, N_MUESTRA, replace=False)
    muestra = poblacion.iloc[indices][OBSERVADAS].sort_values("id_persona")

    assert len(poblacion) == N_POBLACION
    assert len(muestra) == N_MUESTRA and muestra.id_persona.is_unique
    assert not poblacion.isna().any().any()
    assert set(muestra.region) == {"Capital", "Valle"}
    assert poblacion.tasa_anual.between(3.5, 45).all()
    assert poblacion.ingreso_miles.gt(0).all()
    assert np.allclose(tasa_1 - tasa_0, EFECTO_TASA_PP, atol=1e-12)
    assert np.array_equal(tasa, np.where(usa == 1, tasa_1, tasa_0))
    assert set(muestra.usa_agente) == set(muestra.cambio_banco) == {0, 1}
    assert not set(OBSERVADAS) & {"sofisticacion_latente", "tasa_sin_agente",
                                  "tasa_con_agente", "probabilidad_uso"}

    (BASE / "datos").mkdir(exist_ok=True)
    (BASE / "docente").mkdir(exist_ok=True)
    muestra.to_csv(BASE / "datos/muestra.csv", index=False)
    poblacion[["tasa_anual"]].to_csv(BASE / "datos/poblacion_tasas.csv", index=False)
    poblacion.to_csv(BASE / "docente/poblacion.csv", index=False)
    # Los resultados esperados se calculan sobre el CSV realmente distribuido.
    muestra = pd.read_csv(BASE / "datos/muestra.csv")
    g0 = muestra.loc[muestra.usa_agente == 0]
    g1 = muestra.loc[muestra.usa_agente == 1]
    n0, n1 = len(g0), len(g1)
    s0, s1 = resumen_grupo(g0), resumen_grupo(g1)
    diferencia = s1["media_tasa"] - s0["media_tasa"]
    v0 = g0.tasa_anual.var(ddof=1) / n0
    v1 = g1.tasa_anual.var(ddof=1) / n1
    ee = np.sqrt(v0 + v1)
    gl = (v0 + v1) ** 2 / (v0**2 / (n0 - 1) + v1**2 / (n1 - 1))
    critico_t = stats.t.ppf(0.975, gl)
    welch = stats.ttest_ind(g1.tasa_anual, g0.tasa_anual, equal_var=False)
    assert np.isclose(welch.statistic, diferencia / ee)

    p0, p1 = s0["proporcion_cambio"], s1["proporcion_cambio"]
    diferencia_p = p1 - p0
    p_agrupada = muestra.cambio_banco.mean()
    ee_h0 = np.sqrt(p_agrupada * (1 - p_agrupada) * (1/n1 + 1/n0))
    ee_p = np.sqrt(p1 * (1-p1) / n1 + p0 * (1-p0) / n0)
    critico_z = stats.norm.ppf(0.975)
    z = diferencia_p / ee_h0
    # La aproximación normal de proporciones es adecuada para este ejercicio.
    assert min(g0.cambio_banco.sum(), n0-g0.cambio_banco.sum(),
               g1.cambio_banco.sum(), n1-g1.cambio_banco.sum()) >= 10
    correlacion = stats.pearsonr(muestra.ingreso_miles, muestra.tasa_anual)
    regresion = stats.linregress(muestra.ingreso_miles, muestra.tasa_anual)
    critico_reg = stats.t.ppf(0.975, N_MUESTRA - 2)
    diferencia_pob = (poblacion.loc[usa == 1, "tasa_anual"].mean()
                      - poblacion.loc[usa == 0, "tasa_anual"].mean())
    seleccion_pob = (poblacion.loc[usa == 1, "tasa_sin_agente"].mean()
                    - poblacion.loc[usa == 0, "tasa_sin_agente"].mean())
    assert np.isclose(diferencia_pob, EFECTO_TASA_PP + seleccion_pob)

    resumen = {
        "diseno": {
            "semilla": SEMILLA, "N": N_POBLACION, "n": N_MUESTRA,
            "periodo": "2031 T1", "regiones": ["Capital", "Valle"],
            "poblacion_objetivo": "Clientes ficticios con crédito activo elegibles para el piloto en Capital y Valle",
            "muestreo": "Aleatorio simple sin reemplazo; no representa a todo Marginalia",
            "asignacion": "Adopción voluntaria endógena a sofisticación financiera latente",
            "unidades_tasa": "Porcentaje anual; diferencias en puntos porcentuales",
            "unidades_ingreso": "Miles de áureos por mes",
            "inferencia": "Bilateral al 5%; aproximación independiente; sin corrección por población finita",
            "origen": "Simulación pedagógica; parámetros y regiones del piloto son supuestos añadidos",
        },
        "poblacion": {
            "media_tasa_observada": float(poblacion.tasa_anual.mean()),
            "desviacion_tasa_observada": float(poblacion.tasa_anual.std(ddof=0)),
            "proporcion_uso": float(poblacion.usa_agente.mean()),
            "efecto_causal_tasa_pp": EFECTO_TASA_PP,
            "diferencia_observada_tasa_pp": float(diferencia_pob),
            "sesgo_seleccion_tasa_pp": float(seleccion_pob),
        },
        "muestra": {
            "media_tasa": float(muestra.tasa_anual.mean()),
            "desviacion_tasa": float(muestra.tasa_anual.std(ddof=1)),
            "ee_media_sin_correccion_finita": float(muestra.tasa_anual.std(ddof=1) / np.sqrt(N_MUESTRA)),
            "sin_agente": s0, "con_agente": s1,
        },
        "welch": {
            "contraste": "Media con agente menos media sin agente",
            "diferencia_pp": float(diferencia), "ee_pp": float(ee),
            "gl": float(gl), "t": float(welch.statistic),
            "p_bilateral": float(welch.pvalue),
            "ic95_pp": [float(diferencia - critico_t*ee), float(diferencia + critico_t*ee)],
        },
        "proporciones": {
            "contraste": "Cambio de banco: con agente menos sin agente",
            "p_sin_agente": p0, "p_con_agente": p1,
            "diferencia": float(diferencia_p), "diferencia_pp": float(100*diferencia_p),
            "ee_h0_agrupado": float(ee_h0), "z": float(z),
            "p_bilateral": float(2 * stats.norm.sf(abs(z))),
            "metodo_prueba": "z de dos proporciones, H0 agrupada, sin corrección de continuidad",
            "ee_ic_no_agrupado": float(ee_p),
            "ic95": [float(diferencia_p-critico_z*ee_p), float(diferencia_p+critico_z*ee_p)],
            "metodo_ic": "Wald no agrupado, sin corrección de continuidad; equivale a prop.test de dos proporciones con correct=FALSE",
        },
        "correlacion": {
            "variables": ["ingreso_miles", "tasa_anual"],
            "r_pearson": float(correlacion.statistic),
            "p_bilateral": float(correlacion.pvalue),
        },
        "regresion": {
            "formula": "tasa_anual ~ ingreso_miles",
            "intercepto": float(regresion.intercept),
            "pendiente": float(regresion.slope),
            "ee_pendiente": float(regresion.stderr),
            "gl": N_MUESTRA - 2,
            "t": float(regresion.slope / regresion.stderr),
            "p_bilateral": float(regresion.pvalue),
            "ic95_pendiente": [float(regresion.slope-critico_reg*regresion.stderr),
                               float(regresion.slope+critico_reg*regresion.stderr)],
            "r2": float(regresion.rvalue**2),
            "inferencia": "OLS convencional homocedástica; interpretación descriptiva",
        },
        "sha256_muestra_csv": hashlib.sha256((BASE / "datos/muestra.csv").read_bytes()).hexdigest(),
    }
    with (BASE / "docente/resumen.json").open("w", encoding="utf-8") as archivo:
        json.dump(resumen, archivo, ensure_ascii=False, indent=2, allow_nan=False)
        archivo.write("\n")
    return resumen


if __name__ == "__main__":
    resultado = generar()
    print(json.dumps(resultado, ensure_ascii=False, indent=2))

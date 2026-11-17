#!/usr/bin/env python3
"""Cuentas de depósito a la vista: agregados sintéticos de septiembre de 2026.

Marco didáctico: 12 000 clientes con cuenta de depósito a la vista y tarjeta de
débito; una cuenta por cliente y muestra aleatoria simple de 480, sin reemplazo.
Una fila es un cliente con su cuenta observado durante un único mes.
No representa a una institución ni
al sistema financiero mexicano. Los montos se expresan en miles de pesos MXN;
los conteos son operaciones durante el mes, no montos ni tasas. Se distinguen
entradas y salidas por tipo/canal; el catálogo es didáctico, no exhaustivo.
No se modelan crédito ni un libro de movimientos conciliado. El saldo promedio
no se obtiene restando conteos, ni equivale al saldo final del mes.

La estabilidad de ingresos latente se relaciona con recibir nómina, los abonos
y el saldo. Se genera saldo = 6 + 0.30*abonos + 3*estabilidad + ruido. No se
simula una intervención ni se identifica un efecto de recibir nómina. El error
estructural incluye estabilidad y por ello no tiene media condicional cero
dado abonos. Una recta estimada sigue siendo un resumen descriptivo útil.

Participantes: datos/muestra.csv y datos/poblacion_saldos.csv. Docente:
poblacion.csv con estabilidad/error latentes, resumen.json y guía. No se modela
dependencia entre clientes, entre bancos ni un panel. La inferencia introductoria
usa independencia aproximada y omite corrección por población finita (4%).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from scipy.special import expit

BASE = Path(__file__).resolve().parent
SEMILLA = 202609
N_POBLACION = 12_000
N_MUESTRA = 480
SEMILLAS = {"poblacion": SEMILLA, "muestra": SEMILLA + 1, "actividad": SEMILLA + 2}
ENTRADAS = {
    "n_spei_entrada": "Número de transferencias SPEI recibidas durante el mes",
    "n_abonos_ventanilla": "Número de depósitos en ventanilla durante el mes",
    "n_abonos_cajero": "Número de depósitos en cajeros receptores durante el mes",
    "n_abonos_comisionista": "Número de depósitos por comisionistas durante el mes",
    "n_otros_abonos": "Número de otros abonos; incluye traspasos internos",
}
SALIDAS = {
    "n_spei_salida": "Número de transferencias SPEI enviadas durante el mes",
    "n_pagos_debito": "Número de pagos con la tarjeta de débito asociada a la cuenta",
    "n_retiros_cajero": "Número de retiros de efectivo en cajero durante el mes",
    "n_retiros_ventanilla": "Número de retiros de efectivo en ventanilla durante el mes",
    "n_retiros_comisionista": "Número de retiros de efectivo por comisionistas durante el mes",
    "n_otros_cargos": "Número de otros cargos; p. ej., domiciliaciones, comisiones y traspasos internos",
}
OBSERVADAS = ["id_cliente", "recibe_nomina", "abonos_miles",
              "saldo_promedio_miles", "pago_debito", "n_entradas", "n_salidas",
              *ENTRADAS, *SALIDAS]


def resumen_grupo(g: pd.DataFrame) -> dict:
    return {
        "n": int(len(g)),
        "media_saldo": float(g.saldo_promedio_miles.mean()),
        "desviacion_saldo": float(g.saldo_promedio_miles.std(ddof=1)),
        "media_abonos": float(g.abonos_miles.mean()),
        "clientes_pago_debito": int(g.pago_debito.sum()),
        "proporcion_pago_debito": float(g.pago_debito.mean()),
    }


def generar() -> dict:
    # Flujos separados: añadir canales no debe volver a seleccionar la muestra.
    rng = np.random.default_rng(SEMILLAS["poblacion"])
    rng_muestra = np.random.default_rng(SEMILLAS["muestra"])
    rng_actividad = np.random.default_rng(SEMILLAS["actividad"])
    estabilidad = rng.uniform(-1, 1, N_POBLACION)
    nomina = (rng.random(N_POBLACION) < expit(.2 + 1.6*estabilidad)).astype(int)
    abonos = np.round(np.exp(3.1 + .4*estabilidad + rng.normal(0, .35, N_POBLACION)), 3)
    ruido = rng.uniform(-3, 3, N_POBLACION)
    error = 3*estabilidad + ruido
    saldo = np.round(6 + .3*abonos + error, 4)
    # Nómina clasifica el origen del abono, no un canal adicional. En esta
    # receta se asigna a SPEI o a un traspaso interno, sin contarlo dos veces.
    # El 65% es una decisión de simulación; no una proporción observada en México.
    nomina_spei = ((nomina == 1) & (rng_actividad.random(N_POBLACION) < .65)).astype(int)
    entradas = {
        "n_spei_entrada": rng_actividad.poisson(np.exp(.2 + .2*estabilidad + .15*np.log(abonos))) + nomina_spei,
        "n_abonos_ventanilla": rng_actividad.poisson(.25*np.exp(-.2*estabilidad)),
        "n_abonos_cajero": rng_actividad.poisson(.45*np.exp(.1*estabilidad)),
        "n_abonos_comisionista": rng_actividad.poisson(.6*np.exp(-.3*estabilidad)),
        "n_otros_abonos": rng_actividad.poisson(.3, N_POBLACION) + nomina - nomina_spei,
    }
    # Todos los abonos monetarios generados son positivos: al menos una entrada.
    entradas["n_otros_abonos"] += (np.sum(list(entradas.values()), axis=0) == 0).astype(int)
    activo = rng_actividad.random(N_POBLACION) < expit(.2 + 1.2*nomina + .4*estabilidad)
    debito = np.where(activo, 1+rng_actividad.poisson(5, N_POBLACION), 0)
    pago = (debito > 0).astype(int)
    salidas = {
        "n_spei_salida": rng_actividad.poisson(np.exp(1 + .3*estabilidad + .15*np.log(abonos))),
        "n_pagos_debito": debito,
        "n_retiros_cajero": rng_actividad.poisson(1.5*np.exp(-.15*estabilidad)),
        "n_retiros_ventanilla": rng_actividad.poisson(.12*np.exp(-.4*estabilidad)),
        "n_retiros_comisionista": rng_actividad.poisson(.6*np.exp(-.3*estabilidad)),
        "n_otros_cargos": rng_actividad.poisson(.5, N_POBLACION),
    }
    poblacion = pd.DataFrame({
        "id_cliente": np.arange(1, N_POBLACION+1), "recibe_nomina": nomina,
        "abonos_miles": abonos, "saldo_promedio_miles": saldo,
        "pago_debito": pago, "n_entradas": np.sum(list(entradas.values()), axis=0),
        "n_salidas": np.sum(list(salidas.values()), axis=0), **entradas, **salidas,
        "estabilidad_ingreso": estabilidad, "ruido_saldo": ruido,
        "error_estructural_saldo": error,
    })
    muestra = poblacion.iloc[rng_muestra.choice(N_POBLACION, N_MUESTRA, replace=False)][OBSERVADAS]
    muestra = muestra.sort_values("id_cliente")
    assert len(muestra) == N_MUESTRA and muestra.id_cliente.is_unique
    assert len(poblacion) == N_POBLACION and poblacion.id_cliente.is_unique
    assert not poblacion.isna().any().any()
    assert poblacion.abonos_miles.gt(0).all() and poblacion.saldo_promedio_miles.gt(0).all()
    for col in [*ENTRADAS, *SALIDAS, "n_entradas", "n_salidas"]:
        assert (poblacion[col] >= 0).all() and (poblacion[col] % 1 == 0).all()
    assert np.array_equal(pago, (poblacion.n_pagos_debito > 0).astype(int))
    assert poblacion.n_entradas.eq(poblacion[list(ENTRADAS)].sum(axis=1)).all()
    assert poblacion.n_salidas.eq(poblacion[list(SALIDAS)].sum(axis=1)).all()
    assert poblacion.n_entradas.ge(1).all()
    assert (poblacion.n_spei_entrada + poblacion.n_otros_abonos >= nomina).all()
    assert np.allclose(saldo, 6+.3*abonos+error, atol=.000051)
    assert set(muestra.recibe_nomina) == set(muestra.pago_debito) == {0, 1}
    assert not set(OBSERVADAS) & {"estabilidad_ingreso", "error_estructural_saldo", "ruido_saldo"}

    (BASE/"datos").mkdir(exist_ok=True)
    (BASE/"docente").mkdir(exist_ok=True)
    muestra.to_csv(BASE/"datos/muestra.csv", index=False)
    poblacion[["saldo_promedio_miles"]].to_csv(BASE/"datos/poblacion_saldos.csv", index=False)
    poblacion.to_csv(BASE/"docente/poblacion.csv", index=False)
    muestra = pd.read_csv(BASE/"datos/muestra.csv")
    g0 = muestra.loc[muestra.recibe_nomina == 0]
    g1 = muestra.loc[muestra.recibe_nomina == 1]
    n0, n1 = len(g0), len(g1)
    s0, s1 = resumen_grupo(g0), resumen_grupo(g1)
    welch = stats.ttest_ind(g1.saldo_promedio_miles, g0.saldo_promedio_miles, equal_var=False)
    ci = welch.confidence_interval(.95)
    diferencia = s1["media_saldo"]-s0["media_saldo"]
    v0 = g0.saldo_promedio_miles.var(ddof=1)/n0
    v1 = g1.saldo_promedio_miles.var(ddof=1)/n1
    ee = np.sqrt(v0+v1)
    assert np.isclose(welch.statistic, diferencia/ee)
    p0, p1 = s0["proporcion_pago_debito"], s1["proporcion_pago_debito"]
    difp = p1-p0
    pool = muestra.pago_debito.mean()
    se_h0 = np.sqrt(pool*(1-pool)*(1/n1+1/n0))
    se_ic = np.sqrt(p1*(1-p1)/n1+p0*(1-p0)/n0)
    z = difp/se_h0
    zcrit = stats.norm.ppf(.975)
    assert min(g0.pago_debito.sum(), n0-g0.pago_debito.sum(),
               g1.pago_debito.sum(), n1-g1.pago_debito.sum()) >= 10
    corr = stats.pearsonr(muestra.abonos_miles, muestra.saldo_promedio_miles)
    reg = stats.linregress(muestra.abonos_miles, muestra.saldo_promedio_miles)
    crit = stats.t.ppf(.975, N_MUESTRA-2)
    residuos = muestra.saldo_promedio_miles-(reg.intercept+reg.slope*muestra.abonos_miles)
    assert abs(residuos.sum()) < 1e-8
    resumen = {
        "diseno": {
            "semilla": SEMILLA, "semillas": SEMILLAS, "N": N_POBLACION, "n": N_MUESTRA,
            "periodo": "2026-09", "grano": "Una cuenta de depósito a la vista por cliente, en un único mes (corte transversal)",
            "alcance": "Débito y movimientos de la cuenta; sin crédito ni libro diario conciliado",
            "canales": "Catálogo didáctico de entradas y salidas, con categorías residuales; no exhaustivo",
            "poblacion_objetivo": "Marco didáctico de clientes con cuenta de depósito a la vista y tarjeta de débito",
            "muestreo": "Aleatorio simple sin reemplazo; no representa a una institución ni al sistema financiero",
            "comparacion": "Recibe nómina=1 menos recibe nómina=0; grupos observados, sin asignación aleatoria",
            "unidades_montos": "Miles de pesos mexicanos (MXN)",
            "unidades_conteos": "Número de operaciones durante septiembre de 2026",
            "inferencia": "Bilateral al 5%; independencia aproximada; sin corrección por población finita",
            "origen": "Datos enteramente sintéticos; sin calibración a estadísticas observadas",
        },
        "diccionario": {
            "id_cliente": "Identificador sintético único, sin datos personales reales",
            "recibe_nomina": "1 si recibió un abono identificado como nómina durante el mes, 0 si no",
            "abonos_miles": "Suma de abonos durante el mes, de cualquier canal, en miles de MXN",
            "saldo_promedio_miles": "Saldo promedio del mes en la cuenta de depósito, en miles de MXN",
            "pago_debito": "1 si n_pagos_debito > 0, 0 en otro caso; no incluye retiros",
            "n_entradas": "Suma de los conteos de entradas por canal durante el mes",
            "n_salidas": "Suma de los conteos de salidas por tipo/canal durante el mes",
            **ENTRADAS, **SALIDAS,
        },
        "poblacion": {
            "media_saldo": float(poblacion.saldo_promedio_miles.mean()),
            "desviacion_saldo": float(poblacion.saldo_promedio_miles.std(ddof=0)),
            "proporcion_nomina": float(poblacion.recibe_nomina.mean()),
            "ecuacion_saldo": "saldo = 6 + 0.30*abonos + 3*estabilidad_ingreso + ruido_saldo (redondeado a 4 decimales)",
            "interpretacion": "Receta de simulación; no identifica efecto causal de recibir nómina",
        },
        "muestra": {
            "media_saldo": float(muestra.saldo_promedio_miles.mean()),
            "desviacion_saldo": float(muestra.saldo_promedio_miles.std(ddof=1)),
            "ee_media_sin_correccion_finita": float(muestra.saldo_promedio_miles.std(ddof=1)/np.sqrt(N_MUESTRA)),
            "sin_nomina": s0, "con_nomina": s1,
            "rango_abonos_miles": [float(muestra.abonos_miles.min()), float(muestra.abonos_miles.max())],
            "rango_saldo_miles": [float(muestra.saldo_promedio_miles.min()), float(muestra.saldo_promedio_miles.max())],
        },
        "welch": {"contraste": "Saldo con nómina menos saldo sin nómina",
                  "diferencia_miles": float(diferencia), "ee_miles": float(ee), "gl": float(welch.df),
                  "t": float(welch.statistic), "p_bilateral": float(welch.pvalue),
                  "ic95_miles": [float(ci.low), float(ci.high)]},
        "proporciones": {"contraste": "Pago con débito: con nómina menos sin nómina",
                         "p_sin_nomina": p0, "p_con_nomina": p1,
                         "diferencia": float(difp), "diferencia_pp": float(100*difp),
                         "ee_h0_agrupado": float(se_h0), "z": float(z),
                         "p_bilateral": float(2*stats.norm.sf(abs(z))),
                         "ee_ic_no_agrupado": float(se_ic),
                         "ic95": [float(difp-zcrit*se_ic), float(difp+zcrit*se_ic)],
                         "metodo_prueba": "z agrupada bilateral sin corrección de continuidad",
                         "metodo_ic": "Wald no agrupado"},
        "correlacion": {"variables": ["abonos_miles", "saldo_promedio_miles"],
                        "r_pearson": float(corr.statistic), "p_bilateral": float(corr.pvalue)},
        "regresion": {"formula": "saldo_promedio_miles ~ abonos_miles",
                      "intercepto": float(reg.intercept), "pendiente": float(reg.slope),
                      "ee_pendiente": float(reg.stderr), "gl": N_MUESTRA-2,
                      "p_bilateral": float(reg.pvalue), "r2": float(reg.rvalue**2),
                      "ic95_pendiente": [float(reg.slope-crit*reg.stderr), float(reg.slope+crit*reg.stderr)],
                      "suma_cuadrados_residuos": float(np.sum(residuos**2)),
                      "inferencia": "OLS convencional homocedástica como repaso; interpretación descriptiva"},
        "sha256_muestra_csv": hashlib.sha256((BASE/"datos/muestra.csv").read_bytes()).hexdigest(),
    }
    (BASE/"docente/resumen.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    return resumen


if __name__ == "__main__":
    print(json.dumps(generar(), ensure_ascii=False, indent=2))

"""
Generador de datos sintéticos para Sesión 2: Resultados Potenciales y Sesgo de Selección
Población: Clientes de tarjeta de crédito
Variables: Intereses pagados, recepción de estado de cuenta estandarizado (ECE)
"""

import numpy as np
import pandas as pd
from pathlib import Path

# Configuración
N_POBLACION = 500
N_MUESTRA = 100
SEMILLA_POBLACION = 202609
SEMILLA_MUESTRA = 202610

np.random.seed(SEMILLA_POBLACION)

# Generar población
print("Generando población sintética...")

# Atención financiera (latente, 0 a 100)
atencion = np.random.gamma(shape=2, scale=20, size=N_POBLACION)
atencion = np.clip(atencion, 0, 100)

# Intereses sin ECE (Y0): dependen de atención + ruido
Y0 = 300 - 2 * atencion + np.random.normal(0, 20, N_POBLACION)
Y0 = np.clip(Y0, 0, 500)

# Efecto del ECE: mayor para quienes menos atentos (todos se benefician, pero más los despistados)
efecto = -0.5 * (100 - atencion) + np.random.normal(0, 5, N_POBLACION)
Y1 = Y0 + efecto
Y1 = np.clip(Y1, 0, 500)

# Decisión de pedir ECE (opcional): más probable si atento, pero con ruido
prob_pedir = 0.1 + 0.008 * atencion  # Va de 10% a 90%
D = np.random.binomial(1, prob_pedir)

# Crear dataframe de población
poblacion = pd.DataFrame({
    'id_cliente': np.arange(1, N_POBLACION + 1),
    'atencion': atencion,
    'Y0_sin_ECE': Y0,
    'Y1_con_ECE': Y1,
    'efecto_individual': efecto,
    'D_pide_ECE': D,
    'Y_observado': np.where(D == 1, Y1, Y0)
})

# Guardar población (con latentes, solo para validación)
Path('docente').mkdir(exist_ok=True)
poblacion.to_csv('docente/poblacion_potencial.csv', index=False)
print(f"  Población guardada: {N_POBLACION} clientes")

# Muestreo aleatorio sin reemplazo
np.random.seed(SEMILLA_MUESTRA)
indices_muestra = np.random.choice(N_POBLACION, N_MUESTRA, replace=False)
muestra = poblacion.iloc[indices_muestra][['id_cliente', 'Y_observado', 'D_pide_ECE']].reset_index(drop=True)
muestra.columns = ['id_cliente', 'intereses', 'recibio_ece']

# Verificaciones
print(f"\nMuestra generada: {N_MUESTRA} clientes")
print(f"Proporción que pidió ECE: {muestra['recibio_ece'].mean():.1%}")
print(f"Intereses promedio: {muestra['intereses'].mean():.2f} pesos")

# Estadísticas por grupo
print("\nEstadísticas por grupo (observadas):")
for grupo in [0, 1]:
    subset = muestra[muestra['recibio_ece'] == grupo]['intereses']
    label = "Con ECE" if grupo == 1 else "Sin ECE"
    print(f"  {label}: media={subset.mean():.2f}, DE={subset.std():.2f}, n={len(subset)}")

# Guardar muestra
Path('datos').mkdir(exist_ok=True)
muestra.to_csv('datos/muestra.csv', index=False)
print(f"\nMuestra guardada en datos/muestra.csv")

# Crear resumen para docentes
resumen = {
    'ATE_verdadero': poblacion['efecto_individual'].mean(),
    'ATT_verdadero': poblacion[poblacion['D_pide_ECE'] == 1]['efecto_individual'].mean(),
    'Sesgo_seleccion': poblacion[poblacion['D_pide_ECE'] == 1]['Y0_sin_ECE'].mean() - 
                       poblacion[poblacion['D_pide_ECE'] == 0]['Y0_sin_ECE'].mean(),
}

print(f"\nParámetros de referencia (no compartir con participantes):")
print(f"  ATE (efecto en todos): {resumen['ATE_verdadero']:.2f} pesos")
print(f"  ATT (efecto en quienes pidieron): {resumen['ATT_verdadero']:.2f} pesos")
print(f"  Sesgo de selección: {resumen['Sesgo_seleccion']:.2f} pesos")

# Guardar para docentes
Path('docente').mkdir(exist_ok=True)
import json
with open('docente/parametros.json', 'w') as f:
    json.dump(resumen, f, indent=2)

print("\nSemillas utilizadas:")
print(f"  Población: {SEMILLA_POBLACION}")
print(f"  Muestra: {SEMILLA_MUESTRA}")
print("\nGeneración completada.")

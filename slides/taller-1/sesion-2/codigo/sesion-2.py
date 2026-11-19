"""
Sesión 2: Resultados Potenciales y Sesgo de Selección
Python · Laboratorio comparación de grupos
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Configurar estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Cargar datos
datos = pd.read_csv('datos/muestra.csv')
print("Primeras filas:")
print(datos.head())
print()

# Estadísticas descriptivas
print("Resumen de la muestra:")
print(f"N total: {len(datos)}")
print(f"Con ECE: {datos['recibio_ece'].sum()}")
print(f"Sin ECE: {(datos['recibio_ece'] == 0).sum()}")
print()

# Comparación de medias: diferencia observada
media_con = datos[datos['recibio_ece'] == 1]['intereses'].mean()
media_sin = datos[datos['recibio_ece'] == 0]['intereses'].mean()
diferencia = media_con - media_sin

print("Intereses promedio:")
print(f"  Con ECE: {media_con:.2f} pesos")
print(f"  Sin ECE: {media_sin:.2f} pesos")
print(f"  Diferencia (observada): {diferencia:.2f} pesos")
print()

# Prueba t de Welch (dos varianzas desiguales)
grupo_1 = datos[datos['recibio_ece'] == 1]['intereses']
grupo_0 = datos[datos['recibio_ece'] == 0]['intereses']

t_stat, p_valor = stats.ttest_ind(grupo_1, grupo_0, equal_var=False)
ic = stats.t.interval(0.95, 
                      len(grupo_1) + len(grupo_0) - 2,
                      loc=diferencia,
                      scale=np.sqrt(grupo_1.var()/len(grupo_1) + grupo_0.var()/len(grupo_0)))

print("Prueba t de Welch:")
print(f"Estadístico t: {t_stat:.4f}")
print(f"Valor p: {p_valor:.4f}")
print(f"IC 95%: [{ic[0]:.2f}, {ic[1]:.2f}]")
print()

# Visualizaciones
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Densidades
axes[0].hist(grupo_0, alpha=0.6, label='Sin ECE', bins=12, color='#1B2A4A', edgecolor='black')
axes[0].hist(grupo_1, alpha=0.6, label='Con ECE', bins=12, color='#007279', edgecolor='black')
axes[0].set_xlabel('Intereses (pesos)')
axes[0].set_ylabel('Frecuencia')
axes[0].set_title('Distribución de intereses por grupo')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Boxplot
datos['Grupo'] = datos['recibio_ece'].map({0: 'Sin ECE', 1: 'Con ECE'})
datos.boxplot(column='intereses', by='Grupo', ax=axes[1])
axes[1].set_xlabel('Grupo')
axes[1].set_ylabel('Intereses (pesos)')
axes[1].set_title('Distribución de intereses: Boxplot')
plt.suptitle('')  # Quitar el título automático

plt.tight_layout()
plt.show()

# Interpretación
print("\nInterpretación:")
print(f"La diferencia observada es de {diferencia:.2f} pesos.")
print("En la próxima sesión aprenderemos a:")
print("  - Descomponer esta diferencia en efecto verdadero y sesgo de selección")
print("  - Usar métodos para limpiar la comparación cuando hay autoselección")

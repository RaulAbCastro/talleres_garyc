* Sesión 2: Resultados Potenciales y Sesgo de Selección
* Stata · Código local

* Cargar datos
import delimited datos/muestra.csv, clear
describe

* Estadísticas descriptivas
summarize intereses

* Comparación de medias: diferencia observada
tabstat intereses, by(recibio_ece) statistics(count mean sd min max)

* Prueba t de Welch (dos varianzas desiguales)
ttest intereses, by(recibio_ece) unequal

* Gráfica: densidad
twoway kdensity intereses if recibio_ece == 0, ///
  || kdensity intereses if recibio_ece == 1, ///
  legend(order(1 "Sin ECE" 2 "Con ECE")) ///
  title("Distribución de intereses por grupo") ///
  xtitle("Intereses (pesos)") ytitle("Densidad")

* Gráfica: boxplot
graph box intereses, over(recibio_ece) ///
  title("Distribución de intereses: Boxplot") ///
  ylabel("Intereses (pesos)"

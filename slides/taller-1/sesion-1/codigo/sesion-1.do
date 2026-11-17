* Taller 1 / Sesión 1: De la muestra a la inferencia
* Generado desde index.qmd por exportar_codigo.py; edita el QMD.
* Ejecutar desde slides/taller-1/sesion-1/. Datos sintéticos.
* Referencia estática: no ejecutada ni validada con Stata en este entorno.
set more off

* Laboratorio 1
import delimited "datos/muestra.csv", clear
list id_cliente recibe_nomina abonos_miles saldo_promedio_miles n_entradas n_salidas in 1/4
count
tabulate recibe_nomina
tabstat saldo_promedio_miles, by(recibe_nomina) statistics(n mean)


* Laboratorio 2
* Cada repetición vuelve a leer el marco; sample ..., count usa muestreo sin reemplazo.
import delimited "datos/poblacion_saldos.csv", clear
quietly summarize saldo_promedio_miles
local mu = r(mean)
capture program drop media_muestra
program define media_muestra, rclass
    import delimited "datos/poblacion_saldos.csv", clear
    sample 40, count
    quietly summarize saldo_promedio_miles
    return scalar media = r(mean)
end
* Cambia 40 por 200 dentro del programa y vuelve a ejecutar todo este bloque.
simulate media=r(media), reps(300) seed(42) nodots: media_muestra
summarize media
histogram media, frequency xline(`mu') xscale(range(10 16)) ///
    xtitle("Media del saldo (miles de MXN)")


* Laboratorio 3
import delimited "datos/muestra.csv", clear
* Stata resta el primer grupo menos el segundo: 0 de sin_nomina = recibe_nomina 1.
generate byte sin_nomina = 1 - recibe_nomina
label define grupos_nomina 0 "Con nomina" 1 "Sin nomina", replace
label values sin_nomina grupos_nomina
ttest saldo_promedio_miles, by(sin_nomina) unequal level(95)
* unequal permite varianzas distintas y usa los mismos grados de libertad que R y SciPy.
* La diferencia y el IC se expresan en miles de MXN.


* Laboratorio 4
import delimited "datos/muestra.csv", clear
generate byte sin_nomina = 1 - recibe_nomina
label define grupos_nomina 0 "Con nomina" 1 "Sin nomina", replace
label values sin_nomina grupos_nomina
prtest pago_debito, by(sin_nomina) level(95)
* Diferencia: nómina 1 menos nómina 0; multiplica diferencia e IC por 100 para pp.
* La prueba usa una proporción común bajo H0; el IC conserva una por grupo.


* Laboratorio 5
import delimited "datos/muestra.csv", clear
correlate abonos_miles saldo_promedio_miles
twoway (scatter saldo_promedio_miles abonos_miles if recibe_nomina==0) ///
       (scatter saldo_promedio_miles abonos_miles if recibe_nomina==1), ///
       xtitle("Abonos del mes (miles de MXN)") ///
       ytitle("Saldo promedio (miles de MXN)") ///
       legend(order(1 "Sin nomina" 2 "Con nomina"))


* Laboratorio 6
import delimited "datos/muestra.csv", clear
regress saldo_promedio_miles abonos_miles, level(95)
predict double ajustado, xb
predict double residuo, residuals
list saldo_promedio_miles ajustado residuo in 1/3
* H0: pendiente=0. IC y p convencionales; sin vce(robust) en este repaso.

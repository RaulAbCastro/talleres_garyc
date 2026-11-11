* Ejecutar en Stata dentro del Windows remoto del banco.
clear all
set more off
set obs 5
generate x = _n
generate y = 2 * x + mod(_n, 2)
regress y x
* Este ejemplo usa datos creados aquí y no necesita archivos externos.

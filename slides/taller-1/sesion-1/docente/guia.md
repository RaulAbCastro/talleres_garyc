# Guía docente — Taller 1, sesión 1

Esta versión estudia exclusivamente cuentas de depósito a la vista, pagos con débito y sus movimientos de entrada y salida.
Todos los registros son sintéticos; no describen a un banco ni al sistema
financiero mexicano. La duración orientativa es de 60 minutos. Las notas del QMD
contienen las preguntas y el ritmo de presentación. Los resultados de esta guía
corresponden a la semilla **202609** y al CSV distribuido.

## Referencia pedagógica

Inspiración: Angus Foulis, *Introduction: Econometrics With Microdata*, Centre
for Central Banking Studies, Bank of England, 10 de noviembre de 2026,
diapositivas 1–17, en
[`referencias/slides-de-referencia/10_11_26_Causal_Econometrics_Intro.pdf`](../../../../referencias/slides-de-referencia/10_11_26_Causal_Econometrics_Intro.pdf).
Se retoma la secuencia de intuiciones: población y muestra, relación entre dos
variables, recta estimada, error frente a residuo y supuestos de regresión. Los
ejemplos, los datos, las animaciones y el código se construyen para este taller.
La referencia no aporta ni avala cifras del caso bancario.

## Marco, muestra y unidades

El marco didáctico contiene **12 000 clientes** con cuenta de depósito a la vista
y tarjeta de débito. Se seleccionan **480 clientes** por muestreo aleatorio simple
sin reemplazo. Cada fila describe **la cuenta de un cliente durante septiembre de 2026**:
es un corte transversal de agregados mensuales, no una tabla de transacciones ni
un panel. Tener una tarjeta no implica usarla en el mes.

| Variable | Interpretación |
|---|---|
| `id_cliente` | Identificador sintético único, sin datos personales reales. |
| `recibe_nomina` | 1 si recibió un abono identificado como nómina durante el mes, 0 si no. |
| `abonos_miles` | Suma de abonos durante el mes, de cualquier canal, en miles de MXN. |
| `saldo_promedio_miles` | Saldo promedio del mes en la cuenta de depósito, en miles de MXN. |
| `pago_debito` | 1 si n_pagos_debito > 0, 0 en otro caso; no incluye retiros. |
| `n_entradas` | Suma de los conteos de entradas por canal durante el mes. |
| `n_salidas` | Suma de los conteos de salidas por tipo/canal durante el mes. |
| `n_spei_entrada` | Número de transferencias SPEI recibidas durante el mes. |
| `n_abonos_ventanilla` | Número de depósitos en ventanilla durante el mes. |
| `n_abonos_cajero` | Número de depósitos en cajeros receptores durante el mes. |
| `n_abonos_comisionista` | Número de depósitos por comisionistas durante el mes. |
| `n_otros_abonos` | Número de otros abonos; incluye traspasos internos. |
| `n_spei_salida` | Número de transferencias SPEI enviadas durante el mes. |
| `n_pagos_debito` | Número de pagos con la tarjeta de débito asociada a la cuenta. |
| `n_retiros_cajero` | Número de retiros de efectivo en cajero durante el mes. |
| `n_retiros_ventanilla` | Número de retiros de efectivo en ventanilla durante el mes. |
| `n_retiros_comisionista` | Número de retiros de efectivo por comisionistas durante el mes. |
| `n_otros_cargos` | Número de otros cargos; p. ej., domiciliaciones, comisiones y traspasos internos. |


El objeto es la **cuenta de depósito a la vista**, no un conjunto de productos
financieros. El marco supone una cuenta por cliente y una tarjeta de débito
asociada; no se modelan crédito ni sus saldos, compras o pagos.

Las entradas y salidas se clasifican por sentido y tipo/canal. SPEI puede ser
recibido o enviado; ventanilla, cajero y comisionista pueden registrar depósitos
y retiros. Un retiro se cuenta en su canal, no también como pago con débito.
`n_entradas` y `n_salidas` son totales derivados: no deben sumarse otra vez junto
con sus componentes. «Otros» permite incluir traspasos internos, domiciliaciones
y comisiones sin presentar el catálogo como exhaustivo.

`recibe_nomina` identifica el origen de algún abono; no es un canal adicional.
En la simulación una nómina se registra en SPEI o en otros abonos internos, sin
duplicarla. La asignación entre canales es una decisión sintética, no una cuota
estimada para México. `pago_debito = 1` únicamente cuando `n_pagos_debito > 0`.

Los conteos miden operaciones, `abonos_miles` mide su importe total de entrada
y `saldo_promedio_miles` es un stock promediado. No hay importes por canal ni un
libro diario conciliado: no se puede reconstruir el saldo final o el promedio
restando conteos. Los grupos con y sin nómina son observados; el muestreo no
asigna aleatoriamente la recepción de nómina.


Fuentes conceptuales: [Banco de México sobre SPEI](https://www.banxico.org.mx/servicios/mi-spei_-transferencias-ban.html),
[CONDUSEF sobre cuentas y débito](https://www.condusef.gob.mx/index.php/conoce-la-condusef?p=cuentas-dep)
y [CONDUSEF sobre comisionistas/corresponsales](https://www.condusef.gob.mx/?idc=2080&idcat=1&p=contenido).
La disponibilidad de servicios depende de la entidad y del canal. Estas fuentes
respaldan las distinciones conceptuales; no calibran las probabilidades ni las
cifras de nuestro simulador.

Se omite la corrección por población finita (fracción de muestreo del 4%). En el
simulador los clientes se generan de forma independiente; no se modelan hogares,
clusters de bancos ni dependencia temporal. Las pruebas e intervalos son una
aproximación introductoria. La regresión usa errores estándar OLS convencionales;
la inferencia requiere discutir los supuestos, no solo ejecutar el comando.

## Secuencia didáctica y ritmo

La sesión sigue el orden de `temario.tex`: **pruebas de hipótesis → comparación
de medias y proporciones → correlación → regresión lineal simple**. La pregunta
sobre saldos aparece desde el inicio; población, muestreo, error estándar e
intervalos se introducen dentro del primer bloque porque explican cómo funciona
un contraste, no como un repaso separado que retrase la pregunta principal.

El guion tiene 38 diapositivas. Cada explicación conecta la afirmación o pregunta
con el parámetro, el estimador, su incertidumbre y una conclusión con unidades.
Las fórmulas se traducen al caso y luego se reconocen en el código; no se presentan
como una lista de definiciones desconectadas.

| Minutos | Tema y desarrollo |
|---|---|
| 0–3 | Pregunta bancaria, unidad de análisis y ruta de trabajo. |
| 3–22 | Pruebas de hipótesis: parámetro, H0/H1, distribución muestral, EE, estadístico, p, alfa, errores de decisión e IC. |
| 22–37 | Medias: EE de la diferencia y Welch; proporciones: media de 0/1, prueba agrupada e IC no agrupado. |
| 37–43 | Correlación: nube de puntos, covarianza estandarizada, dirección, escala y límites. |
| 43–56 | Regresión simple: ecuación, error/residuo, criterio y nombre de MCO, supuestos, EE de la pendiente, prueba, IC, R² y laboratorio. |
| 56–60 | Memo argumentado y comprobación final de interpretación. |

Ejecutar **un lenguaje por laboratorio** en plenaria. El laboratorio 2, con 300
muestras repetidas, se mantiene como **práctica complementaria**; la animación
explica su intuición durante la hora de clase. Los otros cinco laboratorios
están incluidos en los tiempos. Ejecutar también el laboratorio 2 con discusión,
o comparar los tres lenguajes durante la clase, requiere ampliar la duración.
R y Python se ejecutan en el navegador; Stata se copia a una instalación local.

### Dependencias conceptuales

Las explicaciones deben estar en las slides visibles, antes del uso del concepto,
incluido el uso en un botón, leyenda, fórmula o resultado de código. Las notas
amplían la explicación para el docente; no son un prerrequisito oculto del grupo.

| Antes de pedir… | Explicar primero… |
|---|---|
| Formular H0 sobre una diferencia | Población y muestra; qué es un parámetro y qué significan los grupos y sus medias. |
| Leer una fórmula de estimación | Regla frente a valor calculado; índices, suma, barra de media y sombrero de estimación. |
| Usar DE/EE en el laboratorio 2 | Dispersión entre saldos, varianza y dispersión de un estimador entre muestras. La animación previa muestra un rango, sin adelantar DE. |
| Calcular p e intervalos | Estadístico; distribución de referencia normal/t; colas, grados de libertad, valor crítico e IC. |
| Promediar una variable binaria | Por qué sumar unos y dividir entre clientes produce una proporción. Se hace en el bloque de proporciones, no en el laboratorio 1. |
| Usar una covarianza o Pearson | Desviaciones respecto a las medias, producto conjunto y división entre las DE para quitar unidades. |
| Usar la sigla MCO | Recta, coeficientes y residuos; cuadrados y su suma; nombre completo «mínimos cuadrados ordinarios». La animación previa dice «Encontrar la recta». |
| Usar E[u\|X] o homocedasticidad | Promedio del error entre clientes con los mismos abonos; después, misma dispersión del error a cada nivel de abonos. |
| Leer R² o la inferencia del laboratorio 6 | Condiciones de los EE convencionales, precisión de la pendiente y reducción de errores cuadrados respecto a predecir con la media. |

El bloque de regresión conserva sus 13 minutos: ecuación (43–44), valores
ajustados y residuos (44–46), animación (46–48), nombre y fórmula de MCO (48–49),
supuestos sobre el error (49–51), inferencia (51–52), interpretación y R² (52–54),
laboratorio 6 (54–56). La nueva explicación de distribuciones de referencia ocupa
14–15, después de estadístico/p (13–14). Este es un ritmo de repaso; una introducción
desde cero o ejecutar todos los lenguajes requiere más tiempo.

## Cobertura del syllabus y conexiones que debe poder explicar el grupo

| Tema de la sesión 1 | Desarrollo y verificación |
|---|---|
| Pruebas de hipótesis | Distinguir H0/H1 sobre parámetros de las estimaciones observadas; explicar cómo el EE permite construir un estadístico y obtener un p bajo H0. Separar alfa, p, error tipo I, error tipo II e intervalo. |
| Comparación de medias | Reconstruir SE(Delta) a partir de las varianzas de las medias independientes; usar Welch, interpretar signo, MXN, IC y decisión. Laboratorio 3. |
| Comparación de proporciones | Explicar la media de una variable 0/1 y sus denominadores; distinguir el EE agrupado bajo H0 del EE no agrupado del IC; comunicar en pp. Laboratorio 4. |
| Correlación | Explicar los productos centrados de la covarianza y la estandarización de Pearson; verificar forma y valores extremos en la nube. Laboratorio 5. |
| Regresión lineal simple | Separar parámetro/estimación y error/residuo; explicar la elección MCO, b1 = r sY/sX, EE y contraste de la pendiente, R² y límites causales. Laboratorio 6. |

El laboratorio 1 identifica los insumos de los contrastes. El laboratorio 2
refuerza la variabilidad muestral, que también se muestra mediante animación.
Así se conserva cada tema previsto sin desplazar las pruebas de medias y
proporciones por contenidos de regresión avanzada.

## Puntos técnicos que conviene desarrollar en voz alta

- **Hipótesis:** una diferencia distinta de cero en la muestra no basta para
  rechazar igualdad poblacional; se compara con su variación de muestreo.
  Alfa controla rechazos bajo H0 verdadera, mientras p es una probabilidad de
  resultados al menos tan extremos bajo H0 y los supuestos. No rechazar no
  demuestra equivalencia.
- **Welch:** para medias independientes, la varianza de su diferencia es la
  suma de sus varianzas. EE = 0.411932 y diferencia = 2.544969 producen
  t = 6.178134 y aproximadamente 470.950 grados de libertad. La independencia
  importa: las mediciones pareadas requieren otro cálculo.
- **Intervalos:** el IC t de la media global es [12.850717, 13.700451] miles
  de MXN. El IC de un parámetro no contiene al 95% de los datos individuales.
  Prueba e IC son duales cuando usan el mismo procedimiento; no extender esa
  equivalencia al test z agrupado y el IC Wald no agrupado de proporciones.
- **Proporciones:** la estimación común bajo H0 es 310/480 = 0.645833.
  El EE del test es 0.044104; el del IC es 0.042092. Hay suficientes éxitos y
  fracasos en ambos grupos para la aproximación introductoria (220/54 y 90/116).
- **Correlación y regresión:** r no tiene unidades y es simétrico; la pendiente
  sí depende de qué variable ponemos como resultado y de las unidades de ambos
  ejes. En regresión simple con intercepto, b1 = r sY/sX y R² = r².
- **Inferencia de la pendiente:** el EE convencional usa la varianza residual
  estimada con n−2 grados de libertad y la variación de X. Necesita condiciones
  adicionales al mero cálculo MCO. La homocedasticidad sustenta esa fórmula de
  EE, pero no es necesaria para insesgadez de MCO bajo exogeneidad. El ejemplo
  de estabilidad omitida impide leer la pendiente como el coeficiente estructural.

## Resultados de referencia

La comparación mantiene siempre el orden **con nómina menos sin nómina**.

| Cantidad | Resultado |
|---|---:|
| Clientes con / sin nómina | 274 / 206 |
| Saldo medio con / sin nómina | 14.367800 / 11.822831 miles de MXN |
| Diferencia de medias | 2.544969 miles de MXN |
| IC95 Welch de la diferencia | [1.735518, 3.354421] miles de MXN |
| Valor p Welch, bilateral | 1.404421e−09 |
| Clientes que pagaron con débito, con / sin nómina | 220/274 / 90/206 |
| Proporción de pago con débito, con / sin nómina | 80.291971% / 43.689320% |
| Diferencia de proporciones | 36.602650 puntos porcentuales |
| IC95 Wald no agrupado de la diferencia | [28.352676, 44.852625] puntos porcentuales |
| Valor p z agrupada, bilateral, sin corrección | 1.048063e−16 |
| Correlación Pearson abonos–saldo | 0.887913 |
| Intercepto / pendiente OLS | 3.915756 / 0.384931 |
| IC95 de la pendiente, OLS convencional | [0.367008, 0.402854] |
| R² | 0.788389 |
| Media del marco / de la muestra | 13.184802 / 13.275584 miles de MXN |
| DE del saldo en la muestra / EE de su media | 4.737255 / 0.216225 miles de MXN |

El intervalo que acompaña a cada media en la figura está calculado por separado;
el intervalo de la **diferencia** es el de Welch. No sustituir la prueba de la
diferencia por una regla visual sobre el traslape de dos intervalos.

En el laboratorio de muestreo, aumentar n de 40 a 200 reduce aproximadamente la
DE de las medias por un factor de √5. El muestreo sin reemplazo añade una pequeña
corrección finita. R y Python no producen las mismas selecciones con una semilla
numéricamente idéntica: usan generadores distintos, pero deben mostrar el mismo
comportamiento al repetir muestras. El eje fijo 10–16 miles de MXN permite
comparar la dispersión alrededor de la media del marco (13.1848).

## Un memo posible

En esta muestra sintética de 480 clientes, quienes recibieron nómina tienen un
saldo promedio mensual de aproximadamente 2,545 MXN más que quienes no la recibieron (IC95
Welch: 1.74 a 3.35 mil MXN; p<0.001). Pagaron con débito 220 de 274 clientes con
nómina (80.3%) y 90 de 206 sin nómina (43.7%): diferencia de 36.6 puntos
porcentuales (IC95: 28.4 a 44.9). Abonos y saldo tienen correlación 0.888; la recta
descriptiva asocia 1000 MXN adicionales de abonos mensuales con unos 385 MXN más
de saldo promedio. Estas asociaciones no identifican qué ocurriría si un cliente
empezara a recibir nómina. Antes de proponer una intervención, conviene estudiar
las diferencias previas entre los grupos y definir el diseño de identificación.

## Lo que sabe el simulador

`docente/poblacion.csv` añade `estabilidad_ingreso`, `ruido_saldo` y
`error_estructural_saldo`. El recurso que usa el laboratorio de participantes,
`datos/poblacion_saldos.csv`, contiene solamente la columna de saldo. La separación
es pedagógica: el repositorio permite inspeccionar el generador completo.

La semilla raíz es 202609. Se separan los generadores de población (202609),
muestra (202610) y actividad (202611) para que ampliar un canal no vuelva a
seleccionar clientes. Los abonos, nómina y saldo conservan la misma receta
poblacional; la muestra y el resultado de uso de débito se regeneraron bajo el
nuevo alcance, por lo que también se actualizaron todas las cifras narradas.

El generador comprueba que los totales igualen sus componentes, que los conteos
sean enteros no negativos, que cada cuenta con abonos tenga al menos una entrada
y que el indicador de pagos coincida exactamente con pagos de débito positivos.

La receta para el saldo es:

```text
saldo = 6 + 0.30 × abonos + u
u = 3 × estabilidad_ingreso + ruido_saldo
```

El saldo se redondea a cuatro decimales en miles de MXN. La estabilidad de ingresos
latente influye tanto en recibir nómina como en los abonos y el saldo. Por ello,
para esta ecuación generadora **E[u | abonos] ≠ 0**: el componente omitido cambia
con los abonos. La pendiente estimada (0.385) no tiene por qué recuperar el
coeficiente de la receta (0.30), incluso en una muestra grande. La receta no
simula una intervención y sus coeficientes no se presentan como efectos causales
identificados para clientes reales.

El **error** u pertenece a una ecuación poblacional propuesta; no se observa en
un estudio ordinario. El **residuo** es la distancia vertical entre el saldo
observado y la recta estimada. Con intercepto, mínimos cuadrados hace que los
residuos sumen cero y sean ortogonales a los abonos en la muestra por construcción.
Eso **no demuestra** E[u | abonos] = 0. También es posible definir una proyección
lineal poblacional cuyo error sea ortogonal a X: esa definición descriptiva no
convierte su pendiente en efecto causal ni garantiza media condicional cero.

Al trabajar el supuesto, preguntar qué rasgos no observados podrían vincularse
con ambos ejes: estabilidad laboral, ahorro previo o necesidades de liquidez.
Son hipótesis para discutir, no variables medidas por este CSV.

## Comprobación y reproducción

Desde la raíz del repositorio:

```bash
.venv/bin/python slides/taller-1/sesion-1/generar_datos.py
.venv/bin/python slides/taller-1/sesion-1/generar_figuras.py
```

Desde `slides/taller-1/sesion-1/`:

```bash
Rscript generar_figuras.R
```

`resumen.json` guarda las cifras completas, las unidades, el contraste y el hash
SHA-256 del CSV observado. El generador valida identificadores únicos, valores
no faltantes, conteos enteros no negativos y consistencia del indicador de pagos.
Las figuras R y Python leen el mismo CSV y calculan los mismos resúmenes.

## Criterios para retroalimentación

- Define la unidad de análisis, el mes y la población a la que se refiere.
- Conserva el orden con nómina menos sin nómina y las unidades de cada variable.
- Distingue puntos porcentuales de variaciones relativas porcentuales.
- Distingue dispersión de saldos individuales de incertidumbre de una media.
- No interpreta p como probabilidad de que H0 sea cierta.
- No usa “no rechazar” para demostrar equivalencia.
- Distingue error no observado de residuo calculado y estimación de supuesto.
- No atribuye causalidad a correlación, R², significancia o pendiente por sí solos.
- Ejecuta el código propuesto por cualquier asistente de IA y coteja un resultado.

Si la red impide cargar los runtimes, usar scripts locales y figuras SVG. No se
necesita una cuenta de IA para completar el taller ni redactar el memo.

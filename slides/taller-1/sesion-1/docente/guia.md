# Guía docente (taller 1, sesión 1)

Esta versión estudia exclusivamente cuentas de depósito a la vista, pagos con débito y sus movimientos de entrada y salida.
Todos los registros son sintéticos; no describen a un banco ni al sistema
financiero mexicano. El recorrido dura aproximadamente 60 minutos e integra
ANOVA y los contrastes de varianzas en el bloque de comparaciones. Las notas
del QMD contienen las preguntas y el ritmo de presentación. Los resultados de esta guía
corresponden a la semilla **202609** y al CSV distribuido.

## Referencia pedagógica

Inspiración: Angus Foulis, *Introduction: Econometrics With Microdata*, Centre
for Central Banking Studies, Bank of England, 10 de noviembre de 2026,
diapositivas 1 a 17, en
[`referencias/slides-de-referencia/10_11_26_Causal_Econometrics_Intro.pdf`](../../../../referencias/slides-de-referencia/10_11_26_Causal_Econometrics_Intro.pdf).
Se retoma la secuencia de intuiciones: población y muestra, relación entre dos
variables, recta estimada, error frente a residuo y supuestos de regresión. Los
ejemplos, los datos, las animaciones y el código se construyen para este taller.
La referencia no aporta ni avala cifras del caso bancario.

La pauta *Lesson Plan Builder* propone formular un objetivo observable, diseñar
una tarea final que lo evalúe y usar las respuestas durante la clase para decidir
qué explicación retomar. En esta sesión el objetivo es que, ante una pregunta
bancaria nueva, cada participante **elija un método y justifique una conclusión
con el parámetro que estudia, las unidades y la incertidumbre**. El reto de
retiros en ventanilla permite comprobarlo. [Lesson Plan Builder de SkillMedev](https://github.com/SkillMedev/skills/blob/main/skills/lesson-plan-builder/SKILL.md).

### Cuatro actividades adaptadas de cursos universitarios

- **Elegir la cola.** En Data 8 el grupo anticipa el signo que favorecería la alternativa antes de calcular la diferencia. Para el encargo sobre nómina del mes siguiente, recoger el signo y la cola que propone cada pareja. Después de revelar el estadístico, invertir la resta y pedirles que expliquen por qué se conserva el valor p de la misma pregunta. [UC Berkeley, Data 8, lección 18](https://data8.org/materials-sp26/lec18/)
- **Separar dos fuentes de variación.** Biocore presenta grupos con distinta separación en relación con su dispersión. En nuestra figura, ambos paneles conservan exactamente las tres medias y los tamaños. Pedir al grupo que señale qué se movió y prediga en qué panel resultaría más fácil distinguir medias. Las barras representan una desviación estándar a cada lado de la media. [Universidad de Wisconsin (Madison), Biocore, capítulo 5, sección 5.2](https://wisc.pb.unizin.org/biocorestatistics/chapter/statistical-inference-comparing-more-than-2-groups/)
- **Elegir el denominador.** En la práctica de Granada, los estudiantes distinguen cuántas personas presentan la característica y cuántas integran cada grupo antes de ejecutar una prueba de dos proporciones. Con nuestros datos, pedir una oración para 220/274 y otra para 220/310. El mismo numerador permite contestar dos preguntas distintas. Si la pareja duda, que lea en voz alta el encabezado de la fila o columna que suma el denominador. [Universidad de Granada, Práctica 6 de Estadística, contraste de dos proporciones](https://wpd.ugr.es/~bioestad/guia-r-studio/practica-6/)
- **Leer el ajuste.** Edimburgo transforma la nube original en una gráfica de residuos para identificar patrones. En los dos paneles del taller, pedir primero que sigan el centro de los residuos y después su amplitud vertical. En el laboratorio 7, cada participante puede contrastar su descripción con las 480 cuentas y señalar qué información sobre el diseño necesitaría para evaluar independencia. [Universidad de Edimburgo, Foundations of Data Science, sección 10.3, pp. 78 a 80](https://opencourse.inf.ed.ac.uk/sites/default/files/2024-01/FDS-lecture-notes-2024-01-28.pdf#page=88)

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

Las **48 diapositivas** siguen el orden de `temario.tex`. Después del contraste
de dos medias por nómina, formular una pregunta nueva sobre el mismo saldo en
tres grupos de clientes. Conservar esos grupos para estudiar su dispersión.
Luego volver a los grupos de nómina y cambiar el resultado a un indicador de
pago. Para correlación y regresión, conservar los importes de cada cliente y
estudiar conjuntamente sus abonos y su saldo.

| Minutos | Desarrollo y actividad del alumnado |
|---|---|
| 0 a 3 | Identificar la unidad cliente-mes y precisar qué quiere saber el equipo. |
| 3 a 18 | Formular hipótesis sobre el saldo. Usar la animación de muestreo para explicar el error estándar, elegir la cola según la alternativa y discutir el valor p, los errores de decisión y el intervalo. |
| 18 a 24 | Ejecutar Welch en el laboratorio 3. Situar cero y el umbral de 3,000 MXN respecto del intervalo para interpretar la diferencia. |
| 24 a 35 | Pasar a tres tramos de pagos. Comparar los dos paneles de dispersión antes de calcular F. Ejecutar el laboratorio 4 y emparejar cada valor p con su hipótesis. |
| 35 a 41 | Construir el indicador de pago, elegir el denominador de cada grupo y explicar en puntos porcentuales el intervalo del laboratorio 5. |
| 41 a 46 | Describir la nube del laboratorio 6 y relacionar la dirección y la fuerza de la asociación con el signo y la magnitud de la correlación. |
| 46 a 56 | Explorar la recta de mínimos cuadrados y sus distribuciones condicionales. Identificar la curva y el abanico en parejas. Traducir la pendiente y su intervalo a pesos con el resultado visible del laboratorio 7. |
| 56 a 60 | Discutir en parejas qué resultado respalda cada conclusión y qué interpretación admite la pendiente. Plantear el caso de retiros en ventanilla y recoger el parámetro y el método elegidos antes de mostrar la solución. |

En el recorrido de una hora se ejecutan en plenaria los **laboratorios 3 y 4**
en R o Python. Para los **laboratorios 1, 2, 5, 6 y 7** se interpretan la
muestra, la animación de muestreo, las cifras de pago, la nube de puntos y el
ajuste ya visibles. Su código queda disponible para práctica individual.
Para trabajar en Stata se usa la instalación local.

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
| Interpretar los valores F del laboratorio 4 | Comparar variación entre los promedios y dentro de cada grupo para ANOVA. Para la dispersión identificar la DE de referencia, el cociente de varianzas o las distancias a la mediana, según la pregunta. |
| Promediar una variable binaria | Por qué sumar unos y dividir entre clientes produce una proporción. Se hace en el bloque de proporciones, no en el laboratorio 1. |
| Usar una covarianza o Pearson | Desviaciones respecto a las medias, producto conjunto y división entre las DE para quitar unidades. |
| Usar la sigla MCO | Recta, coeficientes y residuos; cuadrados y su suma; nombre completo «mínimos cuadrados ordinarios». La animación previa dice «Encontrar la recta». |
| Usar E[u\|X] o homocedasticidad | Promedio del error entre clientes con los mismos abonos; después, misma dispersión del error a cada nivel de abonos. |
| Leer R² o la inferencia del laboratorio 7 | Condiciones de los EE convencionales, precisión de la pendiente y reducción de errores cuadrados respecto a predecir con la media. |

El ejemplo de 1,000 MXN con un EE de 500 introduce el estadístico y su
distribución de referencia. Pedir que el grupo elija
cuáles de −2.3, +1.8 y +2.4 están al menos a dos EE del cero. Al avanzar, las
dos colas de la normal muestran qué probabilidades suma el valor p.
Para el mismo z = +2, comparar p = 0.9772, 0.0455 y 0.0228 bajo las alternativas
izquierda, bilateral y derecha, respectivamente. La dirección se fija antes de
observar el resultado.

Antes de empezar con proporciones, preguntar qué compara el ANOVA y qué compara
la prueba de Levene centrada en la mediana. Escuchar a dos parejas. Si confunden las preguntas, retomar un saldo y calcular su distancia a la
mediana de su grupo. Pedirles que vuelvan a nombrar qué variable analiza cada
prueba y qué hipótesis corresponde a cada valor p antes de avanzar.

## Cobertura del syllabus y conexiones que debe poder explicar el grupo

| Tema de la sesión 1 | Desarrollo y verificación |
|---|---|
| Pruebas de hipótesis | Distinguir H0/H1 sobre parámetros de las estimaciones observadas. Elegir la cola según la alternativa y calcular p bajo H0. Separar alfa, p, error tipo I, error tipo II e intervalo. |
| Comparación de medias | Reconstruir el EE de la diferencia de medias, aplicar Welch e interpretar signo, MXN e IC en el laboratorio 3. En el laboratorio 4 formular la hipótesis global de igualdad de tres medias para ANOVA y justificar la conclusión. |
| Comparación de dispersiones | Cambiar la pregunta sobre el saldo a una sobre su DE o varianza. Identificar la referencia fija para ji cuadrada, los dos grupos de la razón F y las distancias a las medianas para Levene. Laboratorio 4. |
| Comparación de proporciones | Explicar la media de un indicador 0/1 y sus denominadores. Distinguir el EE agrupado de la prueba del EE no agrupado del IC y comunicar el resultado en pp. Laboratorio 5. |
| Correlación | Explicar los productos centrados de la covarianza y la estandarización de Pearson. Verificar forma y valores extremos en la nube. Laboratorio 6. |
| Regresión lineal simple | Distinguir parámetro y estimación, error y residuo. Explicar el criterio de MCO, b1 = r sY/sX, el EE y el contraste de la pendiente, R² y los límites de la interpretación causal. Laboratorio 7. |

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
- **Welch.** Para medias independientes, la varianza de su diferencia es la
  suma de sus varianzas. Al dividir la diferencia (2.544969) entre su EE
  (0.411932) obtenemos $t=6.178134$. Para elegir la curva t, la aproximación
  de Satterthwaite combina las dos contribuciones $v_g=s_g^2/n_g$ con los
  grados de libertad de cada grupo (273 y 205). El resultado, 470.9496, se
  reproduce en el laboratorio 3. Las mediciones pareadas requieren otro cálculo.
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

Las diferencias entre los dos grupos de nómina mantienen el orden **con nómina
menos sin nómina**. En el laboratorio 4, el factor que define los tres grupos
es el número de pagos con débito.

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
| Correlación de Pearson (abonos y saldo) | 0.887913 |
| Intercepto / pendiente OLS | 3.915756 / 0.384931 |
| IC95 de la pendiente, OLS convencional | [0.367008, 0.402854] |
| R² | 0.788389 |
| Media del marco / de la muestra | 13.184802 / 13.275584 miles de MXN |
| DE del saldo en la muestra / EE de su media | 4.737255 / 0.216225 miles de MXN |

El intervalo que acompaña a cada media en la figura está calculado por separado;
el intervalo de la **diferencia** es el de Welch. No sustituir la prueba de la
diferencia por una regla visual sobre el traslape de dos intervalos.

En el reto final, preguntar «¿Difiere por nómina la proporción de clientes
que retiró en ventanilla?». Antes de dar una pista sobre el código, pedir a cada
participante que nombre el parámetro y el método, y que indique qué cuenta en
el numerador y en el denominador. Después cotejar la respuesta con el
laboratorio 5. El indicador vale uno por cliente con al menos un retiro.
Retiraron 25/274 con nómina y 26/206 sin nómina. La diferencia es −3.50 pp y
su IC de Wald del 95% va de −9.17 a +2.18 pp. Si alguien concluye que los
grupos son iguales, pedirle que identifique una diferencia distinta de cero
compatible con ese intervalo.

En el laboratorio de muestreo, aumentar n de 40 a 200 reduce aproximadamente la
DE de las medias por un factor de √5. El muestreo sin reemplazo añade una pequeña
corrección finita. R y Python no producen las mismas selecciones con una semilla
numéricamente idéntica: usan generadores distintos, pero deben mostrar el mismo
comportamiento al repetir muestras. El eje fijo 10 a 16 miles de MXN permite
comparar la dispersión alrededor de la media del marco (13.1848).

## Respuestas de referencia para la discusión final

Invitar a distintas parejas a responder una pregunta cada una. Pedirles que
identifiquen las cuentas que comparan, las unidades y el resultado que respalda
su interpretación. Estas respuestas sirven para orientar la conversación.

1. En esta muestra de 480 clientes, el saldo promedio fue 2,545 MXN mayor en el grupo con nómina, y el intervalo del 95% (1,736 a 3,354 MXN) admite diferencias tanto inferiores como superiores al umbral de 3,000 MXN.
2. Al comparar los saldos medios de quienes hicieron cero, de uno a cuatro o al menos cinco pagos con débito, la evidencia resultó insuficiente para concluir al nivel del 5% que al menos dos medias poblacionales difieren (ANOVA, p = 0.098).
3. La proporción que pagó con débito fue 36.6 puntos porcentuales mayor entre clientes con nómina que entre clientes sin ella (220/274 frente a 90/206, IC del 95% de 28.4 a 44.9 pp).
4. Por cada 1,000 MXN adicionales de abonos mensuales, la recta estima un saldo promedio 385 MXN mayor entre clientes (r = 0.888), una asociación que podría reflejar en parte diferencias en la estabilidad de sus ingresos.

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

### Resultados del laboratorio 4 y fuentes técnicas

| Contraste | Estadístico | Valor p |
| --- | ---: | ---: |
| ANOVA clásico de saldo por tramo de pagos, F(2, 477) | 2.331737 | 0.098233 |
| Levene centrado en la mediana, F(2, 477) | 0.659251 | 0.517709 |
| DE de 4 mil MXN en el grupo de cero pagos, ji cuadrada(169) | 221.971575 | 0.007791 |
| Razón de varianzas de 5+ frente a cero pagos, F(227, 169) | 1.058666 | 0.697521 |

Los grupos de 0, 1 a 4 y 5+ pagos tienen 170, 82 y 228 clientes. El ANOVA
contrasta las medias y Levene la dispersión. Los saldos de la muestra son
asimétricos, especialmente en los grupos extremos. Los resultados de las
pruebas clásicas ilustran el cálculo bajo su referencia normal.

- ANOVA de un factor y contraste global de medias. [NIST, tabla de ANOVA](https://itl.nist.gov/div898/handbook/prc/section4/prc433.htm).
- Contrastes clásicos de dispersión. [NIST, una varianza](https://www.itl.nist.gov/div898/handbook/eda/section3/eda358.htm), [NIST, razón de dos varianzas](https://itl.nist.gov/div898/handbook/eda/section3/eda359.htm) y [NIST, Levene](https://www.itl.nist.gov/div898/handbook/eda/section3/eda35a.htm).
- Condiciones LINE para regresión simple. Los perfiles de la diapositiva ilustran la distribución $Y\mid X=x$ con media $5+0.4x$ y DE de 2.2 mil MXN. La independencia se discute a partir del diseño. [Penn State, STAT 501](https://online.stat.psu.edu/stat501/Lesson04).
- Sintaxis de referencia para Stata. [oneway](https://www.stata.com/manuals/roneway.pdf), [sdtest y robvar](https://www.stata.com/manuals/rsdtest.pdf).

### Generar datos y figuras

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
Las figuras basadas en datos leen el mismo CSV y calculan los mismos resúmenes
en R y Python. Los perfiles condicionales se generan con la misma distribución
ilustrativa en ambos lenguajes.

## Criterios para retroalimentación

- Define la unidad de análisis, el mes y la población a la que se refiere.
- Conserva el orden con nómina menos sin nómina y las unidades de cada variable.
- Distingue puntos porcentuales de variaciones relativas porcentuales.
- Distingue dispersión de saldos individuales de incertidumbre de una media.
- Formula la igualdad que contrasta ANOVA y reconoce qué cambia al estudiar dispersión.
- No interpreta p como probabilidad de que H0 sea cierta.
- No usa “no rechazar” para demostrar equivalencia.
- Distingue error no observado de residuo calculado y estimación de supuesto.
- No atribuye causalidad a correlación, R², significancia o pendiente por sí solos.
- Ejecuta el código propuesto por cualquier asistente de IA y coteja un resultado.

Si la red impide cargar los runtimes, usar scripts locales y figuras SVG. No se
necesita una cuenta de IA para participar en las actividades.

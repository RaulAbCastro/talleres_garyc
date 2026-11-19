# Slides de los talleres GARyC

La primera sesión del Taller 1, **De la muestra a la inferencia**, está en
[`taller-1/sesion-1/index.qmd`](taller-1/sesion-1/index.qmd). Es una presentación
Quarto **reveal.js**, en español, para una sesión de aproximadamente una hora.
Usa cuentas de depósito a la vista, transferencias SPEI y pagos con débito
como contexto cotidiano, con **datos completamente sintéticos**. Conserva el
alcance de la sesión 1 de `documents_overleaf/temario.tex`; sustituye la historia
futurista de la primera versión.

La secuencia explicativa se inspira en Angus Foulis, *Introduction: Econometrics
With Microdata*, Centre for Central Banking Studies, Bank of England,
10 de noviembre de 2026, [diapositivas 1 a 17 del PDF de referencia](../referencias/slides-de-referencia/10_11_26_Causal_Econometrics_Intro.pdf).
Parte de preguntas concretas, distingue población y muestra, introduce errores
y residuos y visualiza el criterio de MCO antes de discutir sus supuestos.
Los textos, datos y gráficos de esta sesión son propios.
El temario define el alcance: hipótesis, comparación de medias y proporciones,
correlación y regresión lineal simple. La referencia externa guía la pedagogía;
se conserva cada tema en una progresión de lo simple a lo complejo.

Las **48 diapositivas** parten de una pregunta sobre la diferencia de saldo
entre clientes con y sin nómina. Esta pregunta da pie a explicar el muestreo,
el error estándar, los intervalos y las pruebas de una y dos colas. Después de
comparar dos medias con Welch, el grupo compara tres medias por tramo de pagos
con ANOVA y estudia la dispersión de los saldos dentro de esos mismos tramos.
Al cambiar el resultado a «pagó con débito al menos una vez», pasa a comparar
proporciones. Finalmente usa la correlación y la regresión para estudiar cómo
se relacionan los abonos con el saldo.

El alumnado elige un método a partir de la pregunta y justifica su conclusión
con las cifras y los supuestos del caso. Para una clase de **60 minutos** se
ejecutan en plenaria los laboratorios 3 y 4 en un lenguaje. En los laboratorios
1, 2, 5, 6 y 7 se interpretan las cifras, animaciones y figuras disponibles y
se puede ejecutar el código después. El ritmo por tema y las preguntas de
seguimiento se detallan en la [guía docente](taller-1/sesion-1/docente/guia.md).

Cada concepto se explica antes de usarse en fórmulas, animaciones o laboratorios.
La elección de una recta se explora antes de nombrar mínimos cuadrados ordinarios
(MCO). Una figura de distribuciones condicionales ilustra la linealidad, la
normalidad y la varianza igual. La independencia se discute a partir del
muestreo. La guía docente registra estas dependencias.

## Abrir y presentar

El [menú de presentaciones en GitHub Pages](https://raulabcastro.github.io/talleres_garyc/)
se puede abrir desde cualquier equipo con internet.

Desde la raíz del repositorio, con el entorno del Codespace ya instalado:

```bash
bash slides/render.sh preview
```

Abre el puerto **4200** en la pestaña **Ports** de Codespaces: la dirección raíz
redirige automáticamente a `/taller-1/sesion-1/`. El proceso queda ejecutándose
hasta pulsar `Ctrl+C`.
También está disponible la tarea **Slides: vista previa sesión 1** de VS Code.

Para compilar sin dejar abierto un servidor:

```bash
bash slides/render.sh
```

Se genera `slides/taller-1/sesion-1/index.html` con su carpeta de dependencias.
El HTML generado y sus dependencias no se versionan. `slides/index.html` es una
entrada escrita a mano que sí se versiona y permite abrir las slides desde la raíz.
La presentación no es un HTML autocontenido:
conserva las carpetas acompañantes, los CSV, `codigo/`, `assets/` e
`interacciones.js`, además de `animaciones.js` y `animaciones.css`. Para abrirlo
usa Quarto Preview o un servidor HTTP; abrirlo
directamente con `file://` impide cargar módulos y datos.

Para presentar desde otra computadora, copia la URL reenviada del puerto 4200
en **Ports**. Ese enlace requiere que el Codespace y el servidor sigan activos
y que tu cuenta tenga acceso al puerto. No es una publicación permanente.

## Publicar en GitHub Pages

El workflow [slides-pages.yml](../.github/workflows/slides-pages.yml) compila
la presentación con Quarto **1.11.9** y publica al cambiar `slides/` o `website/` en `main`.
También puede ejecutarse desde **Actions → Publicar slides en GitHub Pages →
Run workflow**. La extensión Quarto Live, los datos sintéticos y las figuras se
leen del repositorio; R y Python se ejecutan en el navegador de cada participante.

La activación inicial requiere que una persona con permisos para administrar
Pages abra [Settings → Pages](https://github.com/RaulAbCastro/talleres_garyc/settings/pages)
y elija **Build and deployment → Source → GitHub Actions**. Después puede ejecutar
el workflow o volver a ejecutar el despliegue que estuviera pendiente. El estado
se consulta en [Actions](https://github.com/RaulAbCastro/talleres_garyc/actions/workflows/slides-pages.yml).

Para preparar exactamente los archivos que se publicarán:

```bash
bash slides/publicar.sh
python3 -m http.server 8000 --directory slides/_site
```

El script reconstruye `slides/_site/`, una carpeta ignorada por Git. Copia el
menú de `website/`, la presentación y sus dependencias, los dos CSV de participantes y
los scripts R/Python/Stata. No publica `docente/`, los generadores, el PDF externo
ni documentos de Overleaf. Las notas del expositor integradas en el HTML sí
acompañan a la presentación. Las rutas relativas permiten alojarla dentro de
`/talleres_garyc/`.

En la dirección raíz aparece el menú. También puede usarse el
[enlace directo a la sesión](https://raulabcastro.github.io/talleres_garyc/taller-1/sesion-1/).
La carga inicial de webR/Pyodide y KaTeX continúa requiriendo acceso a sus CDNs.
Referencia de configuración: [workflows de GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Navegación y actividades

Las flechas navegan, `Esc` abre la vista general y `S` las notas del expositor.
Las notas contienen tiempos, preguntas sugeridas y resultados de referencia.
Hay tres preguntas de opción múltiple con retroalimentación y siete laboratorios:

1. Explorar la muestra.
2. Repetir muestreo y cambiar tamaño muestral.
3. Comparar medias con Welch.
4. Comparar tres medias con ANOVA y contrastar hipótesis sobre la dispersión.
5. Comparar proporciones.
6. Calcular la correlación y visualizar la nube de puntos.
7. Estimar la recta y graficar sus residuos frente al saldo ajustado de las 480 cuentas.

Las animaciones permiten repetir muestras, observar la cobertura de intervalos
y cambiar una recta para comparar sus residuos. Tienen controles explícitos,
reinicio y soporte para movimiento reducido. Las poblaciones ilustrativas de
las animaciones se identifican por separado del CSV de los laboratorios.

## Pestañas R, Python y Stata

Cada laboratorio tiene pestañas **R** y **Python** con un editor, **Run Code** y
**Start Over**. Los chunks `{webr}` y `{pyodide}` de
[Quarto Live](https://r-wasm.github.io/quarto-live/other/slides.html) ejecutan
R y Python mediante WebAssembly en el navegador. No necesitan un servidor de
R/Python ni envían el código a un kernel remoto. Cada celda vuelve a leer el
mismo CSV, de modo que no depende de haber ejecutado una celda anterior.
`Ctrl/Cmd+Enter` también ejecuta; Start Over restaura el código de la celda,
no reinicia todo el entorno de ejecución.

La pestaña **Stata** muestra código copiable con el mismo CSV y una descarga
[`codigo/sesion-1.do`](taller-1/sesion-1/codigo/sesion-1.do). Se ejecuta en una
instalación local de Stata; **no se ejecuta en el navegador**. La sintaxis se
revisa contra los manuales oficiales, pero sin una instalación de Stata no se
puede afirmar que el `.do` se haya ejecutado o validado en ese programa.

La primera carga **requiere internet** para descargar webR, Pyodide y los
paquetes Python NumPy, pandas, SciPy y Matplotlib. Espera a que se habilite
Run Code. El tiempo depende de la conexión y la caché del navegador.
La red institucional debe permitir los CDNs usados por estos proyectos
(incluyendo `webr.r-wasm.org`, `cdn.jsdelivr.net` y `pypi.org`). Las fórmulas usan
KaTeX 0.16.22 desde CDN. La presentación,
las preguntas y las figuras precalculadas siguen visibles si esa descarga falla.
Esta versión no incluye runtimes para uso completamente sin conexión.

La extensión se incluye en `_extensions/r-wasm/live/`, descargada del tag
**v0.2.0**. Ese tag conserva internamente `version: 0.1.3-dev`; no se modifica
el código del proveedor. Sus defaults fijan webR 0.6.0 y Pyodide 0.28.1. Se usa
Quarto 1.11.9 del entorno del repositorio. `assets/live-bootstrap.js` resuelve
la inicialización OJS en Quarto reciente mediante un import local explícito;
véase el [issue de compatibilidad](https://github.com/r-wasm/quarto-live/issues/134).

## Datos y continuidad de los talleres

El ejercicio tiene un marco sintético de **12,000 clientes** con cuenta de
depósito a la vista y tarjeta de débito, y una muestra aleatoria simple de
**480 clientes sin reemplazo**. La observación corresponde a un cliente durante
septiembre de 2026: es un corte transversal de un mes. Ni el tamaño del marco
ni los importes representan cifras de una institución o del sistema financiero.

La comparación entre clientes con y sin abonos de nómina es observacional.
Una variable latente de estabilidad financiera interviene en el mecanismo de
simulación y puede explicar diferencias entre grupos y la relación entre
abonos y saldos. Una diferencia significativa o una pendiente positiva no
identifican por sí solas un efecto causal.

- `datos/muestra.csv`: variables observadas para participantes.
- `datos/poblacion_saldos.csv`: saldos del marco sintético para simular muestreo.
- `generar_datos.py`: mecanismo reproducible, semilla raíz **202609** (población 202609, muestra 202610 y actividad 202611) y validaciones.
- `docente/`: población, latentes, errores, resultados esperados y guía. No se incluyen
  en los recursos que los runtimes descargan. La separación es didáctica,
  no un control de acceso al repositorio.

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

Los tres lenguajes leen el mismo archivo. Las diferencias por nómina mantienen el orden
**con nómina menos sin nómina**, confianza de 95% y las mismas convenciones de
inferencia. Las diferencias de proporciones se expresan en **puntos porcentuales**.
Para Welch, Stata usa `unequal` (Satterthwaite), no su opción `welch`, que cambia
los grados de libertad. Las simulaciones Monte Carlo no producen las mismas
realizaciones entre lenguajes por compartir una semilla.

## Regenerar y trabajar localmente

Desde la raíz:

```bash
.venv/bin/python slides/taller-1/sesion-1/generar_datos.py
.venv/bin/python slides/taller-1/sesion-1/generar_figuras.py
.venv/bin/python slides/taller-1/sesion-1/exportar_codigo.py
```

Las figuras equivalentes en R se regeneran desde la carpeta de la sesión:

```bash
cd slides/taller-1/sesion-1
Rscript generar_figuras.R
```

Si editas los chunks del QMD, vuelve a ejecutar `exportar_codigo.py` para
actualizar los scripts descargables. No edites estos scripts derivados a mano.
Para ejecutar todos los laboratorios localmente, desde la carpeta de la sesión:

```bash
Rscript codigo/sesion-1.R
../../../.venv/bin/python codigo/sesion-1.py
```

La ruta correcta de Python desde esa carpeta es `../../..` hasta la raíz.
Si el entorno se instaló en otro sitio, usa su ejecutable Python. Los scripts
locales permiten impartir la sesión cuando la red bloquea los runtimes del
navegador. Para figuras reproducibles usa los generadores, que guardan SVG.
Para Stata, abre `codigo/sesion-1.do` en el editor de do-files con la carpeta de
la sesión como directorio de trabajo y ejecútalo desde tu instalación local.

## Editar la siguiente versión

El guion está en `index.qmd`, el diseño en `tema.scss` y las preguntas en HTML
con comportamiento en `interacciones.js`. Las animaciones están en
`animaciones.js` y `animaciones.css`. Cada laboratorio se escribe una sola
vez por lenguaje, dentro de un `.panel-tabset`. Las figuras reproducen datos
observados o modelos ilustrativos identificados en el guion. Al modificar parámetros, actualiza las cifras
narradas y la guía docente; las estadísticas de referencia se recalculan en
`docente/resumen.json`.

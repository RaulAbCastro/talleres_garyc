# Patrón técnico probado para Quarto Live

Referencia de este repositorio: Quarto 1.11.9, extensión `r-wasm/quarto-live`
descargada del tag v0.2.0, webR 0.6.0 y Pyodide 0.28.1. Son las versiones de la
primera sesión, no una exigencia para todos los proyectos ni una afirmación
sobre las últimas versiones disponibles. La extensión está versionada en
`slides/_extensions/r-wasm/live/`; su metadata upstream dice `0.1.3-dev` aunque
proviene de ese tag. Conservar la licencia y verificar compatibilidad al actualizar.

## Reutilizar la configuración

Partir del [QMD de la sesión 1](../../../slides/taller-1/sesion-1/index.qmd) y
adaptar título, footer, rutas, recursos y paquetes. Copiar a la sesión nueva
`tema.scss`, `interacciones.js` y `assets/live-bootstrap.js` si se conserva esa
estructura. La extensión se comparte desde `slides/`; no reinstalarla por sesión.

Este es el núcleo de la configuración; supone que existen los archivos indicados:

```yaml
engine: markdown
format:
  live-revealjs:
    theme: [default, tema.scss]
    width: 1280
    height: 800
    center: false
    slide-level: 2
    title-slide-attributes:
      data-visibility: hidden
    html-math-method:
      method: katex
      url: https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/
    include-after-body:
      text: '<script src="interacciones.js"></script>'
resources:
  - datos/muestra.csv
  - assets/live-bootstrap.js
  - interacciones.js
webr:
  resources: [datos/muestra.csv]
  cell-options:
    autorun: false
    max-lines: 6
    fig-width: 9
    fig-height: 3.2
    timelimit: 30
pyodide:
  packages: [numpy, pandas, scipy, matplotlib]
  resources: [datos/muestra.csv]
  cell-options:
    autorun: false
    max-lines: 6
    fig-width: 9
    fig-height: 3.2
    timelimit: 30
```

La portada manual es un encabezado `##`. Con esta combinación de versiones,
`title-slide: false` por sí solo no eliminó la portada automática; el atributo
`data-visibility: hidden` sí la excluyó de la navegación.

El módulo local contiene `export const liveBootstrap = true;`. Importarlo en
una celda OJS oculta **dentro de la primera slide**, después del primer `##`:

````markdown
```{ojs}
//| echo: false
//| output: false
import { liveBootstrap } from './assets/live-bootstrap.js'
```
````

El import explícito resuelve la inicialización OJS observada en Quarto reciente
([issue upstream](https://github.com/r-wasm/quarto-live/issues/134)). Colocar la
celda antes del primer encabezado generaba una slide inicial vacía. Mantener
este ajuste mientras sea necesario; reevaluarlo al actualizar la extensión.

Se eligió KaTeX porque en Quarto 1.11.9 el modo MathJax probado combinaba una
URL de MathJax 4 con un plugin que esperaba la API de MathJax 2. En KaTeX,
`url` es el **directorio** con barra final: Quarto agrega `katex.min.js` y
`katex.min.css`. Las fórmulas también dependen de la descarga inicial del CDN.

## Pestañas R/Python ejecutables y Stata para uso local

Usar `{webr}` y `{pyodide}` para ejecutar en el navegador. Los chunks `{r}` y
`{python}` convencionales ejecutados al compilar no ofrecen por sí solos este
editor interactivo. Ejemplo mínimo dentro de una slide:

````markdown
## Laboratorio · Explorar {.lab}

::: {.panel-tabset group="lenguaje"}
### R

```{webr}
#| exercise: explorar-r
d <- read.csv("datos/muestra.csv")
head(d, 4)
```

### Python

```{pyodide}
#| exercise: explorar-py
import pandas as pd
d = pd.read_csv("datos/muestra.csv")
print(d.head(4).to_string(index=False))
```

### Stata

Para ejecutar en Stata; no se ejecuta en el navegador.

```stata
import delimited "datos/muestra.csv", clear
list in 1/4
```
:::
````

Cada `exercise` debe ser único en todo el documento, incluidos ambos lenguajes.
Usar celdas autocontenidas: importar paquetes y leer los datos en cada una.
No depender del orden de ejecución de celdas ocultas de setup global.
El bloque `stata` es estático: no usar `{stata}`, que sugeriría un motor de
ejecución de Quarto. Mantener disponible copiar código y exportar los bloques a
un `.do` mediante `exportar_codigo.py`; el QMD sigue siendo la única fuente.
Documentar el directorio de trabajo local para que funcionen las rutas al CSV.

Declarar explícitamente los mismos CSV en `webr.resources` y `pyodide.resources`
además de los recursos de entrega. Esos archivos se copian a los sistemas de
archivos virtuales y conservan las rutas relativas. Añadir otros CSV según
necesidad; nunca usar un glob que incluya `docente/`.

Preferir R base para reducir descargas cuando cubra el ejercicio; declarar
paquetes R adicionales si la tarea los necesita. Para Python, instalar solo los
paquetes usados y comprobar que estén disponibles en Pyodide. Los paquetes del
Codespace y los del navegador son entornos distintos.

Run Code y Ctrl/Cmd+Enter ejecutan. Start Over restaura el código inicial de esa
celda; no promete reiniciar todo el runtime. Conservar `autorun: false` cuando
el objetivo sea que el auditorio prediga y ejecute deliberadamente.

## Hacer comparables los métodos

Usar el mismo CSV, nivel de confianza y orden del contraste. En la sesión 1,
la diferencia se expresa como **con nómina menos sin nómina**. Por defecto,
Stata resta el segundo grupo del primero; una variable `sin_nomina =
1 - recibe_nomina` pone primero a quienes sí reciben nómina.

```stata
import delimited "datos/muestra.csv", clear
generate byte sin_nomina = 1 - recibe_nomina
ttest saldo_promedio_miles, by(sin_nomina) unequal level(95)
prtest pago_debito, by(sin_nomina) level(95)
```

En Stata, `unequal` usa los grados de libertad de Satterthwaite, correspondientes
a `t.test(..., var.equal=FALSE)` de R y `ttest_ind(..., equal_var=False)` de
SciPy. La opción Stata `welch` cambia la fórmula de grados de libertad: no
añadirla por el nombre coloquial de la prueba. Consultar el
[manual de ttest](https://www.stata.com/manuals/rttest.pdf).

`prtest` utiliza el error estándar combinado bajo la hipótesis nula para el
contraste bilateral y el no combinado para el intervalo normal de la diferencia.
Igualar esa convención en R/Python y expresar diferencias de proporciones en
puntos porcentuales cuando se multipliquen por 100. Consultar el
[manual de prtest](https://www.stata.com/manuals/rprtest.pdf).

Para la regresión simple, `regress saldo_promedio_miles abonos_miles` incluye
intercepto; `predict double saldo_ajustado, xb` obtiene los valores ajustados y
`predict double residuo, residuals` obtiene los residuos. Mantener la misma
convención de errores estándar e intervalos en los tres lenguajes. Referencia:
[postestimación de regress](https://www.stata.com/manuals/rregresspostestimation.pdf).
Revisar estos comandos contra los manuales no equivale a haberlos ejecutado en
Stata: indicar por separado esa limitación si no está instalado.

## Animaciones didácticas

Reutilizar `animaciones.js` y `animaciones.css` si la sesión necesita muestreo,
cobertura de intervalos o elección de una recta. Declarar los archivos en los
recursos de entrega y cargar sus estilos y scripts desde el QMD. El estado de
la animación debe ser independiente del runtime R/Python y conservarse al
cambiar de pestaña. Usar botones y controles etiquetados, sin arrancar
animaciones al entrar a la slide; pausar al salir y respetar
`prefers-reduced-motion`. Mostrar las unidades y distinguir las poblaciones
ilustrativas del CSV de laboratorio. Para revisar nuevas animaciones, comprobar
avance, pausa, reinicio y valores extremos de sus controles.

## Renderizado y comprobación

Desde la raíz, sustituir N y M por la sesión:

```bash
quarto render slides/taller-N/sesion-M/index.qmd
quarto preview slides/taller-N/sesion-M/index.qmd --host 0.0.0.0 --port 4200 --no-browser
```

Si la caché de Quarto no es escribible, usar una ruta de caché permitida, como
hace `slides/render.sh`. Servir por HTTP: `file://` no permite cargar los módulos
y CSV de esta presentación. Conservar el HTML y todas sus dependencias al mover
una compilación; no es un archivo autocontenido.

En la prueba de navegador, esperar a que se habilite Run Code. Para capturas,
esperar el final de `fade` o desactivarlo solo durante la prueba. CodeMirror debe
probarse con selección y escritura reales; cambiar únicamente el DOM no prueba
que cambió el código que ejecutará el editor.

Las gráficas generadas por ambos runtimes usan `canvas` dentro de
`.cell-output-container`. El tema limita su tamaño conservando proporciones.
Revisar conjuntamente altura del editor, salida y panel: un histograma puede
haberse ejecutado bien y tener el eje inferior fuera del área visible. Ajustar
espacio o scroll según la longitud del laboratorio, sin reducir excesivamente
la letra para proyectar.

Si se automatiza la revisión, mantener vivo el servidor mientras navega el
browser. Un servidor temporal y el navegador bajo el mismo proceso de prueba
evitan depender de sesiones de terminal que podrían terminar entre llamadas.
No añadir dependencias del navegador al proyecto si solo se usaron para revisar.

Fuentes para cambios de API:
[Quarto reveal.js](https://quarto.org/docs/presentations/revealjs/),
[Quarto Live](https://r-wasm.github.io/quarto-live/other/slides.html) y
[módulos OJS](https://quarto.org/docs/interactive/ojs/code-reuse.html).

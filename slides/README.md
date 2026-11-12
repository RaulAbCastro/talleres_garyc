# Slides de los talleres GARyC

La primera sesión del Taller 1, **De la muestra a la inferencia**, está en
[`taller-1/sesion-1/index.qmd`](taller-1/sesion-1/index.qmd). Es una presentación
Quarto **reveal.js**, en español, para una sesión de aproximadamente una hora.
Toma la historia de Marginalia de `documents_overleaf/caso.tex` y el alcance de
la sesión 1 de `documents_overleaf/temario.tex`.

## Abrir y presentar

Desde la raíz del repositorio, con el entorno del Codespace ya instalado:

```bash
bash slides/render.sh preview
```

Abre el puerto **4200** en la pestaña **Ports** de Codespaces y entra en
`/taller-1/sesion-1/`. El proceso queda ejecutándose hasta pulsar `Ctrl+C`.
También está disponible la tarea **Slides: vista previa sesión 1** de VS Code.

Para compilar sin dejar abierto un servidor:

```bash
bash slides/render.sh
```

Se genera `slides/taller-1/sesion-1/index.html` con su carpeta de dependencias.
El HTML generado y sus dependencias no se versionan. No es un HTML autocontenido:
conserva las carpetas acompañantes, los CSV, `codigo/`, `assets/` e
`interacciones.js`. Para abrirlo usa Quarto Preview o un servidor HTTP; abrirlo
directamente con `file://` impide cargar módulos y datos.

Las flechas navegan, `Esc` abre la vista general y `S` las notas del expositor.
Las notas contienen tiempos, preguntas sugeridas y resultados de referencia.
Hay tres preguntas de opción múltiple con retroalimentación y seis laboratorios:

1. Explorar la muestra.
2. Repetir muestreo y cambiar tamaño muestral.
3. Comparar medias con Welch.
4. Comparar proporciones.
5. Calcular correlación y graficar.
6. Estimar regresión lineal simple.

## Pestañas R y Python ejecutables

Cada laboratorio tiene pestañas **R** y **Python** con un editor, **Run Code** y
**Start Over**. Los chunks `{webr}` y `{pyodide}` de
[Quarto Live](https://r-wasm.github.io/quarto-live/other/slides.html) ejecutan
R y Python mediante WebAssembly en el navegador. No necesitan un servidor de
R/Python ni envían el código a un kernel remoto. Cada celda vuelve a leer el
mismo CSV, de modo que no depende de haber ejecutado una celda anterior.
`Ctrl/Cmd+Enter` también ejecuta; Start Over restaura el código de la celda,
no reinicia todo el entorno de ejecución.

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

## Datos y continuidad del caso

Esta sesión agrega **supuestos didácticos** al caso: un marco de 12,000 clientes
elegibles con crédito activo de Capital y Valle y una muestra aleatoria simple
de 480 personas sin reemplazo. No representa a todo Marginalia. El caso describe
un piloto/invitaciones aleatorios; aquí se compara **uso observado**, no
asignación. La adopción depende de sofisticación financiera latente. Una
diferencia estadísticamente significativa no identifica por sí sola impacto.

- `datos/muestra.csv`: siete variables observadas para participantes.
- `datos/poblacion_tasas.csv`: tasas del marco sintético para simular muestreo.
- `generar_datos.py`: mecanismo reproducible, semilla **203101** y validaciones.
- `docente/`: potenciales, latente, resultados esperados y guía. No se incluyen
  en los recursos que los runtimes descargan. La separación es didáctica,
  no un control de acceso al repositorio.

La tasa anual se guarda en porcentaje (`18 = 18%`); sus diferencias van en
**puntos porcentuales**. El ingreso se guarda en miles de áureos al mes y cambio
de banco es 0/1. Ambos lenguajes leen el mismo archivo y producen las mismas
estimaciones deterministas. Una semilla igual no hace iguales las muestras
Monte Carlo de los dos lenguajes.

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

## Editar la siguiente versión

El guion está en `index.qmd`, el diseño en `tema.scss` y las preguntas en HTML
con comportamiento en `interacciones.js`. Cada laboratorio se escribe una sola
vez por lenguaje, dentro de un `.panel-tabset`. Las figuras de respaldo leen
solo los datos observados. Al modificar parámetros, actualiza las cifras
narradas y la guía docente; las estadísticas de referencia se recalculan en
`docente/resumen.json`.

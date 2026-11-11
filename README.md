# talleres_garyc

Materiales, diapositivas y código para el taller. El entorno de GitHub Codespaces
incluye R, Python, Jupyter, Quarto y LaTeX. Los archivos Stata se editan aquí y se
ejecutan mediante Conexión a Escritorio remoto en el Windows del banco.

## Empezar en Codespaces

1. Al crear un Codespace, espera a que termine `.devcontainer/setup.sh`.
2. Si acabas de añadir esta configuración a un Codespace existente, espera a que
   termine cualquier instalación y usa **Rebuild now**, o abre la paleta con
   `Ctrl+Shift+P` y ejecuta **Codespaces: Rebuild Container**.
3. Abre **Terminal > New Terminal** y ejecuta desde la raíz del repositorio:

   ```bash
   source .venv/bin/activate
   bash scripts/check-environment.sh
   ```

Las extensiones de Python, Jupyter, R, Quarto, LaTeX Workshop y sintaxis de Stata
se instalan con la configuración del contenedor. HTML ya tiene soporte en VS Code.
Si aún no reconstruyes, puedes instalarlas desde **Extensions** usando las
recomendaciones de este repositorio.

Para repetir la instalación manualmente:

```bash
bash .devcontainer/setup.sh
```

El script usa `sudo` para instalar paquetes de Ubuntu y descarga dependencias.
Puede tardar varios minutos la primera vez. La configuración se puede repetir;
las versiones de paquetes de Ubuntu siguen sus repositorios y los paquetes R de
CRAN pueden cambiar. `requirements.lock.txt` fija las dependencias de Python y
Quarto tiene versión y suma SHA-256 fijadas en `.devcontainer/quarto-version.env`.
TeX Live 2026 se instala mediante TinyTeX 2026.11; la versión y las sumas del
archivo oficial están fijadas en `.devcontainer/texlive-version.env`.

## Qué se instala

| Herramienta | Uso |
| --- | --- |
| Python 3.12 en `.venv/` | NumPy, pandas, SciPy, Matplotlib, seaborn, statsmodels, scikit-learn, openpyxl y pyreadstat |
| R de Ubuntu 24.04 | tidyverse, readxl, haven, broom, knitr, rmarkdown, reticulate y soporte de VS Code |
| JupyterLab y Notebook | Kernels `Python (talleres)` y `R (talleres)` |
| Quarto | Documentos y presentaciones; generación de HTML y PDF |
| TeX Live 2026 (TinyTeX 2026.11) | pdfLaTeX, XeLaTeX, latexmk, bibliografías con Biber y español |
| HTML | Edición en VS Code y servidor de vista previa en el puerto 8000 |
| Stata | Sintaxis de `.do` y `.ado`; ejecución en el servidor Windows del banco |

El Python global del Codespace puede tener otra versión. Activa `.venv/` o usa
`.venv/bin/python` para trabajar con los paquetes de este proyecto.

Si el editor muestra **«Se ha seleccionado un intérprete Python no válido»** al
abrir el Codespace, espera a que termine la detección de entornos. Si el aviso
continúa, abre `Ctrl+Shift+P` > **Python: Select Interpreter** y selecciona
`.venv` (Python 3.12). También puedes usar **Enter interpreter path** e introducir
`/workspaces/talleres_garyc/.venv/bin/python`. El intérprete de los notebooks se
elige por separado con **Select Kernel**.

## Primeras pruebas

Desde la raíz del repositorio:

```bash
# Python y R: regresión sencilla y gráficas en outputs/
.venv/bin/python code/examples/hola-python.py
Rscript code/examples/hola-r.R

# Quarto: documentos con código ejecutado
bash scripts/render-example.sh python html
bash scripts/render-example.sh python pdf
bash scripts/render-example.sh r html
bash scripts/render-example.sh r pdf

# LaTeX: prueba independiente de Overleaf
mkdir -p outputs
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=outputs code/examples/hola-latex.tex
```

Los resultados se guardan en `outputs/`, que no se sube a Git. Abre un PDF en el
explorador de VS Code para verlo con LaTeX Workshop.

Si durante la primera instalación apareció **R Language Server ... exit code
10**, el editor arrancó antes de que estuviera instalado `languageserver`.
Una vez que la comprobación anterior termine correctamente, ejecuta
**Developer: Reload Window** desde la paleta. La biblioteca de paquetes de R
del proyecto ya está configurada en `.vscode/settings.json`.

Para trabajar con R interactivamente, abre un archivo `.R`, ejecuta **R: Create R
terminal** en la paleta y usa `Ctrl+Enter` para enviar una línea o selección.

### Jupyter Notebooks

Abre `code/examples/hola-python.ipynb` o `code/examples/hola-r.ipynb`. En
**Select Kernel**, elige `Python (talleres)` o `R (talleres)` y pulsa **Run All**.
Si aparece otra selección, usa **Select Another Kernel** y busca el entorno
`.venv` o los kernels de Jupyter.

También puedes abrir JupyterLab completo:

```bash
.venv/bin/jupyter lab --no-browser --ip=0.0.0.0 --port=8888
```

En la pestaña **Ports**, abre el puerto 8888 en el navegador. Jupyter muestra un
token de sesión en la terminal; úsalo si te pide iniciar sesión. Conserva la
visibilidad del puerto en **Private**.

### HTML y vista previa de Quarto

```bash
# Abre el puerto 8000 desde la pestaña Ports
.venv/bin/python -m http.server 8000 --bind 0.0.0.0 --directory website

# En otra terminal, con .venv activado; abre el puerto 4200
quarto preview code/examples/hola-python.qmd --host 0.0.0.0 --port 4200 --no-browser
```

Cada servidor permanece ejecutándose en su terminal hasta pulsar `Ctrl+C`.
En **Terminal > Run Task** también encontrarás las tareas de comprobación,
JupyterLab, HTML y renderizado de ejemplos de Quarto.

## Conectar el puntero de Overleaf

El submódulo `documents_overleaf/` ya apunta al proyecto correcto. GitHub guarda
el identificador de un commit; los documentos viven en Overleaf, que sigue
siendo su fuente de verdad. La instalación general no intenta autenticarlo.

El puntero guarda una revisión concreta; no se sincroniza automáticamente con
Overleaf. `init` descarga esa revisión guardada en GitHub. `pull` trae la versión
actual de Overleaf, con sus archivos e imágenes nuevos. `check` muestra tanto la
revisión de Overleaf como la copia local y avisa si difieren.

1. Abre tu proyecto en Overleaf y busca **Integrations > Git**. Según el diseño,
   también puede aparecer en **Menu > Git**.
2. Si puedes ver una dirección que empieza por `https://git.overleaf.com/`, tienes
   acceso a la integración. Si aparece una solicitud de mejora de plan, revisa
   si tu institución ofrece Overleaf Commons o una suscripción con esta función.
3. En **Account Settings > Git Integration**, crea un token. No lo pegues en el
   chat, en archivos del repositorio ni dentro de una URL.
4. Guarda el token como secret de **Codespaces** con nombre `OVERLEAF` y da acceso
   a `RaulAbCastro/talleres_garyc`. También se aceptan los nombres
   `OVERLEAF_GIT_TOKEN` y `OVERLEAF_TOKEN`.
5. Si lo acabas de crear, abre la paleta con `Ctrl+Shift+P`, ejecuta
   **Codespaces: Stop Current Codespace** y vuelve a abrir este mismo Codespace
   desde GitHub. Los nuevos secrets se cargan al reiniciar; cerrar la terminal
   por sí solo no basta.
6. En una terminal del Codespace ejecuta:

   ```bash
   bash scripts/overleaf.sh check
   bash scripts/overleaf.sh init
   ```

   `check` verifica la autenticación y compara revisiones sin cambiar archivos ni el puntero. `init`
   descarga exactamente la revisión a la que apunta este repositorio. El script
   usa el secret sin mostrarlo ni guardarlo. Si no hay ningún secret disponible,
   puede pedir el token de forma oculta en una terminal interactiva.

   La carpeta `build/` que puede generar LaTeX Workshop dentro del submódulo se
   excluye localmente de Git para evitar incluir archivos de compilación.

Para consultar el estado o traer la versión más reciente:

```bash
bash scripts/overleaf.sh status
bash scripts/overleaf.sh pull
git diff --submodule
```

`pull` usa el mismo secret y actualiza el puntero local. Revisa y guarda ese cambio
con Git cuando corresponda; no se publica automáticamente. No contiene un comando
para sobrescribir cambios locales o remotos. GitHub documenta la carga de secrets
al reiniciar en su [guía de secrets de Codespaces](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-your-account-specific-secrets-for-github-codespaces).

Después de descargar el submódulo puedes compilar los documentos existentes:

```bash
# Desde la raíz del repositorio: traer primero los cambios de Overleaf
bash scripts/overleaf.sh pull

# Compilar un documento o los tres con pdfLaTeX y TeX Live 2026
bash scripts/render-overleaf.sh recursos
bash scripts/render-overleaf.sh caso
bash scripts/render-overleaf.sh all
```

`temario.tex`, `recursos.tex` y `caso.tex` utilizan pdfLaTeX, el estilo compartido
`garyc.sty` y el logo en `img/`. Los PDF se generan en `documents_overleaf/build/`,
que usa el visor del editor, y se copian también a `outputs/overleaf/`.
LaTeX Workshop tiene seleccionada la receta **pdfLaTeX (TeX Live 2026)**. En
**Terminal > Run Task** también puedes compilar recursos o los tres documentos.

Si faltan `caso.tex`, el logo o la portada, comprueba las revisiones con
`bash scripts/overleaf.sh check`: una copia antigua puede compilar correctamente
y aun así producir un diseño anterior. Después de `pull`, el cambio del puntero
se guarda en GitHub con un commit del repositorio principal.

La [integración Git de Overleaf](https://docs.overleaf.com/integrations-and-add-ons/git-integration-and-github-synchronization/git-integration)
requiere una suscripción que incluya esa función y utiliza tokens. Si tu cuenta
no tiene acceso, puedes seguir editando y compilando en el navegador de Overleaf;
el puntero no descargará archivos sin acceso a Git.

## Stata mediante el Windows remoto del banco

Aquí puedes editar `code/examples/hola-stata.do` y tus demás archivos `.do`.
Para ejecutarlos, abre **Conexión a Escritorio remoto** desde tu equipo y usa
Stata en el Windows del banco. Lleva los archivos de código al servidor mediante
el procedimiento de transferencia que uses allí.

Con el acceso por Escritorio remoto descrito, el Codespace no tiene una licencia
local de Stata ni un canal para ejecutarlo en el servidor. Por ello no se
registra un kernel de Stata ni se instala PyStata como si fuera Stata.
[PyStata requiere una instalación de Stata 17 o posterior](https://www.stata.com/python/pystata19/install.html).
Si el banco proporciona más adelante acceso SSH permitido y disponible desde
Codespaces, se podrá configurar la ejecución remota.

Python puede leer y escribir archivos `.dta` con pandas/pyreadstat, y R con haven,
sin ejecutar Stata.

## Guardar la configuración y cerrar el Codespace

Los cambios de configuración y los ejemplos son archivos del repositorio. Para
conservarlos en GitHub, revísalos y haz commit/push desde **Source Control**.
Los entornos `.venv/` y `.local/`, los resultados y las credenciales están
excluidos de Git y se recrean cuando corresponde.

Cuando termines, detén el Codespace desde GitHub. Puedes volver a abrirlo luego.
La [configuración de dev containers](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers)
permite que otros Codespaces instalen este mismo conjunto de herramientas una
vez que hayas guardado estos archivos en GitHub.

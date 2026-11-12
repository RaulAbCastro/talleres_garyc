---
name: crear-presentaciones-quarto
description: "Crear o adaptar diapositivas de los talleres GARyC en Quarto/reveal.js, basadas en el caso de Marginalia, con datos sintéticos y pestañas de código R/Python ejecutables en el navegador. Usar al preparar sesiones o modificar sus laboratorios interactivos."
---

# Crear presentaciones interactivas de los talleres

Crear una sesión que el auditorio pueda seguir, ejecutar y discutir. Usar la
sesión 1 como implementación de referencia; adaptar la historia, los métodos,
la duración y los lenguajes al encargo, sin fijar su número de diapositivas o
laboratorios para todos los talleres.

## Uso con cualquier asistente

Esta guía es un documento Markdown independiente del modelo y del proveedor de
IA. El encabezado `name`/`description` solo identifica la guía; no requiere una
API, cuenta o integración de una compañía concreta.

Para aplicarla, pedir al asistente que lea este archivo y siga sus referencias.
Si la herramienta no admite cargar skills, proporcionar el texto como
instrucciones junto con los archivos del repositorio que necesite. Las rutas
relativas de los enlaces parten del archivo que los contiene; las rutas de los
comandos parten de la raíz del repositorio.

Usar las herramientas disponibles para leer y editar archivos, ejecutar comandos
y revisar el navegador. Cuando alguna capacidad falte, entregar los archivos o
cambios propuestos y los comandos para ejecutarlos, indicando qué verificaciones
siguen pendientes. Distinguir siempre el código generado de los resultados
efectivamente ejecutados. Las presentaciones usan Quarto, R y Python; su
funcionamiento no depende del modelo que ayude a prepararlas.

## Fuentes y alcance

Trabajar desde la raíz del repositorio. Antes de escribir el guion, leer:

- [caso.tex](../../documents_overleaf/caso.tex): mundo ficticio, instituciones,
  medidas, cronología y trampas de selección.
- [temario.tex](../../documents_overleaf/temario.tex): alcance de la sesión y
  temas que se reservan para después.
- [slides/README.md](../../slides/README.md): entorno, comandos y entrega.
- [Sesión 1](../../slides/taller-1/sesion-1/index.qmd): ejemplo funcional de
  guion, notas del expositor, cuestionarios y laboratorios bilingües.

Los documentos de Overleaf son la fuente narrativa; no cambiarlos para acomodar
una simulación. Si faltan, revisar el estado del submódulo y señalar qué fuente
no se pudo consultar. Distinguir los hechos del caso de los supuestos nuevos
(regiones concretas del piloto, tamaños, parámetros y fechas adicionales).

## Construir una historia que enseñe el método

Elegir una pregunta de la UARC y una medida del caso que permitan aprender los
temas solicitados. Organizar la sesión en intuición, formalización útil y
práctica. Alternar explicaciones breves con predicciones del auditorio,
laboratorios y lectura de resultados. Incluir notas con tiempos y preguntas
para el expositor; el total debe ajustarse a la duración del temario.

Cada laboratorio debe plantear una decisión observable: modificar un parámetro,
contrastar una hipótesis, comparar estimaciones o justificar una interpretación.
Cerrar con un producto breve, como un memo para la UARC. Si se incorpora IA,
pedir ejecución y verificación de sus resultados, con alternativa para quien
no tenga un asistente disponible.

No confundir selección de la muestra, asignación de una intervención y uso
efectivo. Interpretar diferencias, correlaciones y pendientes de acuerdo con el
diseño; un valor p pequeño no identifica por sí solo un efecto causal. Mantener
explícitos población de referencia, unidad de observación, horizonte,
denominadores y unidades, especialmente porcentajes frente a puntos porcentuales.

## Preparar datos y cálculos reproducibles

Guardar la nueva sesión en `slides/taller-N/sesion-M/`. Mantener como fuentes
el QMD, generadores, estilos y scripts de interacción. Reutilizar el diseño y
las utilidades existentes cuando corresponda; no copiar datos y cifras de la
sesión 1 si la pregunta o la población cambian.

- Generar datos con semilla fija y documentar el mecanismo, los supuestos y el
  significado de cada variable. Validar identificadores, valores faltantes,
  rangos y relaciones relevantes para el diseño.
- Hacer que R y Python lean **el mismo CSV observado**. Una semilla igual en
  ambos lenguajes no garantiza las mismas realizaciones aleatorias.
- Guardar latentes y resultados potenciales en `docente/`, fuera de los recursos
  cargados por las slides. Esta separación es didáctica, no un control de acceso
  al repositorio.
- Calcular resultados de referencia sobre los archivos realmente distribuidos.
  Igualar entre lenguajes el orden del contraste, método de inferencia, nivel de
  confianza, tratamiento de faltantes y correcciones que aplique cada función.
- Generar las gráficas en los lenguajes pedidos. Mantener figuras precalculadas
  para la exposición cuando la red impida arrancar los entornos del navegador.
  Etiquetar ejes, grupos y unidades; fijar ejes cuando sea necesario comparar
  simulaciones con distintos parámetros.

Cuando cambien datos o código, actualizar conjuntamente las cifras narradas,
figuras, scripts descargables y referencias docentes. El QMD es la fuente del
código de los laboratorios; adaptar `exportar_codigo.py` para extraer sus
versiones locales sin mantener copias editadas a mano.

## Implementar la presentación

Para crear una sesión o modificar la ejecución interactiva, leer
[references/quarto-live.md](references/quarto-live.md). Contiene la configuración
probada, el patrón de pestañas y las particularidades de OJS y KaTeX.

Conservar la identidad visual de `tema.scss`: azul `#1B2A4A`, verde azulado
`#007279` para Taller 1 y ámbar `#B26A00` para referencias. Para otros talleres,
consultar sus colores en `documents_overleaf/garyc.sty`. Usar tipografías del
sistema, títulos legibles y espacio suficiente para código y resultados.

Los cuestionarios existentes usan `.quiz`, botones con `data-correct` y
`data-feedback`, y un contenedor `.quiz-feedback` con `aria-live="polite"`.
Reutilizar `interacciones.js` para su comportamiento y la protección del teclado
al editar código. Evitar que flechas o espacio dentro del editor avancen slides.

## Verificar y entregar

Compilar la sesión y, si se modifica código, ejecutar los bloques afectados en
R y Python para comparar resultados deterministas con tolerancia numérica.
Las simulaciones se comparan por su comportamiento esperado, no por igualdad
de realizaciones entre lenguajes.

Para una sesión nueva o cambios de interactividad, abrir el HTML mediante HTTP
y comprobar en navegador: pestañas, ejecución de ambos lenguajes, edición real,
restauración con Start Over, gráficas y feedback de cuestionarios. Una
compilación exitosa no prueba que webR/Pyodide hayan arrancado. Si no se pudo
comprobar algún punto, describirlo como pendiente en la entrega.

Revisar capturas después de terminar la transición de reveal.js. Comprobar
también la salida tras ejecutar: ejes, etiquetas y conclusiones deben poder
leerse; usar scroll donde haga falta y evitar confundirlo con contenido perdido.

Registrar la nueva ruta en `slides/_quarto.yml` y documentar cómo compilarla y
abrirla. `slides/render.sh` y las tareas actuales apuntan específicamente a la
sesión 1: no presentarlos como comandos de una sesión nueva sin adaptarlos.
Mantener excluidos HTML generado, `*_files/`, cachés y archivos temporales.
Versionar los fuentes, datos sintéticos distribuibles y figuras de respaldo.

Al entregar, enlazar el QMD y las instrucciones, resumir lo verificado y explicar
que la primera carga de los runtimes requiere internet. Para abrir desde otra
computadora, usar la URL reenviada del puerto en Codespaces; ese acceso depende
de que sigan activos el Codespace y el servidor. Un enlace permanente requiere
una publicación aparte.

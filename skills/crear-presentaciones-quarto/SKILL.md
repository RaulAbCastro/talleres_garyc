---
name: crear-presentaciones-quarto
description: "Crear o adaptar diapositivas de los talleres GARyC en Quarto/reveal.js con casos bancarios cotidianos, datos sintéticos, animaciones explicativas, pestañas R/Python ejecutables y código Stata para uso local. Usar al preparar sesiones o modificar sus laboratorios interactivos."
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
efectivamente ejecutados. Las presentaciones usan Quarto, R, Python y Stata; su
funcionamiento no depende del modelo que ayude a prepararlas.

## Fuentes y alcance

Trabajar desde la raíz del repositorio. Antes de escribir el guion, leer:

- [temario.tex](../../documents_overleaf/temario.tex): alcance de la sesión y
  temas que se reservan para después.
- [slides/README.md](../../slides/README.md): entorno, comandos y entrega.
- [Sesión 1](../../slides/taller-1/sesion-1/index.qmd): ejemplo funcional de
  guion, notas del expositor, cuestionarios y laboratorios en tres lenguajes.
- [Referencia del Banco de Inglaterra](../../referencias/slides-de-referencia/10_11_26_Causal_Econometrics_Intro.pdf):
  Angus Foulis, *Introduction: Econometrics With Microdata*, Centre for Central
  Banking Studies, 10 de noviembre de 2026, diapositivas 1–17.
- [caso.tex](../../documents_overleaf/caso.tex): antecedente narrativo de la
  primera versión. Su historia futurista dejó de ser la base de las slides.

La directriz vigente es trabajar con **situaciones bancarias cotidianas y datos
sintéticos**. La sesión 1 se concentra en **cuentas de depósito a la vista**:
SPEI recibidos/enviados, depósitos y retiros por canal, y pagos con débito.
Dejar crédito fuera de este caso salvo que el usuario cambie el alcance. Las preguntas deben ser verosímiles, pero los
registros, cifras, bancos y resultados simulados no se deben presentar como
evidencia real. No conservar personajes, monedas o intervenciones futuristas.
No modificar documentos de Overleaf fuera del alcance solicitado. Si faltan,
revisar el submódulo e indicar qué fuente no se pudo consultar.

Para describir actividad de una cuenta, distinguir entradas y salidas y separar
conteos de operaciones, importes y saldo promedio. Considerar ventanilla, cajero
y comisionista en ambos sentidos; conservar categorías de otros movimientos sin
presentar el catálogo como exhaustivo. Nómina es un origen del abono, no un canal
que se suma de nuevo. No contar retiros como pagos con débito ni volver a sumar
los totales junto con sus componentes. Documentar si se modela una cuenta por
cliente y si el dataset es un agregado mensual o un libro conciliado.

## Construir una historia que enseñe el método

Elegir una pregunta bancaria y una unidad de observación que permitan aprender
los temas solicitados. Organizar la sesión en intuición, formalización útil y
práctica. Alternar explicaciones breves con predicciones del auditorio,
laboratorios y lectura de resultados. Incluir notas con tiempos y preguntas
para el expositor; el total debe ajustarse a la duración del temario.

Redactar un argumento conectado, con mayor profundidad técnica cuando el tema
lo requiera. Cada diapositiva debe explicar cómo la pregunta lleva a un parámetro,
por qué se elige el método y cómo se interpreta el resultado. Usar párrafos breves
y transiciones explícitas; reservar viñetas para pasos o comparaciones que las
necesiten. No reducir las explicaciones a nombres de conceptos o frases aisladas.
Definir los símbolos de cada fórmula, traducirla al caso y vincularla con el
código. Separar supuestos, propiedades del estimador e interpretaciones causales.

**Explicar antes de usar.** En la primera aparición de cada concepto, dar su
significado en palabras y en el caso; después presentar su nombre, símbolo o
sigla. Una definición en notas del expositor no sustituye una explicación visible.
Auditar también títulos, etiquetas, botones, leyendas, feedback y salidas del
código: ninguno debe exigir un concepto que se explica en una slide posterior.
Los títulos de la agenda pueden anunciar temas si la pregunta que los acompaña
permite entender qué se aprenderá, sin exigir conocer el método.

En particular, desarrollar «mínimos cuadrados ordinarios (MCO)» antes de usar
la sigla. Una animación previa puede mostrar residuos y buscar su menor suma de
cuadrados con etiquetas descriptivas. Definir DE, EE/SE, IC, grados de libertad,
promedio condicional y R² antes de pedir su interpretación. Revisar dependencias
de los laboratorios: primero significado del resultado y supuestos, luego código.
Si falta una explicación, incorporarla o reordenar el bloque; no cubrir el salto
solo con un glosario final ni quitar profundidad técnica o temas del syllabus.

En la sesión 1, seguir el orden acordado: **pruebas de hipótesis → comparación
de medias y proporciones → correlación → regresión lineal simple**. Introducir
muestreo, error estándar e intervalos dentro del bloque de hipótesis para explicar
su funcionamiento. Si la profundidad exige más tiempo, mantener todos los temas
y distinguir la práctica complementaria de la ruta central; no prometer que todos
los ejercicios caben en una hora sin asignarles tiempo.

Cada laboratorio debe plantear una decisión observable: modificar un parámetro,
contrastar una hipótesis, comparar estimaciones o justificar una interpretación.
Cerrar con un producto breve, como una nota de análisis para el equipo. Si se incorpora IA,
pedir ejecución y verificación de sus resultados, con alternativa para quien
no tenga un asistente disponible.

No confundir selección de la muestra, asignación de una intervención y uso
efectivo. Interpretar diferencias, correlaciones y pendientes de acuerdo con el
diseño; un valor p pequeño no identifica por sí solo un efecto causal. Mantener
explícitos población de referencia, unidad de observación, horizonte,
denominadores y unidades, especialmente porcentajes frente a puntos porcentuales.

Tomar de Foulis la progresión didáctica, sin copiar sus textos ni gráficos:

1. Plantear una pregunta concreta y posibles mecanismos antes de la ecuación.
2. Distinguir población y muestra, parámetro y estimación, error y residuo.
3. Visualizar la elección de una recta y las distancias verticales antes de
   introducir el criterio de mínimos cuadrados y su fórmula.
4. Explicar el método y después sus condiciones; traducir `E[u|X] = 0` a una
   pregunta sobre factores omitidos. La media cero de los residuos de MCO con
   intercepto es una propiedad mecánica y no verifica esa condición.
5. Cerrar con una explicación alternativa plausible y los límites causales del
   resultado, reservando los métodos posteriores para su sesión.

Dar crédito a la referencia cuando se use. Mantener los temas y el tiempo del
temario propio; la referencia guía la explicación, no sustituye el alcance.
No omitir temas para acomodar la referencia. En la sesión 1 deben aparecer
hipótesis, comparación de medias y proporciones, correlación y regresión
lineal simple, en una progresión de lo simple a lo complejo. Registrar su
cobertura en la guía docente y distinguir el núcleo de los ejercicios opcionales.

## Preparar datos y cálculos reproducibles

Guardar la nueva sesión en `slides/taller-N/sesion-M/`. Mantener como fuentes
el QMD, generadores, estilos y scripts de interacción. Reutilizar el diseño y
las utilidades existentes cuando corresponda; no copiar datos y cifras de la
sesión 1 si la pregunta o la población cambian.

- Generar datos con semilla fija y documentar el mecanismo, los supuestos y el
  significado de cada variable. Validar identificadores, valores faltantes,
  rangos y relaciones relevantes para el diseño.
- Hacer que R, Python y el código Stata lean **el mismo CSV observado**. Una
  semilla igual no garantiza las mismas realizaciones entre lenguajes.
- Guardar latentes y errores de simulación en `docente/`, fuera de los recursos
  cargados por las slides. Esta separación es didáctica, no un control de acceso
  al repositorio. Incluir resultados potenciales solo si el diseño los necesita.
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

Cada laboratorio incluye pestañas R, Python y Stata. R/Python usan editores
ejecutables en el navegador; Stata usa un bloque estático copiable y una descarga
`.do`, con aviso visible de ejecución local. No simular un botón Run de Stata
ni afirmar que se ejecutó sin haber usado una instalación de Stata.

Las animaciones deben explicar una transformación: muestrear, acumular intervalos
o cambiar una recta y sus residuos. Ofrecer controles para avanzar, pausar y
reiniciar; evitar reproducción automática y respetar movimiento reducido.
Mantener ejes y escalas comparables y una semilla fija cuando haya azar. Si la
animación usa una población ilustrativa distinta del CSV, indicarlo junto a la
figura. Una animación no sustituye el cálculo reproducible en R/Python.

## Verificar y entregar

Compilar la sesión y, si se modifica código, ejecutar los bloques afectados en
R y Python para comparar resultados deterministas con tolerancia numérica.
Las simulaciones se comparan por su comportamiento esperado, no por igualdad
de realizaciones entre lenguajes.
Revisar la sintaxis y opciones de Stata contra su documentación oficial; si no
hay Stata disponible, reportar que su ejecución queda sin verificar.

Para una sesión nueva o cambios de interactividad, abrir el HTML mediante HTTP
y comprobar en navegador: pestañas, ejecución de ambos lenguajes, edición real,
restauración con Start Over, gráficas y feedback de cuestionarios. Una
compilación exitosa no prueba que webR/Pyodide hayan arrancado. Si no se pudo
comprobar algún punto, describirlo como pendiente en la entrega.
Comprobar también que Stata se puede leer/copiar, que el `.do` corresponde al
QMD y que los controles de animación funcionan con teclado y movimiento reducido.

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

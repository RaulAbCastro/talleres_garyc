# Guía docente — Taller 1, sesión 1

Versión inicial basada en `caso.tex` y sesión 1 de `temario.tex`. Duración:
60 minutos. Las notas del QMD contienen el ritmo y las preguntas por slide.
Los números siguientes corresponden a la semilla 203101 y la muestra guardada.

## Historia y alcance

La UARC recibe los primeros datos de uso del Agente Ciudadano. Debe separar
descripción, incertidumbre y validez causal. El piloto del caso es aleatorizado;
esta sesión analiza uso endógeno, sin mostrar asignación ni invitaciones.
Capital y Valle, N=12000 y n=480 son supuestos del ejercicio. Muestreo aleatorio
no implica adopción aleatoria. No atribuir los resultados a toda la población
de Marginalia ni afirmar que esta tabla estima un ITT.

La muestra tiene una observación por persona: no se modelan clusters, impago,
respuestas de precios de los bancos ni múltiples créditos de una misma persona.
La inferencia omite corrección por población finita (fracción de muestreo 4%).
La regresión usa errores estándar OLS convencionales como repaso introductorio;
sus supuestos merecen revisión y la sesión 12 incorpora errores robustos y
dependencia. Una recta descriptiva no debe leerse como modelo causal correcto.

## Resultados de referencia

| Cantidad | Resultado |
|---|---:|
| Usuarios / no usuarios | 216 / 264 |
| Tasa media usuarios / no usuarios | 19.282964% / 22.684128% |
| Diferencia usuarios − no usuarios | −3.401164 pp |
| IC95 Welch | [−4.025712, −2.776615] pp |
| Valor p Welch, bilateral | 5.205812e−24 |
| Cambios usuarios / no usuarios | 60/216 / 23/264 |
| Proporción cambio usuarios / no usuarios | 27.777778% / 8.712121% |
| Diferencia de proporciones | 19.065657 pp |
| IC95 Wald no agrupado | [12.191691, 25.939622] pp |
| Valor p z agrupada, bilateral, sin corrección | 3.907321e−8 |
| Correlación Pearson ingreso–tasa | −0.627154 |
| Intercepto / pendiente | 27.162729 / −0.278019 |
| IC95 de la pendiente, OLS convencional | [−0.309051, −0.246987] |
| R² | 0.393323 |
| Media del marco / de la muestra | 21.019145% / 21.153604% |

En el laboratorio de muestreo, cambiar n=40 a n=200 reduce aproximadamente la
DE de las medias por un factor de √5. La realización concreta es distinta en R
y Python. El eje fijo 18–24 facilita comparar las distribuciones.

## Un memo posible

En la muestra de 480 clientes de Capital y Valle, los usuarios del Agente
presentan una tasa anual media 3.40 pp menor que los no usuarios (IC95 Welch:
−4.03 a −2.78 pp; p<0.001). Cambió de banco el 27.8% de 216 usuarios y el 8.7%
de 264 no usuarios, una diferencia de 19.1 pp (IC95: 12.2 a 25.9 pp). El ingreso
y la tasa muestran correlación −0.627; la recta descriptiva asocia 1000 áureos
más de ingreso mensual con −0.278 pp de tasa. Estas asociaciones no identifican
el impacto causal del Agente: el uso puede depender de sofisticación financiera
y necesitamos recuperar el mecanismo de asignación/invitación y definir el
estimando antes de recomendar expansión.

## Lo que sabe el simulador

`poblacion.csv` contiene los resultados potenciales y la sofisticación latente.
El efecto individual de uso sobre la tasa se fijó en **−1.5 pp** para todas las
personas. En el marco completo:

    diferencia observada = efecto sobre usuarios + selección
             −3.499180 =              −1.500000 + −1.999180 pp

La diferencia muestral añade variabilidad de muestreo. Conservar esta verdad
para la sesión 3; no aparece en los recursos del HTML del participante.
El repositorio permite inspeccionarla: la separación de carpetas es pedagógica.

## Criterios para retroalimentación

- Escribe usuarios menos no usuarios y conserva el signo.
- Distingue puntos porcentuales de variación relativa porcentual.
- No interpreta p como probabilidad de que H0 sea cierta.
- No usa “no rechazar” para demostrar equivalencia.
- No atribuye causalidad a correlación, R² o pendiente sin un diseño.
- Reporta denominadores, población de referencia e incertidumbre.
- Ejecuta el código propuesto por IA y coteja al menos un resultado.

Si la red impide cargar los runtimes, usar scripts locales y figuras SVG.
No pedir una cuenta de IA para completar el ejercicio: se puede redactar el
memo con los resultados de los laboratorios.

# Sesión 2 · Resultados Potenciales y Sesgo de Selección

## Pregunta central

¿Cuánto reduce el estado de cuenta estandarizado (ECE) los intereses que pagan los clientes de tarjeta de crédito?

## Objetivos

Al final de esta sesión, los participantes podrán:

1. **Entender resultados potenciales:** para cada persona hay dos versiones (con y sin intervención), pero solo una ocurre.
2. **Identificar el problema fundamental:** no podemos medir el efecto individual porque falta el contrafactual.
3. **Descomponer diferencias observadas:** separar el efecto verdadero del sesgo de selección.
4. **Reconocer fuentes de confusión:** cómo una característica oculta crea sesgo.
5. **Valorar aleatorización:** por qué el azar resuelve el problema de sesgo de selección.

## Contenido

| Bloque | Tiempo | Tema |
|--------|--------|------|
| 1 | 0–5 min | **Gancho:** tres comparaciones tentadoras |
| 2 | 5–20 min | **Resultados potenciales:** contrafactuales y la ecuación Y = D·Y₁ + (1–D)·Y₀ |
| 3 | 20–35 min | **"Tabla de Dios":** ATE, ATT y la diferencia observada |
| 4 | 35–50 min | **Sesgo de selección:** un mapa causal mínimo y dos formas de cerrar la puerta trasera |
| 5 | 50–57 min | **Aleatorización:** cómo el sorteador desacopla confusión de asignación |
| 6 | 57–60 min | **Cierre:** quiz y minuto de papel |

## Datos

- **Población:** 500 clientes sintéticos de tarjeta de crédito
- **Muestra:** 100 clientes seleccionados al azar (semilla 202610)
- **Variable de resultado:** Intereses pagados en septiembre 2026 (pesos)
- **Variable de tratamiento:** 1 si solicitó ECE, 0 si no
- **Variable latente:** Atención financiera (no observada, solo en docente/)

**Archivo principal:** `datos/muestra.csv`

Columnas:
- `id_cliente`: identificador (1 a 100)
- `intereses`: resultado observado (pesos)
- `recibio_ece`: 1 si solicitó, 0 si no

## Notas de docente

Parámetros de referencia (no compartir con participantes):

```json
{
  "ATE_verdadero": -31.32,
  "ATT_verdadero": -25.23,
  "Sesgo_seleccion": -40.55
}
```

Estos valores están en `docente/parametros.json`.

La diferencia observada en la muestra es: 180.27 - 244.08 = **-63.81 pesos**.

Esta diferencia se descompone aproximadamente así:
- ATT (efecto verdadero): ~-25 pesos
- Sesgo de selección: ~-39 pesos

Aproximadamente el 61% de lo que vemos es sesgo; el 39% es efecto verdadero.

## Código y laboratorios

Tres lenguajes ejecutan el mismo análisis sobre `datos/muestra.csv`:

- `codigo/sesion-2.R`: R con ggplot2 y tidyverse
- `codigo/sesion-2.py`: Python con pandas, scipy y matplotlib
- `codigo/sesion-2.do`: Stata (no se ejecuta en navegador; es copiable para uso local)

Todos:
1. Cargan `datos/muestra.csv`
2. Calculan diferencia de medias observada
3. Corren prueba t de Welch
4. Grafican distribuciones

## Compilación y visualización

Desde la raíz del repositorio:

```bash
# Generar datos (si no existen)
cd slides/taller-1/sesion-2
source ../../../.venv/bin/activate
python generar_datos.py

# Compilar la presentación
cd ../..
quarto render taller-1/sesion-2/index.qmd

# Vista previa en navegador
quarto preview taller-1/sesion-2/index.qmd --host 0.0.0.0 --port 4200 --no-browser
```

La presentación usa Quarto Live (webR y Pyodide) para ejecución en navegador.

## Referencias pedagógicas

- Rubin, Donald B. (1974). "Estimating causal effects of treatments in randomized and nonrandomized studies." *Journal of educational Psychology*, 66(5), 688.
- Angrist & Pischke (2009). *Mostly harmless econometrics*. Cap. 1–2.
- Imbens & Wooldridge (2009). "Recent developments in the econometrics of program evaluation." *Journal of Economic Literature*.

## Validación

Verificar antes de usar con participantes:

- [ ] Datos generados (`datos/muestra.csv` existe y tiene 100 filas)
- [ ] QMD compila sin errores
- [ ] WebR y Pyodide se cargan en navegador
- [ ] Los laboratorios de R y Python producen tablas y gráficas
- [ ] Los números reportados coinciden con docente/parametros.json (dentro de tolerancia muestral)
- [ ] Stata .do se puede copiar e interpretar

## Notas técnicas

- Semilla de población: 202609 (500 clientes)
- Semilla de muestreo: 202610 (selecciona 100 de los 500)
- El efecto del ECE en la población verdadera es **negativo**: reduce intereses.
- La autoselección es **positiva**: quiénes lo piden ya tenían intereses más bajos.
- El sesgo de selección es **negativo y grande**: supera el efecto verdadero en la diferencia observada.

## Próxima sesión

Sesión 3 introuc ción a métodos de control: regresión simple, estratificación y matching para recuperar el efecto en datos observacionales.

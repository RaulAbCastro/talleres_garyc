# Sesión 2: Resultados Potenciales y Sesgo de Selección
# R · Laboratorio comparación de grupos

# Cargar datos
datos <- read.csv("datos/muestra.csv")
head(datos)

# Estadísticas descriptivas
cat("Resumen de la muestra:\n")
cat("N total:", nrow(datos), "\n")
cat("Con ECE:", sum(datos$recibio_ece), "\n")
cat("Sin ECE:", sum(datos$recibio_ece == 0), "\n\n")

# Comparación de medias: diferencia observada
media_con <- mean(datos$intereses[datos$recibio_ece == 1])
media_sin <- mean(datos$intereses[datos$recibio_ece == 0])
diferencia <- media_con - media_sin

cat("Intereses promedio:\n")
cat("  Con ECE:", round(media_con, 2), "pesos\n")
cat("  Sin ECE:", round(media_sin, 2), "pesos\n")
cat("  Diferencia (observada):", round(diferencia, 2), "pesos\n\n")

# Prueba t de Welch (dos varianzas desiguales)
prueba_t <- t.test(
  datos$intereses[datos$recibio_ece == 1],
  datos$intereses[datos$recibio_ece == 0],
  var.equal = FALSE,
  conf.level = 0.95
)

cat("Prueba t de Welch:\n")
cat("Estadístico t:", round(prueba_t$statistic, 4), "\n")
cat("Valor p:", round(prueba_t$p.value, 4), "\n")
cat("IC 95%:", round(prueba_t$conf.int[1], 2), "a", round(prueba_t$conf.int[2], 2), "\n\n")

# Visualización
library(ggplot2)

# Densidades
ggplot(datos, aes(x = intereses, fill = factor(recibio_ece))) +
  geom_density(alpha = 0.5) +
  scale_fill_manual(values = c("#1B2A4A", "#007279"), 
                    labels = c("Sin ECE", "Con ECE"),
                    name = "") +
  labs(title = "Distribución de intereses por grupo",
       x = "Intereses (pesos)",
       y = "Densidad") +
  theme_minimal() +
  theme(legend.position = "top")

# Boxplot
ggplot(datos, aes(x = factor(recibio_ece), y = intereses, fill = factor(recibio_ece))) +
  geom_boxplot(alpha = 0.7) +
  scale_x_discrete(labels = c("Sin ECE", "Con ECE")) +
  scale_fill_manual(values = c("#1B2A4A", "#007279"), guide = "none") +
  labs(title = "Distribución de intereses: Boxplot",
       x = "Grupo",
       y = "Intereses (pesos)") +
  theme_minimal()

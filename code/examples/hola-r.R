# Ejecutar desde la raíz: Rscript code/examples/hola-r.R
library(ggplot2)
datos <- data.frame(x = 1:5, y = c(2, 4, 5, 4, 6))
print(coef(lm(y ~ x, data = datos)))
dir.create("outputs", showWarnings = FALSE)
grafica <- ggplot(datos, aes(x, y)) + geom_point() + theme_minimal()
ggsave("outputs/hola-r.png", grafica, width = 6, height = 4)
cat("Gráfica guardada en outputs/hola-r.png\n")

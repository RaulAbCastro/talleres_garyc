# Taller 1 / Sesión 1: De la muestra a la inferencia
# Generado desde index.qmd por exportar_codigo.py; edita el QMD.
# Ejecutar desde slides/taller-1/sesion-1/. Datos sintéticos.

#| exercise: explorar-r
d <- read.csv("datos/muestra.csv")
head(d, 4)
cat("Personas:", nrow(d), "\n")
table(d$region, d$usa_agente)
aggregate(cbind(tasa_anual, cambio_banco) ~ usa_agente,
          data = d, FUN = mean)


#| exercise: muestreo-r
pob <- read.csv("datos/poblacion_tasas.csv")$tasa_anual
set.seed(42)
n <- 40  # prueba 200; debe ser menor que length(pob)
medias <- replicate(300, mean(sample(pob, n, replace = FALSE)))
cat("DE de medias:", round(sd(medias), 3), "pp\n")
par(mar = c(4, 4, 1, 1))
hist(medias, breaks = 20, col = "#007279", border = "white",
     xlim = c(18, 24), main = "", xlab = "Media de tasa anual (%)")
abline(v = mean(pob), col = "#B26A00", lwd = 3)


#| exercise: medias-r
d <- read.csv("datos/muestra.csv")
y1 <- d$tasa_anual[d$usa_agente == 1]
y0 <- d$tasa_anual[d$usa_agente == 0]
prueba <- t.test(y1, y0, alternative = "two.sided", var.equal = FALSE)
cat("Diferencia (pp):", mean(y1) - mean(y0), "\n")
cat("IC 95%:", prueba$conf.int, "\n")
cat("p bilateral:", format(prueba$p.value, scientific = TRUE, digits = 4), "\n")


#| exercise: proporciones-r
d <- read.csv("datos/muestra.csv")
a <- d$cambio_banco[d$usa_agente == 1]
b <- d$cambio_banco[d$usa_agente == 0]
p1 <- mean(a); p0 <- mean(b); n1 <- length(a); n0 <- length(b)
dif <- p1 - p0
se <- sqrt(p1 * (1-p1)/n1 + p0 * (1-p0)/n0)
ic <- dif + c(-1, 1) * qnorm(.975) * se
pool <- (sum(a) + sum(b)) / (n1 + n0)
z <- dif / sqrt(pool * (1-pool) * (1/n1 + 1/n0))
cat("Proporciones (uso 1, 0):", p1, p0, "\n")
cat("Diferencia e IC (pp):", 100 * c(dif, ic), "\n")
cat("p bilateral:", 2 * pnorm(-abs(z)), "\n")


#| exercise: correlacion-r
d <- read.csv("datos/muestra.csv")
cat("r de Pearson:", cor(d$ingreso_miles, d$tasa_anual), "\n")
par(mar = c(4, 4, 1, 1))
plot(d$ingreso_miles, d$tasa_anual, pch = 16,
     col = adjustcolor(c("#9BA5B7", "#007279")[d$usa_agente + 1], .6),
     xlab = "Ingreso (miles de áureos / mes)", ylab = "Tasa anual (%)")
abline(lm(tasa_anual ~ ingreso_miles, data = d), col = "#B26A00", lwd = 3)


#| exercise: regresion-r
d <- read.csv("datos/muestra.csv")
modelo <- lm(tasa_anual ~ ingreso_miles, data = d)
cat("Intercepto y pendiente:\n")
print(coef(modelo))
cat("IC 95% de la pendiente:", confint(modelo)["ingreso_miles", ], "\n")
cat("p bilateral:", coef(summary(modelo))["ingreso_miles", "Pr(>|t|)"], "\n")
cat("R cuadrada:", summary(modelo)$r.squared, "\n")


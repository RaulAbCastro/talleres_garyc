# Taller 1 / Sesión 1: De la muestra a la inferencia
# Generado desde index.qmd por exportar_codigo.py; edita el QMD.
# Ejecutar desde slides/taller-1/sesion-1/. Datos sintéticos.

#| exercise: explorar-r
d <- read.csv("datos/muestra.csv")
print(head(d[, c("id_cliente", "recibe_nomina", "abonos_miles",
                 "saldo_promedio_miles", "n_entradas", "n_salidas")], 4))
cat("Clientes:", nrow(d), "\n")
print(table(d$recibe_nomina))
print(aggregate(saldo_promedio_miles ~ recibe_nomina, data = d, FUN = mean))


#| exercise: muestreo-r
pob <- read.csv("datos/poblacion_saldos.csv")$saldo_promedio_miles
set.seed(42)
n <- 40  # prueba 200; debe ser menor que length(pob)
medias <- replicate(300, mean(sample(pob, n, replace = FALSE)))
cat("DE de medias:", round(sd(medias), 3), "miles de MXN\n")
par(mar = c(4, 4, 1, 1))
hist(medias, breaks = 20, col = "#007279", border = "white",
     xlim = c(10, 16), main = "", xlab = "Media del saldo (miles de MXN)")
abline(v = mean(pob), col = "#B26A00", lwd = 3)


#| exercise: medias-r
d <- read.csv("datos/muestra.csv")
y1 <- d$saldo_promedio_miles[d$recibe_nomina == 1]
y0 <- d$saldo_promedio_miles[d$recibe_nomina == 0]
prueba <- t.test(y1, y0, alternative = "two.sided", var.equal = FALSE)
cat("Diferencia (miles de MXN):", mean(y1) - mean(y0), "\n")
cat("IC 95%:", prueba$conf.int, "\n")
t_obs <- unname(prueba$statistic)
p <- c(izquierda = pt(t_obs, prueba$parameter),
       bilateral = prueba$p.value,
       derecha = pt(t_obs, prueba$parameter, lower.tail = FALSE))
print(p, digits = 12)


#| exercise: anova-varianzas-r
d <- read.csv("datos/muestra.csv")
pagos <- d$n_pagos_debito
grupo <- cut(pagos, breaks = c(-1, 0, 4, Inf), labels = c("0", "1 a 4", "5+"))
saldo <- d$saldo_promedio_miles
print(summary(aov(saldo ~ grupo)))
distancia <- abs(saldo - ave(saldo, grupo, FUN = median))
cat("Levene centrado en la mediana:\n")
print(summary(aov(distancia ~ grupo)))
cero <- saldo[grupo == "0"]
muchos <- saldo[grupo == "5+"]
gl <- length(cero) - 1
chi2 <- gl * var(cero) / 4^2
p_chi2 <- 2 * min(pchisq(chi2, gl), pchisq(chi2, gl, lower.tail = FALSE))
cat("Una varianza: chi2 =", chi2, "p =", p_chi2, "\n")
razon <- var.test(muchos, cero)
cat("Razón de varianzas 5+ / 0: F =", razon$statistic, "p =", razon$p.value, "\n")


#| exercise: proporciones-r
d <- read.csv("datos/muestra.csv")
a <- d$pago_debito[d$recibe_nomina == 1]
b <- d$pago_debito[d$recibe_nomina == 0]
p1 <- mean(a); p0 <- mean(b); n1 <- length(a); n0 <- length(b)
dif <- p1 - p0
se <- sqrt(p1 * (1-p1)/n1 + p0 * (1-p0)/n0)
ic <- dif + c(-1, 1) * qnorm(.975) * se
pool <- (sum(a) + sum(b)) / (n1 + n0)
z <- dif / sqrt(pool * (1-pool) * (1/n1 + 1/n0))
cat("Proporciones (nómina 1, 0):", p1, p0, "\n")
cat("Diferencia e IC (pp):", 100 * c(dif, ic), "\n")
cat("p bilateral:", 2 * pnorm(-abs(z)), "\n")


#| exercise: correlacion-r
d <- read.csv("datos/muestra.csv")
cat("r de Pearson:", cor(d$abonos_miles, d$saldo_promedio_miles), "\n")
par(mar = c(4, 4, 1, 1))
plot(d$abonos_miles, d$saldo_promedio_miles, pch = 16,
     col = adjustcolor(c("#9BA5B7", "#007279")[d$recibe_nomina + 1], .6),
     xlab = "Abonos del mes (miles de MXN)", ylab = "Saldo promedio (miles de MXN)")


#| exercise: regresion-r
d <- read.csv("datos/muestra.csv")
modelo <- lm(saldo_promedio_miles ~ abonos_miles, data = d)
cat("Intercepto y pendiente:\n")
print(coef(modelo))
cat("IC 95% de la pendiente:", confint(modelo)["abonos_miles", ], "\n")
cat("p bilateral:", coef(summary(modelo))["abonos_miles", "Pr(>|t|)"], "\n")
cat("R cuadrada:", summary(modelo)$r.squared, "\n")
cat("Primeros valores ajustados y residuos:\n")
print(head(data.frame(observado = d$saldo_promedio_miles,
                      ajustado = fitted(modelo), residuo = resid(modelo)), 3))
par(mar = c(4, 4, 1, 1))
plot(fitted(modelo), resid(modelo), pch = 16, col = adjustcolor("#007279", .55),
     xlab = "Saldo ajustado (miles de MXN)", ylab = "Residuo (miles de MXN)")
abline(h = 0, lty = 2, col = "#1B2A4A")

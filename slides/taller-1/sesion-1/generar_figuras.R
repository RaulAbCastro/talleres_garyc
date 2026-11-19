# Figuras en R del caso bancario y de los escenarios didácticos.
# Ejecutar desde slides/taller-1/sesion-1/: Rscript generar_figuras.R
d <- read.csv("datos/muestra.csv")
dir.create("assets", showWarnings = FALSE)

svg("assets/saldos-r.svg", width = 11, height = 4, bg = "#F7F8FA")
par(mar = c(4.2, 10, 1, 1), fg = "#253347", col.axis = "#253347")
plot(0, 0, type = "n", xlim = c(9, 18), ylim = c(-.5, 1.5),
     yaxt = "n", ylab = "", bty = "l",
     xlab = "Saldo promedio del mes (miles de MXN) · IC del 95% de cada media")
axis(2, at = c(0, 1), labels = c("Recibe nómina", "No recibe nómina"), las = 1)
abline(v = axTicks(1), col = "#E2E6EB", lwd = 1)
for (nomina in 0:1) {
  y <- d$saldo_promedio_miles[d$recibe_nomina == nomina]
  m <- mean(y)
  margen <- qt(.975, length(y)-1) * sd(y) / sqrt(length(y))
  color <- c("#5D6D7E", "#007279")[nomina+1]
  arrows(m-margen, 1-nomina, m+margen, 1-nomina, angle = 90, code = 3,
         length = .08, col = color, lwd = 3)
  points(m, 1-nomina, pch = 16, col = color, cex = 1.4)
  text(m, 1-nomina+.2, sprintf("%.2f · n=%d", m, length(y)), col = color)
}
dev.off()

svg("assets/abonos-r.svg", width = 11, height = 4, bg = "#F7F8FA")
par(mar = c(4.2, 4.5, 1, 1), fg = "#253347", col.axis = "#253347")
colores <- c("#9BA5B7", "#007279")
plot(d$abonos_miles, d$saldo_promedio_miles, pch = 16, bty = "l",
     col = adjustcolor(colores[d$recibe_nomina+1], .6),
     xlab = "Abonos totales del mes (miles de MXN)",
     ylab = "Saldo promedio (miles de MXN)", xlim = c(0, 82), ylim = c(0, 36))
legend("topleft", c("No recibe nómina", "Recibe nómina"),
       col = colores, pch = 16, bty = "n", cex = .8)
dev.off()

# Distribución de referencia bajo la hipótesis nula en el ejemplo bilateral.
svg("assets/colas-r.svg", width = 11, height = 2.65, bg = "#F7F8FA", pointsize = 14)
par(mar = c(3.1, 1, .4, 1), mgp = c(1.9, .5, 0), fg = "#253347",
    col.axis = "#253347", col.lab = "#253347")
z <- (-450:450) / 100
extremo <- 2
porcentaje_cola <- 100 * pnorm(extremo, lower.tail = FALSE)
plot(z, dnorm(z), type = "n", axes = FALSE, xaxs = "i", yaxs = "i",
     ylim = c(0, .42), xlab = "Valor del estadístico bajo la hipótesis nula", ylab = "")
for (signo in c(-1, 1)) {
  cola <- z[signo * z >= extremo]
  polygon(c(cola[1], cola, tail(cola, 1)), c(0, dnorm(cola), 0),
          col = "#E0A33B", border = NA)
  segments(signo * extremo, 0, signo * extremo, dnorm(extremo), col = "#805600")
  text(signo * 2.95, .17, sprintf("%.3f%%", porcentaje_cola),
       col = "#805600", cex = 1.2, font = 2)
  arrows(signo * 2.9, .14, signo * 2.2, .017, length = .08, col = "#805600")
}
lines(z, dnorm(z), col = "#007279", lwd = 2.5)
abline(h = 0, col = "#253347")
axis(1, at = c(-extremo, 0, extremo), labels = c("−2", "0", "+2"))
dev.off()

# La extensión horizontal del perfil representa densidad, no un cambio en X.
svg("assets/supuestos-regresion-r.svg", width = 11, height = 3.15,
    bg = "#F7F8FA", pointsize = 14)
par(mar = c(3.2, 5, .6, 1), mgp = c(2, .6, 0),
    fg = "#253347", col.axis = "#253347", col.lab = "#253347")
abonos <- c(10, 25, 40)
centros <- 5 + 0.4 * abonos
desvios <- seq(-3.2, 3.2, length.out = 129)
plot(abonos, centros, type = "n", xaxt = "n", bty = "l", xaxs = "i",
     xlim = c(2, 51), ylim = c(0, 30),
     xlab = "Abonos del mes (miles de MXN)", ylab = "Saldo promedio (miles de MXN)")
axis(1, at = abonos)
abline(5, 0.4, col = "#1B2A4A", lwd = 2)
for (i in seq_along(abonos)) {
  x <- abonos[i]
  saldos <- centros[i] + 2.2 * desvios
  densidad_horizontal <- x + 7 * exp(-0.5 * desvios^2)
  polygon(c(x, densidad_horizontal, x), c(saldos[1], saldos, tail(saldos, 1)),
          col = "#D4EBE8", border = NA)
  segments(x, saldos[1], x, tail(saldos, 1), col = "#5D6D7E", lty = 2)
  lines(densidad_horizontal, saldos, col = "#007279", lwd = 2)
  points(x, centros[i], col = "#1B2A4A", pch = 19)
}
legend("topleft", "Saldo medio condicional", lty = 1, lwd = 2,
       col = "#1B2A4A", bty = "n")
dev.off()

# Comparar los mismos grupos manteniendo sus tamaños y medias.
pagos <- cut(d$n_pagos_debito, breaks = c(-1, 0, 4, Inf),
             labels = c("0 pagos", "1 a 4 pagos", "5 o más pagos"))
saldos <- split(d$saldo_promedio_miles, pagos)
medias <- vapply(saldos, mean, numeric(1))
desvios <- vapply(saldos, sd, numeric(1))
svg("assets/dispersion-anova-r.svg", width = 11, height = 2.95,
    bg = "#F7F8FA", pointsize = 14)
par(mfrow = c(1, 2), mar = c(1.8, 6.8, 1.7, .6), oma = c(2, 0, 0, 0),
    mgp = c(2, .5, 0), fg = "#253347", col.axis = "#253347")
escenarios <- c("Muestra del taller" = 1, "Distancias a la mitad" = .5)
for (titulo in names(escenarios)) {
  plot.new()
  plot.window(xlim = c(7, 20), ylim = c(-.5, 2.5), xaxs = "i", yaxs = "i")
  abline(v = seq(8, 18, 2), col = "#D9DDE5")
  axis(1, at = seq(8, 18, 2))
  axis(2, at = 2:0, labels = names(medias), las = 1, tick = FALSE)
  margen <- escenarios[[titulo]] * desvios
  arrows(medias - margen, 2:0, medias + margen, 2:0,
         angle = 90, code = 3, length = .06, col = "#007279", lwd = 3)
  points(medias, 2:0, pch = 19, cex = 1.25, col = "#1B2A4A")
  title(main = titulo, col.main = "#1B2A4A", line = .25)
}
mtext("Saldo promedio del mes (miles de MXN)", side = 1, outer = TRUE, line = .35)
dev.off()

# Seis saldos por nivel ajustado. El centro y la amplitud cambian por separado.
niveles <- seq(8, 26, by = 3)
perfil <- ((niveles - mean(niveles)) / 9)^2
centro_curvo <- 5.4 * (perfil - mean(perfil))
abanico <- seq(.5, 4.1, length.out = length(niveles))
desvios_relativos <- c(-1, -.6, -.25, .25, .6, 1)
escenarios <- list(
  "Cartera A" = list(centros = centro_curvo, amplitudes = rep(1, length(niveles))),
  "Cartera B" = list(centros = rep(0, length(niveles)), amplitudes = abanico)
)
svg("assets/lectura-residuos-r.svg", width = 11.5, height = 3.5,
    bg = "#F7F8FA", pointsize = 14)
par(mfrow = c(1, 2), mar = c(3.4, 3.9, 1.5, .8), mgp = c(2.2, .6, 0),
    fg = "#253347", col.axis = "#253347", col.lab = "#253347")
for (nombre in names(escenarios)) {
  cartera <- escenarios[[nombre]]
  plot(0, 0, type = "n", axes = FALSE, main = nombre,
       xlim = c(6, 28), ylim = c(-5, 5), xaxs = "i", yaxs = "i",
       xlab = "Saldo ajustado (miles de MXN)", ylab = "Residuo (miles de MXN)")
  axis(1, at = niveles[c(1, 3, 5, 7)])
  axis(2, at = seq(-4, 4, by = 2), las = 1)
  box(bty = "l")
  abline(h = 0, lty = 2, col = "#667788")
  for (i in seq_along(niveles)) {
    residuos <- cartera$centros[i] + cartera$amplitudes[i] * desvios_relativos
    points(rep(niveles[i], length(residuos)), residuos, pch = 16,
           col = "#007279", cex = .7)
  }
  lines(niveles, cartera$centros, type = "o", pch = 18, col = "#A05A00", lwd = 1.6)
}
dev.off()
cat("Figuras R en assets/: saldos-r.svg, abonos-r.svg, colas-r.svg, supuestos-regresion-r.svg, dispersion-anova-r.svg y lectura-residuos-r.svg\n")

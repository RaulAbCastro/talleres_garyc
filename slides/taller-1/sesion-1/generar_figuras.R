# Figuras equivalentes en R; solo leen el CSV observado de participantes.
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
cat("Figuras R: saldos-r.svg, abonos-r.svg y colas-r.svg en assets/\n")

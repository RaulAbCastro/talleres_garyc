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
cat("Figuras R: saldos-r.svg y abonos-r.svg en assets/\n")

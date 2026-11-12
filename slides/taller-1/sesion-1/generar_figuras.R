# Figuras equivalentes en R. Ejecutar desde slides/taller-1/sesion-1/.
d <- read.csv("datos/muestra.csv")
dir.create("assets", showWarnings = FALSE)
svg("assets/tasas-r.svg", width = 11, height = 4, bg = "#F7F8FA")
par(mar = c(4.2, 10, 1, 1), fg = "#253347", col.axis = "#253347")
plot(0, 0, type = "n", xlim = c(17, 25), ylim = c(-.5, 1.5),
     yaxt = "n", ylab = "", bty = "l",
     xlab = "Tasa anual media (%) · intervalos de confianza del 95%")
axis(2, at = c(0, 1), labels = c("Usa el Agente", "No usa el Agente"), las = 1)
for (uso in 0:1) {
  y <- d$tasa_anual[d$usa_agente == uso]
  m <- mean(y)
  margen <- qt(.975, length(y)-1) * sd(y) / sqrt(length(y))
  color <- c("#5D6D7E", "#007279")[uso+1]
  arrows(m-margen, 1-uso, m+margen, 1-uso, angle = 90, code = 3,
         length = .08, col = color, lwd = 3)
  points(m, 1-uso, pch = 16, col = color, cex = 1.4)
  text(m, 1-uso+.2, sprintf("%.2f%% · n=%d", m, length(y)), col = color)
}
dev.off()

svg("assets/ingreso-r.svg", width = 11, height = 4, bg = "#F7F8FA")
par(mar = c(4.2, 4.2, 1, 1), fg = "#253347", col.axis = "#253347")
colores <- c("#9BA5B7", "#007279")
plot(d$ingreso_miles, d$tasa_anual, pch = 16, bty = "l",
     col = adjustcolor(colores[d$usa_agente+1], .6),
     xlab = "Ingreso (miles de áureos al mes)", ylab = "Tasa anual (%)")
abline(lm(tasa_anual ~ ingreso_miles, d), col = "#B26A00", lwd = 3)
legend("topright", c("No usa el Agente", "Usa el Agente", "Recta conjunta"),
       col = c(colores, "#B26A00"), pch = c(16, 16, NA),
       lty = c(NA, NA, 1), bty = "n", cex = .8)
dev.off()

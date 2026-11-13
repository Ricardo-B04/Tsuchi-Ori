# Ejecutar desde la raíz del proyecto con Rscript enfoque_estadistico/analisis.R.
# Usa únicamente funciones de R base y stats.
datos <- read.csv("datos/transformados/series_diarias_pagina.csv", fileEncoding = "UTF-8-BOM")
datos$fecha <- as.Date(datos$fecha)
stopifnot(all(diff(datos$fecha) == 1))
columnas <- c("visualizaciones", "espectadores", "interacciones", "visitas",
              "seguidores_metrica_diaria", "ingresos_aproximados")
columnas <- paste0("pagina_", columnas)
inicio <- which(datos$pagina_visualizaciones > 0)[1]
activo <- datos[inicio:nrow(datos), ]
pico <- which.max(activo$pagina_visualizaciones)

# Partición exacta que minimiza la desviación absoluta respecto de la mediana
# del segmento, más una penalización por ruptura. Cada segmento dura >= 14 días.
segmentar <- function(x, penalizacion, minimo = 14L) {
  n <- length(x)
  costo <- rep(Inf, n + 1L)
  costo[1] <- -penalizacion
  anterior <- integer(n + 1L)
  for (fin in seq.int(minimo, n)) {
    candidatos <- c(0L, seq_len(fin - minimo))
    candidatos <- candidatos[is.finite(costo[candidatos + 1L])]
    objetivos <- vapply(candidatos, function(previo) {
      segmento <- x[(previo + 1L):fin]
      costo[previo + 1L] + sum(abs(segmento - median(segmento))) + penalizacion
    }, numeric(1))
    mejor <- which.min(objetivos)
    costo[fin + 1L] <- objetivos[mejor]
    anterior[fin + 1L] <- candidatos[mejor]
  }
  inicios <- integer()
  fin <- n
  while (fin > 0L) {
    previo <- anterior[fin + 1L]
    inicios <- c(previo + 1L, inicios)
    fin <- previo
  }
  inicios
}

cat("Cobertura", as.character(min(datos$fecha)), as.character(max(datos$fecha)), nrow(datos), "días\n")
picos <- do.call(rbind, lapply(columnas, function(columna) {
  x <- datos[[columna]]
  i <- which.max(x)
  data.frame(metrica = sub("^pagina_", "", columna), fecha = datos$fecha[i],
             valor = x[i], porcentaje_acumulado = round(100 * x[i] / sum(x), 2),
             dias_cero_iniciales = which(x > 0)[1] - 1L)
}))
print(picos, row.names = FALSE)

cat("\nRupturas de nivel en log(1 + visualizaciones)\n")
y <- log1p(activo$pagina_visualizaciones)
for (penalizacion in c(8, 12, 16)) {
  cortes <- segmentar(y, penalizacion)
  print(data.frame(penalizacion = penalizacion, desde = activo$fecha[cortes],
                   hasta = activo$fecha[c(cortes[-1] - 1, nrow(activo))],
                   mediana = vapply(seq_along(cortes), function(i) {
                     fin <- c(cortes[-1] - 1, length(y))[i]
                     median(activo$pagina_visualizaciones[cortes[i]:fin])
                   }, numeric(1))), row.names = FALSE)
}
# Análisis de sensibilidad sin el máximo, sustituido por la mediana local.
sin_pico <- y
sin_pico[pico] <- median(y[c((pico - 7):(pico - 1), (pico + 1):(pico + 7))])
cat("Rupturas con penalización 12 y pico sustituido:", format(activo$fecha[segmentar(sin_pico, 12)]), "\n")

cat("\nSTL semanal robusto en escala logarítmica\n")
for (columna in columnas) {
  x <- log1p(activo[[columna]])
  ajuste <- stl(ts(x, frequency = 7), s.window = "periodic", robust = TRUE)
  componentes <- ajuste$time.series
  residual <- componentes[, "remainder"]
  estacional <- componentes[, "seasonal"]
  fuerza <- max(0, 1 - var(residual) / var(residual + estacional))
  sin_tendencia <- x - componentes[, "trend"]
  acf7 <- function(z) cor(z[1:(length(z) - 7)], z[8:length(z)])
  # Examinar el efecto del máximo en pares de rezago, sin concatenar días.
  i <- seq_len(length(x) - 7L)
  valido <- i != pico & i + 7L != pico
  acf_sin <- cor(sin_tendencia[i[valido]], sin_tendencia[i[valido] + 7L])
  cat(sub("^pagina_", "", columna), sprintf("fuerza=%.3f r7=%.3f r7_sin_pico=%.3f\n",
       fuerza, acf7(sin_tendencia), acf_sin))
}

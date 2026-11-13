# Datos de Tsuchiori

## Exportaciones de origen

[originales/](originales/) contiene los ocho CSV descargados. Conservan el contenido de las exportaciones y llevan los nombres normalizados durante la descarga.

- Las seis series de página registran espectadores, ingresos, interacciones, seguidores, visitas y visualizaciones.
- El archivo con fechas del 1 de octubre al 11 de noviembre contiene las métricas por video y fecha.
- El resumen de formatos contiene cifras por tipo de contenido y carece de fechas.

## Bases preparadas

| Archivo | Unidad | Uso |
| --- | --- | --- |
| [Series diarias de la página](transformados/series_diarias_pagina.csv) | 315 filas, una por fecha | Base para el análisis estadístico, el pronóstico y el análisis topológico de la página. |
| [Series diarias por video](transformados/series_diarias_por_video.csv) | 1.260 filas, una por video y fecha | Base para Mapper. Incluye los días desde la publicación para alinear trayectorias individuales. |
| [Cruce diario de página y video](transformados/series_diarias_tsuchiori.csv) | 315 filas, una por fecha | Base para comparar métricas de página con los totales diarios de los 30 videos durante los 42 días compartidos. |

Los resultados de cada método se guardan junto a su código en las carpetas de análisis.

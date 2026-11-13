# Diccionario de datos de videos

La [base diaria de Tsuchiori](../datos/transformados/series_diarias_por_video.csv) contiene **1.260 filas**, una por video y fecha de registro, para **30 videos**. La exportación cubre del **1 de octubre al 11 de noviembre de 2026**. Para Mapper, usamos los días 0 a 6 desde la publicación. **27 videos** tienen la primera semana completa. El día 0 puede ser parcial según la hora de publicación.

## Campos del análisis final

| Columna | Tipo y unidad | Definición de trabajo |
| --- | --- | --- |
| `Identificador del activo de video` | Texto | Identificador del activo en Facebook. Junto con Fecha identifica una fila. |
| `Duración (segundos)` | Entero, segundos | Duración del video. Los 30 videos duran entre 6 y 50 segundos. |
| `Hora de publicación` | Fecha y hora | Momento de publicación según la exportación. |
| `Fecha` | Fecha | Día calendario de las métricas de la fila. |
| `Reproducciones de video de 3 segundos` | Entero, reproducciones | Reproducciones que alcanzan el umbral de tres segundos. |
| `Segundos reproducidos` | Decimal, segundos | Tiempo total de reproducción registrado para el video durante el día. |
| `Reacciones, comentarios y veces que se compartió` | Entero, acciones | Suma diaria de reacciones, comentarios y veces que se compartió. |
| `Días desde la publicación` | Entero, días | Diferencia en días calendario entre la fecha del registro y la fecha de publicación. Campo derivado. |

En Mapper, cada video se representa mediante la distribución diaria de reproducciones de tres segundos, segundos reproducidos o interacciones, según la métrica seleccionada. El total semanal se conserva para interpretar el volumen.

## Campos de apoyo

| Columna | Tipo y unidad | Definición de trabajo |
| --- | --- | --- |
| `Identificador de la página` | Texto | Identificador de la página que publicó los videos. |
| `Nombre de la página` | Texto | Nombre de la página que publicó los videos. |
| `Segundos en promedio reproducidos` | Decimal, segundos | Tiempo medio de reproducción diario según la exportación. |
| `Espectadores de 3 segundos` | Entero, espectadores | Espectadores diarios asociados a reproducciones de tres segundos. Una persona puede aparecer en varios días. |
| `Reacciones` | Entero, acciones | Reacciones registradas en el día. |
| `Comentarios` | Entero, acciones | Comentarios registrados en el día. |
| `Veces que se compartió` | Entero, acciones | Veces que se compartió el video durante el día. |
| `Segundos reproducidos en Seguidores` | Decimal, segundos | Tiempo total diario atribuido a Seguidores. |
| `Segundos reproducidos en Recomendaciones` | Decimal, segundos | Tiempo total diario atribuido a Recomendaciones. |
| `Segundos reproducidos en Contenido compartido` | Decimal, segundos | Tiempo total diario atribuido a Contenido compartido. |
| `Segundos en promedio producidos en Recomendaciones` | Decimal, segundos | Tiempo promedio diario atribuido a Recomendaciones. |
| `Segundos en promedio producidos en Contenido compartido` | Decimal, segundos | Tiempo promedio diario atribuido a Contenido compartido. |
| `Segundos en promedio producidos en Seguidores` | Decimal, segundos | Tiempo promedio diario atribuido a Seguidores. |

Los desgloses de tiempo por fuente contienen valores vacíos. Para agregar promedios diarios se necesita confirmar su denominador. La suma de espectadores diarios puede contar a una misma persona en varias fechas.

## Campos excluidos del análisis final

| Columna | Definición de trabajo | Motivo de exclusión |
| --- | --- | --- |
| `Identificador de video universal` | Identificador universal del video según el rótulo de origen. | Vacío en todas las filas. |
| `Título` | Título del video. | Vacío en todas las filas. |
| `Etiquetas personalizadas` | Etiquetas personalizadas del video. | Vacío en todas las filas. |
| `Comentario sobre los datos` | Observaciones de la exportación sobre el registro. | Vacío en todas las filas. |
| `Reproducciones de video de 1 minuto` | Reproducciones que alcanzan el umbral de un minuto. | Cero en todas las filas y los videos duran menos de un minuto. |
| `Espectadores de 1 minuto` | Espectadores asociados al umbral de un minuto. | Cero en todas las filas. |
| `Reproducciones de video de 3 segundos de Publicaciones promocionadas` | Reproducciones de tres segundos atribuidas a publicaciones promocionadas. | Cero en todas las filas. |
| `Reproducciones de video de 3 segundos de Publicaciones orgánicas` | Reproducciones de tres segundos atribuidas a publicaciones orgánicas. | Coincide exactamente con las reproducciones de tres segundos. |
| `Segundos en promedio producidos en Publicaciones promocionadas` | Tiempo promedio diario atribuido a publicaciones promocionadas. | Cero en todas las filas. |
| `Ingresos estimados (USD)` | Ingreso estimado en dólares según el encabezado. | Cero en todas las filas. |
| `Ingresos aproximados por monetización de contenido` | Ingreso aproximado atribuido a monetización de contenido. | La monetización queda fuera del foco del análisis de trayectorias. Registra 46 valores distintos de cero y su unidad está por confirmar. |

El desglose de vacíos y ceros por columna está disponible en la [metodología de Mapper](metodologia_mapper_videos.md#desglose-por-columna).

# Ventana de análisis para Mapper de videos

**Decisión del 12 de noviembre de 2026.** Usar una ventana fija de siete días calendario por video, desde el día de publicación (día 0) hasta el día 6 inclusive. El día 0 puede ser parcial según la hora de publicación.

Una semana es una unidad fácil de interpretar y ofrece un horizonte común para comparar videos. La exportación termina el 11 de noviembre de 2026. De 30 videos, 27 completan los siete días. Los otros tres se publicaron el 7, 8 y 10 de noviembre y tienen 5, 4 y 2 días observados, respectivamente. Los 30 tienen registros consecutivos desde la publicación hasta el corte.

Para evaluar la ventana se usaron los mismos 19 videos con al menos 21 días observados. La mediana de la proporción de reproducciones de al menos tres segundos acumulada en los primeros 7, 10 y 14 días, respecto de los primeros 21 días de cada video, fue 93,0 %, 95,6 % y 98,7 %, respectivamente. Ampliar la ventana de 7 a 14 días añade 5,7 puntos porcentuales en la mediana y reduce de 27 a 23 los videos elegibles. La decisión se apoya en el patrón típico. Hay repuntes tardíos, como el del video 1111200735143753 con 28.343 reproducciones el día 11.

## Cobertura por variable

La disponibilidad de filas por video y día es común a todas las métricas. En las 189 filas de la primera semana de los 27 videos elegibles, 18 de las 21 columnas de métricas están completas. Incluyen reproducciones, espectadores, tiempo reproducido total y promedio, reacciones, comentarios, compartidos e ingresos. Algunas columnas completas contienen únicamente ceros en esta ventana.

| Métrica | Celdas vacías de 189 | Videos con siete valores |
| --- | ---: | ---: |
| Segundos reproducidos en Seguidores | 2 | 25 |
| Segundos reproducidos en Recomendaciones | 2 | 25 |
| Segundos reproducidos en Contenido compartido | 89 | 5 |

La fuente distingue celdas vacías de ceros registrados. Su significado debe revisarse si se incorporan los desgloses de tiempo reproducido a Mapper.

Con siete días fijados, el siguiente eje de exploración es cómo representar cada video. La primera versión utiliza la distribución diaria de reproducciones y la proporción acumulada en los días 0 y 1 como lente. El tiempo reproducido y las interacciones permiten plantear análisis de consumo y respuesta del público sobre la misma semana.

[Datos diarios por video](../datos/transformados/series_diarias_por_video.csv) · [Implementación de Mapper](mapper_videos.py)

## Comparación de métricas en la primera semana

El grafo permite elegir reproducciones de al menos tres segundos, segundos reproducidos o la suma de reacciones, comentarios y veces que se compartió. Cada video se representa por los siete valores diarios divididos entre su total semanal. La lente usa la proporción del total de los días 0 y 1. Los tres grafos usan los mismos 27 videos y las mismas configuraciones de cobertura y radio euclidiano. Para que una curva pueda normalizarse, debe tener siete valores y un total positivo.

La configuración inicial usa cinco intervalos con 35 % de solapamiento y radio 0,12. Produce seis nodos y una arista para reproducciones y tiempo reproducido, y siete nodos y tres aristas para interacciones. Los resultados se pueden explorar con el selector de configuración.

[Grafo interactivo](mapper_videos.html)

## Campos útiles del archivo por video

La revisión cubre las 1.260 filas de los 30 videos. Sus duraciones van de **6 a 50 segundos**, por lo que corresponden a formato corto. El archivo permite estudiar curvas de arranque y caída, así como repuntes tardíos. El formato exacto de publicación y las decisiones del sistema de recomendación requieren evidencia adicional.

| Uso | Campos | Criterio |
| --- | --- | --- |
| Identificar y alinear | Identificador del activo, fecha del registro, hora de publicación y días desde la publicación | La unidad es video por día. Para Mapper usamos los días 0 a 6. La hora ayuda a interpretar el día 0 parcial. |
| Caracterizar el video | Duración en segundos | Permite comparar piezas de distinta duración y contextualizar el tiempo promedio reproducido. |
| Medir alcance y consumo | Reproducciones de tres segundos, espectadores de tres segundos, segundos reproducidos y segundos en promedio reproducidos | Las reproducciones y los espectadores difieren en 106 filas. El tiempo total mide consumo acumulado. El promedio se interpreta por día y requiere conocer su denominador para calcular un promedio semanal ponderado. Los espectadores diarios pueden repetirse entre fechas. |
| Medir respuesta | Reacciones, comentarios, veces que se compartió y el total de interacciones del video | El total coincide con la suma de los tres componentes en las 1.260 filas. Usar el total o el desglose según la pregunta y evitar ponderar dos veces la misma información. |
| Examinar fuentes de consumo | Segundos reproducidos y segundos promedio desglosados en Seguidores, Recomendaciones y Contenido compartido | Los totales tienen 762, 714 y 1.065 valores vacíos, respectivamente. Los promedios tienen ceros en las filas correspondientes a esos vacíos. Conservar la distinción al interpretar cada fuente. |
| Examinar monetización | Ingresos aproximados por monetización de contenido | Tiene valores distintos de cero en 46 filas. Mantener como métrica secundaria y confirmar la unidad antes de interpretar montos. |
| Evitar duplicar | Reproducciones orgánicas de tres segundos | Coinciden exactamente con las reproducciones de tres segundos en las 1.260 filas. |
| Excluir del conjunto de variables de este análisis | Reproducciones y espectadores de un minuto, reproducciones promocionadas de tres segundos, segundos promedio de publicaciones promocionadas e ingresos estimados (USD) | Todas estas columnas registran cero en las 1.260 filas. El archivo incluye segundos **promedio** promocionados y carece de una columna específica para segundos **totales** promocionados. Los segundos totales y promedio generales sí varían. |
| Conservar como metadatos de origen | Identificador y nombre de la página | Ambos son constantes porque la exportación corresponde a una sola página. |
| Excluir por falta de datos | Identificador de video universal, título, etiquetas personalizadas y comentario sobre los datos | Las cuatro columnas están vacías en todas las filas. |

Para comparar perfiles de primera semana, el conjunto principal usa las **reproducciones de tres segundos**, el **tiempo total reproducido** y las **interacciones**. Mapper usa la distribución diaria de cada métrica y conserva el total semanal para distinguir la forma de la trayectoria de su volumen. Los desgloses por fuente pueden ayudar a examinar si un repunte coincidió con mayor consumo desde Recomendaciones.

## Desglose por columna

Cada par indica **celdas vacías / ceros registrados**. La primera semana corresponde a los días 0 a 6 de los 27 videos elegibles. El guion indica que el conteo de ceros no aplica al campo. En días desde la publicación, cero identifica el día de publicación.

| Columna | Vacíos / ceros en 1.260 filas | Vacíos / ceros en 189 filas | Uso |
| --- | ---: | ---: | --- |
| Identificador del activo de video | 0 / — | 0 / — | Clave del video |
| Identificador de video universal | 1260 / — | 189 / — | Vacía en toda la exportación |
| Identificador de la página | 0 / — | 0 / — | Metadato constante de la página |
| Nombre de la página | 0 / — | 0 / — | Metadato constante de la página |
| Título | 1260 / — | 189 / — | Vacía en toda la exportación |
| Duración (segundos) | 0 / 0 | 0 / 0 | Contexto del tiempo visto. Entre 6 y 50 s |
| Hora de publicación | 0 / — | 0 / — | Alineación temporal y revisión del día 0 parcial |
| Etiquetas personalizadas | 1260 / — | 189 / — | Vacía en toda la exportación |
| Comentario sobre los datos | 1260 / — | 189 / — | Vacía en toda la exportación |
| Fecha | 0 / — | 0 / — | Clave de fecha del registro |
| Reproducciones de video de 3 segundos | 0 / 728 | 0 / 1 | Métrica principal de reproducciones |
| Reproducciones de video de 1 minuto | 0 / 1260 | 0 / 189 | Sin variación |
| Segundos reproducidos | 0 / 667 | 0 / 0 | Métrica principal de consumo |
| Segundos en promedio reproducidos | 0 / 667 | 0 / 0 | Consumo medio diario. Verificar el denominador antes de agregar |
| Espectadores de 3 segundos | 0 / 728 | 0 / 1 | Alcance diario. Evitar sumar como personas únicas |
| Espectadores de 1 minuto | 0 / 1260 | 0 / 189 | Sin variación |
| Reproducciones de video de 3 segundos de Publicaciones promocionadas | 0 / 1260 | 0 / 189 | Sin variación |
| Reproducciones de video de 3 segundos de Publicaciones orgánicas | 0 / 728 | 0 / 1 | Duplicado exacto de reproducciones de 3 s |
| Reacciones, comentarios y veces que se compartió | 0 / 993 | 0 / 40 | Métrica principal de interacción |
| Reacciones | 0 / 994 | 0 / 41 | Desglose de interacciones |
| Comentarios | 0 / 1185 | 0 / 138 | Desglose de interacciones |
| Veces que se compartió | 0 / 1184 | 0 / 136 | Desglose de interacciones |
| Segundos reproducidos en Seguidores | 762 / 0 | 2 / 0 | Fuente de consumo. Interpretar los vacíos por separado |
| Segundos reproducidos en Recomendaciones | 714 / 0 | 2 / 0 | Fuente de consumo. Examinar repuntes |
| Segundos reproducidos en Contenido compartido | 1065 / 0 | 89 / 0 | Fuente de consumo. Cobertura limitada |
| Segundos en promedio producidos en Recomendaciones | 0 / 714 | 0 / 2 | Promedio diario por fuente. Ceros coinciden con vacíos del total |
| Segundos en promedio producidos en Contenido compartido | 0 / 1065 | 0 / 89 | Promedio diario por fuente. Ceros coinciden con vacíos del total |
| Segundos en promedio producidos en Seguidores | 0 / 762 | 0 / 2 | Promedio diario por fuente. Ceros coinciden con vacíos del total |
| Segundos en promedio producidos en Publicaciones promocionadas | 0 / 1260 | 0 / 189 | Sin variación |
| Ingresos estimados (USD) | 0 / 1260 | 0 / 189 | Sin variación |
| Ingresos aproximados por monetización de contenido | 0 / 1214 | 0 / 161 | Monetización secundaria. Unidad por confirmar |
| Días desde la publicación | 0 / 30 | 0 / 27 | Alineación por edad. Día 0 es publicación |

## Sensibilidad al radio de agrupamiento

Se comparó el radio inicial de 0,12 con un radio de 0,08, usando los mismos 27 videos, cinco intervalos, 35 % de solapamiento y siete días. Un radio menor exige mayor similitud entre los videos unidos directamente dentro de cada intervalo. Un nodo puede contener varios videos unidos por una cadena de vecinos.

| Métrica | Nodos con 0,12 → 0,08 | Aristas con 0,12 → 0,08 | Tamaño del nodo mayor con 0,12 → 0,08 |
| --- | ---: | ---: | ---: |
| Reproducciones de tres segundos | 6 → 7 | 1 → 1 | 23 → 22 |
| Tiempo reproducido | 6 → 8 | 1 → 1 | 23 → 17 |
| Interacciones | 7 → 12 | 3 → 4 | 24 → 16 |

El video 1111200735143753 forma un nodo individual en las tres métricas con ambos radios. El grupo principal de reproducciones es más estable ante este ajuste que los grupos de tiempo reproducido e interacciones.

## Lente de día promedio ponderado

La lente alternativa suma el día desde la publicación multiplicado por la proporción semanal de actividad de ese día. Utiliza los días 0 a 6 y se expresa en días desde la publicación. La lente original mide la proporción acumulada de los días 0 y 1.

Mapper divide el rango observado de cada lente en intervalos solapados de igual longitud. Dentro de cada intervalo, conecta pares de videos cuya distancia euclidiana entre sus siete proporciones diarias es menor o igual al radio. Cada componente conexa se convierte en un nodo. Dos nodos tienen una arista cuando comparten algún video. La configuración inicial usa cinco intervalos, 35 % de solapamiento y radio 0,12.

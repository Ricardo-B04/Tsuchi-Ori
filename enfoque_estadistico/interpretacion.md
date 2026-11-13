# Cambios de nivel, picos y estacionalidad semanal

La serie de la página tiene 315 días consecutivos, del 1 de enero al 11 de noviembre de 2026. Las visualizaciones tienen 97 ceros consecutivos al comienzo y su primer registro positivo aparece el 8 de abril. El análisis de cambios de nivel y estacionalidad se concentra en los **218 días del tramo activo**. La causa de los ceros iniciales queda abierta.

El **26 de agosto** concentra el máximo de las seis métricas examinadas. Aporta **911.216 visualizaciones**, el **12,51 %** del acumulado, y **64.134 interacciones**, el **17,09 %**. El repunte abarca varios días. Las visualizaciones pasan de 28.066 el 24 de agosto a 91.867 el 25, alcanzan el máximo el 26 y bajan a 283.343 el 27 y a 65.577 el 28.

La segmentación minimiza la suma de desviaciones absolutas respecto de la mediana de cada tramo de `log1p(visualizaciones)` más una penalización por ruptura. Cada tramo dura al menos 14 días. Con penalización 12, se obtienen estos tramos.

| Desde | Hasta | Mediana diaria de visualizaciones |
| --- | --- | ---: |
| 8 de abril | 30 de mayo | 2.255 |
| 31 de mayo | 2 de octubre | 30.957 |
| 3 de octubre | 11 de noviembre | 13.495 |

El aumento de nivel se ubica **entre el 29 y el 31 de mayo** al variar la penalización entre 8, 12 y 16. La caída del **3 de octubre** aparece con 8 y 12. Con 16, el modelo agrupa el periodo final. Con penalización 12, sustituir el máximo del 26 de agosto por la mediana de los siete días a cada lado conserva ambas fechas de ruptura. Los cortes son descriptivos y dependen de la penalización y la escala elegidas.

La descomposición STL robusta sobre la escala logarítmica estima una fuerza estacional semanal de **0,008** para visualizaciones, con valores entre **0 y 0,008** para las seis métricas. En visualizaciones, la correlación entre días separados por siete días tras sustraer la tendencia STL es **−0,016**, y **−0,021** al omitir los pares que contienen el máximo. En esta exploración, la evidencia de un patrón semanal fijo es débil.

El tramo activo contiene menos de un año y solo representa una página. Estos resultados no identifican causas para los picos o cambios. Para comparar con el análisis topológico, las fechas de finales de mayo, el 26 de agosto y el 3 de octubre sirven como referencias con distinta sensibilidad a los parámetros.

El cálculo se reproduce desde la raíz del proyecto con `Rscript enfoque_estadistico/analisis.R`. El archivo [resultados.txt](resultados.txt) contiene los valores de cada métrica y de cada configuración.

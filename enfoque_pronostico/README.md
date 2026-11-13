# Pronóstico de visualizaciones de la página

La evaluación retrospectiva utiliza los 218 días calendario desde el primer valor positivo, el 8 de abril de 2026, hasta el 11 de noviembre. El bloque inicial de 97 ceros queda fuera para centrar la pregunta en el pronóstico durante la actividad observada. La fecha de inicio identifica el primer registro positivo y no confirma cuándo comenzó a operar la página.

Comparamos persistencia del último dato, pronóstico ingenuo semanal, mediana de los últimos siete días y regresión Ridge directa sobre `log1p(visualizaciones)`. Ridge usa los rezagos 1, 2, 7 y 14 respecto del primer día posterior al origen, medias recientes de 7 y 14 días y dos términos cíclicos para el día de la semana objetivo. Se ajusta un modelo distinto para cada horizonte y se fija la penalización en 10 sobre predictores estandarizados. La variante robusta limita el historial al percentil 95 de lo disponible en cada origen, tanto para predictores como para objetivos de entrenamiento. El error se mide en la escala original.

El primer origen usa 56 días de historial y avanza un día en cada iteración. En cada origen se vuelven a calcular la escala, los coeficientes y el percentil con datos disponibles hasta ese día. El ingenuo semanal y el último día coinciden para el horizonte de siete días. Los 162 objetivos de un día empiezan el 3 de junio y los 156 objetivos de siete días el 9 de junio. Ambos terminan el 11 de noviembre.

| Horizonte | Mejor referencia por MAE | MAE de referencia | Ridge log | Ridge log con tope p95 |
| --- | --- | ---: | ---: | ---: |
| Un día | Último día | 26.437 | 22.194 | 22.745 |
| Siete días | Mediana de siete días | 33.684 | 30.740 | 30.089 |

En la evaluación principal los objetivos incluyen el pico del 26 de agosto. En la comprobación de sensibilidad las predicciones históricas se conservan y se retira únicamente el error con fecha objetivo del 26 de agosto. El menor MAE sigue correspondiendo a Ridge en ambos horizontes. A un día se obtiene un MAE de 16.966 frente a 21.512 del último día. A siete días el modelo con tope alcanza 24.557 frente a 28.082 de la mediana móvil. Para la pérdida absoluta mediana a un día, el último día sí mejora a ambas variantes Ridge. El método preferido depende de cuánto pesen los errores grandes en la aplicación.

La elección del mejor modelo resume este mismo ejercicio retrospectivo. Para estimar el rendimiento tras elegir el modelo haría falta un tramo futuro independiente. Los orígenes consecutivos comparten historial y errores dependientes, por lo que estas diferencias se presentan como descriptivas.

Ejecutar `python3 enfoque_pronostico/pronostico.py` desde el espacio de trabajo con NumPy disponible. El script genera `predicciones.csv` con cada predicción y `metricas.csv` con MAE, RMSE y error absoluto mediano por modelo.

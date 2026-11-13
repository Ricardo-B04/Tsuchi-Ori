# ¿Aporta TDA al pronóstico del día siguiente?

Se evaluaron **162 pronósticos diarios**, del 3 de junio al 11 de noviembre de 2026. Los dos Ridge recibieron el mismo historial de visualizaciones, espectadores, interacciones, visitas y seguidores. La versión con TDA añadió dos variables, las distancias Wasserstein de orden uno en H₀ y H₁ entre las dos últimas nubes multivariadas.

Cada nube contiene 28 vectores de siete días con retardo de un día. El par de nubes abarca 35 días. Para cada fecha, se aplicó log(1 + x) y se centraron y escalaron ambas nubes con la misma mediana y rango intercuartílico de esos 35 días, disponibles al cierre de esa fecha. Un rango cero usa divisor uno. Se calculó persistencia Vietoris–Rips con distancia euclidiana. Este escalado local causal puede producir distancias distintas de las exploratorias del notebook, que usan una escala fija ajustada con todo el tramo activo.

Ambos Ridge se ajustaron con historial creciente desde el 8 de abril, con el primer pronóstico tras 56 días de historial. Solo se usaron filas de entrenamiento con objetivo ya observado. Ambos modelos usan cuatro rezagos, dos medias móviles por métrica y el día de la semana, con penalización fija de 10. Los predictores se estandarizaron solo con las filas de entrenamiento de cada corte. El objetivo se modeló en escala log(1 + x) y los errores se calcularon en visualizaciones.

| Modelo | MAE en 162 fechas | MAE sin el objetivo del 26 de agosto |
| --- | ---: | ---: |
| Último valor observado | 26.436,81 | 21.511,89 |
| Ridge multivariado | 24.809,97 | 19.636,14 |
| Ridge multivariado con TDA | 24.798,26 | 19.639,75 |

Añadir TDA redujo el MAE global en 11,71 visualizaciones (0,047 %). Al omitir solo el error del 26 de agosto, lo aumentó en 3,61. El error absoluto mediano bajó de 9.592,53 a 9.375,96 con TDA. El resultado es descriptivo de este ejercicio retrospectivo y la mejora en MAE no es consistente en la prueba de sensibilidad. El 26 de agosto sigue disponible en el historial de cortes posteriores.

Desde la raíz del proyecto, ejecutar `python3 "Página/pronostico_tda.py"` con Python 3.10 o superior y NumPy. [Código](pronostico_tda.py) · [Predicciones por fecha](predicciones_ridge_tda.csv)

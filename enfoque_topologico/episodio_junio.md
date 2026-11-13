# El cambio topológico del 16 de junio

La configuración de referencia usa visualizaciones diarias en escala log(1 + x), vectores de Takens de siete coordenadas y nubes de 28 vectores consecutivos. Cada nube abarca 34 días de la serie original. La homología persistente de Vietoris–Rips en dimensión uno resume los ciclos de cada nube. Wasserstein de orden uno compara cada diagrama con el anterior.

| Cierre de ventana | Visualizaciones del día | Ciclos con persistencia positiva | Persistencia máxima | Wasserstein H₁ frente al cierre anterior |
| --- | ---: | ---: | ---: | ---: |
| 15 de junio | 79.127 | 10 | 0,825 | — |
| 16 de junio | 33.073 | 7 | 1,644 | 1,467 |
| 17 de junio | 33.631 | 6 | 1,649 | 0,303 |

El intervalo más persistente del día 15 aparece entre las escalas 3,559 y 4,384. El del día 16 aparece entre 2,568 y 4,212. Los intervalos son los de mayor persistencia en cada diagrama. Para seguir un ciclo individual entre ventanas haría falta identificar y contrastar sus representantes.

En las 184 comparaciones para las que ambas ventanas se sitúan desde el primer registro positivo del 8 de abril, el 16 de junio ocupa el primer lugar por distancia Wasserstein H₁ y el puesto 38 por cambio absoluto de la media móvil en la misma escala. El mayor cambio de H₀ en este tramo se traslada al 1 de junio, cerca del cambio de nivel observado con la segmentación estadística a finales de mayo.

## Sensibilidad al pico

En una prueba retrospectiva se sustituyeron las 79.127 visualizaciones del 15 de junio por 19.877, la mediana de los siete días anteriores y los siete posteriores. Se recalcularon los tres diagramas.

| Comparación | Distancia observada | Distancia con el pico sustituido |
| --- | ---: | ---: |
| 15 a 16 de junio | 1,467 | 1,164 |
| 16 a 17 de junio | 0,303 | 1,019 |

La primera distancia cae aproximadamente 21 % y la segunda aumenta. El cambio de H₁ sigue presente en el episodio y su distribución entre fechas depende del valor del pico. La prueba describe sensibilidad a una observación. La persistencia de un ciclo en una nube local admite varias explicaciones y, por sí sola, deja abierta la periodicidad de la serie.

Desde la raíz del proyecto, ejecutar `python3 enfoque_topologico/episodio_junio.py`. El script utiliza la salida de `analisis.py` para comparar el tramo activo y escribe los intervalos de persistencia y las distancias en [episodio_junio.json](episodio_junio.json).

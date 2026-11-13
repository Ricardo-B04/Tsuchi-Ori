# Cambios en las visualizaciones diarias mediante homología persistente

El análisis usa las 315 observaciones diarias de visualizaciones de la página. La configuración principal aplica log(1 + visualizaciones), construye vectores de Takens de dimensión 7 y retardo de un día y agrupa 28 vectores consecutivos por nube. Cada nube abarca 34 fechas originales. Se calcula persistencia de Vietoris–Rips con distancia euclidiana y coeficientes en F₂ para H₀ y H₁. Después se compara cada diagrama con el del cierre anterior mediante Wasserstein de orden 1 con norma L∞. Se omite la componente esencial de H₀, que es idéntica en todas las ventanas. La primera de las 282 ventanas carece de comparación anterior, lo que deja 281 distancias por dimensión.

H₀ resume a qué escalas se conectan los puntos y H₁ resume la aparición y desaparición de ciclos en la nube. Como referencia sencilla se calcula el cambio absoluto de la media móvil en el mismo soporte temporal y sobre la misma escala que el análisis topológico.

| Serie de cambio en la configuración principal | Fecha del máximo | Valor |
| --- | --- | ---: |
| Wasserstein H₀ | 11 de mayo | 3,9940 |
| Wasserstein H₁ | 16 de junio | 1,4666 |
| Cambio absoluto de la media móvil en escala logarítmica | 6 de mayo | 0,3288 |

Los máximos de H₀ en las cinco configuraciones logarítmicas se concentraron entre el 2 y el 13 de mayo. Al variar el largo de la ventana con dimensión fija 7, el máximo se movió del 2 al 11 y al 13 de mayo. La ventana que cierra el 11 de mayo comienza el 8 de abril, justo al inicio de la actividad registrada. Parte de la señal coincide con la salida del tramo inicial de ceros del soporte temporal. Por su parte, los cinco análisis en logaritmos incluyeron alguna fecha del 15 al 18 de junio entre sus cuatro primeros cambios de H₁. Las visualizaciones saltaron de 8.620 el 14 de junio a 79.127 el día 15 y bajaron a 33.073 al día siguiente. El 16 de junio quedó en el puesto 72 por cambio de media móvil en la configuración principal.

El máximo observado de visualizaciones fue el 26 de agosto, con 911.216. En H₀ quedó en el puesto 95 de 281 con logaritmo, 12 con valores originales y 10 con raíz cuadrada, usando la misma ventana. En valores originales, los dos cambios de H₁ más grandes ocurrieron el 29 y el 30 de agosto. El cambio de escala modifica qué episodios destacan. Por el retardo, el dato del 26 de agosto entra y sale de distintos vectores a lo largo de varios días.

Las ventanas consecutivas comparten 27 de sus 28 vectores. Las distancias son indicadores descriptivos de cambio en las nubes, con dependencia temporal entre fechas. Para atribuir un pico a un cambio sostenido o hablar de periodicidad se necesitaría analizar su contexto o usar una referencia estadística que conserve la dependencia temporal.

## Reproducción

Desde el espacio de trabajo, ejecutar `python3 enfoque_topologico/analisis.py` con Python 3.10 o superior. Usa la biblioteca estándar y escribe [distancias.csv](distancias.csv). Cada fila identifica la escala, la dimensión de Takens, el número de puntos, el cierre y arranque del soporte temporal, la actividad del último día, las dos distancias, la mayor persistencia H₁ y el cambio de media. Se verificó el cálculo de persistencia con puntos coincidentes y un cuadrado unitario, y la asignación de Wasserstein contra búsqueda exhaustiva en matrices pequeñas.

[Perea y Harer, ventanas deslizantes y persistencia](https://arxiv.org/abs/1307.6188) · [Definición de Wasserstein en GUDHI](https://gudhi.inria.fr/python/3.10.0/wasserstein_distance_user.html)

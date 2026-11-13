# Análisis topológico de la actividad de Tsuchiori

El proyecto estudia cuándo cambia el patrón conjunto de actividad de una página de Facebook y cómo se distribuyen las reproducciones y las interacciones de sus videos durante la primera semana. El análisis de datos topológicos (TDA) permite revisar la forma de las trayectorias a partir de las distancias entre observaciones. Las series originales, las medianas y los totales dan contexto para interpretar los cambios que destacan.

| Objeto de estudio | Pregunta | Decisión informada por el análisis |
| --- | --- | --- |
| Página | ¿En qué fechas cambia la estructura conjunta del alcance y la respuesta del público? | Priorizar episodios para revisar las métricas originales y su evolución alrededor de un repunte. |
| Videos | ¿Qué perfiles de primera semana se repiten y cuáles presentan un despegue o un repunte tardío? | Seleccionar videos para revisión individual y distinguir la forma de su trayectoria del volumen total. |

## Datos y preparación

Las ocho exportaciones de origen están en [datos/originales](datos/originales/). Las bases preparadas y su procedencia se describen en el [índice de datos](datos/README.md).

- **Página.** La base tiene 315 fechas consecutivas del 1 de enero al 11 de noviembre de 2026. Las exportaciones se alinearon por fecha y se conservaron los ceros registrados. El análisis usa visualizaciones, espectadores, interacciones, visitas y la métrica diaria de seguidores. Los ingresos quedaron fuera por su bajo volumen, la duplicación exacta entre ingresos aproximados y monetización de contenido y la serie constante de Estrellas. El primer registro positivo de visualizaciones es del 8 de abril. El tramo anterior se conserva para comprobar la sensibilidad a los ceros iniciales. [Diccionario de Página](Página/diccionario_de_datos.md)
- **Videos.** La base contiene 30 videos y 1.260 filas, una por video y fecha de registro. Se normalizaron las fechas y se calculó la edad en días calendario desde la publicación. El análisis semanal compara los días 0 a 6 y exige siete valores observados y un total positivo en la métrica analizada. El día 0 puede ser parcial. Tres videos se publicaron cerca del cierre y quedaron fuera por cobertura incompleta. Los valores vacíos se distinguen de los ceros. [Diccionario de Videos](Videos/diccionario_de_datos.md)

## Protocolo de Página

1. **Inspección visual.** Graficar las cinco series con eje temporal común. Usar unidades originales para apreciar el volumen y la transformación `log1p` para examinar variaciones durante el tramo activo.
2. **Construcción de las nubes.** En la comparación multivariada se aplica `log1p` a cada métrica, se resta su mediana y se divide por su rango intercuartílico, calculados sobre el tramo activo. Cada vector de retardos reúne siete valores por métrica, con retardo de un día. La nube reúne 28 vectores consecutivos y abarca 34 días de datos originales. Se avanza un día por ventana. Siete coordenadas representan una semana de actividad y 28 vectores aportan contexto de aproximadamente cuatro semanas de cierres. Ambos parámetros son puntos de partida exploratorios.
3. **Persistencia y cambio.** Construir la filtración de Vietoris–Rips con distancia euclidiana y coeficientes en `F₂`. Calcular diagramas de componentes conexas (`H₀`) y ciclos (`H₁`). Comparar cada par de diagramas consecutivos mediante Wasserstein de orden 1 con norma `L∞` y emparejamiento a la diagonal. Omitir la componente esencial común de `H₀` y asignar la distancia a la fecha de cierre más reciente.
4. **Comprobaciones.** Contrastar los resultados univariados con el cambio absoluto de la media móvil en el mismo soporte temporal y escala. Examinar dimensiones de Takens de 5, 7 y 9, nubes de 21, 28 y 35 vectores en las combinaciones documentadas y transformaciones logarítmica, raíz cuadrada y original. Comparar las ventanas activas con el periodo completo. Para la comparación multivariada, mantener los parámetros y contrastar visualizaciones solas, las cinco métricas y el subconjunto de interacciones, visitas y seguidores.

| Método | Resultado e interpretación frente a una referencia sencilla |
| --- | --- |
| Vectores de retardos y persistencia | Los retardos conservan el orden de los días dentro de cada vector. El promedio móvil resume el nivel de la ventana. En el análisis univariado del tramo activo, el 16 de junio encabezó las 184 distancias en `H₁` y quedó 38.º por cambio de media móvil. Los diagramas muestran que la persistencia máxima pasó de 0,825 a 1,644 entre el 15 y el 16. |
| Wasserstein multivariado | El 29 de agosto quedó 92.º de 184 con visualizaciones solas y primero con las cinco métricas. Con interacciones, visitas y seguidores, el máximo pasó al 30 de agosto y el día 29 quedó segundo. El resultado identifica un cambio conjunto alrededor del pico de visualizaciones del 26, que todavía estaba incluido en esas ventanas. |

Las ventanas consecutivas comparten 27 de sus 28 vectores. Las distancias están temporalmente relacionadas y la fecha del máximo depende de las variables, la escala y los parámetros elegidos. Los ciclos de las nubes se interpretan como geometría local. Atribuirlos a una periodicidad de la serie o a decisiones del algoritmo de distribución requiere evidencia adicional.

[Notebook de Página](Página/exploracion_series_diarias.ipynb) · [Método topológico y sensibilidad](enfoque_topologico/README.md) · [Episodio de junio](enfoque_topologico/episodio_junio.md)

## Protocolo de Videos

1. **Ventana fija.** Usar los primeros siete días calendario. Entre los 19 videos con al menos 21 días observados, la mediana de la proporción de reproducciones de tres segundos acumulada en la primera semana fue 93,0 % de su total de 21 días. Extender a 14 días elevó esa mediana a 98,7 % y redujo de 27 a 23 el número de videos elegibles.
2. **Representación.** Para reproducciones de tres segundos, tiempo total reproducido o interacciones, representar cada video por siete proporciones diarias del total semanal. Conservar el total separado como contexto de volumen. Entre videos se usa distancia euclidiana.
3. **Mapper.** Construir cinco intervalos con 35 % de solapamiento sobre el rango observado de la lente. Dentro de cada intervalo, agrupar por enlace simple con radio 0,12. Cada componente conexa forma un nodo y dos nodos se unen si comparten un video. Las lentes ensayadas son la proporción en los días 0 y 1, el día promedio ponderado y, en el notebook, la mayor persistencia finita `H₀` dividida por el total semanal.
4. **Persistencia de repuntes y sensibilidad.** Aplicar una filtración por superniveles a cada curva semanal, con adyacencia entre días consecutivos. Cada barra finita positiva mide la diferencia entre la altura de un pico secundario y el valle donde su componente se une a la de un pico más alto. Separar en la interpretación los picos interiores y los del borde de la semana. Comparar lentes, coberturas y radios. En reproducciones, al pasar de 0,12 a 0,08 con la lente inicial, el nodo mayor pasó de 23 a 22 videos.

| Método | Resultado e interpretación frente a una referencia sencilla |
| --- | --- |
| Mapper | La proporción de los primeros dos días resume la concentración inicial. Mapper añade agrupamiento por la trayectoria de los siete días y permite inspeccionar los videos de cada nodo. El perfil predominante reunió 23 videos y el video de 134.422 reproducciones formó un nodo individual con las configuraciones de referencia probadas. |
| Persistencia `H₀` | La lente detectó el mayor repunte secundario relativo en un video de 1.763 reproducciones, de 59 el día 2 a 300 el día 4. Su persistencia fue 13,7 % del total semanal. Con los parámetros de referencia, la lente topológica y la inicial produjeron seis nodos y una arista, con 23 videos en el nodo mayor. El aporte observado está en identificar repuntes individuales. |

Seis de los ocho repuntes con mayor persistencia relativa alcanzan su pico en el día 6. Su evolución posterior queda fuera de la ventana semanal. Solo tres de los 27 videos superaron las 2.000 reproducciones en siete días, por lo que la evidencia se usa para describir trayectorias y casos, con alcance limitado para generalizar sobre viralidad.

[Notebook de Videos](Videos/02_mapper_videos.ipynb) · [Grafo interactivo](Videos/mapper_videos.html) · [Metodología de Mapper](Videos/metodologia_mapper_videos.md)

## Reproducción y alcance predictivo

Los notebooks incluyen figuras guardadas. Para regenerar los resultados calculados, ejecutar desde la raíz del repositorio con Python 3.10 o superior.

```bash
python3 enfoque_topologico/analisis.py
python3 enfoque_topologico/episodio_junio.py
python3 "Página/topologia_multivariada.py"
python3 Videos/mapper_videos.py
```

Ejecutar las celdas de los notebooks con un kernel Python 3. El notebook de Página utiliza también `Rscript` para generar las figuras. La lente de persistencia de Videos usa el módulo [persistencia_semanal.py](Videos/persistencia_semanal.py).

La evaluación cronológica de [Ridge](enfoque_pronostico/README.md) aporta una referencia predictiva para Página. La [comparación multivariada con y sin TDA](Página/validacion_predictiva.md) evaluó 162 pronósticos a un día. Añadir Wasserstein H₀ y H₁ redujo el MAE de 24.809,97 a 24.798,26, una diferencia menor al 0,05 %. Al omitir el error del 26 de agosto, Ridge con TDA obtuvo un MAE ligeramente mayor. Las distancias con escala ajustada al tramo activo completo se usan para describir los episodios. La prueba predictiva recalcula los descriptores con una escala local usando solo el historial disponible.

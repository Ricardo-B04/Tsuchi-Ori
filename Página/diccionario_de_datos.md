# Diccionario de datos de la página

La [base diaria de Tsuchiori](../datos/transformados/series_diarias_pagina.csv) contiene **315 filas**, una por día calendario, del **1 de enero al 11 de noviembre de 2026**. El análisis final utiliza la fecha y cinco métricas diarias. Las definiciones son operativas y se basan en los rótulos de las exportaciones de Facebook. El archivo no incluye los identificadores de métricas de la API de Meta.

## Campos del análisis final

| Columna | Tipo y unidad | Definición de trabajo |
| --- | --- | --- |
| `fecha` | Fecha, AAAA-MM-DD | Día calendario al que corresponden las métricas de la fila. Es el índice temporal de la serie. |
| `pagina_visualizaciones` | Entero, visualizaciones por día | Veces que el contenido de la página se mostró o se reprodujo durante el día. Una cuenta puede generar varias visualizaciones. |
| `pagina_espectadores` | Entero, cuentas por día | Cuentas distintas que vieron contenido de la página durante el día, según la interpretación del rótulo «Espectadores». Al sumar días, una cuenta puede contarse más de una vez. |
| `pagina_interacciones` | Entero, acciones por día | Acciones sobre el contenido, como reacciones, comentarios y veces que se compartió. La exportación entrega un agregado diario sin desglose por acción. |
| `pagina_visitas` | Entero, visitas por día | Veces que se visitó la página de Facebook durante el día. La unidad es la visita a la página. |
| `pagina_seguidores_metrica_diaria` | Entero, valor diario | Valor exportado como «Seguidores de Facebook». Su comportamiento es compatible con un flujo diario de seguimientos. Queda por confirmar en Meta si representa seguimientos nuevos brutos o cambio neto. Hasta entonces se interpreta como la métrica diaria exportada. |

## Campos excluidos del análisis final

| Columna | Hallazgo | Motivo de exclusión |
| --- | --- | --- |
| `pagina_ingresos_aproximados` | Suma de 31,09347898 en el periodo, con valores positivos en 165 de 315 días. La exportación no indica la moneda. | El ingreso observado es reducido y queda fuera del foco del análisis final, centrado en alcance, interacción, visitas y seguimiento. |
| `pagina_ingresos_monetizacion_contenido` | Coincide exactamente con ingresos aproximados en las 315 fechas. | Duplica la señal de ingresos en esta exportación y le daría peso adicional en un análisis multivariado. |
| `pagina_ingresos_estrellas` | Registra cero en las 315 fechas. | Es una serie constante y carece de variación temporal. |

Los tres campos se conservan en la base diaria y pueden rastrearse a la [exportación original de ingresos](../datos/originales/ingresos.csv). La exclusión se aplica al conjunto de variables del análisis final.

[Referencia de estadísticas de páginas de Meta](https://developers.facebook.com/docs/graph-api/reference/insights/?locale=es_LA)

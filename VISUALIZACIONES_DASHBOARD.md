# 📊 Visualizaciones Dashboard Liga 24-25

Este documento presenta algunas de las visualizaciones del dashboard interactivo de análisis de la Liga 24-25 en forma de capturas de imagen.

Lo óptima es poder runear el código del archivo dashboard.py para poder ver las visualizaciones de forma interactiva, pero entendemos que, en caso de no ser posible, esto podría dar una buena idea de a qué hacen referencia los gráficos.

---

## 📊 Resumen General

### Métricas Principales

![Métricas Principales](./capturas/01_metricas_principales.png)

*Métricas clave: Partidos jugados, goles totales, promedio de goles, asistencia media y victorias locales.*

### Distribución de Resultados

![Distribución de Resultados](./capturas/02_distribucion_resultados.png)

*Histograma que muestra la frecuencia de victorias locales, empates y victorias visitantes.*

---

## ⚽ Análisis de Goles

### Distribución del Número de Goles

![Distribución Goles](./capturas/04_distribucion_goles.png)

*Histograma que evalúa si la liga es ofensiva o defensiva según el número total de goles por partido.*

### Tiros Totales vs Goles del Equipo Local

![Tiros vs Goles Local](./capturas/07_tiros_vs_goles_local.png)

*Eficiencia ofensiva del equipo local: relación entre tiros realizados y goles anotados con línea de tendencia.*

### Distribución de Tiros a Puerta según Resultado

![Tiros a Puerta por Resultado](./capturas/08_tiros_puerta_resultado.png)

*Gráfico de violín que muestra cómo se distribuyen los tiros a puerta según el resultado final.*

---

## 🏠 Local vs Visitante

### Promedio de Goles por Equipo vs Asistencia Media

![Goles vs Asistencia por Equipo](./capturas/13_goles_vs_asistencia_equipo.png)

*Scatter plot que compara el rendimiento ofensivo promedio de cada equipo con la asistencia media.*

---

## 🟥 Disciplina

### Distribución de Tarjetas por Partido

![Distribución Tarjetas](./capturas/14_distribucion_tarjetas.png)

*Histograma que mide el nivel de agresividad mediante la suma de tarjetas amarillas y rojas.*

### Tarjetas vs Resultado

![Tarjetas vs Resultado](./capturas/15_tarjetas_vs_resultado.png)

*Boxplot que analiza si la indisciplina influye en el resultado final del partido.*

---

## 🌦️ Clima

### Distribución de Condiciones Climáticas

![Condiciones Climáticas](./capturas/16_condiciones_climaticas.png)

*Gráfico de barras con emojis que muestra la frecuencia de cada condición climática.*

### Tabla de Partidos por Clima

![Tabla Clima](./capturas/17_tabla_clima.png)

*Tabla completa con fecha, equipos, clima, temperatura, precipitación, viento y goles.*

### Temperatura vs Goles

![Temperatura vs Goles](./capturas/18_temperatura_vs_goles.png)

*Scatter plot que analiza si la temperatura influye en el número total de goles por partido.*

### Precipitación vs Tarjetas

![Precipitación vs Tarjetas](./capturas/19_precipitacion_vs_tarjetas.png)

*Estudia si la lluvia incrementa el número de tarjetas mostradas.*

### Clima vs Asistencia

![Clima vs Asistencia](./capturas/20_clima_vs_asistencia.png)

*Scatter plot 3D que relaciona temperatura, precipitación y asistencia (tamaño = goles totales).*

### Tabla de Rendimiento según Clima

![Rendimiento por Clima](./capturas/21_rendimiento_clima.png)

*Estadísticas promedio (goles, tarjetas, asistencia) ordenadas por condición climática.*

---

## 🗺️ Estadios & Asistencia

### Mapa: Rendimiento Ofensivo Local por Estadio

![Mapa Goles Locales](./capturas/22_mapa_goles_locales.png)

*Mapa geográfico donde el tamaño = asistencia media y el color = goles del equipo local.*

### Mapa: Goles Recibidos por Estadio

![Mapa Goles Encajados](./capturas/23_mapa_goles_encajados.png)

*Mapa geográfico donde el tamaño = asistencia media y el color = goles recibidos por el local.*

---

## 👥 Asistencia

### Evolución Temporal de la Asistencia

![Evolución Asistencia](./capturas/24_evolucion_asistencia.png)

*Gráfico de líneas que muestra la evolución de asistencia media a lo largo de la temporada por equipo local.*

### Distribución de Asistencia

![Distribución Asistencia](./capturas/25_distribucion_asistencia.png)

*Histograma con curva KDE que muestra la distribución de asistencia a los partidos.*

---

## 💰 Mercado de Apuestas

### Cuota Media Local vs Goles

![Cuota vs Goles](./capturas/26_cuota_vs_goles.png)

*Scatter plot que relaciona las expectativas del mercado (cuotas) con los resultados reales de goles.*

### Cuota Esperada del Resultado Real

![Cuota por Resultado](./capturas/27_cuota_resultado.png)

*Gráfico de violín que muestra la distribución de cuotas asociadas a cada resultado final.*

### Partidos Sorpresa

![Partidos Sorpresa](./capturas/28_partidos_sorpresa.png)

*Gráfico de dona que identifica victorias locales o visitantes con cuotas elevadas (resultados inesperados).*

---

## 🏟️ Predicción de Resultados - Regresión Logística

### Selección Progresiva Hacia Adelante

![Forward Selection](./capturas/30_forward_selection.png)

*Gráfico F1-score vs número de variables mostrando el proceso de selección hacia adelante.*

### Variables del Mejor Modelo Forward

![Variables Forward](./capturas/31_variables_forward.png)

*Tabla con las 50 variables seleccionadas del mejor modelo forward (F1 = 0.58).*

### Selección Progresiva Hacia Atrás

![Backward Selection](./capturas/32_backward_selection.png)

*Gráfico F1-score vs número de variables mostrando el proceso de selección hacia atrás.*

### Variables del Mejor Modelo Backward

![Variables Backward](./capturas/33_variables_backward.png)

*Tabla con las 45 variables seleccionadas del mejor modelo backward (F1 = 0.55).*

### Comparativa de Modelos

![Comparativa Modelos](./capturas/34_comparativa_modelos.png)

*Tabla comparativa de F1-score y número de variables entre ambos métodos de selección.*

### Errores de Generalización

![Errores Generalización](./capturas/35_errores_generalizacion.png)

*Tabla con F1-score en conjunto de prueba para ambos modelos.*

### Matriz de Confusión

![Matriz Confusión](./capturas/36_matriz_confusion.png)

*Heatmap que muestra cómo el modelo clasifica cada resultado (H, D, A).*

### Distribución de Probabilidades de Predicción

![Probabilidades Predicción](./capturas/37_probabilidades_prediccion.png)

*Boxplot de probabilidades predichas para cada tipo de resultado.*

### Análisis de Errores: Correctas vs Incorrectas

![Análisis Errores](./capturas/38_analisis_errores.png)

*Histograma que compara la confianza del modelo en predicciones correctas e incorrectas.*

## 🏟️ Predicción de Asistencia - Random Forest

### Métricas del Modelo

![Métricas Random Forest](./capturas/41_metricas_random_forest.png)

*Tabla con MAE, MSE y R² del modelo Random Forest Regressor.*

### Top 20 Variables Más Influyentes

![Variables Influyentes](./capturas/42_variables_influyentes.png)

*Gráfico de barras horizontal con las variables más importantes según feature importance.*

### Predicciones con Intervalo de Confianza

![Intervalo Confianza](./capturas/43_intervalo_confianza.png)

*Gráfico que muestra predicciones, valores reales e intervalo de confianza al 95%.*

### Asistencia Real vs Predicha

![Real vs Predicha](./capturas/44_real_vs_predicha.png)

*Scatter plot con línea diagonal que compara valores reales y predichos.*

### Distribución de Errores (Residuos)

![Distribución Residuos](./capturas/45_distribucion_residuos.png)

*Histograma de residuos y Q-Q plot para evaluar normalidad.*

### Errores por Equipo Local

![Errores por Equipo](./capturas/47_errores_por_equipo.png)

*Gráfico de barras con el error absoluto medio por equipo local.*

### Top 5 Mayores Subestimaciones y top 5 meyores sobreestimaciones

![Subestimaciones](./capturas/48_subestimaciones.png)

*Tabla con partidos donde la predicción fue menor que la asistencia real y tabla con partidos donde la predicción fue mayor que la asistencia real..*

### Residuos vs Predicciones

![Residuos vs Predicciones](./capturas/50_residuos_vs_predicciones.png)

*Scatter plot para detectar patrones sistemáticos en los errores del modelo.*

---

## 📋 Datos Completos

### Vista de Tabla de Datos

![Tabla Datos](./capturas/51_tabla_datos.png)

*Vista completa de los datos filtrados con todas las columnas disponibles.*

---

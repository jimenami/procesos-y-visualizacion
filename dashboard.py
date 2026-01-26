# Instalar en la terminal
# pip install streamlit pandas numpy plotly
# pip install folium streamlit-folium

from sklearn.model_selection import train_test_split
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import plotly.graph_objects as go
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, classification_report
from scipy import stats


# ---------------------------------
# FUNCIONES AUXILIARES
# ---------------------------------
def obtener_emoji_clima(codigo_clima):
    """
    Retorna un emoji según el código del clima WMO simplificado
    Códigos basados en la clasificación de precipitación WMO
    """
    # Manejar valores NaN
    if pd.isna(codigo_clima):
        return "🌤️"

    # Convertir a entero para evitar problemas con flotantes
    codigo = int(codigo_clima)

    # Mapeo de códigos WMO simplificados a emojis
    emojis = {
        0: "☀️",   # Despejado (sin nubes)
        1: "🌤️",   # Mayormente despejado
        2: "⛅",   # Parcialmente nublado
        3: "☁️",   # Nublado
        45: "🌫️",  # Niebla
        48: "🌫️",  # Niebla con escarcha
        51: "🌦️",  # Llovizna ligera
        53: "🌧️",  # Llovizna moderada
        55: "🌧️",  # Llovizna densa
        56: "🌧️",  # Llovizna helada ligera
        57: "🌧️",  # Llovizna helada densa
        61: "🌧️",  # Lluvia ligera
        63: "🌧️",  # Lluvia moderada
        65: "🌧️",  # Lluvia fuerte
        66: "🌧️",  # Lluvia helada ligera
        67: "🌧️",  # Lluvia helada fuerte
        71: "🌨️",  # Nevada ligera
        73: "🌨️",  # Nevada moderada
        75: "❄️",   # Nevada fuerte
        77: "❄️",   # Nieve granulada
        80: "🌦️",  # Chubascos de lluvia ligeros
        81: "🌧️",  # Chubascos de lluvia moderados
        82: "🌧️",  # Chubascos de lluvia violentos
        85: "🌨️",  # Chubascos de nieve ligeros
        86: "❄️",   # Chubascos de nieve fuertes
        95: "⛈️",   # Tormenta ligera o moderada
        96: "⛈️",   # Tormenta con granizo ligero
        99: "⛈️",   # Tormenta con granizo fuerte
    }

    return emojis.get(codigo, "🌤️")  # Emoji por defecto

def obtener_descripcion_clima(codigo_clima):
    """
    Retorna descripción textual del clima según el código WMO
    """
    if pd.isna(codigo_clima):
        return "Desconocido"

    codigo = int(codigo_clima)
    descripciones = {
        0: "Despejado",
        1: "Mayormente despejado",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Niebla",
        48: "Niebla con escarcha",
        51: "Llovizna ligera",
        53: "Llovizna moderada",
        55: "Llovizna densa",
        61: "Lluvia ligera",
        63: "Lluvia moderada",
        65: "Lluvia fuerte",
        71: "Nevada ligera",
        73: "Nevada moderada",
        75: "Nevada fuerte",
        80: "Chubascos ligeros",
        81: "Chubascos moderados",
        82: "Chubascos violentos",
        85: "Chubascos de nieve ligeros",
        86: "Chubascos de nieve fuertes",
        95: "Tormenta",
        96: "Tormenta con granizo ligero",
        99: "Tormenta con granizo fuerte",
    }
    return descripciones.get(codigo, "Desconocido")

# ---------------------------------
# CONFIGURACIÓN GENERAL
# ---------------------------------
st.set_page_config(
    page_title="Dashboard Liga 24-25",
    layout="wide"
)

st.title("⚽ Dashboard Interactivo – Liga 24-25")

# ---------------------------------
# CARGA DE DATOS
# ---------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("outputs/partidos_con_clima_completo.csv")
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df["Time"] = pd.to_datetime(df["Time"], format="%H:%M", errors="coerce").dt.time
    df["Goles_Totales"] = df["FTHG"] + df["FTAG"]
    df["Dif_goles_local"] = df["FTHG"] - df["FTAG"]
    df["Over_2_5"] = df["Goles_Totales"] > 2.5
    df["Resultado"] = df["FTR"].map({"H": "Gana Local","D": "Empate","A": "Gana Visitante"})
    df["Tarjetas"] = df["HY"] + df["AY"] + df["HR"] + df["AR"]
    df["Goles_Descanso"] = df["HTHG"] + df["HTAG"]
    df["Tiros_Puerta_Totales"] = df["HST"] + df["AST"]
    df["Cuota_Resultado"] = df.apply(
        lambda x: x["AvgH"] if x["FTR"] == "H" else
                x["AvgD"] if x["FTR"] == "D" else
                x["AvgA"],
        axis=1)
    umbral = 4
    df["Sorpresa"] = "No"
    df.loc[(df["FTR"] == "H") & (df["AvgH"] > umbral), "Sorpresa"] = "Sorpresa Local"
    df.loc[(df["FTR"] == "A") & (df["AvgA"] > umbral), "Sorpresa"] = "Sorpresa Visitante"

    # Añadir emojis y descripción del clima
    df["Emoji_Clima"] = df["Codigo_Clima"].apply(obtener_emoji_clima)
    df["Descripcion_Clima"] = df["Codigo_Clima"].apply(obtener_descripcion_clima)
    df["Clima_Completo"] = df["Emoji_Clima"] + " " + df["Descripcion_Clima"]

    return df

def load_data1():
    df1 = pd.read_csv("outputs/partidos_con_clima_completo.csv")
    return df1

df = load_data()
df1 = load_data1()

# ---------------------------------
# SIDEBAR – FILTROS
# ---------------------------------
st.sidebar.header("🔍 Filtros")
equipos = sorted(set(df["Local"]).union(df["Visitante"]))
equipos_sel = st.sidebar.multiselect("Selecciona equipos (vacío = todos)", equipos)
fecha_inicio, fecha_fin = st.sidebar.date_input("Rango de fechas", [df["Date"].min(), df["Date"].max()])

pagina = st.sidebar.radio("📑 Sección", [
    "📊 Resumen",
    "⚽ Goles",
    "🏠 Local VS Visitante",
    "📈 Estadísticas de Juego",
    "🟥 Disciplina",
    "🌦️ Clima",
    "🗺️ Estadios",
    "👥 Asistencia",
    "💰 Mercado de Apuestas",
    "📋 Datos",
    "🏟️ Predicción en los Partidos"
])

# ---------------------------------
# FILTRO DE DATOS
# ---------------------------------
df_filt = df.copy()
if equipos_sel:
    df_filt = df_filt[(df_filt["Local"].isin(equipos_sel)) | (df_filt["Visitante"].isin(equipos_sel))]
df_filt = df_filt[df_filt["Date"].between(pd.to_datetime(fecha_inicio), pd.to_datetime(fecha_fin))]

# ======================================================
# 📊 RESUMEN GENERAL
# ======================================================
if pagina == "📊 Resumen":
    st.subheader("Resumen General de la Competición")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Partidos", len(df_filt))
    c2.metric("Goles Totales", int(df_filt["Goles_Totales"].sum()))
    c3.metric("Promedio de Goles", round(df_filt["Goles_Totales"].mean(), 2))
    c4.metric("Asistencia Media", int(df_filt["Asistencia"].mean()))
    c5.metric("% Victorias Locales", f"{round((df_filt['FTR'] == 'H').mean() * 100, 2)}%")

    c6, c7, c8, c9, c10 = st.columns(5)
    c6.metric("% Victorias Visitante", f"{round((df_filt['FTR'] == 'A').mean() * 100, 2)}%")
    c7.metric("Media de Tarjetas", round(df_filt["Tarjetas"].mean(), 2))
    c8.metric("Media Temperatura (°C)", round(df_filt["Temperatura_C"].mean(), 1))
    c9.metric("Media Viento (km/h)", round(df_filt["Viento_kmh"].mean(), 1))
    c10.metric("Media Precipitación (mm)", round(df_filt["Precipitacion_mm"].mean(), 1))
    
    fig = px.histogram(df_filt, x="Resultado", color="Resultado", title="Distribución de resultados de un partido")
    st.plotly_chart(fig, width="stretch")
    st.caption("Gráfico de barras para comparar los resultados de un partido (gana el equipo local, gana el equipo visitante o quedan empate).")

    df_corr = df_filt.select_dtypes(include=["int64", "float64"])
    corr_matrix = df_corr.corr()
    fig, ax = plt.subplots(figsize=(14, 10))
    sns.heatmap(corr_matrix, cmap="coolwarm", center=0, linewidths=0.5, cbar_kws={"shrink": 0.8}, ax=ax)
    ax.set_title("Matriz de correlación", fontsize=14)
    st.pyplot(fig)
    st.caption("Matriz de correlación entre las variables numéricas.")


# ======================================================
# ⚽ GOLES
# ======================================================
elif pagina == "⚽ Goles":
    st.subheader("Análisis de Goles")
    
    fig1 = px.histogram(df_filt, x="Goles_Totales", title="Distribución del número de goles", labels={"Goles_Totales": "Número de goles"})
    st.plotly_chart(fig1, width="stretch")
    st.caption("Histograma para determinar la distribución del número de goles que se marcan durante un partido.")

    fig2 = px.histogram(df_filt, x="Over_2_5", color="Over_2_5", title="Over / Under 2.5 Goles")
    st.plotly_chart(fig2, width="stretch")
    st.caption("Gráfico de barras para medir la frecuencia de partidos con más de 2.5 goles (Over) y menos de 2.5 goles (Under).")

    fig3 = px.scatter(df_filt, x="Goles_Descanso", y="Goles_Totales", title="Goles al descanso VS al final", labels={"Goles_Descanso": "Goles al descanso", "Goles_Totales": "Goles al final del partido"})
    st.plotly_chart(fig3, width="stretch")
    st.caption("Scatter plot para analizar la relación entre los goles al descanso y los goles finales del partido.")


    fig4 = px.scatter(df_filt, x="HS", y="FTHG", color="Resultado", trendline="ols", title="Tiros totales vs Goles del equipo local", labels={ "HS": "Tiros totales (local)", "FTHG": "Goles (local)"})
    st.plotly_chart(fig4, use_container_width=True)
    st.caption("Scatter plot para estudiar la relación causa-efecto entre cuántas veces dispara el equipo local y cuántos goles marca realmente, diferenciando con colores si el equipo local ganó, perdió o empató. Se le superpone por etiqueta la línea de tendencia.")

    fig5 = px.violin(df_filt, x="Resultado", y="Tiros_Puerta_Totales", box=True, points="all", title="Distribución de tiros a puerta totales según el resultado del partido", labels={"Resultado": "Resultado final", "Tiros_Puerta_Totales": "Tiros a puerta totales"})
    st.plotly_chart(fig5, use_container_width=True)
    st.caption("Gráfico de violín para comparar la distribución de tiros a puerta totales realizados en función del resultado final del partido.")


# ======================================================
# 🏠 LOCAL VS VISITANTE
# ======================================================
elif pagina == "🏠 Local VS Visitante":
    st.subheader("Comparativa local VS Visitante")
    df_lv = pd.DataFrame({"Local": df_filt["FTHG"], "Visitante": df_filt["FTAG"]})
    fig = px.box(df_lv, title="Distribución de Goles", labels={"variable": "Equipo", "value": "Número de goles"})
    st.plotly_chart(fig, width="stretch")
    st.caption("Box plot para comparar el rendimiento ofensivo jugando en casa y fuera; es decir, se estudia la distribución del número de goles para los equipos locales y para los equipos visitantes.")


# ======================================================
# 📈 ESTADÍSTICAS DE JUEGO
# ======================================================
elif pagina == "📈 Estadísticas de Juego":
    st.subheader("Estadísticas del Partido")
    fig1 = px.scatter(df_filt, x="HS", y="FTHG", title="Tiros locales VS Goles", labels={"HS": "Tiros totales (local)", "FTHG": "Goles (local)"})
    st.plotly_chart(fig1, width="stretch")
    st.caption("Scatter plot que relaciona los tiros que realizan los equipos locales con los goles que realmente marcan.")
    
    fig2 = px.scatter(df_filt, x="HST", y="FTHG", title="Tiros a puerta VS Goles", labels={"HST": "Tiros a puerta", "FTHG": "Goles (local)"})
    st.plotly_chart(fig2, width="stretch")
    st.caption("Scatter plot relacionando los tiros a puerta con el número total de goles.")
    
    fig3 = px.scatter(df_filt, x="HC", y="FTHG", title="Córners VS Goles", labels={"HC": "Córners", "FTHG": "Goles"})
    st.plotly_chart(fig3, width="stretch")
    st.caption("Scatter plot para analizar la relación entre el número de córners vs goles; esto es, se analiza si la presión ofensiva generada por córners produce más goles.")
    
    # Promedio de goles por equipo vs asistencia
    df_local = df_filt.groupby("Local").agg({"Goles_Totales": "mean","Asistencia": "mean"}).reset_index()
    fig4 = px.scatter(df_local, x="Goles_Totales", y="Asistencia", hover_data=["Local"], size="Asistencia", title="Promedio de goles por equipo VS Asistencia media", labels={"Goles_Totales": "Promedio de goles por equipo", "Asistencia": "Asistencia media"})
    st.plotly_chart(fig4, width="stretch")
    st.caption("Scatter plot de burbujas para relacionar el promedio de goles por equipo con la asistencia media a los partidos de ese equipo, en el que cada punto representa a un equipo específico y su tamaño nos da información extra.")

# ======================================================
# 🟥 DISCIPLINA
# ======================================================
elif pagina == "🟥 Disciplina":
    st.subheader("Disciplina y Juego Brusco")
    fig1 = px.histogram(df_filt, x="Tarjetas", title="Distribución de tarjetas por partido")
    st.plotly_chart(fig1, width="stretch")
    st.caption("Histograma para estudiar la distribución que siguen las tarjetas sacadas por partido.")
    
    fig2 = px.box(df_filt, x="Resultado", y="Tarjetas", title="Tarjetas VS Resultado")
    st.plotly_chart(fig2, width="stretch")
    st.caption("Box plot para estudiar cómo se distribuyen las tarjetas en función del resultado de un partido.")

# ======================================================
# 🌦️ CLIMA
# ======================================================
elif pagina == "🌦️ Clima":
    st.subheader("Impacto del Clima")

    # Distribución de condiciones climáticas con emojis
    st.subheader("🌤️ Distribución de Condiciones Climáticas")
    clima_counts = df_filt["Clima_Completo"].value_counts().reset_index()
    clima_counts.columns = ["Clima", "Cantidad"]
    fig_clima = px.bar(clima_counts, x="Clima", y="Cantidad",
                       title="Frecuencia de condiciones climáticas en los partidos",
                       text="Cantidad",
                       color="Cantidad",
                       color_continuous_scale="Blues")
    fig_clima.update_traces(textposition='outside')
    fig_clima.update_xaxes(tickangle=-45)
    st.plotly_chart(fig_clima, use_container_width=True)
    st.caption("Diagrama de barras que visualiza las condiciones climáticas más frecuentes durante los partidos de la temporada.")

    # Tabla con partidos y su clima
    st.subheader("📋 Partidos por condición climática")
    df_clima_tabla = df_filt[["Date", "Local", "Visitante", "Clima_Completo", "Temperatura_C", "Precipitacion_mm", "Viento_kmh", "Goles_Totales"]].copy()
    df_clima_tabla = df_clima_tabla.sort_values("Date", ascending=False)
    df_clima_tabla.columns = ["Fecha", "Local", "Visitante", "Clima", "Temp. (°C)", "Precip. (mm)", "Viento (km/h)", "Goles"]
    st.dataframe(df_clima_tabla, use_container_width=True)

    fig1 = px.scatter(df_filt, x="Temperatura_C", y="Goles_Totales", title="Temperatura VS Goles", hover_data=["Local", "Visitante", "Emoji_Clima"], labels={"Temperatura_C": "Temperatura (°C)", "Goles_Totales": "Número total de goles"})
    st.plotly_chart(fig1, width="stretch")
    st.caption("Scatter plot para analizar si la temperatura influye en el número total de goles por partido.")

    fig2 = px.scatter(df_filt, x="Precipitacion_mm", y="Tarjetas", title="Precipitación VS Tarjetas", hover_data=["Local", "Visitante", "Emoji_Clima"], labels={"Precipitacion_mm": "Precipitación (mm)", "Tarjetas": "Número de tarjetas"})
    st.plotly_chart(fig2, width="stretch")
    st.caption("Scatter plot que estudia si la lluvia incrementa el número de tarjetas sacadas.")

    fig3 = px.scatter(df_filt, x="Temperatura_C", y="Asistencia", size="Goles_Totales", color="Precipitacion_mm", title="Clima VS Asistencia", hover_data=["Local", "Visitante", "Emoji_Clima"], labels={"Temperatura_C": "Temperatura (°C)", "Asistencia": "Asistencia", "Precipitacion_mm": "Precipitación (mm)", "Goles_Totales": "Número total de goles"})
    st.plotly_chart(fig3, width="stretch")
    st.caption("Gráfico de dispersión multidimensional que relaciona la asistencia y el número de goles que ocurren en un partido junto con la precipitación y temperatura que se dan en el mismo. El tamaño de los puntos representa el número de goles, mientras que el color indica la cantidad de precipitación.")

    # Análisis de rendimiento por clima
    st.subheader("⚽ Rendimiento según condiciones climáticas")
    clima_stats = df_filt.groupby("Clima_Completo").agg({
        "Goles_Totales": "mean",
        "Tarjetas": "mean",
        "Asistencia": "mean"
    }).round(2).reset_index()
    clima_stats.columns = ["Condición Climática", "Goles Promedio", "Tarjetas Promedio", "Asistencia Promedio"]
    clima_stats = clima_stats.sort_values("Goles Promedio", ascending=False)
    st.dataframe(clima_stats, use_container_width=True)
    st.caption("Estadísticas promedio de los partidos según las condiciones climáticas. Ordenado por goles promedio de mayor a menor.")

# ======================================================
# 🗺️ ESTADIOS 
# ======================================================
elif pagina == "🗺️ Estadios":
    st.subheader("Análisis Geográfico: Estadios, Asistencia y Goles")

    # Preparación de datos para el Mapa de Rendimiento Local
    # Agrupamos solo por dimensiones geográficas y calculamos las medias
    df_estadios_local = (df_filt.groupby(["Estadio", "Latitud", "Longitud"]).agg(Asistencia_Media=("Asistencia", "mean"), Goles_Local_Media=("FTHG", "mean")).reset_index())

    fig1 = px.scatter_mapbox(df_estadios_local, lat="Latitud", lon="Longitud", size="Asistencia_Media", color="Goles_Local_Media", hover_name="Estadio", hover_data={"Latitud": False, "Longitud": False, "Asistencia_Media": ":.0f", "Goles_Local_Media": ":.2f"}, color_continuous_scale="RdYlGn", zoom=5, mapbox_style="carto-positron", title="Asistencia media y rendimiento ofensivo local por estadio", labels={"Goles_Local_Media": "Promedio Goles Local", "Asistencia_Media": "Asistencia Media"})
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("Mapa interactivo que muestra la asistencia media por estadio y el promedio de goles marcados por el equipo local en su propio campo. El tamaño de los puntos representa la asistencia media, mientras que el color indica la cantidad de goles que se marcan.")

    # Preparación de datos para el Mapa de Vulnerabilidad (Goles Visitantes)
    df_estadios_visitantes = (df_filt.groupby(["Estadio", "Latitud", "Longitud"]).agg(Asistencia_Media=("Asistencia", "mean"), Goles_Recibidos_Media=("FTAG", "mean")).reset_index())

    fig2 = px.scatter_mapbox(
    df_estadios_visitantes, lat="Latitud", lon="Longitud", size="Asistencia_Media", color="Goles_Recibidos_Media", hover_name="Estadio", hover_data={"Latitud": False, "Longitud": False, "Asistencia_Media": ":.0f", "Goles_Recibidos_Media": ":.2f"}, color_continuous_scale="Reds", zoom=5, mapbox_style="carto-positron", title="Asistencia media y goles recibidos por el equipo local en su estadio",labels={"Goles_Recibidos_Media": "Promedio Goles Visitante", "Asistencia_Media": "Asistencia Media"})
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Mapa interactivo que muestra la asistencia media por estadio y el promedio de goles marcados por el equipo visitante. El tamaño de los puntos representa la asistencia media, mientras que el color indica la cantidad de goles que se marcan.")

# ======================================================
# 💰 APUESTAS
# ======================================================
elif pagina == "💰 Mercado de Apuestas":
    st.subheader("Análisis del Mercado de Apuestas")
    fig = px.scatter(df_filt, x="AvgH", y="Dif_goles_local", title="Cuota media local VS Goles", labels={"AvgH": "Cuota media equipo local", "Dif_goles_local": "Diferencia de goles (local - visitante)"})
    st.plotly_chart(fig, width="stretch")
    st.caption("Scatter plot para comparar lo que las casas de apuestas creen que va a pasar (cuotas) frente a lo que acaba ocurriendo en realidad, en lo que respecta a los equipos locales. En las apuestas, una cuota baja significa que el equipo es muy favorito y una cuota alta, que es muy poco probable que gane.")

    fig2 = px.violin(df_filt, x="Resultado", y="Cuota_Resultado", box=True, points="all", title="Cuota esperada del resultado reaL", labels={"Resultado": "Resultado final", "Cuota_Resultado": "Cuota media asociada"})
    st.plotly_chart(fig2, width="stretch")
    st.caption("Gráfico de violín para analizar la distribución de la cuota media asociada al resultado final del partido.")

    df_sorpresa = df_filt[df_filt["Sorpresa"] != "No"]
    fig3 = px.pie(df_sorpresa, names="Sorpresa", title="Partidos sorpresa según el mercado de apuestas", hole=0.3)
    st.plotly_chart(fig3, width="stretch")
    st.caption("Gráfico de tarta para, de todos los partidos que tiene una resultado sorpresa (ocurre lo contrario que dicen las cuotas), ver el porcentaje de sorpresas locales o sorpresas visitantes.")


# ======================================================
# 📋 DATOS
# ======================================================
elif pagina == "📋 Datos":
    st.subheader("Datos Completos")
    st.dataframe(df_filt, use_container_width=True)


# ======================================================
# ASISTENCIA
# ======================================================

elif pagina == "👥 Asistencia":
    st.subheader("Evolución de la Asistencia a lo Largo de la Temporada")

    df_asistencia_tiempo = (df_filt.groupby(["Date", "Local"], as_index=False).agg({"Asistencia": "mean"}))
    fig = px.line(df_asistencia_tiempo, x="Date", y="Asistencia", color="Local", markers=True, title="Evolución Temporal de la Asistencia por Equipo Local")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Gráfico de líneas temporales donde se muestra cómo evoluciona la asistencia media a los estadios a lo largo de la temporada para cada equipo local.")

    fig, ax = plt.subplots(figsize=(10,5))
    sns.histplot(df_filt['Asistencia'], bins=30, kde=True, color='skyblue', ax=ax)
    ax.set_xlabel("Asistencia")
    ax.set_ylabel("Número de partidos")
    ax.set_title("Distribución de la asistencia a los partidos")
    st.pyplot(fig)
    st.caption("Histograma para estudiar la distribución de la asistencia a los partidos.")



# ======================================================
# 🏟️ PREDICCIÓN DE PARTIDOS
# ======================================================
elif pagina == "🏟️ Predicción en los Partidos":
    st.subheader("Predicciones de Partidos – Modelos de Fútbol")

    # Texto descriptivo
    st.write(""" 
             En esta página, realizamos predicciones sobre diferentes puntos de interés relacionados con los partidos de fútbol.
             En primer lugar, queremos predicir si un equipo local ganará, empatará o perderá utilizando el modelo de regresión logística como modelo
             de clasificación. En segundo lugar, queremos predecir la asistencia a un partido.
            """)

    subpagina = st.radio("Selecciona tipo de predicción:", ["Predicción sobre el resultado de un partido.", "Predicción sobre la asistencia a un partido."])

    if subpagina == "Predicción sobre el resultado de un partido.":
        st.write("""
                 Para predicir si un equipo local ganará, empatará o perderá, utilizamos el modelo de regresión logística como modelo
                 de clasificación. Dada que el número de variables es muy alto, hemos aplicado técnicas de selección de variables para quedarnos
                 con las más relevantes. En concreto, hemos utilizado selección progresiva hacia adelante y selección progresiva hacia atrás para 
                 identificar los subconjuntos de variables que proporcionan mejores resultados predictivos.

                 Por tanto, tomamos como output la variable 'FTR' (Full Time Result), que indica si el equipo local ganó (H), empató (D) o perdió (A).
                 En cuanto a las variables explicativas, hemos considerado todas las variables numéricas disponibles en el dataset, excluyendo aquellas 
                 que no aportan información relevante y que están relacionadas con el resultado final del partido (por ejemplo, goles totales, goles 
                 al descanso, etc.). Así, las variables explicativas que hemos utilizado son las siguientes:
                """)
        
        # Definimos variables que no se conocen antes del partido o que contienen información del resultado
        leakage_cols = [
            'FTR', 'FTHG', 'FTAG',  # Resultado final    
            'HTHG', 'HTAG', 'HTR', # Información al descanso
            'HS', 'AS', 'HST', 'AST', # Estadísticas del partido
            'HC', 'AC', 'HF', 'AF',
            'HO', 'AO', 'HY', 'AY',
            'HR', 'AR', 'HBP', 'ABP',
            'Asistencia', 'Referee', # Información posterior al partido
            "Date", "Time", "Estadio" # Información no relevante para el modelo
        ]

        # Eliminamos las variables de leakage y variable objetivo
        X1 = df1.drop(columns=[c for c in leakage_cols if c in df1.columns]) 
        st.dataframe(pd.DataFrame({"Variables explicativas": X1.columns}), use_container_width=True)

        st.write("""
                 Dividimos el conjunto de datos en 3 subconjuntos: un conjunto de entrenamiento (60%), un conjunto de validación (20%) y un conjunto 
                 de prueba (20%). Además, estandarizamos las variables explicativas para que todas tengan la misma escala y pasamos las variables 
                 Local y Visitante a variables categóricas mediante one-hot encoding.
                """)

        st.subheader("Selección Progresiva Hacia Adelante")
        
        st.write("""
                 Ajustamos el modelo de regresión logística con la selección progresiva hacia adelante a los datos de entrenamiento
                 y calculamos la métrica de error F1-score sobre el conjunto de validación, para elegir el mejor modelo. No seguimos el método de 
                 la selección progresiva hacia adelante clásico, sino que en lugar de partir del modelo nulo hasta el modelo completo, partimos de un modelo 
                 con las variables Local y Visitantecategorizadas.
                """)
        
        n_vars = list(range(39, 142))
        f1_scores_forward = [
            0.52031364, 0.54554656, 0.54554656, 0.54554656, 0.54554656, 0.55799092,
            0.5685663, 0.57005641, 0.56976377, 0.57910514, 0.58018626, 0.58043185,
            0.56869674, 0.57011052, 0.57011052, 0.57011052, 0.57073038, 0.57178929,
            0.57178929, 0.57178929, 0.57178929, 0.57178929, 0.57178929, 0.57178929,
            0.57178929, 0.57178929, 0.57178929, 0.57178929, 0.57178929, 0.57178929,
            0.57178929, 0.56920176, 0.56010187, 0.56010187, 0.56010187, 0.56010187,
            0.55847371, 0.55773252, 0.57906775, 0.58962989, 0.59057613, 0.57910514,
            0.57910514, 0.57816488, 0.57816488, 0.57448435, 0.57448435, 0.57448435,
            0.57447838, 0.57587025, 0.57607246, 0.57607246, 0.57607246, 0.57607246,
            0.57587025, 0.57587025, 0.57587025, 0.57587025, 0.56436186, 0.56462363,
            0.56436186, 0.55419615, 0.55419615, 0.55783576, 0.55976174, 0.55976174,
            0.55976174, 0.55976174, 0.55976174, 0.55976174, 0.55450213, 0.56782627,
            0.55789051, 0.54574472, 0.54574472, 0.53064248, 0.52744073, 0.53917487,
            0.53764411, 0.53764411, 0.53297163, 0.5103854, 0.51038784, 0.50932284,
            0.49676189, 0.49676189, 0.49676189, 0.48842279, 0.49242424, 0.48161038,
            0.46639326, 0.46639326, 0.46753449, 0.47722603, 0.47722603, 0.47722603,
            0.46560607, 0.44321372, 0.44321372, 0.44321372, 0.44321372, 0.4374785,
            0.43702139
        ]

        # Encontrar máximo F1 para la selección hacia adelante
        max_idx = np.argmax(f1_scores_forward)
        max_n = n_vars[max_idx]
        max_f1 = f1_scores_forward[max_idx]

        df_f1 = pd.DataFrame({"Número de variables": n_vars, "F1-score": f1_scores_forward})
        fig = go.Figure()

        # Línea principal
        fig.add_trace(go.Scatter(x=df_f1["Número de variables"], y=df_f1["F1-score"], mode="lines+markers", name="F1-score"))

        # Punto máximo
        fig.add_trace(go.Scatter(x=[max_n], y=[max_f1], mode="markers", name=f"Máximo F1 = {max_f1}", marker=dict(size=12, color="red")))
        fig.update_layout( title="Selección progresiva hacia adelante: F1-score vs número de variables", xaxis_title="Número de variables", yaxis_title="F1-score", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

        st.write("""
                 Así, tenemos que el mejor modelo es el que tiene:
                """)
        tabla = pd.DataFrame({
            "Métrica": ["Mejor F1-score", "Número de variables"],
            "Valor": [max_f1, int(max_n)]
        })
  
        variables_adelante = [
            'Local_Atlético de Madrid', 'Local_CA Osasuna', 'Local_CD Leganés',
            'Local_Deportivo Alavés', 'Local_FC Barcelona', 'Local_Getafe CF',
            'Local_Girona FC', 'Local_RC Celta', 'Local_RCD Espanyol',
            'Local_RCD Mallorca', 'Local_Rayo Vallecano', 'Local_Real Betis',
            'Local_Real Madrid', 'Local_Real Sociedad', 'Local_Real Valladolid',
            'Local_Sevilla FC', 'Local_UD Las Palmas', 'Local_Valencia CF',
            'Local_Villarreal CF', 'Visitante_Atlético de Madrid',
            'Visitante_CA Osasuna', 'Visitante_CD Leganés',
            'Visitante_Deportivo Alavés', 'Visitante_FC Barcelona',
            'Visitante_Getafe CF', 'Visitante_Girona FC',
            'Visitante_RC Celta', 'Visitante_RCD Espanyol',
            'Visitante_RCD Mallorca', 'Visitante_Rayo Vallecano',
            'Visitante_Real Betis', 'Visitante_Real Madrid',
            'Visitante_Real Sociedad', 'Visitante_Real Valladolid',
            'Visitante_Sevilla FC', 'Visitante_UD Las Palmas',
            'Visitante_Valencia CF', 'Visitante_Villarreal CF',
            'AHCh', 'MaxAHA', 'Longitud', 'Latitud', 'BWD', 'PCAHA',
            'BFECAHH', 'WHD', 'WHCD', 'AvgCD', 'BWCD', 'MaxCH',
            'Viento_kmh', 'Max<2.5', 'BFE>2.5', 'B365CH', 'B365CAHH',
            'B365C>2.5', 'P<2.5', 'PC>2.5', 'B365<2.5', 'AvgAHH',
            'Avg<2.5', 'BFA', 'B365CD', 'PSCD', '1XBCH', 'MaxCD',
            '1XBA', '1XBCD', 'AvgCH', 'AvgA', 'BFE<2.5', 'PSA',
            'MaxA', 'BFED', 'B365A', 'B365AHH', 'AvgCAHA', 'BFEA',
            'AvgC>2.5'
        ]

        df_variables_adelante = pd.DataFrame({"Variables explicativas del mejor modelo de selección progresiva hacia adelante": variables_adelante})

        st.table(tabla)
        st.dataframe(df_variables_adelante, use_container_width=True)

        st.subheader("Selección Progresiva Hacia Atrás")
        st.write("""
                 Ahora, ajustamos el modelo de regresión logística con la selección progresiva hacia atrás. No seguimos el método de 
                 la selección progresiva hacia atrás clásico, sino que en lugar de partir del modelo completo hasta modelo nulo, partimos del modelo completo
                 hasta llegar a uno que solo contenga las variables Local y Visitante categorizadas.
                """)
        
        n_vars = list(range(140, 37, -1))
        f1_scores_backward =[
            0.46459981, 0.46639726, 0.46653606, 0.47727652, 0.47949304, 0.47949304, 
            0.47949304, 0.47949304, 0.47949304, 0.47949304, 0.47949304, 0.47949304, 
            0.47949304, 0.48754848, 0.48754848, 0.48754848, 0.48754848, 0.48754848, 
            0.48754848, 0.48754848, 0.48754848, 0.48789315, 0.48789315, 0.48789315, 
            0.48789315, 0.48789315, 0.48789315, 0.48789315, 0.48789315, 0.48789315, 
            0.48789315, 0.48789315, 0.48789315, 0.48789315, 0.49229588, 0.49463241, 
            0.49463241, 0.49463241, 0.49463241, 0.49463241, 0.49463241, 0.49463241, 
            0.49655871, 0.49655871, 0.49655871, 0.49655871, 0.49655871, 0.49655871, 
            0.49655871, 0.49655871, 0.49655871, 0.49655871, 0.49655871, 0.49655871, 
            0.49655871, 0.49655871, 0.49655871, 0.49655871, 0.51071495, 0.51071495, 
            0.52130326, 0.52130326, 0.52130326, 0.52130326, 0.52130326, 0.53203608, 
            0.53702354, 0.53702354, 0.53702354, 0.53702354, 0.53702354, 0.53702354, 
            0.53702354, 0.53702354, 0.53702354, 0.53885531, 0.53885531, 0.53885531, 
            0.53545911, 0.52598929, 0.53843975, 0.54875826, 0.56430523, 0.55387549, 
            0.54277695, 0.54066986, 0.55228982, 0.55268527, 0.55268527, 0.54114081, 
            0.56430523, 0.57487335, 0.55889461, 0.54804095, 0.55849708, 0.55849708, 
            0.55822368, 0.5371383, 0.5345618, 0.53797939, 0.53240468, 0.52031364, 
            0.48044294
        ]


        # Encontrar máximo F1 para la selección hacia atrás
        max_idx1 = np.argmax(f1_scores_backward)
        max_n1 = n_vars[max_idx1]
        max_f11 = f1_scores_backward[max_idx1]

        df_f2 = pd.DataFrame({"Número de variables": n_vars, "F1-score": f1_scores_backward})
        fig = go.Figure()

        # Línea principal
        fig.add_trace(go.Scatter(x=df_f2["Número de variables"], y=df_f2["F1-score"], mode="lines+markers", name="F1-score"))
        # Punto máximo
        fig.add_trace(go.Scatter(x=[max_n1], y=[max_f11], mode="markers", name=f"Máximo F1 = {max_f11}", marker=dict(size=12, color="red")))
        fig.update_layout( title="Selección progresiva hacia atrás: F1-score vs número de variables", xaxis_title="Número de variables", yaxis_title="F1-score", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

        st.write("""
                 Así, tenemos que el mejor modelo es el que tiene:
                """)
        tabla = pd.DataFrame({
            "Métrica": ["Mejor F1-score", "Número de variables"],
            "Valor": [max_f1, int(max_n1)]
        })
  
        variables_atras = [
            'AHh', 'AvgAHH', 'BFEAHA', 'BWCH', 'BWCA', 'WHCH', 'BFECD', 'AHCh',
            'Sensacion_Termica_C', 'Precipitacion_mm', 'Codigo_Clima',
            'Local_Atlético de Madrid', 'Local_CA Osasuna', 'Local_CD Leganés',
            'Local_Deportivo Alavés', 'Local_FC Barcelona', 'Local_Getafe CF',
            'Local_Girona FC', 'Local_RC Celta', 'Local_RCD Espanyol',
            'Local_RCD Mallorca', 'Local_Rayo Vallecano', 'Local_Real Betis',
            'Local_Real Madrid', 'Local_Real Sociedad', 'Local_Real Valladolid',
            'Local_Sevilla FC', 'Local_UD Las Palmas', 'Local_Valencia CF',
            'Local_Villarreal CF', 'Visitante_Atlético de Madrid', 'Visitante_CA Osasuna',
            'Visitante_CD Leganés', 'Visitante_Deportivo Alavés', 'Visitante_FC Barcelona',
            'Visitante_Getafe CF', 'Visitante_Girona FC', 'Visitante_RC Celta',
            'Visitante_RCD Espanyol', 'Visitante_RCD Mallorca', 'Visitante_Rayo Vallecano',
            'Visitante_Real Betis', 'Visitante_Real Madrid', 'Visitante_Real Sociedad',
            'Visitante_Real Valladolid', 'Visitante_Sevilla FC', 'Visitante_UD Las Palmas',
            'Visitante_Valencia CF', 'Visitante_Villarreal CF'
        ]


        df_variables_atras = pd.DataFrame({"Variables explicativas del mejor modelo de selección progresiva hacia atrás": variables_atras})

        st.table(tabla)
        st.dataframe(df_variables_atras, use_container_width=True)

        table = pd.DataFrame([
            {
                'Tipo de modelo': 'Selección progresiva hacia adelante',
                'Mejor F1-score': max_f1,
                'Número de variables': max_n
            },
            {
                'Tipo de modelo': 'Selección progresiva hacia atrás',
                'Mejor F1-score': max_f11,
                'Número de variables': max_n1
            }
        ])

        st.subheader("Comparativa de Modelos de Selección de Variables")
        st.write("Tabla comparativa de ambos modelos de selección de variables con el mejor F1-score y el número de variables de cada tipo de modelo:")
        st.dataframe(table, use_container_width=True)

        st.write("""
                 Observamos que ambos modelos tiene prácticamente el mismo F1-score, por lo que podríamos elegir cualquiera de los dos según nuestras preferencias. 
                 Si lo que nos interesa solamente es el modelo que mejores predicciones haga, nos quedaríamos con el modelo de selección progresiva hacia adelante, 
                 ya que tiene un F1-score ligeramente superior. Si no solo nos interesa la capacidad predictiva, sino también la interpretabilidad del modelo, nos quedaríamos
                con el modelo de selección progresiva hacia atrás, ya que utiliza menos variables, lo que facilita la interpretación de los resultados.

                Finalmente, calculamos el F1-score sobre el conjunto de prueba, que se puede interpretar como el error de generalización de ambos modelos:
                """)

        table = pd.DataFrame([
            {
                'Tipo de modelo': 'Selección progresiva hacia adelante',
                'F1-score de prueba': 0.458004768017605,
            },
            {
                'Tipo de modelo': 'Selección progresiva hacia atrás',
                'F1-score de prueba': 0.4538468674624281,
            }
        ])

        st.subheader("Errores de Generalización")
        st.write("Tabla comparativa del error de generalización (error de prueba) para ambos modelos:")
        st.dataframe(table, use_container_width=True)

        st.write("""
                 Ambos modelos presentan un F1-score de prueba similar, lo que indica que tienen una capacidad predictiva similar en datos no vistos,
                 al generalizarse a datos nuevos.
                """)

        # ==================================================
        # NUEVAS VISUALIZACIONES DE PREDICCIÓN DE RESULTADOS
        # ==================================================
        st.subheader("📊 Visualizaciones Adicionales del Modelo")

        # Preparar datos para el modelo
        leakage_cols_viz = [
            'FTR', 'FTHG', 'FTAG',
            'HTHG', 'HTAG', 'HTR',
            'HS', 'AS', 'HST', 'AST',
            'HC', 'AC', 'HF', 'AF',
            'HO', 'AO', 'HY', 'AY',
            'HR', 'AR', 'HBP', 'ABP',
            'Asistencia', 'Referee',
            "Date", "Time", "Estadio"
        ]

        X_viz = df1.drop(columns=[c for c in leakage_cols_viz if c in df1.columns])
        y_viz = df1['FTR']

        # One-hot encoding para variables categóricas
        X_viz_encoded = pd.get_dummies(X_viz, columns=['Local', 'Visitante'], drop_first=False)

        # Limpiar datos: reemplazar espacios en blanco y valores no numéricos
        # Identificar columnas numéricas (excluyendo las categóricas creadas por get_dummies)
        for col in X_viz_encoded.columns:
            if X_viz_encoded[col].dtype == 'object':
                # Convertir espacios en blanco a NaN
                X_viz_encoded[col] = X_viz_encoded[col].replace(r'^\s*$', np.nan, regex=True)
                # Convertir a numérico, forzando errores a NaN
                X_viz_encoded[col] = pd.to_numeric(X_viz_encoded[col], errors='coerce')

        # Rellenar valores NaN con la media de cada columna
        X_viz_encoded = X_viz_encoded.fillna(X_viz_encoded.mean())

        # Si aún quedan NaN (columnas completamente vacías), rellenar con 0
        X_viz_encoded = X_viz_encoded.fillna(0)

        # Dividir en train y test
        X_train_viz, X_test_viz, y_train_viz, y_test_viz = train_test_split(
            X_viz_encoded, y_viz, test_size=0.2, random_state=42
        )

        # Estandarizar
        scaler_viz = StandardScaler()
        X_train_scaled_viz = scaler_viz.fit_transform(X_train_viz)
        X_test_scaled_viz = scaler_viz.transform(X_test_viz)

        # Entrenar modelo de regresión logística
        modelo_viz = LogisticRegression(max_iter=1000, random_state=42)
        modelo_viz.fit(X_train_scaled_viz, y_train_viz)

        # Predicciones
        y_pred_viz = modelo_viz.predict(X_test_scaled_viz)
        y_proba_viz = modelo_viz.predict_proba(X_test_scaled_viz)

        # 1. MATRIZ DE CONFUSIÓN
        st.subheader("🔢 Matriz de Confusión")
        cm = confusion_matrix(y_test_viz, y_pred_viz, labels=['H', 'D', 'A'])
        fig_cm, ax_cm = plt.subplots(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=['Local (H)', 'Empate (D)', 'Visitante (A)'],
                    yticklabels=['Local (H)', 'Empate (D)', 'Visitante (A)'],
                    ax=ax_cm)
        ax_cm.set_ylabel('Valor Real')
        ax_cm.set_xlabel('Predicción')
        ax_cm.set_title('Matriz de Confusión - Predicción de Resultados')
        st.pyplot(fig_cm)
        st.caption("La matriz muestra cómo el modelo clasifica cada resultado. Los valores en la diagonal representan las predicciones correctas.")

        # 2. ANÁLISIS DE PROBABILIDADES DE PREDICCIÓN
        st.subheader("📈 Distribución de Probabilidades de Predicción")

        # Crear DataFrame con probabilidades
        df_probas = pd.DataFrame(y_proba_viz, columns=['Prob_H', 'Prob_D', 'Prob_A'])
        df_probas['Real'] = y_test_viz.values
        df_probas['Prediccion'] = y_pred_viz
        df_probas['Correcto'] = df_probas['Real'] == df_probas['Prediccion']

        # Boxplot de probabilidades
        fig_box_prob = go.Figure()
        for resultado in ['H', 'D', 'A']:
            nombre = {'H': 'Local', 'D': 'Empate', 'A': 'Visitante'}[resultado]
            col_prob = f'Prob_{resultado}'
            fig_box_prob.add_trace(go.Box(
                y=df_probas[col_prob],
                name=nombre,
                boxmean='sd'
            ))
        fig_box_prob.update_layout(
            title="Distribución de Probabilidades Predichas por Resultado",
            yaxis_title="Probabilidad",
            xaxis_title="Tipo de Resultado"
        )
        st.plotly_chart(fig_box_prob, use_container_width=True)
        st.caption("Muestra cómo se distribuyen las probabilidades predichas para cada tipo de resultado.")

        # 3. ANÁLISIS DE ERRORES: Predicciones Correctas vs Incorrectas
        st.subheader("❌ Análisis de Errores de Predicción")

        # Calcular confianza máxima de cada predicción
        df_probas['Confianza_Max'] = df_probas[['Prob_H', 'Prob_D', 'Prob_A']].max(axis=1)

        fig_errores = px.histogram(
            df_probas,
            x='Confianza_Max',
            color='Correcto',
            barmode='overlay',
            title='Distribución de Confianza: Predicciones Correctas vs Incorrectas',
            labels={'Confianza_Max': 'Confianza de la Predicción', 'Correcto': 'Predicción Correcta'},
            color_discrete_map={True: 'green', False: 'red'},
            opacity=0.7
        )
        st.plotly_chart(fig_errores, use_container_width=True)
        st.caption("Compara la confianza del modelo en predicciones correctas e incorrectas. Si el modelo está bien calibrado, debería tener mayor confianza en predicciones correctas.")

        # Estadísticas de acierto
        tasa_acierto = df_probas['Correcto'].mean()
        st.metric("Tasa de Acierto del Modelo", f"{tasa_acierto:.2%}")

        # 4. ERRORES MÁS SIGNIFICATIVOS
        st.subheader("🎯 Predicciones con Mayor Error")
        df_errores_grandes = df_probas[~df_probas['Correcto']].copy()
        df_errores_grandes = df_errores_grandes.sort_values('Confianza_Max', ascending=False).head(10)

        st.write("Top 10 predicciones incorrectas con mayor confianza (errores más llamativos):")
        df_errores_display = df_errores_grandes[['Real', 'Prediccion', 'Confianza_Max', 'Prob_H', 'Prob_D', 'Prob_A']].copy()
        df_errores_display.columns = ['Resultado Real', 'Predicción', 'Confianza', 'Prob. Local', 'Prob. Empate', 'Prob. Visitante']
        st.dataframe(df_errores_display.round(3), use_container_width=True)


    elif subpagina == "Predicción sobre la asistencia a un partido.":
        st.write("""
                 Para predicir la asistencia a un partido, utilizamos un modelo Random Forest Regressor.
                 
                 Tomamos como output la variable "Asistencia". En cuanto a las variables explicativas, consideramos todas las variables numéricas 
                 disponibles en el dataset, excluyendo aquellas que no aportan información relevante y que están relacionadas con el resultado final 
                 del partido (por ejemplo, goles totales, goles al descanso, etc.). También, creamos las variables día de la semana, mes del año 
                 y si es fin de semana. Codificamos estas variables para convertilas en numéricas, además de Local, Visitante y Estadio.
                 
                 Así, las variables explicativas que empleamos son las siguientes:
                 """)
        
        df1 = pd.read_csv("outputs/partidos_con_clima_completo.csv")
        df1["Date"] = pd.to_datetime(df1["Date"], dayfirst=True)
        df1["Dia_Semana_Num"] = df1["Date"].dt.weekday
        df1["Mes_Num"] = df1["Date"].dt.month
        df1["Finde"] = df1["Date"].dt.weekday.isin([5, 6]).astype(int)
        df1["Local_Num"] = df1["Local"].astype("category").cat.codes
        df1["Visitante_Num"] = df1["Visitante"].astype("category").cat.codes
        df1["Estadio_Num"] = df1["Estadio"].astype("category").cat.codes

        leakage_cols = [
            'FTR', 'FTHG', 'FTAG',  # Resultado final    
            'HTHG', 'HTAG', 'HTR', # Información al descanso
            'HS', 'AS', 'HST', 'AST', # Estadísticas del partido
            'HC', 'AC', 'HF', 'AF',
            'HO', 'AO', 'HY', 'AY',
            'HR', 'AR', 'HBP', 'ABP',
            "Asistencia",'Referee', # Información posterior al partido
            "Date", "Time", "Estadio", "Local", "Visitante" # Información no relevante para el modelo
        ]

        X = df1.drop(columns=[c for c in leakage_cols if c in df1.columns]) 
        st.dataframe(pd.DataFrame({"Variables explicativas": X.columns}), use_container_width=True)

        st.write("""
                 Dividimos el conjunto de datos en 2 subconjuntos: Train (75%) y Test (25%)
                 """)
        
        st.subheader("Random Forest Regressor")

        st.write("""
                 Ajustamos el modelo Random Forest Regressor a los datos de entrenamiento y calculamos las métricas de error MAE, MSE y R² sobre el conjunto 
                 de prueba, que aparecen en la siguiente tabla:                 
                """)
        
        table = pd.DataFrame([
            {
                'Métrica': 'MAE',
                'Valor': 3123.86,
            },
            {
                'Métrica': 'MSE',
                'Valor': 46528949.05,
            },
            {
                'Métrica': 'R²',
                'Valor': 0.85,
            }
        ])

        st.write("""
                 A partir de estas métricas de error sobre el conjunto de prueba, podemos decir lo siguiente:
                 - MAE (Mean Absolute Error): En promedio, nuestras predicciones de asistencia se desvían en aproximadamente 3124 personas del valor real.
                 - MSE (Mean Squared Error): El MSE es una métrica que penaliza más los errores grandes. Un valor de 46528949.05 indica que hay algunas 
                 predicciones con errores significativos.
                 - R² (Coeficiente de Determinación): Un R² de 0.85 indica que el 85% de la variabilidad en la asistencia puede ser explicada por 
                 nuestro modelo. Esto sugiere que el modelo tiene un buen ajuste a los datos de entrenamiento.  

                 Por tanto, podemos concluir que, a grandes rasgos, el modelo Random Forest Regressor tiene un buen desempeño en datos nuevos 
                 para predecir la asistencia a los partidos de fútbol.   

                 Además, podemos mostrar las variables explicativas que más han aportado al modelo en términos de importancia:   
                """)
        

        num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist() 
        X[num_cols] = X.groupby('Local_Num')[num_cols].transform(lambda x: x.fillna(x.mean())) 
        odds_cols = [
            col for col in X.columns
            if any(book in col for book in [
                'B365', 'BW', 'WH', 'PS', 'BF', 'Avg', 'Max', '1XBH', '1XBD', '1XBA', 'P>2.5', 'P<2.5', 'PAHH', 'PAHA','PC>2.5', 'PC<2.5', 'BWA'
            ])
        ]
        for col in odds_cols:
            X[col] = pd.to_numeric(X[col], errors='coerce')
        X[odds_cols] = X.groupby('Local_Num')[odds_cols].transform(lambda x: x.fillna(x.mean()))
        X[odds_cols] = X[odds_cols].fillna(X[odds_cols].mean())
        X[num_cols] = X[num_cols].fillna(X[num_cols].mean())
        y = df1['Asistencia']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

        rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_test)

        importances = rf.feature_importances_
        indices = np.argsort(importances)[-20:] 
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(range(len(indices)), importances[indices], color="skyblue", align="center")
        ax.set_yticks(range(len(indices)))
        ax.set_yticklabels([X.columns[i] for i in indices])
        ax.set_xlabel("Importancia relativa")
        ax.set_title("Top 20 variables más influyentes en la asistencia")
        st.pyplot(fig)

        st.write("""
                 Finalmente, calculamos intervalos de confianza al 95% para las predicciones de asistencia realizadas por el modelo. El intervalo de 
                 confianza lo calculamos a partir de la variabilidad entre los árboles del Random Forest. Refleja la incertidumbre de la predicción para 
                 cada partido. Los graficamos, junto con las predicciones y los valores reales: 
                """)
        

        per_tree_preds = np.array([tree.predict(X_test) for tree in rf.estimators_])
        y_mean = np.mean(per_tree_preds, axis=0)
        y_std = np.std(per_tree_preds, axis=0)
        idx = np.argsort(y_test.values)
        y_test_sorted = y_test.values[idx]
        y_mean_sorted = y_mean[idx]
        y_std_sorted = y_std[idx]

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.fill_between(range(len(y_test_sorted)), y_mean_sorted - 2 * y_std_sorted, y_mean_sorted + 2 * y_std_sorted, color="skyblue", alpha=0.3, label="Intervalo de confianza (95%)")
        ax.plot(range(len(y_test_sorted)), y_test_sorted, "k.", markersize=4, label="Asistencia real", alpha=0.6)
        ax.plot(range(len(y_test_sorted)), y_mean_sorted, color="red", label="Predicción media", linewidth=1)
        ax.set_title("Predicciones de asistencia con intervalo de confianza")
        ax.set_xlabel("Partidos (ordenados por asistencia)")
        ax.set_ylabel("Asistencia")
        ax.legend()
        st.pyplot(fig)

        st.write("""
                 Observamos que, tal como nos decía la métrica de error MSE, algunas predicciones tienen un error considerable y distan bastante del valor real.
                 Apreciamos también que los intervalos de confianza son más amplios en estas predicciones con mayor error, lo que indica una mayor incertidumbre
                 en dichas predicciones.
                """)

        # ==================================================
        # NUEVAS VISUALIZACIONES DE PREDICCIÓN DE ASISTENCIA
        # ==================================================
        st.subheader("📊 Visualizaciones Adicionales del Modelo de Asistencia")

        # 1. SCATTER PLOT: Asistencia Real vs Predicha
        st.subheader("🎯 Asistencia Real vs Predicha")

        df_scatter = pd.DataFrame({
            'Real': y_test.values,
            'Predicha': y_pred
        })

        fig_scatter = px.scatter(
            df_scatter,
            x='Real',
            y='Predicha',
            title='Asistencia Real vs Predicha',
            labels={'Real': 'Asistencia Real', 'Predicha': 'Asistencia Predicha'},
            opacity=0.6
        )

        # Añadir línea diagonal (predicción perfecta)
        min_val = min(df_scatter['Real'].min(), df_scatter['Predicha'].min())
        max_val = max(df_scatter['Real'].max(), df_scatter['Predicha'].max())
        fig_scatter.add_trace(go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode='lines',
            name='Predicción Perfecta',
            line=dict(color='red', dash='dash')
        ))

        st.plotly_chart(fig_scatter, use_container_width=True)
        st.caption("Los puntos cercanos a la línea roja diagonal indican predicciones precisas. La dispersión muestra el error del modelo.")

        # 2. DISTRIBUCIÓN DE ERRORES (RESIDUOS)
        st.subheader("📉 Distribución de Errores de Predicción")

        residuos = y_test.values - y_pred

        fig_residuos, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        # Histograma de residuos
        ax1.hist(residuos, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
        ax1.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Error = 0')
        ax1.set_xlabel('Error (Real - Predicha)')
        ax1.set_ylabel('Frecuencia')
        ax1.set_title('Distribución de Errores de Predicción')
        ax1.legend()
        ax1.grid(alpha=0.3)

        # Q-Q plot para normalidad
        stats.probplot(residuos, dist="norm", plot=ax2)
        ax2.set_title('Q-Q Plot de Residuos')
        ax2.grid(alpha=0.3)

        st.pyplot(fig_residuos)
        st.caption("Izquierda: Distribución de errores. Derecha: Q-Q plot para evaluar normalidad de residuos.")

        # Estadísticas de residuos
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Error Promedio", f"{residuos.mean():.0f}")
        col2.metric("Error Absoluto Medio", f"{np.abs(residuos).mean():.0f}")
        col3.metric("Desv. Estándar Error", f"{residuos.std():.0f}")
        col4.metric("Error Máximo", f"{np.abs(residuos).max():.0f}")

        # 3. MAPA DE CALOR: RESIDUOS POR EQUIPO LOCAL
        st.subheader("🔥 Errores de Predicción por Equipo Local")

        # Recuperar información de equipos del dataset original
        df_test_info = df1.iloc[X_test.index].copy()
        df_test_info['Asistencia_Real'] = y_test.values
        df_test_info['Asistencia_Pred'] = y_pred
        df_test_info['Error'] = residuos
        df_test_info['Error_Abs'] = np.abs(residuos)

        # Agrupar por equipo local
        errores_por_equipo = df_test_info.groupby('Local').agg({
            'Error_Abs': 'mean',
            'Asistencia_Real': 'mean',
            'Asistencia_Pred': 'mean'
        }).round(0)
        errores_por_equipo = errores_por_equipo.sort_values('Error_Abs', ascending=False)

        fig_equipos = px.bar(
            errores_por_equipo.reset_index(),
            x='Local',
            y='Error_Abs',
            title='Error Absoluto Medio por Equipo Local',
            labels={'Local': 'Equipo Local', 'Error_Abs': 'Error Absoluto Medio'},
            color='Error_Abs',
            color_continuous_scale='Reds'
        )
        fig_equipos.update_xaxes(tickangle=-45)
        st.plotly_chart(fig_equipos, use_container_width=True)
        st.caption("Equipos con mayores errores de predicción en asistencia. Puede deberse a variabilidad en su afición o factores específicos del equipo.")

        # 4. TOP PARTIDOS CON MAYOR/MENOR ERROR
        st.subheader("🏆 Casos Extremos de Predicción")

        col_top1, col_top2 = st.columns(2)

        with col_top1:
            st.write("**Top 5 Mayores Subestimaciones** (Predicción < Real)")
            top_subestimados = df_test_info.nsmallest(5, 'Error')[['Local', 'Visitante', 'Asistencia_Real', 'Asistencia_Pred', 'Error']]
            top_subestimados.columns = ['Local', 'Visitante', 'Real', 'Predicha', 'Error']
            st.dataframe(top_subestimados.round(0), use_container_width=True)

        with col_top2:
            st.write("**Top 5 Mayores Sobrestimaciones** (Predicción > Real)")
            top_sobrestimados = df_test_info.nlargest(5, 'Error')[['Local', 'Visitante', 'Asistencia_Real', 'Asistencia_Pred', 'Error']]
            top_sobrestimados.columns = ['Local', 'Visitante', 'Real', 'Predicha', 'Error']
            st.dataframe(top_sobrestimados.round(0), use_container_width=True)

        # 5. RESIDUOS vs VALORES PREDICHOS
        st.subheader("📊 Análisis de Residuos vs Predicciones")

        fig_residuos_pred = px.scatter(
            x=y_pred,
            y=residuos,
            title='Residuos vs Asistencia Predicha',
            labels={'x': 'Asistencia Predicha', 'y': 'Residuos (Real - Predicha)'},
            opacity=0.6
        )
        fig_residuos_pred.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig_residuos_pred, use_container_width=True)
        st.caption("Idealmente, los residuos deberían distribuirse aleatoriamente alrededor de 0. Patrones sistemáticos indicarían sesgo del modelo.")


# Para ejecutar el dashboard, guarda este código en un archivo llamado `dashboard.py` y ejecuta el 
# siguiente comando en la terminal: streamlit run dashboard.py


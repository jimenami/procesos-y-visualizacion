# Dashboard Interactivo - La Liga 24-25

Dashboard interactivo desarrollado con Streamlit para el análisis de datos de la temporada 24-25 de La Liga española. Incluye análisis de resultados, clima, asistencia, apuestas deportivas y modelos predictivos de Machine Learning.

## Descripción del Proyecto

Este proyecto proporciona un análisis completo de la temporada 24-25 de La Liga española mediante:

- **Visualizaciones interactivas** de partidos, resultados y estadísticas
- **Análisis climático** con emojis del tiempo y códigos WMO
- **Mapas interactivos** de estadios y asistencia
- **Análisis de apuestas** y sorpresas deportivas
- **Modelos de Machine Learning** para:
  - Predicción de resultados de partidos (Victoria Local/Empate/Victoria Visitante)
  - Predicción de asistencia a partidos
- **Google Trends** para análisis del "hype" de los equipos

## Estructura del Proyecto

```
procesos-y-visualizacion/
├── README.md                          # Este archivo
├── VISUALIZACIONES_DASHBOARD.md       # Galería de capturas del dashboard
├── requirements.txt                   # Dependencias del proyecto
├── dashboard.py                       # Dashboard principal de Streamlit
├── filename.hpl                       # Archivo hop de la unión de csv
├── football-data.co.uk_notes.txt.pdf  # Explicación de cada columna del SP1.csv
├── TrabajoFinal1.ipynb                # Notebook de análisis y extracción de datos
├── predicciones.ipynb                 # Notebook con modelos predictivos
├── capturas/                          # Capturas de pantalla del dashboard
├── inputs/                            # Datos de entrada
│   ├── SP1.csv                        # Datos originales de La Liga
│   └── hop.txt.csv                    # Datos adicionales
├── outputs/                           # Datos procesados
│   ├── SP1_Normalizado.csv            # Datos normalizados
│   ├── datos_asistencia_media_estadios.csv
│   ├── datos_coordenadas.csv          # Coordenadas de estadios
│   ├── datos_partidos_asistencia.csv  # Datos de asistencia por partido
│   ├── partidos_completo_con_hype.csv # Datos con Google Trends
│   └── partidos_con_clima_completo.csv # Dataset principal con clima
└── venv/                              # Entorno virtual (no incluido en git)
```

## Características Principales

### Dashboard Interactivo (dashboard.py)

El dashboard incluye las siguientes secciones:

1. **Resultados**: Análisis de goles, resultados por equipo y estadísticas generales
2. **Apuestas**: Visualización de cuotas, sorpresas deportivas y análisis de probabilidades
3. **Tarjetas**: Análisis de tarjetas amarillas y rojas, y su impacto en los resultados
4. **Clima**: Visualización de condiciones climáticas con emojis del tiempo (☀️🌤️⛅☁️🌦️🌧️🌨️⛈️)
5. **Estadios & Asistencia**: Mapas interactivos y análisis de público
6. **Tendencias (Google Trends)**: Análisis del "hype" de los equipos en búsquedas de Google
7. **Modelos Predictivos**:
   - Predicción de resultados con Regresión Logística
   - Predicción de asistencia con Random Forest
   - Matrices de confusión y análisis de errores
   - Distribución de probabilidades y residuos

### Notebooks de Análisis

- **TrabajoFinal1.ipynb**: Notebook principal con extracción de datos climáticos, normalización y análisis exploratorio
- **predicciones.ipynb**: Modelos de Machine Learning y evaluación de predicciones

### Documentación Visual

- **VISUALIZACIONES_DASHBOARD.md**: Galería con capturas de pantalla de todas las visualizaciones del dashboard, útil para revisar el contenido sin ejecutar el código

## Requisitos Previos

- **Python 3.8 o superior** (recomendado 3.11)
- **pip** (gestor de paquetes de Python)
- **git** (opcional, para clonar el repositorio)

## Instalación

### 1. Clonar o descargar el proyecto

Si tienes git instalado:

```bash
git clone https://github.com/MalenaSancho/procesos-y-visualizacion.git
cd procesos-y-visualizacion
```

O descarga el proyecto como archivo ZIP y descomprímelo.

### 2. Crear un entorno virtual

El uso de un entorno virtual es **altamente recomendado** para evitar conflictos entre dependencias.

#### En Windows:

```bash
# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual
venv\Scripts\activate
```

#### En macOS:

```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno virtual
source venv/bin/activate
```

#### En Linux:

```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno virtual
source venv/bin/activate
```

**Nota**: Una vez activado, deberías ver `(venv)` al inicio de tu línea de comandos.

### 3. Instalar las dependencias

Con el entorno virtual activado, instala todas las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

Este comando instalará las siguientes bibliotecas:

- **Framework del dashboard**: streamlit, folium, streamlit-folium
- **Procesamiento de datos**: pandas, numpy, lxml, openpyxl
- **Visualización**: plotly, matplotlib, seaborn
- **Machine Learning**: scikit-learn, scipy
- **Web scraping y APIs**: beautifulsoup4, requests, openmeteo-requests, pytrends

## Uso

### Ejecutar el Dashboard

Una vez instaladas las dependencias, ejecuta el dashboard con el siguiente comando:

```bash
streamlit run dashboard.py
```

El dashboard se abrirá automáticamente en tu navegador predeterminado en la dirección `http://localhost:8501`.

### Explorar los Notebooks

Para explorar los notebooks de análisis:

1. Instala Jupyter (si no lo tienes):

```bash
pip install jupyter
```

2. Inicia Jupyter Notebook:

```bash
jupyter notebook
```

3. Abre `TrabajoFinal1.ipynb` o `predicciones.ipynb` desde la interfaz web.

## Dependencias Detalladas

### Framework Principal

- `streamlit==1.52.2` - Framework para crear aplicaciones web interactivas
- `folium>=0.15.0` - Mapas interactivos con Leaflet.js
- `streamlit-folium>=0.15.0` - Integración de Folium con Streamlit

### Procesamiento de Datos

- `pandas==2.3.3` - Manipulación y análisis de datos
- `numpy==2.4.0` - Operaciones numéricas y arrays
- `lxml>=5.0.0` - Parser XML/HTML para pandas
- `openpyxl>=3.1.0` - Lectura/escritura de archivos Excel

### Visualización

- `plotly==6.5.1` - Gráficos interactivos
- `matplotlib==3.10.8` - Gráficos estáticos
- `seaborn==0.13.2` - Visualizaciones estadísticas

### Machine Learning

- `scikit-learn==1.8.0` - Modelos de ML (Regresión Logística, Random Forest)
- `scipy==1.16.3` - Funciones científicas y estadísticas

### Web Scraping y APIs

- `beautifulsoup4>=4.12.0` - Extracción de datos web
- `requests>=2.31.0` - Peticiones HTTP
- `requests-cache>=1.1.0` - Cache para peticiones HTTP
- `retry-requests>=2.0.0` - Reintentos automáticos
- `urllib3>=2.0.0` - Cliente HTTP
- `openmeteo-requests>=1.1.0` - API de datos climáticos Open-Meteo
- `pytrends>=4.9.0` - API no oficial de Google Trends

## Datos

### Fuentes de Datos

- **Datos de partidos**: Football-Data.co.uk (SP1.csv)
- **Datos climáticos**: Open-Meteo API (temperatura, precipitación, viento, códigos WMO)
- **Google Trends**: API pytrends para análisis de búsquedas
- **Coordenadas de estadios**: Datos recopilados manualmente

### Códigos Climáticos WMO

El proyecto utiliza los códigos WMO simplificados para representar condiciones climáticas:

| Código | Descripción         | Emoji    |
| ------- | -------------------- | -------- |
| 0       | Despejado            | ☀️     |
| 1       | Mayormente despejado | 🌤️     |
| 2       | Parcialmente nublado | ⛅       |
| 3       | Nublado              | ☁️     |
| 45-48   | Niebla               | 🌫️     |
| 51-57   | Llovizna             | 🌦️🌧️ |
| 61-67   | Lluvia               | 🌧️     |
| 71-77   | Nieve                | 🌨️❄️ |
| 80-82   | Chubascos            | 🌦️🌧️ |
| 85-86   | Chubascos de nieve   | 🌨️❄️ |
| 95-99   | Tormentas            | ⛈️     |

## Modelos Predictivos

### Predicción de Resultados

- **Algoritmo**: Regresión Logística
- **Variables**: Cuotas de apuestas, condiciones climáticas, equipos
- **Salida**: Victoria Local (H) / Empate (D) / Victoria Visitante (A)
- **Evaluación**: Matriz de confusión, F1-score, distribución de probabilidades

### Predicción de Asistencia

- **Algoritmo**: Random Forest Regressor
- **Variables**: Equipos, estadio, día de la semana, mes, clima, ubicación
- **Salida**: Asistencia estimada
- **Evaluación**: MAE, MSE, R², análisis de residuos

## Solución de Problemas

### Error: "ModuleNotFoundError"

Asegúrate de que el entorno virtual esté activado y de haber instalado las dependencias:

```bash
pip install -r requirements.txt
```

### Error: "FileNotFoundError"

Verifica que estés ejecutando el dashboard desde la carpeta raíz del proyecto donde se encuentra `dashboard.py`.

### El dashboard no se abre en el navegador

Intenta abrir manualmente la dirección que aparece en la terminal (usualmente `http://localhost:8501`).

### Problemas con pytrends

Si pytrends falla, puede deberse a limitaciones de tasa de Google. Espera unos minutos y vuelve a intentarlo.

## Desactivar el Entorno Virtual

Cuando termines de trabajar, puedes desactivar el entorno virtual:

```bash
deactivate
```

## Contribuciones

Si deseas contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Autores

Magdalena Sancho Docón, Juan Francisco Correas Díaz, Itsaso Ariztimuño Cenoz, Jimena Milla Moreno

## Contacto

Para preguntas o sugerencias, por favor abre un issue en el repositorio.

---

**Última actualización**: Enero 2026

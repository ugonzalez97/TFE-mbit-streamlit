
# Diccionario de localidades y coordenadas
localidades_coordenadas = {
    'ALICANTE-ELCHE AEROPUERTO': [38.2822, -0.5582],
    'ALACANT/ALICANTE': [38.3452, -0.4810],
    'JÁVEA/XÀBIA': [38.7895, 0.1661],
    'EL PINÓS/PINOSO': [38.4017, -1.0422],
    'CASTELLÓ - ALMASSORA': [39.9560, -0.0457],
    'CASTELLFORT': [40.4147, -0.4204],
    'CASTELLÓ DE LA PLANA': [39.9864, -0.0515],
    'VILLAFRANCA DEL CID/VILLAFRANCA': [40.5283, -0.2667],
    'VINARÒS': [40.4706, 0.4750],
    'VALENCIA AEROPUERTO': [39.4893, -0.4816],
    'VALÈNCIA': [39.4699, -0.3763],
    'OLIVA': [38.9191, -0.1210],
    'POLINYÀ DE XÚQUER': [39.3200, -0.4031],
    'UTIEL': [39.5667, -1.2005],
    'VALÈNCIA, VIVEROS': [39.4799, -0.3623],
    'XÀTIVA': [38.9893, -0.5153]
}
import streamlit as st
import pandas as pd
import folium
import branca.colormap as cm
from streamlit_folium import st_folium
from datetime import datetime

# Cargar datos
df = pd.read_parquet('all_data.parquet')

# Convertir 'fecha' a datetime
df['fecha'] = pd.to_datetime(df['fecha'])

# Convertir 'tmed' a numérico y manejar los NA
df['tmed'] = pd.to_numeric(df['tmed'], errors='coerce')
mean_tmed = df['tmed'].dropna().mean()  # Calcular la media de los valores no NA para reemplazar los NA
df['tmed'] = df['tmed'].fillna(mean_tmed).astype(float)  # Rellenar NA con la media y convertir a float

# Ajustar el rango de fechas para el selector de fecha en Streamlit
fecha_minima = df['fecha'].dt.date.min()
fecha_maxima = df['fecha'].dt.date.max()


# Función para obtener las coordenadas de una localidad
def get_location(name):
    return localidades_coordenadas.get(name, [None, None])

# Creación de un slider de fecha en Streamlit
fecha_seleccionada = st.slider("Selecciona una fecha", value=fecha_minima, min_value=fecha_minima, max_value=fecha_maxima, format="YYYY-MM-DD")

# Filtrar los datos para la fecha seleccionada
df_filtrado = df[df['fecha'].dt.date == fecha_seleccionada]

# Definir una escala de colores para la temperatura, asegurándose de que los índices estén ordenados
min_tmed = df['tmed'].min()
max_tmed = df['tmed'].max()

# Crear la escala de colores con umbrales ordenados
indices = [min_tmed + i*(max_tmed-min_tmed)/4 for i in range(5)]  # Dividir el rango de temperaturas en 4 partes iguales
escala_colores = cm.linear.YlOrRd_09.scale(min_tmed, max_tmed).to_step(index=sorted(indices))

# Mostrar la escala de colores como leyenda
st.write(escala_colores.render())

# Función para crear el mapa
def crear_mapa(columna_valor):
    mapa = folium.Map(location=[39.46975, -0.37739], zoom_start=6)
    for _, fila in df_filtrado.iterrows():
        lat, lon = get_location(fila['nombre'])
        temp = fila[columna_valor]
        if lat and lon and not pd.isna(temp):  # Verificar la validez de lat, lon, y temp
            color = escala_colores(temp)
            folium.Circle(
                location=[lat, lon],
                radius=5000,
                color=color,
                fill=True,
                fill_color=color,
                popup=f"{fila['nombre']}: {temp}°C"
            ).add_to(mapa)
    return mapa

# Mostrar el mapa de temperatura
st.header('Temperatura')
mapa_temp = crear_mapa('tmed')
st_folium(mapa_temp, width=725, height=525)

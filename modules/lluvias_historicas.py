import branca.colormap as cm
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

localidades_coordenadas = {
    'ALACANT/ALICANTE': [38.3452, -0.4810],
    'JÁVEA/ XÀBIA': [38.7895, 0.1661],
    'EL PINÓS/PINOSO': [38.4017, -1.0422],
    'CASTELLÓ - ALMASSORA': [39.9560, -0.0457],
    'CASTELLFORT': [40.4147, -0.4204],
    'CASTELLÓ DE LA PLANA': [39.9864, -0.0515],
    'VINARÒS': [40.4706, 0.4750],
    'VALÈNCIA': [39.4699, -0.3763],
    'OLIVA': [38.9191, -0.1210],
    'UTIEL': [39.5667, -1.2005],
    'XÀTIVA': [38.9893, -0.5153]
}

@st.cache_data
def cargar_datos():
    df = pd.read_parquet('data/all_data.parquet')
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['prec'] = df['prec'].str.replace(',', '.').apply(pd.to_numeric, errors='coerce')
    df['prec'].fillna(0, inplace=True)
    return df

df = cargar_datos()

fecha_minima = df['fecha'].min().date()
fecha_maxima = df['fecha'].max().date()
fecha_minima_permitida = pd.Timestamp('1968-01-01').date()
fecha_maxima_permitida = pd.Timestamp('2023-12-31').date()
fecha_minima = max(fecha_minima, fecha_minima_permitida)
fecha_maxima = min(fecha_maxima, fecha_maxima_permitida)

@st.cache_data
def filtrar_datos(fecha_seleccionada):
    return df[df['fecha'].dt.date == fecha_seleccionada]

def crear_mapa(df_filtrado, columna_valor, escala_colores):
    mapa = folium.Map(location=[39.46975, -0.37739], zoom_start=7)
    for _, fila in df_filtrado.iterrows():
        lat, lon = localidades_coordenadas.get(fila['nombre'], [None, None])
        val = fila[columna_valor]
        if lat and lon and not pd.isna(val):
            color = escala_colores(val)
            folium.Circle(
                location=[lat, lon],
                radius=10000,
                color=color,
                fill=True,
                fill_color=color,
                popup=f"{fila['nombre']}: {val} L"
            ).add_to(mapa)
    return mapa



def show_map():
    fecha_seleccionada = st.slider("Selecciona una fecha", value=fecha_minima, min_value=fecha_minima, max_value=fecha_maxima, format="YYYY-MM-DD")

    df_filtrado = filtrar_datos(fecha_seleccionada)

    escala_colores = cm.linear.YlOrRd_09.scale(0, 15)

    mapa_temp = crear_mapa(df_filtrado, 'prec', escala_colores)
    st_folium(mapa_temp, width=725, height=525)

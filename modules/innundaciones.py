import streamlit as st
import geopandas as gpd
import folium
import pandas as pd
from streamlit_folium import st_folium

@st.cache_data
def cargar_geojson(archivo_geojson):
    return gpd.read_file(archivo_geojson)


def crear_mapa(gdf):
    # Convertir las columnas de fecha/hora a string aquí
    for col in gdf.columns:
        if pd.api.types.is_datetime64_any_dtype(gdf[col]):
            gdf[col] = gdf[col].astype(str)
    
    # A continuación, continúa con la creación del mapa como antes
    mapa = folium.Map(location=[40.416775, -3.703790], zoom_start=5)
    
    # Añadir la capa GeoJSON al mapa usando gdf.to_json() ahora debería funcionar sin problema
    folium.GeoJson(gdf.to_json()).add_to(mapa)
    return mapa


@st.cache_data(experimental_allow_widgets=True)
def show_map():
    archivo_geojson = 'data/areas_innundables.geojson'
    gdf = cargar_geojson(archivo_geojson)

    mapa = crear_mapa(gdf)
    st_folium(mapa, width=725, height=525)

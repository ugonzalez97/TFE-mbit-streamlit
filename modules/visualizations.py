import streamlit as st
import folium
from streamlit_folium import folium_static

def show_map():
    latitud_espana = 40.416775
    longitud_espana = -3.703790
    zoom_inicio = 6

    mapa_espana = folium.Map(location=[latitud_espana, longitud_espana], zoom_start=zoom_inicio)

    folium_static(mapa_espana)


def show_location(latitude, longitude, zoom_start):
    folium_static(folium.Map(
        location=[latitude, longitude], zoom_start=zoom_start))


def show_polygon(latitude, longitude, zoom_start, data):
    map = folium.Map(location=[latitude, longitude], zoom_start=zoom_start)
    for location in data:
        folium.vector_layers.Polygon(locations=location, 
                                        color='red',
                                        fill=True,
                                        fill_color='red',
                                
                                        weight=0.1).add_to(map)
    folium_static(map)

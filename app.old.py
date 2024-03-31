"""
import os
import streamlit as st
from modules.visualizations import show_location
from modules.visualizations import show_polygon
from modules.data_loader import load_locations_dict
from modules.data_loader import get_coordinates
from modules.data_loader import get_data
from modules.innundaciones import show_map

TITLE = 'Futur-ista'


def main():
    st.title(TITLE)

    locations = load_locations_dict()

    col1, col2 = st.columns([1, 3], gap="small")

    ver_resultados = False

    with col1:
        selecte_zone = st.selectbox('Comunidad', locations.keys())

        if selected_zone != 'Todas':
            zoom = 10
            zone = st.selectbox(
                'Provincia', [name['name'] for name in locations[selected_zone]])
            latitude, longitude = get_coordinates(
                selected_zone, zone, locations)
            riesgo = st.selectbox(
                'Riesgo', [
                    'Inundación',
                    'Ola de calor',
                    'Seísmos'
                ],
                placeholder="Elije",
                index=None
            )
            if riesgo:
                riesgo = riesgo.lower()
                plazo = st.selectbox(
                    'Plazo', ['Corto', 'Medio', 'Largo']).lower()
                escenario = st.selectbox(
                    'Escenario', ['Optimista', 'Normal', 'Pesimista']).lower()
                ver_resultados = st.checkbox('Ver resultados')

        else:
            latitude, longitude = get_coordinates(
                selected_zone, 'Todas', locations)
            zoom = 6

    with col2:
        if not ver_resultados:
            show_location(latitude, longitude, zoom)
        else:
            show_polygon(latitude, longitude, zoom, get_data(zone, riesgo, escenario, plazo))


if __name__ == "__main__":
    main()
"""
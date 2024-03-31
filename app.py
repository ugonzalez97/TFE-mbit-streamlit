import streamlit as st
from modules.innundaciones import show_map as innundacion
from modules.visualizations import show_map
from modules.temperaturas_historicas import show_map as temp_historicas
from modules.lluvias_historicas import show_map as lluvias_historicas
from modules.temperaturas_mortales import show_map as riesgo_mortal

import os
os.environ["AWS_ACCESS_KEY_ID"] = "CHANGEME"
os.environ["AWS_SECRET_ACCESS_KEY"] = "CHANGEME"

tab1, tab2 = st.tabs(["Futur-ista", "Actual-ista"])

with tab1:
    st.header("Futur-ista")
    col1, col2 = st.columns([1, 3], gap="small")
    with col1:
        opciones = ["Selecciona", "Inundación", "Ola de calor"]
        risk = st.selectbox("¿Qué riesgo quieres ver?", opciones, index=0)  

    with col2:
        if risk == "Selecciona":
            show_map()
        elif risk == "Inundación":
            innundacion()
        elif risk == "Ola de calor":
            show_map()
    

with tab2:
    col1, col2 = st.columns([1, 3], gap="small")
    with col1:
        opciones = ["Selecciona", "Temperaturas", "Lluvias", "Riesgo mortal"]
        risk = st.selectbox("¿Qué riesgo quieres ver?", opciones, index=0)  

    with col2:
        if risk == "Selecciona":
            show_map()
        elif risk == "Temperaturas":
            temp_historicas()
        elif risk == "Lluvias":
            lluvias_historicas()
        elif risk == "Riesgo mortal":
            riesgo_mortal()
    

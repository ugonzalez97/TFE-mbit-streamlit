import os
import json
import pandas as pd 

DATA_PATH = "data"
APP_PATH = "app"
LOCATIONS_FILE = "locations.json"


def read_json(file_name: str):
    """Returns a dictionary with the data of a given zone"""
    with open(os.path.join(DATA_PATH, file_name), encoding="utf-8") as archivo:
        return json.load(archivo)


def load_locations_dict(country: str = 'Spain') -> pd.DataFrame:
    """Returns a dictionary with the data of a given zone"""
    return read_json(os.path.join(APP_PATH, LOCATIONS_FILE))[country]

def get_coordinates(comunidad, provincia, data):
    if comunidad in data:
        for item in data[comunidad]:
            if item['name'] == provincia:
                return item['coordinates']
    return None


def get_data(provincia, riesgo, escenario, plazo):
    return pd.read_parquet(os.path.join(DATA_PATH, 'dataset_riesgos_espana.parquet'),
                    filters=[('provincia', '==', provincia),
                             ('riesgo', '==', riesgo),
                             ('escenario', '==', escenario),
                             ('plazo', '==', plazo)])['Coordenadas']

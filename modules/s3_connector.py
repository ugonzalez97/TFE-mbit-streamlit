import boto3

def obtener_archivo_s3(bucket_name, file_key, local_file_path):
    """
    Descarga un archivo desde un bucket de S3 a una ruta local.

    :param bucket_name: Nombre del bucket de S3.
    :param file_key: Clave del archivo en S3.
    :param local_file_path: Ruta local donde se guardará el archivo.
    """
    # Crear un cliente de S3
    s3 = boto3.client('s3')

    try:
        # Descargar el archivo
        s3.download_file(bucket_name, file_key, local_file_path)
        print(f"Archivo descargado exitosamente: {local_file_path}")
    except Exception as e:
        print(f"Error al descargar el archivo: {str(e)}")

# Uso de la función
obtener_archivo_s3('mi_bucket', 'mi_archivo.txt', '/ruta/local/mi_archivo_descargado.txt')

import pandas as pd


# Ruta del archivo Parquet en S3
s3_path = 's3://mi_bucket/mi_archivo.parquet'

# Leer el archivo Parquet directamente desde S3
df = pd.read_parquet(s3_path, engine='pyarrow')  # o usa engine='fastparquet'

# Muestra las primeras filas del DataFrame
print(df.head())


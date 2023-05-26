############################################################


import boto3
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import time
from datetime import datetime
import os
from io import StringIO

s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')

input_bucket = os.environ['INPUT_BUCKET']
output_bucket = os.environ['OUTPUT_BUCKET']

def lambda_handler(event, context):
    # Obtener la información del archivo
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    print (bucket)
    print (key)

    if bucket != input_bucket:
        # Si el evento no es para el bucket de origen configurado, no hacer nada
        print(f"El evento no es para el bucket de origen configurado: {input_bucket}")
        return
    
    # Descargar el archivo CSV de S3
    response = s3.get_object(Bucket=bucket, Key=key)
    body = response['Body'].read()
    
    # Convertir el contenido del archivo a una cadena
    csv_str = body.decode('UTF-8')
    
    # Convertir el archivo CSV a un DataFrame de Pandas
    df = pd.read_csv(StringIO(csv_str))
    
    # Renombrar columnas
    for column_name in df.columns:
        new_column_name = column_name.replace(" ", "_")
        new_column_name = new_column_name.replace("/", "_")
        new_column_name = new_column_name.replace("(", "")
        new_column_name = new_column_name.replace(")", "")
        df = df.rename(columns={column_name: new_column_name})
    
    # Convertir el DataFrame de Pandas a un archivo Parquet
    file_name = os.path.splitext(os.path.basename(key))[0]
    timestamp = int(time.time())
    dt_object = datetime.fromtimestamp(timestamp)
    formatted_time = dt_object.strftime("%Y%m%d_%H%M%S")
    output_key = f"{file_name}/{file_name}_{formatted_time}.snappy.parquet"
    
    # Guardar el archivo Parquet en S3
    if not s3_resource.Bucket(output_bucket).objects.filter(Prefix=file_name+'/').all():
        s3_resource.Bucket(output_bucket).put_object(Key=f"{file_name}/")
    df.to_parquet(f's3://{output_bucket}/{output_key}', compression='snappy')
    
    print(f'Archivo {key} guardado como {output_key} en S3.')
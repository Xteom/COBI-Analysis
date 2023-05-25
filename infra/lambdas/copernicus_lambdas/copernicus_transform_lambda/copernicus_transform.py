import  boto3
import os
import json
from copernicus_transform_utils import nc_to_csv

s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')

input_bucket = 'COBI-landing-zone-2023'
output_bucket = 'COBI-clean-data-2023'

def lambda_handler(event, context):
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    print (bucket)

    if bucket != input_bucket:
        print(f"El evento no es para el bucket de origen configurado: {input_bucket}")
        return
    
    # Descargar el archivo NetCDF de S3
    response = s3.get_object(Bucket=bucket, Key=key) #porque se ocupa bucket y no input_bucket?
    body = response['Body'].read()

    # Convertir el archivo NetCDF a un archivo CSV y guardarlo en S3
    nc_to_csv(body, output_bucket)

    return {
        'statusCode': 200,
        'body': json.dumps('CSV file saved in S3')
    }

    
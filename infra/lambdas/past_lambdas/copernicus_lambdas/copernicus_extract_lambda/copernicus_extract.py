from copernicus_extract_utils import read_credentials, make_request
import json
import boto3
import os

s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')

input_bucket = 'COBI-input-data-2023'
output_bucket = 'COBI-landing-zone-2023'

def lambda_handler(event, context):

    # Obtener la información del archivo
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    print (bucket)
    print (key)

    if bucket != output_bucket:
        # Si el evento no es para el bucket de destino configurado, no hacer nada
        print(f"El evento no es para el bucket de destino configurado: {output_bucket}")
        return
    
    credentials = read_credentials()
    make_request(credentials, input_bucket, output_bucket)

    return {
        'statusCode': 200,
        'body': json.dumps('Copernicus Extract Lambda executed successfully!')
    }

   

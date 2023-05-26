import xarray as xr
import os
import  boto3
import os
import json

s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')

input_bucket = 'COBI-landing-zone-2023'
output_bucket = 'COBI-clean-data-2023'

def nc_to_csv(input_dir=input_bucket,
           destination_dir=output_bucket):
    
    for filename in os.listdir(input_dir):
        raw_file = os.path.join(input_dir, filename)

        ds = xr.open_dataset(raw_file)

        df = ds.to_dataframe()
        df = df.reset_index()
        ds.close()

        print(df)

        if not os.path.isdir(destination_dir):
                os.makedirs(destination_dir, exist_ok=True)

        
        df.to_csv(os.path.join(destination_dir, filename[:-3]+".csv"))



def handler(event, context):
    
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

    
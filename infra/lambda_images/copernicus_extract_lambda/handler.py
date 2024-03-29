from typing import List
import configparser
from datetime import datetime
import os
import csv
from motu_utils import motu_api
import motuclient
import json
import boto3

class MotuOptions:
    """
    The MotuOptions class is a custom class that enables attribute setting and retrieval using dictionary-like syntax. 
    It provides methods for initialization, attribute setting, and attribute retrieval. 
    This class is designed to store and retrieve options or configurations in the form of key-value pairs.
    """

    def _init_(self, attrs: dict):
        """
        The class constructor that initializes a MotuOptions object.
        It takes a dictionary, attrs, as an argument and sets it as the initial attribute dictionary.

        Args:
            attrs (dict): Initial attribute dictionary.
        """
        self.attrs = attrs

    def setattr(self, k, v):
        """
        A method to set an attribute. It takes a key k and a value v as arguments and adds or updates the corresponding 
        key-value pair in the attrs dictionary.

        Args:
            k: Key of the attribute.
            v: Value of the attribute.
        """
        self.attrs[k] = v

    def getattr(self, k):
        """
        A method to get an attribute. It takes a key k as an argument and returns the value associated with that key 
        in the attrs dictionary. If the key is not found, it returns None.

        Args:
            k: Key of the attribute.

        Returns:
            The value associated with the key, or None if the key doesn't exist.
        """
        try:
            return self.attrs[k]
        except KeyError:
            return None
        
def read_credentials() -> List[str]:
    """
    Reads credentials for copernicus from the config.ini file.

    Returns:
        A list of strings containing the username and password for the MOTU API.

    """
    config = configparser.ConfigParser()
    config.read('config/config.ini')

    username = config.get('api_keys', 'user_cop')
    password = config.get('api_keys', 'password_cop')
    
    return [username, password]

def read_variable_list(file_path):
    '''
    Reads the CSV file with the list of variables to download from the Copernicus API.	
    
    file_path (str): Path to the CSV file with the list of variables to download from the Copernicus API.
    Returns: 
        a list of dictionaries, each one containing the information of a row in the CSV file.
    '''

    # Create an empty list to store the dictionaries
    var_dict_list = []

    # Read the CSV file
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        
        # Iterate over each row in the CSV file
        for row in reader:
            # Append the row dictionary to the list
            var_dict_list.append(row)

    # Return the list of dictionaries
    return var_dict_list

def create_request(service_id, product_id, date, motu, directory_to, name, user, password):
    '''
    Creates a request with the parameters needed to download the data from the Copernicus API.
    
    service_id (str): Service ID of the service that manages the product we want to download 
    product_id (str): ID of the product we want to download
    date (str): Initial date from where we want to download the data, in format YYYY-MM-DD
    motu (str): URL to the server where the product is hosted
    directory_to (str): Directory where the downloaded product will be placed 
    name (str): Name under which the downloaded product will be saved
    user (str): User with which we'll connect to the server
    password (str): Password with which we'll connect to the server

    Returns:
        A dictionary with the parameters needed to download the data from the Copernicus API.

    ''' 
    return {"service_id": service_id,
            "product_id": product_id,
            "date_min": datetime.strptime('2017-01-01', '%Y-%m-%d').date(),
            "date_max": datetime.strptime(date, '%Y-%m-%d').date(),
            "longitude_min": -116.,
            "longitude_max": -113.,
            "latitude_min": 26.,
            "latitude_max": 29.,
            "variable": [],
            "motu": motu,
            "out_dir": directory_to,
            "out_name": name+".nc",
            "auth_mode": "cas",
            "user": user,
            "pwd": password
            }
file_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
destination_path=os.path.join(file_path, 'data', 'copernicus', 'raw')

def make_request(credentials,
                 file_path=file_path, 
                 destination_path=destination_path):
    '''
    Creates a request with the parameters needed to download the data from the Copernicus API.

    credentials (list): List of strings containing the username and password for the MOTU API.
    file_path (str): Path to the CSV file with the list of variables to download from the Copernicus API.
        default: same directory as this file
    destination_path (str): Path to the directory where the downloaded product will be placed
        default: same directory as this file/data/copernicus/raw
    '''

    # Read the CSV file with the list of variables to download from the Copernicus API
    var_dict_list = read_variable_list(file_path)

    for dict in var_dict_list:
        try:
            date = datetime.today().strftime('%Y-%m-%d')

            # Construct a relative file path to the data directory

            directory_to = os.path.join(destination_path, 'data', 'copernicus', 'raw')
            if not os.path.isdir(directory_to):
                os.makedirs(directory_to, exist_ok=True)


            data_request_options_dict_manual = create_request(dict["service_id"],
                                                            dict["product_id"],
                                                            date,
                                                            dict["motu"],
                                                            directory_to, 
                                                            dict["name"],
                                                            credentials[0], 
                                                            credentials[1]
                                                            )
        
            motu_api.execute_request(MotuOptions(data_request_options_dict_manual))

        
        except Exception as e:
            print(e)

s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')

input_bucket = 'COBI-input-data-2023'
output_bucket = 'COBI-landing-zone-2023'

def handler(event, context):

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

   

from typing import List
import configparser
import pandas as pd
from datetime import datetime


class MotuOptions:
    def __init__(self, attrs: dict):
        super(MotuOptions, self).__setattr__("attrs", attrs)

    def __setattr__(self, k, v):
        self.attrs[k] = v

    def __getattr__(self, k):
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
# Create an empty list to store the dictionaries
    dict_list = []

    # Read the CSV file
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        
        # Iterate over each row in the CSV file
        for row in reader:
            # Append the row dictionary to the list
            dict_list.append(row)

    # Return the list of dictionaries
    return dict_list

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


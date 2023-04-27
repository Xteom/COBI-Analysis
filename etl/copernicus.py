from typing import List
import configparser



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




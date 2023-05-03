from motu_utils import motu_api
import motuclient
from datetime import datetime
import os

from copernicus import read_credentials, MotuOptions

def main():
    
    try:

        date = datetime.today().strftime('%Y-%m-%d')

        # Get the absolute path to the directory containing the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Get the absolute path to the parent directory of the script directory
        parent_dir = os.path.dirname(script_dir)


        # Construct a relative file path to the data directory

        directory_to = os.path.join(parent_dir, 'data', 'copernicus', 'raw')
        if not os.path.isdir(directory_to):
            os.makedirs(directory_to, exist_ok=True)

        output_name = "test.nc"

        credentials = read_credentials()

        data_request_options_dict_manual = {
            "service_id": "SST_GLO_SST_L4_NRT_OBSERVATIONS_010_001-TDS",
            "product_id": "METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2",
            "date_min": datetime.strptime('2017-01-01', '%Y-%m-%d').date(),
            "date_max": datetime.strptime(date, '%Y-%m-%d').date(),
            "longitude_min": -116.,
            "longitude_max": -113.,
            "latitude_min": 26.,
            "latitude_max": 29.,
            "variable": [],
            "motu": "https://nrt.cmems-du.eu/motu-web/Motu",
            "out_dir": directory_to,
            "out_name": output_name,
            "auth_mode": "cas",
            "user": credentials[0],
            "pwd": credentials[1]
        }

        motu_api.execute_request(MotuOptions(data_request_options_dict_manual))

    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()


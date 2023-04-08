from motu_utils import motu_api
import motuclient
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

date = datetime.today().strftime('%Y-%m-%d')
username = 'jorcazas'
password = 'Copernico18072000.'


data_request_options_dict_manual = {
    "service_id": "SST_GLO_SST_L4_REP_OBSERVATIONS_010_011-TDS",
    "product_id": "METOFFICE-GLO-SST-L4-REP-OBS-SST",
    "date_min": datetime.strptime('2017-01-01', '%Y-%m-%d').date(),
    "date_max": datetime.strptime(date, '%Y-%m-%d').date(),
    "longitude_min": -116.,
    "longitude_max": -113.,
    "latitude_min": 26.,
    "latitude_max": 29.,
    "variable": ["analysed_sst","analysis_error","mask","sea_ice_fraction"],
    "motu": "https://nrt.cmems-du.eu/motu-web/Motu",
    "out_dir": "C:/Users/javi2/Documents/CD_aplicada_1/COBI/data/",
    "out_name": "test.nc",
    "auth_mode": "cas",
    "user": username,
    "pwd": password
}

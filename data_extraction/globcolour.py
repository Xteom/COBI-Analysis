# !pip install netCDF4
import netCDF4 as nc
import xarray as xr
import pandas as pd
import time
from ftplib import FTP
import os 

variable_dict = {
    "normalised_fluorescence_line_height":"__GLOB_RESOLUTION_AV-MOD_NFLH_DAY_00",
    "particulate_organic_carbon":"__GLOB_RESOLUTION_AVW-MODVIR_POC_DAY_00",
    "particulate_inorganic_carbon":"__GLOB_RESOLUTION_AVW-MODVIR_PIC_DAY_00",
    
}

directory = "C:\\Users\\javi2\\Documents\\CD_aplicada_1\\COBI\\data\\simar\\"

credentials = ['ftp_gc_JOrcazas_Leal', 'JOrcazas_Leal_6463']

def download_raw(variable, directory, resolution, credentials):
    
    years = ["2017","2018","2019","2020","2021","2022","2023"]
    months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    days = ["01","02","03","04","05","06","07","08","09","10","11","12", "13","14","15",
            "16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
    user = credentials[0] 
    password = credentials[1] 

    directory_path = directory + variable
    if not os.path.isdir(directory_path):
        os.mkdir(directory_path)

    os.chdir(directory_path) #changes the active dir - this is where downloaded files will be saved to
    
    ftp = FTP("ftp.hermes.acri.fr")
    ftp.login(user,password)
    
    for year in years:
        for month in months:
            for day in days:

                try:
                    download_dir ="GLOB/merged/day/"+year+"/"+month+"/"+day+"/" #dir i want to download files from, can be changed or left for user input

                    filematch = 'L3m_*'+variable_dict[variable].replace("RESOLUTION", resolution)+'.nc' # a match for any file in this case, can be changed or left for user to input


                    ftp.cwd(download_dir)

                    for filename in ftp.nlst(filematch): # Loop - looking for matching files
                        fhandle = open(filename, 'wb')
    #                     print('Getting ' + filename) #for confort sake, shows the file that's being retrieved
                        ftp.retrbinary('RETR ' + filename, fhandle.write)
                        fhandle.close()
                except Exception as e:
                    print("La fecha", year, month, day, "no se registró", e)

    return "finished"
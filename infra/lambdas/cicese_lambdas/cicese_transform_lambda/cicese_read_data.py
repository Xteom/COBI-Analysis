import pandas as pd
import os
import glob
from datetime import datetime


def read_cicese_data(place, directory_from):
    columns=["anio","mes","dia","hora","minuto","segundo",
             "id_estacion","voltaje_sistema","nivel_mar_leveltrol","nivel_mar_burbujeador",
             "sw_1","sw_2","temperatura_agua","nivel_mar_ott_rsl", "radiacion_solar",
             "direccion_viento", "magnitud_viento", "temperatura_aire","humedad_relativa",
             "presion_atmosferica","precipitacion","voltaje_estacion_met","nivel_mar_sutron"]
    # Set the directory path
    dir_path = directory_from+place
    
    # Get a list of all .dat files in the directory
    dat_files = glob.glob(os.path.join(dir_path, "*.dat"))

    # Initialize an empty list to store the dataframes
    dfs = []

    # Loop through each file and read it into a dataframe
    for file in dat_files:
        df = pd.read_csv(file, lineterminator='\n', delim_whitespace=True, header=None)
        dfs.append(df)

    # Concatenate all the dataframes into a single dataframe
    result_df = pd.concat(dfs, axis=0, ignore_index=True)
    
    # Rename df columns with the ones defined before
    dict_columns = {}
    for col, i in zip(columns, range(len(columns))):
        dict_columns[i] = col
    dict_columns
    result_df = result_df.rename(columns=dict_columns)

    
    return result_df
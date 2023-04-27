import netCDF4 as nc
import xarray as xr
import pandas as pd
from ftplib import FTP
import os 
import re
import numpy as np

from globcolour import read_variable_dict, process_data


def main():
    # Get the absolute path to the directory containing the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Get the absolute path to the parent directory of the script directory
    parent_dir = os.path.dirname(script_dir)

    # Construct a relative file path to the data directory
    directory_from = os.path.join(parent_dir, 'data', 'globcolour', 'raw')

    # Construct a relative file path to the data directory
    if not os.path.isdir(os.path.join(parent_dir, 'data', 'globcolour')):
        os.mkdir(os.path.join(parent_dir, 'data', 'globcolour'))
    if not os.path.isdir(os.path.join(parent_dir, 'data', 'globcolour', 'processed')):
        os.mkdir(os.path.join(parent_dir, 'data', 'globcolour', 'processed'))

    directory_to = os.path.join(parent_dir, 'data', 'globcolour', 'processed')
    
    

    variable_dict = read_variable_dict('input/variable_dict.csv')

    for v in list(variable_dict.keys()):
        process_data(v, directory_from, directory_to)

if __name__ == '__main__':
    main()
            
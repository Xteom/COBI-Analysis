import os
import re
from datetime import datetime, date
from typing import Set

from globcolour import download_raw, daterange, read_credentials, read_variable_dict


def get_dates_from_filenames(directory: str) -> Set[str]:
    """
    Returns a set of unique dates in filenames found in a directory.
    
    Args:
        directory (str): The directory to scan for filenames.
    
    Returns:
        set: A set of unique dates in filenames, in YYYY-MM-DD format.
    """
    date_regex = r'\d{4}\d{2}\d{2}'  # Regex pattern to match date in YYYYMMDD format
    dates = set()
    
    for filename in os.listdir(directory):
        match = re.search(date_regex, filename)
        if match:
            dates.add(match.group())
    return dates


# MODIFICAR PARA QUE LEA LAS FECHAS DIRECTAMENTE DEL S3 O SQL QUE GUARDA LOS DATOS YA LIMPIOS
def download_files_with_missing_dates(dates_to_download: set, directory: str, variable: str, directory_to: str, 
                                     resolution: str, credentials: list, variable_dict: dict) -> list:
    """
    Downloads files with dates that are in `dates_to_download` but not in the filenames in `directory`.
    
    Args:
        dates_to_download (set): A set of dates in YYYY-MM-DD format to download files for.
        directory (str): The directory containing existing files to compare against.
        variable (str): The name of the variable that will be downloaded.
        directory_to (str): The directory where the files will be downloaded to.
        resolution (str): A string indicating the resolution (in km), i.e. the grid size of the data.
        credentials (list): A list of FTP credentials to use for downloading files.
        variable_dict (dict): A dictionary containing the file formats for each variable.
        
    Returns:
        A list of the outputs from the for loop.
    """
    existing_dates = get_dates_from_filenames(directory)
    dates = dates_to_download.difference(existing_dates)
    
    outputs = []
    for date_to_download in dates:
        output = download_raw(variable,
                      directory_to, 
                      resolution,
                      credentials,
                      variable_dict,
                      date_to_download)
        outputs.append(output)
        
    return outputs


def main():

    variable_dict = read_variable_dict('input/variable_dict.csv')
    credentials = read_credentials()
    start_date = date(2017, 1, 1)
    end_date = date(datetime.now().year, datetime.now().month, datetime.now().day-1)
    dates_to_download = set()
    for single_date in daterange(start_date, end_date):
        dates_to_download.add(single_date.strftime("%Y")+single_date.strftime("%m")+single_date.strftime("%d"))
        
    # Get the absolute path to the directory containing the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get the absolute path to the parent directory of the script directory
    parent_dir = os.path.dirname(script_dir)

    # Construct a relative file path to the data directory
    if not os.path.isdir(os.path.join(parent_dir, 'data', 'globcolour')):
        os.mkdir(os.path.join(parent_dir, 'data', 'globcolour'))
    if not os.path.isdir(os.path.join(parent_dir, 'data', 'globcolour', 'raw')):
        os.mkdir(os.path.join(parent_dir, 'data', 'globcolour', 'raw'))

    directory_to = os.path.join(parent_dir, 'data', 'globcolour', 'raw')


    for resolution in ["100", "25", "4"]:
        for variable in variable_dict.keys():
            directory = os.path.join(directory_to, variable)
            print(download_files_with_missing_dates(dates_to_download, directory, variable, directory_to, resolution, credentials, variable_dict))


if __name__ == '__main__':
    main()


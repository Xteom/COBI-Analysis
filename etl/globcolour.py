from ftplib import FTP
import os 
from datetime import datetime

variable_dict = {
    "normalised_fluorescence_line_height":"__GLOB_RESOLUTION_AV-MOD_NFLH_DAY_00",
    "particulate_organic_carbon":"__GLOB_RESOLUTION_AVW-MODVIR_POC_DAY_00",
    "particulate_inorganic_carbon":"__GLOB_RESOLUTION_AVW-MODVIR_PIC_DAY_00",
    
}

directory = "C:\\Users\\javi2\\Documents\\CD_aplicada_1\\COBI\\data\\simar\\"

credentials = ['ftp_gc_JOrcazas_Leal', 'JOrcazas_Leal_6463']

def download_raw(variable, directory_to, resolution, credentials, variable_dict, year_from):
    
    """Downloads data from the GlobColour site using FTP.

    Retrieves daily files (of whole years beginning at from_year) from GlobColour through FTP;
    saves them in a given directory without processing them.
    Credentials are stored in config.ini file.

    Args:
        variable: A string indicating the variable to retrieve.
        directory: A string indicating the directory where the files will be stored.
        resolution: 
        credentials:
        variable_dict:
        from_year: An int indicating the start year of the retrieval.        


    Returns:
        A list of tuples containing the year, month and day of files that were not able to be retrieved.
        For example:

        [(2022, 01, 31), (2023, 02, 01)] 
        this would mean that it was not posible to retrieve files from 2022/01/31 and from 2023/02/01.

        Since it loops through all day numbers from 01 to 31, there will always be dates not retrieved 
        such as (xxxx,02,30), (xxxx,04,31), etc. 

    """
    years = list(range(year_from, datetime.now().year+1))
    months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    days = ["01","02","03","04","05","06","07","08","09","10","11","12", "13","14","15",
            "16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]

    user = credentials[0] 
    password = credentials[1] 

    directory_path = directory_to + variable
    if not os.path.isdir(directory_path):
        os.mkdir(directory_path)
    
    os.chdir(directory_path) #changes the active dir - this is where downloaded files will be saved to
    
    
    filematch = 'L3m_*'+variable_dict[variable].replace("RESOLUTION", resolution)+'.nc' # a match for any file in this case, can be changed or left for user to input
    
    not_loaded = []
    
    for year in years:
        for month in months:
            for day in days:
                try:                    
                    download_dir ="GLOB/merged/day/"+str(year)+"/"+month+"/"+day+"/" #dir i want to download files from, can be changed or left for user input
                    ftp = FTP("ftp.hermes.acri.fr")
                    ftp.login(user,password)
                    
                    ftp.cwd(download_dir)
                    for filename in ftp.nlst(filematch): # Loop - looking for matching files
                        if not os.path.exists(filename):
                            fhandle = open(filename, 'wb')
        #                     print('Getting ' + filename) #for confort sake, shows the file that's being retrieved
                            ftp.retrbinary('RETR ' + filename, fhandle.write)
                            fhandle.close()
                        
                    ftp.quit()
                except Exception as e:
                    not_loaded.append((year, month, day, e))
                    print("error in variable", variable,":", e, str(year)+str(month)+str(day))

    return not_loaded

def globcolour_cleansing(variable, directory_from, directory_to, coordinates=[-116, -113, 26, 29]):
        
    directory_path = directory_to + variable + "_clean"
    if not os.path.isdir(directory_path):
        os.mkdir(directory_path)
    os.chdir(directory_path) #changes the active dir - this is where downloaded files will be saved to
    
        
    directory = directory_from+variable
    try:
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)

            try:
                date_match = re.search('\d\d\d\d\d\d\d\d', filename)
                date = pd.to_datetime(date_match.group()).date()

                ds = xr.open_dataset(f)

                df = ds.to_dataframe()
                df = df.reset_index()
                ds.close()

                df = df[(df.lon > coordinates[0]) & (df.lon < coordinates[1]) &
                  (df.lat > coordinates[2]) & (df.lat < coordinates[3])] # este es el rango de coordenadas en el grid

                # Aquí hacemos selección de columnas, las cuales son únicas para cada VARIABLE
                obs = df #observación de un día

                obs["date"] = obs.apply(lambda x: date, axis=1)

                obs.to_csv(filename.replace(".nc", "_clean.csv"))

            except Exception as e:
                print("Error con:", filename, e)
    except Exception as e:
        #borrar esa exception cuando ya estén todas las variables
        print(e)
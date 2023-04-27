import glob
import pandas as pd
import xarray as xr
import os
import psycopg2

# PENDIENTE: pasar en limpio bien

directory = "C:/Users/javi2/Documents/CD_aplicada_1/COBI/etl/data/copernicus/raw/" # PENDIENTE: quitar esto

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)

    

    ds = xr.open_dataset(f)

    df = ds.to_dataframe()
    df = df.reset_index()
    ds.close()
    
    # create a dictionary to map the old column names to new column names
    new_column_names = {}
    for column in df.columns:
        if "time" in column:
            new_column_names[column] = "date"
    # rename the columns using the dictionary created above
            df.rename(columns=new_column_names, inplace=True)
        
    df['date'] = pd.to_datetime(df['date']).dt.date
    
    
    df = df[["lat", "lon", "analysis_error", "sea_ice_fraction", "analysed_sst", "date"]]
    df.to_csv(directory+"test.csv")
df


try:
    # Set the directory where the CSV files are located
    dir_path = "C:/Users/javi2/Documents/CD_aplicada_1/COBI/etl/data/copernicus/processed/" # PENDIENTE: quitar esto 

    # Use glob to find all CSV files in the directory
    all_files = glob.glob(os.path.join(dir_path, "*.csv"))

    # Concatenate all CSV files into a single Pandas DataFrame
    
    for f in all_files:
        df = pd.read_csv(f)

        # set up a connection to the database
        conn = psycopg2.connect(
            host="localhost",
            database="cobi",
            user="postgres",
            password="admin"
        )

        # create a database cursor
        cur = conn.cursor()


        # Iterate over the DataFrame rows and insert them into the PostgreSQL table
        for i, row in df.iterrows():
            cur.execute("INSERT INTO copernicus (lat, lon, analysis_error, sea_ice_fraction, analysed_sst, date) VALUES (%s, %s, %s, %s, %s, %s)",
                        (row["lat"], row["lon"], row["analysis_error"], row["sea_ice_fraction"], row["analysed_sst"], row["date"]))

        # Commit the changes and close the database connection
        conn.commit()
        cur.close()
        conn.close()

except Exception as e:
    print(" error:", e)
import glob
import xarray as xr
import os


input_dir = os.path.join(os.getcwd(),"data","copernicus", "raw")
destination_dir = os.path.join(os.getcwd(),"data","copernicus", "processed")

def nc_to_csv(input_dir=input_dir,
           destination_dir=destination_dir):
    
    for filename in os.listdir(input_dir):
        raw_file = os.path.join(input_dir, filename)

        ds = xr.open_dataset(raw_file)

        df = ds.to_dataframe()
        df = df.reset_index()
        ds.close()

        print(df)

        if not os.path.isdir(destination_dir):
                os.makedirs(destination_dir, exist_ok=True)

        
        df.to_csv(os.path.join(destination_dir, filename[:-3]+".csv"))
        

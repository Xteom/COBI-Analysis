import pandas as pd
import psycopg2

dir = "C:/Users/javi2/Documents/CD_aplicada_1/COBI/etl/data/globcolour/processed/aerosol_optical_thickness_over_water/"

# read in the CSV files
df1 = pd.read_csv(dir+'L3m_20170101__GLOB_100_AVW-MODVIR_T865_DAY_00_clean.csv')
df2 = pd.read_csv(dir+'L3m_20170102__GLOB_100_AVW-MODVIR_T865_DAY_00_clean.csv')
df3 = pd.read_csv(dir+'L3m_20170103__GLOB_100_AVW-MODVIR_T865_DAY_00_clean.csv')

# merge the dataframes
merged_df = pd.concat([df1, df2, df3])

print(merged_df)

# set up a connection to the database
conn = psycopg2.connect(
    host="localhost",
    database="mydatabase",
    user="myusername",
    password="mypassword"
)

# create a database cursor
cur = conn.cursor()

# use COPY command to load data from CSV to existing table
with open('merged_data.csv', 'r') as f:
    next(f) # skip the header row
    cur.copy_from(f, 'existing_table', sep=',') # replace 'existing_table' with the actual table name

# commit changes and close the cursor
conn.commit()
cur.close()

# close the database connection
conn.close()
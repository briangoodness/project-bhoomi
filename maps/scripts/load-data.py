# Python 3.5.2
import time
import os
import pandas as pd
from sqlalchemy import create_engine
import dj_database_url

# load CSV file into DataFrame
filename = '../data/rwanda_cluster_avg_asset_2010.csv'
df = pd.read_csv(filename)
#df.id = df.id.astype(int)

# rename fields
cols_to_rename = {
    'DHSCLUST':'id',
    'X':'longitude',
    'Y':'latitude',
    'hv271':'dhs_wealth_idx'
    }
df = df.rename(columns=cols_to_rename)

# select columns to load
cols = ['id',
        'dhs_wealth_idx',
        'latitude',
        'longitude',]

#insert into locations table
conn_info = os.environ['DATABASE_URL']
conn = create_engine(conn_info, pool_size=20, max_overflow=10)
t0 = time.time()
df[cols].to_sql('maps_dhs_cluster', con=conn, if_exists='replace', index=False)
print(time.time() - t0)

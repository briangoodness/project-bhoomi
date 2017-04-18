# Python 3.5.2
import time
import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import dj_database_url
import sys
import getopt

# print-out help / instructions
def help():
    print('\nusage:')
    print('use --file = for setting the path to the DHS wealth indices file (CSV).')
    print('use --country = for setting the country name')
    print('use --year = for setting the year(s) for the data source\n')

# run main
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h", ["file=", "country=", "year="])
    except getopt.GetoptError:
        sys.exit(2)

    optlist = [opt for opt, arg in opts]
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
            sys.exit(2)
        elif opt == '--file':
            filename = arg
        elif opt == '--country':
            country = arg
        elif opt == '--year':
            data_year = arg

    # print country
    if '--country' in optlist:
        print('\nCountry: %s' % country)

    # print year(s)
    if '--year' in optlist:
        print('Year(s): %s\n' % data_year)

    # load CSV file into DataFrame
    df = pd.read_csv(filename)

    # rename fields
    cols_to_rename = {
        'cluster':'id',
        'longitude':'longitude',
        'latitude':'latitude',
        'wlthindf':'dhs_wealth_idx'
        }
    df = df.rename(columns=cols_to_rename)

    # add country, year colummns
    df['country'] = country
    df['data_year'] = data_year

    # select columns to load
    cols = ['id',
            'country',
            'data_year',
            'dhs_wealth_idx',
            'latitude',
            'longitude',]

    # replace zeros with NaN
    df.replace({'latitude':0, 'longitude':0}, np.nan, inplace=True)

    #insert into locations table
    conn_info = os.environ['DATABASE_URL']
    conn = create_engine(conn_info, pool_size=20, max_overflow=10)
    t0 = time.time()
    df[cols].to_sql('maps_dhs_cluster', con=conn, if_exists='append', index=False)
    print(time.time() - t0)

if __name__ == "__main__":
    main(sys.argv[1:])

# Python 3.5.2
import time
import os
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import MultiPolygon
from sqlalchemy import create_engine
from geoalchemy2 import Geometry, WKTElement
import dj_database_url
import sys
import getopt

# print-out help / instructions
def help():
    print('\nusage:')
    print('use --file = for setting the path to the regional shape file.')
    print('use --country = for setting the country name\n')

# run main
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h", ["file=", "country=", "admin_level="])
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
        elif opt == '--admin_level':
            admin_level = int(arg)

    # print country
    if '--country' in optlist:
        print('\nCountry: %s\n' % country)

    # print administrative level
    if '--admin_level' in optlist:
        print('\Administrative Level: %s\n' % admin_level)

    # load CSV file into GeoDataFrame
    gdf = gpd.read_file(filename, crs=4326)

    # Function to return MultiPolygon from Polygon type
    # source: https://gis.stackexchange.com/questions/215408/convert-polygon-to-multipolygon-with-shapely
    def make_multipoly(polygon):
        return MultiPolygon([polygon])

    # Function to generate Well-Known Text (WKT) form
    def wkt(line):
        return line.to_wkt()

    # convert column to WKT format
    # coerce all Polygons to be of type MultiPolygon
    gdf['geom'] = gdf['geometry'].apply(make_multipoly)
    gdf['geom'] = gdf['geom'].apply(wkt)

    # rename fields
    # if country-wide shape (admin_level==0), then use different field
    cols_to_rename = {
        'NAME_%s' % admin_level:'name'
        }
    if admin_level==0:
        cols_to_rename = {
            'NAME_ENGLI':'name'
            }
    gdf = gdf.rename(columns=cols_to_rename)

    # add country column
    gdf['country'] = country
    gdf['admin_level'] = admin_level
    gdf['predicted_wealth_idx'] = 1.2
    gdf['wealth_decile'] = 65

    # select columns to load
    cols = [
            'name',
            'country',
            'admin_level',
            'predicted_wealth_idx',
            'wealth_decile',
            'geom',]

    #insert into table
    t0 = time.time()
    conn_info = os.environ['DATABASE_URL']
    conn = create_engine(conn_info, pool_size=20, max_overflow=10)
    gdf[cols].to_sql('maps_region', con=conn, if_exists='append', index=False)

    print(time.time() - t0)

if __name__ == "__main__":
    main(sys.argv[1:])

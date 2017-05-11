# Python 3.5.2

import time
import sys
import os
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon, MultiPolygon, asShape
from sqlalchemy import create_engine
from geoalchemy2 import Geometry, WKTElement
from osgeo import gdal, ogr, osr
from scipy import misc, ndimage
import dj_database_url
import getopt
gdal.UseExceptions()

# note: prior to running, execute bash script to export regions and cell preditions, into a SHP file
# in ./maps/scripts/export-regions-and-cell-predictions-from-db.sh

# load regions shape file
regions_shp = '%s/maps/data/shp_exports/regions/regions.shp' % os.environ['FINALPROJECT']

# load 'maps_regions' table (name, country, admin_level, geometry); rename columns
# delete extraneous / unused columns
regions = gpd.read_file(regions_shp, crs=4326)
cols_to_rename = {
    'ADMIN_LEVE':'admin_level',
    'COUNTRY':'country',
    'ID':'id',
    'NAME':'name',
    'PREDICTED_':'predicted_wealth_idx',
    'WEALTH_DEC':'wealth_decile'
}
regions.rename(columns=cols_to_rename, inplace=True)
# del regions['id']
del regions['predicted_wealth_idx']
del regions['wealth_decile']

# create empty regional results dict, for given country
regional_preds = {}

# loop-over each country
country_list = ['ghana', 'malawi', 'rwanda', 'tanzania']

# for each country separately:
for country in country_list:

    # slice/partition regions ('maps_region' table), based on country
    print('\nCountry: %s' % country)
    country_regions = regions[regions.country == country]

    # load country-specific cell predictions shape file
    cell_predictions_shp = '%s/maps/data/shp_exports/cell_predictions_%s/cell_predictions_%s.shp' % ( os.environ['FINALPROJECT'], country, country )

    # load 'maps_cell_prediction' table (country, i, j, wealth index, geometry); rename columns
    cell_predictions = gpd.read_file(cell_predictions_shp, crs=4326)
    cols_to_rename = {
        'COUNTRY':'country',
        'I':'i',
        'ID':'id',
        'J':'j',
        'PREDICTED_':'predicted_wealth_idx'
    }
    cell_predictions.rename(columns=cols_to_rename, inplace=True)
    del cell_predictions['country']

    # slice/partition regions ('maps_region' table), based on administrative level
    admin_levels_range = country_regions.admin_level.unique()
    regions_dict = { level : gpd.GeoDataFrame(crs=4326) for level in admin_levels_range }
    for level in regions_dict.keys():
        regions_dict[level] = country_regions[country_regions.admin_level==level]

    # create empty regional results dict, for given country
    regional_preds[country] = {}

    # for each administrative level (0, 1, 2, 3):
    for lvl in admin_levels_range:
        print('\nSpatial Join -- Country: %s, Administrative Level: %s' % (country, lvl))

        t0 = time.time()

        # complete spatial join of 'maps_cell_prediction' table with 'maps_region' table
        predictions_merged_region = gpd.sjoin(regions_dict[lvl], cell_predictions, how="inner", op="intersects")

        # groupby regional name/id: calculate average wealth_index
        # store results for given administrative level into regional results dict
        # note: tried using gpd.dissolve() function, but too slow -- instead merge geometries back later
        cols = ['country','admin_level','name', 'predicted_wealth_idx']
        groupby_cols = ['country','admin_level','name']
        regional_preds[country][lvl] = predictions_merged_region[cols].groupby(groupby_cols).mean()

        # groupby country: compute deciles of wealth, based on wealth_index

        print('Time Elapsed: %s' % (time.time() - t0))

    # combine results across all administrative levels, within country
    regional_preds[country] = pd.concat(regional_preds[country])

# combine results across all countries and administrative levels
regional_preds = pd.concat(regional_preds).reset_index()
print('Columns: %s' % regional_preds.columns)

# export to CSV
outfile = '%s/maps/data/regional-wealth-predictions.csv' % os.environ['FINALPROJECT']
regional_preds.to_csv(outfile)

# merge (on country, admin_level, and name) aggregated results with regional geometries
print('Merge back with regional geometries (on country, admin_level, and name)')
gdf = pd.merge(regions, regional_preds, on=['country', 'admin_level', 'name'])

##########################################################################################################
# load combined results into 'maps_region_prediction' table (which includes wealth index, wealth decile) #
##########################################################################################################
print("load combined results into 'maps_region_prediction' table (which includes wealth index, wealth decile)")

# Function to return MultiPolygon from Polygon type
# source: https://gis.stackexchange.com/questions/215408/convert-polygon-to-multipolygon-with-shapely
def make_multipoly(polygon):
    return MultiPolygon([polygon])

# Function to generate Well-Known Text (WKT) form
def wkt(line):
    return line.to_wkt()

# convert column to WKT format
# coerce all Polygons to be of type MultiPolygon
# gdf['geom'] = gdf['geometry'].apply(make_multipoly)
gdf['geom'] = gdf['geom'].apply(wkt)

# select columns to load
cols = [
        'name',
        'country',
        'admin_level',
        'predicted_wealth_idx',
        'wealth_decile',
        'geom',]

#insert into table
print("Database Load (into 'maps_region_prediction' table)")
t0 = time.time()
conn_info = os.environ['DATABASE_URL']
conn = create_engine(conn_info, pool_size=20, max_overflow=10)
gdf[cols].to_sql('maps_region_prediction', con=conn, if_exists='append', index=False)
print('Time Elapsed (Database Load): %s' % (time.time() - t0))

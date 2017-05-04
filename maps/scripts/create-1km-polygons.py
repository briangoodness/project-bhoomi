# Python 3.5.2
import time
import os
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon, MultiPolygon
from sqlalchemy import create_engine
from geoalchemy2 import Geometry, WKTElement
from osgeo import gdal, ogr, osr
from scipy import misc, ndimage
import dj_database_url
import sys
import getopt
gdal.UseExceptions()

# Helper function to read a raster file
def read_raster(raster_file):
    """
    Function
    --------
    read_raster

    Given a raster file, get the pixel size, pixel location, and pixel value

    Parameters
    ----------
    raster_file : string
        Path to the raster file

    Returns
    -------
    x_size : float
        Pixel size
    top_left_x_coords : numpy.ndarray  shape: (number of columns,)
        Longitude of the top-left point in each pixel
    top_left_y_coords : numpy.ndarray  shape: (number of rows,)
        Latitude of the top-left point in each pixel
    centroid_x_coords : numpy.ndarray  shape: (number of columns,)
        Longitude of the centroid in each pixel
    centroid_y_coords : numpy.ndarray  shape: (number of rows,)
        Latitude of the centroid in each pixel
    bands_data : numpy.ndarray  shape: (number of rows, number of columns, 1)
        Pixel value
    """
    raster_dataset = gdal.Open(raster_file, gdal.GA_ReadOnly)
    # get project coordination
    proj = raster_dataset.GetProjectionRef()
    bands_data = []
    # Loop through all raster bands
    for b in range(1, raster_dataset.RasterCount + 1):
        band = raster_dataset.GetRasterBand(b)
        bands_data.append(band.ReadAsArray())
        no_data_value = band.GetNoDataValue()
    bands_data = np.dstack(bands_data)
    rows, cols, n_bands = bands_data.shape

    # Get the metadata of the raster
    geo_transform = raster_dataset.GetGeoTransform()
    (upper_left_x, x_size, x_rotation, upper_left_y, y_rotation, y_size) = geo_transform

    # Get location of each pixel
    x_size = 1.0 / int(round(1 / float(x_size)))
    y_size = - x_size
    y_index = np.arange(bands_data.shape[0])
    x_index = np.arange(bands_data.shape[1])

    corners = {}

    # top-left corner
    corners['top_left_x_coords'] = upper_left_x + x_index * x_size
    corners['top_left_y_coords'] = upper_left_y + y_index * y_size

    # top-right corner
    corners['top_right_x_coords'] = (upper_left_x + x_size) + x_index * x_size
    corners['top_right_y_coords'] = upper_left_y + y_index * y_size

    # bottom-left corner
    corners['bottom_left_x_coords'] = upper_left_x + x_index * x_size
    corners['bottom_left_y_coords'] = (upper_left_y + y_size) + y_index * y_size

    # bottom-right corner
    corners['bottom_right_x_coords'] = (upper_left_x + x_size) + x_index * x_size
    corners['bottom_right_y_coords'] = (upper_left_y + y_size) + y_index * y_size

    # Add half of the cell size to get the centroid of the cell
    centroid_x_coords = corners['top_left_x_coords'] + (x_size / 2)
    centroid_y_coords = corners['top_left_y_coords'] + (y_size / 2)

    return (x_size, corners, centroid_x_coords, centroid_y_coords, bands_data)


# Helper function to get the pixel index of the point
def get_cell_idx(lon, lat, top_left_x_coords, top_left_y_coords):
    """
    Function
    --------
    get_cell_idx

    Given a point location and all the pixel locations of the raster file,
    get the column and row index of the point in the raster

    Parameters
    ----------
    lon : float
        Longitude of the point
    lat : float
        Latitude of the point
    top_left_x_coords : numpy.ndarray  shape: (number of columns,)
        Longitude of the top-left point in each pixel
    top_left_y_coords : numpy.ndarray  shape: (number of rows,)
        Latitude of the top-left point in each pixel

    Returns
    -------
    lon_idx : int
        Column index
    lat_idx : int
        Row index
    """
    lon_idx = np.where(top_left_x_coords < lon)[0][-1]
    lat_idx = np.where(top_left_y_coords > lat)[0][-1]
    return lon_idx, lat_idx

# Helper function to read a shapefile
def get_shp_extent(shp_file):
    """
    Function
    --------
    get_shp_extent

    Given a shapefile, get the extent (boundaries)

    Parameters
    ----------
    shp_file : string
        Path to the shapefile

    Returns
    -------
    extent : tuple
        Boundary location of the shapefile (x_min, x_max, y_min, y_max)
    """
    inDriver = ogr.GetDriverByName("ESRI Shapefile")
    inDataSource = inDriver.Open(shp_file, 0)
    inLayer = inDataSource.GetLayer()
    extent = inLayer.GetExtent()
    # x_min_shp, x_max_shp, y_min_shp, y_max_shp = extent
    return extent

# print-out help / instructions
def help():
    print('\nusage:')
    print('use --country = for setting the country name\n')
    print('use --country_shp = for setting the path to the shape file (.SHP) for the given country.')

# store country list
country_list = ['malawi', 'ghana', 'rwanda', 'tanzania']

# run main
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h", ["country=", "country_shp="])
    except getopt.GetoptError:
        sys.exit(2)

    optlist = [opt for opt, arg in opts]
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
            sys.exit(2)
        elif opt == '--country':
            country = arg
            if country not in country_list:
                print('\nCountry %s not available. Specify one of the following countries: %s\n' % (country, country_list))
                sys.exit(2)
        elif opt == '--country_shp':
            country_shp = arg

    # print country
    if '--country' in optlist:
        print('\nCountry: %s\n' % country)


    # print country shape file
    if '--country_shp' in optlist:
        print('\Shape File: %s\n' % country_shp)

    # retrieve nightlights data (run only once)
    #night_image_url = 'https://ngdc.noaa.gov/eog/data/web_data/v4composites/F182010.v4.tar'
    #wget.download(night_image_url)

    # this illustrates how you can read the nightlight image
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raster_file = 'data/nightlights/F182010.v4/F182010.v4d_web.stable_lights.avg_vis.tif'
    nightlights={}
    nightlights['x_size'], nightlights['corners'], nightlights['centroid_x_coords'], nightlights['centroid_y_coords'], nightlights['bands_data'] = read_raster(os.path.join(BASE_DIR, raster_file))

    # print-out dimensions:
    print('x_size: %s' % nightlights['x_size'])
    for item in nightlights.keys():
        if item=='x_size' or item=='corners':
            continue
        print('%s: %s' % (item, nightlights[item].shape))

    print('')
    for item in nightlights['corners'].keys():
        print('%s: %s' % (item, nightlights['corners'][item].shape))
    print('')

    # save the result in compressed format - see https://docs.scipy.org/doc/numpy/reference/generated/numpy.savez.html
    #np.savez('data/nightlights/nightlight.npz', nightlights['top_left_x_coords']=nightlights['top_left_x_coords'], nightlights['top_left_y_coords']=nightlights['top_left_y_coords'], nightlights['bands_data']=nightlights['bands_data'])

    # Now read in the shapefile for country and extract the edges of the country
    x_min_shp, x_max_shp, y_min_shp, y_max_shp = get_shp_extent(country_shp)

    # retrieve coordinates
    left_idx, top_idx = get_cell_idx(x_min_shp, y_max_shp, nightlights['corners']['top_left_x_coords'], nightlights['corners']['top_left_y_coords'] )
    right_idx, bottom_idx = get_cell_idx(x_max_shp, y_min_shp, nightlights['corners']['top_left_x_coords'], nightlights['corners']['top_left_y_coords'])

    # loop over each i, j cell; record dimensions (i.e., lat/long points) of each of the cell's four corners
    t0 = time.time()
    counter=0
    cells = {}
    country_height = bottom_idx - top_idx + 1
    country_width = right_idx - left_idx + 1
    for i in range(country_height):
        for j in range(country_width):

            cells[counter]={}

            cells[counter]['i'] = top_idx + i
            cells[counter]['j'] = left_idx + j

            cells[counter]['top_left_y_coords']= nightlights['corners']['top_left_y_coords'][i]
            cells[counter]['top_right_y_coords']= nightlights['corners']['top_right_y_coords'][i]
            cells[counter]['bottom_left_y_coords']= nightlights['corners']['bottom_left_y_coords'][i]
            cells[counter]['bottom_right_y_coords']= nightlights['corners']['bottom_right_y_coords'][i]

            cells[counter]['top_left_x_coords']= nightlights['corners']['top_left_x_coords'][j]
            cells[counter]['top_right_x_coords']= nightlights['corners']['top_right_x_coords'][j]
            cells[counter]['bottom_left_x_coords']= nightlights['corners']['bottom_left_x_coords'][j]
            cells[counter]['bottom_right_x_coords']= nightlights['corners']['bottom_right_x_coords'][j]

            counter+=1

    # print
    print('\nTime Elapsed: %s' % (time.time()-t0))
    print('\nTotal Number of Cells for %s: %s' % (country, len(cells)))

    # create Polygons from set of Points(X, Y)
    def create_polygons(df):
        return Polygon([(df['top_left_x_coords'], df['top_left_y_coords']), (df['top_right_x_coords'], df['top_right_y_coords']), (df['bottom_right_x_coords'], df['bottom_right_y_coords']), (df['bottom_left_x_coords'], df['bottom_left_y_coords'])])

    # Function to return MultiPolygon from Polygon type
    # source: https://gis.stackexchange.com/questions/215408/convert-polygon-to-multipolygon-with-shapely
    def make_multipoly(polygon):
        return MultiPolygon([polygon])

    # Function to generate Well-Known Text (WKT) form
    def wkt(line):
        return line.to_wkt()

    # import into dataframe
    gdf = gpd.GeoDataFrame.from_dict(cells, orient='index')
    gdf['geom'] = gdf.apply(create_polygons, axis=1)

    # convert geometry column to WKT format
    # coerce all Polygons to be of type MultiPolygon
    # gdf['geom'] = gdf['geom'].apply(make_multipoly)
    gdf['geom'] = gdf['geom'].apply(wkt)

    # create country, predicted_wealth_idx (for testing) columns
    gdf['country'] = country
    gdf['predicted_wealth_idx'] = 1.4

    # sub-select columns
    cols = ['country','i','j','predicted_wealth_idx', 'geom']
    gdf = gdf[cols]

    #insert into table
    print('Loading into Database.')
    t0 = time.time()
    conn_info = os.environ['DATABASE_URL']
    conn = create_engine(conn_info, pool_size=20, max_overflow=10)
    gdf[cols].to_sql('maps_cell_prediction', con=conn, if_exists='append', index=False)
    print('Time Elapsed: %s' % (time.time()-t0))

    # calculate # images (based on row, height)
    num_images = (bottom_idx - top_idx + 1) * (right_idx - left_idx + 1)
    row = {
      'country':country,
      'left_idx':left_idx,
      'top_idx':top_idx,
      'right_idx':right_idx,
      'bottom_idx':bottom_idx,
      'num_images':num_images,
    }
    for key in row.keys():
        print('%s: %s' % (key, row[key]))

if __name__ == "__main__":
    main(sys.argv[1:])

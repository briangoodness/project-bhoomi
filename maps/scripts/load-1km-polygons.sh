
# Commands sent to load-map-regions.py to predictions (1km x 1km cells) into database:

cd $FINALPROJECT/maps/scripts

# loading country-specific data
echo 'Loading 1km x 1km predictions into table in database (maps_cell_prediction)'

# malawi
python create-1km-polygons.py --country_shp=$FINALPROJECT/maps/data/MWI_adm_shp/MWI_adm0.shp --country='malawi'

# rwanda
python create-1km-polygons.py --country_shp=$FINALPROJECT/maps/data/RWA_adm_shp/RWA_adm0.shp --country='rwanda'

# ghana
python create-1km-polygons.py --country_shp=$FINALPROJECT/maps/data/GHA_adm_shp/GHA_adm0.shp --country='ghana'

# tanzania
python create-1km-polygons.py --country_shp=$FINALPROJECT/maps/data/TZA_adm_shp/TZA_adm0.shp --country='tanzania'

# run
echo 'Cleaning up table in database (maps_cell_prediction)'
psql $DATABASE_URL --file=cleanup-1km-polygons.sql


# Commands sent to load-map-regions.py to predictions (1km x 1km cells) into database:
# reference: https://gis.stackexchange.com/questions/55206/how-can-i-get-a-shapefile-from-a-postgis-query
cd $FINALPROJECT/maps/data/shp_exports

# loading country-specific data
echo 'Exporting cell predictions, by country'

# create directories
mkdir cell_predictions_ghana
mkdir cell_predictions_malawi
mkdir cell_predictions_rwanda
mkdir cell_predictions_tanzania

# ghana
cd cell_predictions_ghana
pgsql2shp -f cell_predictions_ghana -h localhost -u bhoomi -P $BHOOMI_DB_PWD -p 5433 bhoomi "select * from maps_cell_prediction where country='ghana';"
cd ..

# malawi
cd cell_predictions_malawi
pgsql2shp -f cell_predictions_malawi -h localhost -u bhoomi -P $BHOOMI_DB_PWD -p 5433 bhoomi "select * from maps_cell_prediction where country='malawi';"
cd ..

# rwanda
cd cell_predictions_rwanda
pgsql2shp -f cell_predictions_rwanda -h localhost -u bhoomi -P $BHOOMI_DB_PWD -p 5433 bhoomi "select * from maps_cell_prediction where country='rwanda';"
cd ..

# tanzania
cd cell_predictions_tanzania
pgsql2shp -f cell_predictions_tanzania -h localhost -u bhoomi -P $BHOOMI_DB_PWD -p 5433 bhoomi "select * from maps_cell_prediction where country='tanzania';"
cd ..


# Commands sent to load-map-regions.py to load map regions (SHP files) into database:

cd $FINALPROJECT/maps/scripts

python load-map-regions.py --file=$FINALPROJECT/maps/data/MWI_adm_shp/MWI_adm1.shp --country='malawi'

python load-map-regions.py --file=$FINALPROJECT/maps/data/RWA_adm_shp/RWA_adm1.shp --country='rwanda'

python load-map-regions.py --file=$FINALPROJECT/maps/data/GHA_adm_shp/GHA_adm1.shp --country='ghana'

python load-map-regions.py --file=$FINALPROJECT/maps/data/TZA_adm_shp/TZA_adm1.shp --country='tanzania'

# After loading all rows; run SQL statement to convert the 'geom' column back to Geometry datatype, from text/hex format
# ALTER TABLE maps_region ALTER COLUMN geom TYPE Geometry(MultiPOLYGON);
# SELECT UpdateGeometrySRID('maps_region', 'geom', 4326);


# Commands sent to load-dhs-clusters.py to load DHS Clusters (CSV) into database:

cd $FINALPROJECT/maps/scripts

python load-dhs-clusters.py --file=$FINALPROJECT/maps/data/ghana_cluster_avg_asset_2014.csv --country='ghana' --year=2014

python load-dhs-clusters.py --file=$FINALPROJECT/maps/data/malawi_cluster_avg_asset_2015_2016.csv --country='malawi' --year=2015_2016

python load-dhs-clusters.py --file=$FINALPROJECT/maps/data/rwanda_cluster_avg_asset_2014_2015.csv --country='rwanda' --year=2014_2015

python load-dhs-clusters.py --file=$FINALPROJECT/maps/data/tanzania_cluster_avg_asset_2015_2016.csv --country='tanzania' --year=2015_2016


# After importing rows to the table, run SQL statement to create new POINT field, based on the lat/long values:
# (note: ensure that lat/long is input into function in correct order)
# SELECT AddGeometryColumn ('maps_dhs_cluster', 'geom', 4326, 'POINT', 2);
# UPDATE maps_dhs_cluster SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326);

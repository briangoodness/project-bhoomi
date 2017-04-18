
# Commands sent to load-data.py to load DHS Clusters (CSV) into database:

cd '$FINALPROJECT/maps/scripts'

python load-data.py --file='$FINALPROJECT/maps/data/ghana_cluster_avg_asset_2014.csv' --country='ghana' --year=2014

python load-data.py --file='$FINALPROJECT/maps/data/malawi_cluster_avg_asset_2015_2016.csv' --country='malawi' --year=2015_2016

python load-data.py --file='$FINALPROJECT/maps/data/rwanda_cluster_avg_asset_2014_2015.csv' --country='rwanda' --year=2014_2015

python load-data.py --file='$FINALPROJECT/maps/data/tanzania_cluster_avg_asset_2015_2016.csv' --country='tanzania' --year=2015_2016



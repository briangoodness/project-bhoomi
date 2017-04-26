
# Commands sent to load-map-regions.py to load map regions (SHP files) into database:

cd $FINALPROJECT/maps/scripts

# malawi
python load-map-regions.py --file=$FINALPROJECT/maps/data/MWI_adm_shp/MWI_adm0.shp --country='malawi' --admin_level=0
python load-map-regions.py --file=$FINALPROJECT/maps/data/MWI_adm_shp/MWI_adm1.shp --country='malawi' --admin_level=1
python load-map-regions.py --file=$FINALPROJECT/maps/data/MWI_adm_shp/MWI_adm2.shp --country='malawi' --admin_level=2
python load-map-regions.py --file=$FINALPROJECT/maps/data/MWI_adm_shp/MWI_adm3.shp --country='malawi' --admin_level=3

# rwanda
python load-map-regions.py --file=$FINALPROJECT/maps/data/RWA_adm_shp/RWA_adm0.shp --country='rwanda' --admin_level=0
python load-map-regions.py --file=$FINALPROJECT/maps/data/RWA_adm_shp/RWA_adm1.shp --country='rwanda' --admin_level=1
python load-map-regions.py --file=$FINALPROJECT/maps/data/RWA_adm_shp/RWA_adm2.shp --country='rwanda' --admin_level=2
python load-map-regions.py --file=$FINALPROJECT/maps/data/RWA_adm_shp/RWA_adm3.shp --country='rwanda' --admin_level=3

# ghana
python load-map-regions.py --file=$FINALPROJECT/maps/data/GHA_adm_shp/GHA_adm0.shp --country='ghana' --admin_level=0
python load-map-regions.py --file=$FINALPROJECT/maps/data/GHA_adm_shp/GHA_adm1.shp --country='ghana' --admin_level=1
python load-map-regions.py --file=$FINALPROJECT/maps/data/GHA_adm_shp/GHA_adm2.shp --country='ghana' --admin_level=2
python load-map-regions.py --file=$FINALPROJECT/maps/data/GHA_adm_shp/GHA_adm3.shp --country='ghana' --admin_level=3

# tanzania
python load-map-regions.py --file=$FINALPROJECT/maps/data/TZA_adm_shp/TZA_adm0.shp --country='tanzania' --admin_level=0
python load-map-regions.py --file=$FINALPROJECT/maps/data/TZA_adm_shp/TZA_adm1.shp --country='tanzania' --admin_level=1
python load-map-regions.py --file=$FINALPROJECT/maps/data/TZA_adm_shp/TZA_adm2.shp --country='tanzania' --admin_level=2
python load-map-regions.py --file=$FINALPROJECT/maps/data/TZA_adm_shp/TZA_adm3.shp --country='tanzania' --admin_level=3

# run
psql $DATABASE_URL --file=cleanup-map-regions.sql

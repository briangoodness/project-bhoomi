
# other methods tried for retrieving regions and 1km sq. cell predictions
# could not get any of the below methods to work properly-- ended up exporting directly to SHP file, then re-loading

# import django settings and models
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bhoomi.settings")
django.setup()
from maps.models import Cell_Prediction, DHS_cluster, Region

# using Django ORM
country='rwanda'
predictions_gdf = gpd.GeoDataFrame(list(Cell_Prediction.objects.all().filter(country=country).values()), crs=4326)
predictions_gdf.rename(columns={'geom':'geometry'}, inplace=True)
predictions_gdf['geometry'] = predictions_gdf['geometry'].apply(make_multipoly)
predictions_gdf.set_geometry('geom')

regions_gdf = gpd.GeoDataFrame(list(Region.objects.all().filter(country=country).values()), crs=4326)
regions_gdf.rename(columns={'geom':'geometry'}, inplace=True)
regions_gdf['geometry'] = regions_gdf['geometry'].apply(make_multipoly)
regions_gdf.set_geometry('geom')

# using GeoAlchemy2
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
Base = declarative_base()
class Region(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'maps_region'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)
    geom = Column(Geometry('POLYGON'))
query = session.query(Region).filter_by(country='ghana')
predictions_gdf = gpd.GeoDataFrame(list(query))

# using GeoPandas read_postgis() method
sql = "select * from maps_cell_prediction where country='ghana';"
predictions_gdf = gpd.read_postgis(conn, sql, geom_col='geom', crs=4326)

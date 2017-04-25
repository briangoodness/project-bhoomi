from django.shortcuts import render
import os

from djgeojson.views import GeoJSONLayerView
from .models import Region, DHS_cluster

# store country centers
max_zoom = 16
country_centers = {
    'ghana':{ 'longitude':-1.0232, 'latitude':7.9465, 'zoom_level':5.5, 'min_zoom':4 },
    'malawi':{ 'longitude':34.3015, 'latitude':-13.2543, 'zoom_level':5.5, 'min_zoom':4.5 },
    'rwanda':{ 'longitude':29.8739, 'latitude':-1.9403, 'zoom_level':7, 'min_zoom':6 },
    'tanzania':{ 'longitude':34.8888, 'latitude':-6.3690, 'zoom_level':5, 'min_zoom':3 },
}

# store country-specific Mapbox styles
country_styles = {
    'ghana':'mapbox://styles/briangoodness/cj1wia7ax00162smrphmw1pp9',
    'malawi':'mapbox://styles/briangoodness/cj1wia7ax00162smrphmw1pp9',
    'rwanda':'mapbox://styles/briangoodness/cj1wu823l00132roe3duzgxcc',
    'tanzania':'mapbox://styles/briangoodness/cj1wtzuzy001f2rozj7duibm4',
}

# Create your views here.

# classes DHS_ClusterLayer, RegionLayer to filter ResultSet based on country name
# source: http://geolio.com/weblog/2013/dec/12/passing-argument-django-geojson/
class DHS_ClusterLayer(GeoJSONLayerView):
    def get_queryset(self):
        country = self.request.GET.get('country')
        context = DHS_cluster.objects.all().filter(country=country)
        return context

class RegionLayer(GeoJSONLayerView):
    def get_queryset(self):
        country = self.request.GET.get('country')
        context = Region.objects.all().filter(country=country)
        return context

# return template for base map
def map(request, country='rwanda'):
    return render(request, 'map.html', {'token': os.environ['MAPBOX_TOKEN'],  # don't hardcode Mapbox API tokens
        'country':country,
        'center_lng':country_centers[country]['longitude'],
        'center_lat':country_centers[country]['latitude'],
        'zoom_level':country_centers[country]['zoom_level'],
        'min_zoom':country_centers[country]['min_zoom'],
        'max_zoom':max_zoom,
        'mapbox_style':country_styles[country]
        })

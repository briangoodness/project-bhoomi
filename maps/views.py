from django.shortcuts import render
import os

from djgeojson.views import GeoJSONLayerView
from .models import Cell_Prediction, DHS_cluster, Region

import csv
from django.http import HttpResponse

# store country centers
max_zoom = 16
country_centers = {
    'ghana':{ 'longitude':-1.0232, 'latitude':7.9465, 'zoom_level':5.5, 'min_zoom':4 },
    'malawi':{ 'longitude':34.3015, 'latitude':-13.2543, 'zoom_level':5.5, 'min_zoom':4.5 },
    'rwanda':{ 'longitude':29.8739, 'latitude':-1.9403, 'zoom_level':7, 'min_zoom':6 },
    'tanzania':{ 'longitude':34.8888, 'latitude':-6.3690, 'zoom_level':5, 'min_zoom':3 },
}
country_level_centers = {
    'ghana':{0:{ 'longitude':-1.0232, 'latitude':7.9465, 'zoom_level':5.5, 'min_zoom':4 },
        1:{ 'longitude':-1.0232, 'latitude':7.9465, 'zoom_level':5.5, 'min_zoom':4 },
        2:{ 'longitude':-1.0232, 'latitude':7.9465, 'zoom_level':5.5, 'min_zoom':4 },
        3:{ 'longitude':-1.0232, 'latitude':7.9465, 'zoom_level':5.5, 'min_zoom':4 },},
    'malawi':{0:{ 'longitude':34.3015, 'latitude':-13.2543, 'zoom_level':5.5, 'min_zoom':4.5 },
        1:{ 'longitude':34.3015, 'latitude':-13.2543, 'zoom_level':5.5, 'min_zoom':4.5 },
        2:{ 'longitude':34.3015, 'latitude':-13.2543, 'zoom_level':5.5, 'min_zoom':4.5 },
        3:{ 'longitude':34.3015, 'latitude':-13.2543, 'zoom_level':5.5, 'min_zoom':4.5 },},
    'rwanda':{0:{ 'longitude':29.8739, 'latitude':-1.9403, 'zoom_level':7, 'min_zoom':6 },
        1:{ 'longitude':29.8739, 'latitude':-1.9403, 'zoom_level':7, 'min_zoom':6 },
        2:{ 'longitude':29.8739, 'latitude':-1.9403, 'zoom_level':8, 'min_zoom':6 },
        3:{ 'longitude':29.8739, 'latitude':-1.9403, 'zoom_level':10, 'min_zoom':6 },},
    'tanzania':{0:{ 'longitude':34.8888, 'latitude':-6.3690, 'zoom_level':5, 'min_zoom':3 },
        1:{ 'longitude':34.8888, 'latitude':-6.3690, 'zoom_level':5, 'min_zoom':3 },
        2:{ 'longitude':34.8888, 'latitude':-6.3690, 'zoom_level':5, 'min_zoom':3 },
        3:{ 'longitude':34.8888, 'latitude':-6.3690, 'zoom_level':5, 'min_zoom':3 },},
}

# store country-specific Mapbox styles
country_styles = {
    'ghana':'mapbox://styles/briangoodness/cj1wia7ax00162smrphmw1pp9',
    'malawi':'mapbox://styles/briangoodness/cj1wia7ax00162smrphmw1pp9',
    'rwanda':'mapbox://styles/briangoodness/cj1wu823l00132roe3duzgxcc',
    'tanzania':'mapbox://styles/briangoodness/cj1wtzuzy001f2rozj7duibm4',
}
country_level_styles = {
    'ghana':{0:'mapbox://styles/briangoodness/cj1wia7ax00162smrphmw1pp9',
        1:'mapbox://styles/briangoodness/cj1wia7ax00162smrphmw1pp9',
        2:'mapbox://styles/briangoodness/cj1wia7ax00162smrphmw1pp9',
        3:'mapbox://styles/briangoodness/cj1wia7ax00162smrphmw1pp9',},
    'malawi':{0:'mapbox://styles/briangoodness/cj1wia7ax00162smrphmw1pp9',
        1:'mapbox://styles/briangoodness/cj1wia7ax00162smrphmw1pp9',
        2:'mapbox://styles/briangoodness/cj1wia7ax00162smrphmw1pp9',
        3:'mapbox://styles/briangoodness/cj1wia7ax00162smrphmw1pp9',},
    'rwanda':{0:'mapbox://styles/briangoodness/cj1wu823l00132roe3duzgxcc',
        1:'mapbox://styles/briangoodness/cj1wu823l00132roe3duzgxcc',
        2:'mapbox://styles/briangoodness/cj2fcsunk00432sqm7kbqlg6t',
        3:'mapbox://styles/briangoodness/cj2f93z0y003y2rukcbtc6kbt',},
    'tanzania':{0:'mapbox://styles/briangoodness/cj1wtzuzy001f2rozj7duibm4',
        1:'mapbox://styles/briangoodness/cj1wtzuzy001f2rozj7duibm4',
        2:'mapbox://styles/briangoodness/cj1wtzuzy001f2rozj7duibm4',
        3:'mapbox://styles/briangoodness/cj1wtzuzy001f2rozj7duibm4',},
}

# Create your views here.

# classes Cell_PredictionLayer, DHS_ClusterLayer, RegionLayer to filter ResultSet based on country name
# source: http://geolio.com/weblog/2013/dec/12/passing-argument-django-geojson/
class Cell_PredictionLayer(GeoJSONLayerView):
    def get_queryset(self):
        country = self.request.GET.get('country')
        context = Cell_Prediction.objects.all().filter(country=country)
        return context

class DHS_ClusterLayer(GeoJSONLayerView):
    def get_queryset(self):
        country = self.request.GET.get('country')
        context = DHS_cluster.objects.all().filter(country=country)
        return context

class RegionLayer(GeoJSONLayerView):
    def get_queryset(self):
        country = self.request.GET.get('country')
        admin_level = self.request.GET.get('admin_level')
        context = Region.objects.all().filter(country=country, admin_level=admin_level)
        return context

# return about page
def about(request):
    return render(request, 'about.html')

# return template for base map
def map(request, country='rwanda', admin_level=1):
    admin_level = int(admin_level)
    return render(request, 'map.html', {'token': os.environ['MAPBOX_TOKEN'],  # don't hardcode Mapbox API tokens
        'country':country,
        'admin_level':admin_level,
        'center_lng':country_level_centers[country][admin_level]['longitude'],
        'center_lat':country_level_centers[country][admin_level]['latitude'],
        'zoom_level':country_level_centers[country][admin_level]['zoom_level'],
        'min_zoom':country_level_centers[country][admin_level]['min_zoom'],
        'max_zoom':max_zoom,
        'mapbox_style':country_level_styles[country][admin_level]
        })

def download(request, country='rwanda', admin_level=1):

    admin_level = int(admin_level) # cast string to int from URL text

    #checking whether the user selected only a few regions.
    selected_regions = request.GET.get('selected_regions', '')
    print('regions: ' + selected_regions)

    #if we need to filter the regions for download:
    if selected_regions == '':
        context = Region.objects.values_list('country', 'name', 'predicted_wealth_idx', 'wealth_decile', 'admin_level').filter(country=country, admin_level=admin_level)
    else:
        selected_regions = selected_regions.split(',')
        context = Region.objects.values_list('country', 'name', 'predicted_wealth_idx', 'wealth_decile', 'admin_level').filter(country=country, admin_level=admin_level, name__in=selected_regions)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data-'+country+'-admin_level-'+str(admin_level)+'.csv"'

    writer = csv.writer(response)
    writer.writerow(['Country', 'Name', 'Predicted wealth index', 'Wealth decile', 'Admin level'])
    for row in context:
        writer.writerow([row[0].title(), row[1], row[2], row[3], row[4]])

    return response

# return index page
def index(request):
    return render(request, 'index.html')

from django.shortcuts import render
import os

# store country centers
max_zoom = 16
country_centers = {
    'ghana':{ 'longitude':-1.0232, 'latitude':7.9465, 'zoom_level':5.5, 'min_zoom':4 },
    'malawi':{ 'longitude':34.3015, 'latitude':-13.2543, 'zoom_level':5.5, 'min_zoom':4.5 },
    'rwanda':{ 'longitude':29.8739, 'latitude':-1.9403, 'zoom_level':7, 'min_zoom':6 },
    'tanzania':{ 'longitude':34.8888, 'latitude':-6.3690, 'zoom_level':5, 'min_zoom':3 },
}

# Create your views here.
def map(request, country='rwanda'):
    return render(request, 'map.html', {'token': os.environ['MAPBOX_TOKEN'],  # don't hardcore Mapbox API tokens
        'center_lng':country_centers[country]['longitude'],
        'center_lat':country_centers[country]['latitude'],
        'zoom_level':country_centers[country]['zoom_level'],
        'min_zoom':country_centers[country]['min_zoom'],
        'max_zoom':max_zoom})

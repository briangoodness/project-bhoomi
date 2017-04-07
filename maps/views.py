from django.shortcuts import render
import os

# Create your views here.
def map(request):
    return render(request, 'map.html', {'token': os.environ['MAPBOX_TOKEN']}) # don't hardcore Mapbox API tokens

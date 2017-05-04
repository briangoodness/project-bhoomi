"""bhoomi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from djgeojson.views import GeoJSONLayerView

from maps import views as maps_views
from maps.models import Region, DHS_cluster

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', maps_views.index, name='home'),
    url(r'^about$', maps_views.about, name='about'),
    url(r'^(?P<country>[a-z]+)$', maps_views.map, name='map'),
    url(r'^dhs-data.geojson?.*$', maps_views.DHS_ClusterLayer.as_view(model=DHS_cluster, properties=('country','data_year','dhs_wealth_idx','latitude','longitude')), name='dhs-clusters-data-country'),
    url(r'^dhs-data$', GeoJSONLayerView.as_view(model=DHS_cluster, properties=('country','data_year','dhs_wealth_idx','latitude','longitude')), name='dhs-clusters-data'),
    url(r'^regions-data.geojson?.*$', maps_views.RegionLayer.as_view(model=Region, properties=('country','name','predicted_wealth_idx','wealth_decile','admin_level')), name='regions-predictions-data-country'),
    url(r'^regions-data/$', GeoJSONLayerView.as_view(model=Region, properties=('country','name','predicted_wealth_idx','wealth_decile','admin_level')), name='regions-predictions-data'),
    url(r'^download/(?P<country>[a-z]+)/(?P<admin_level>[1-9]+)$', maps_views.download, name='download'),
]

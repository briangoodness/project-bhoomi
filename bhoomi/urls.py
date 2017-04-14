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
    url(r'^(?P<country>[a-z]+)$', maps_views.map, name='map'),
    url(r'^dhs-data/$', GeoJSONLayerView.as_view(model=DHS_cluster, properties=('dhs_wealth_idx','latitude','longitude')), name='dhs-clusters-data'),
]

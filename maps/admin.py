from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Region, DHS_cluster

# Register your models here.
admin.site.register(Region, LeafletGeoAdmin)
admin.site.register(DHS_cluster, LeafletGeoAdmin)

#from django.contrib import admin
from django.contrib.gis import admin
#from leaflet.admin import LeafletGeoAdmin # throwing error
from .models import Region, DHS_cluster

# Add Models
class RegionAdmin(admin.ModelAdmin):
    fieldsets = (None, {'fields':('name', 'predicted_wealth_idx', 'wealth_decile', 'boundary')})

# Register your models here.
admin.site.register(Region, admin.GeoModelAdmin)
admin.site.register(DHS_cluster, admin.GeoModelAdmin)

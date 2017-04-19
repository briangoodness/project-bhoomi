#from django.db import models
from django.contrib.gis.db import models

# Create your models here.
class Region(models.Model):
    #id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    predicted_wealth_idx = models.DecimalField(max_digits=15, decimal_places=10)
    wealth_decile = models.IntegerField(null=True)
    geom = models.PolygonField(null=True) # add polygon / BoundaryBox

class DHS_cluster(models.Model):
    #id = models.BigIntegerField(primary_key=True)
    #name = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    data_year = models.CharField(max_length=255, null=True)
    dhs_wealth_idx = models.DecimalField(max_digits=15, decimal_places=10)
    latitude = models.DecimalField(max_digits=15, decimal_places=10, null=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=10, null=True)
    geom = models.PointField(null=True)

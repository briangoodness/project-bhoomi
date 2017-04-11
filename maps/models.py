#from django.db import models
from django.contrib.gis.db import models

# Create your models here.
class Region(models.Model):
    #id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    predicted_wealth_idx = models.DecimalField(max_digits=15, decimal_places=10)
    wealth_decile = models.IntegerField()
    # add polygon / BoundaryBox

class DHS_cluster(models.Model):
    #id = models.BigIntegerField(primary_key=True)
    #name = models.CharField(max_length=255, null=True)
    dhs_wealth_idx = models.DecimalField(max_digits=15, decimal_places=10)
    latitude = models.DecimalField(max_digits=15, decimal_places=10)
    longitude = models.DecimalField(max_digits=15, decimal_places=10)
    geom = models.PointField(null=True)

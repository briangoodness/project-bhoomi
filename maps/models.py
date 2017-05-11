#from django.db import models
from django.contrib.gis.db import models

# Create your models here.
class Cell_Prediction(models.Model):
    #id = models.BigIntegerField(primary_key=True)
    country = models.CharField(max_length=255, null=True)
    i = models.IntegerField(null=True)
    j = models.IntegerField(null=True)
    predicted_wealth_idx = models.DecimalField(max_digits=15, decimal_places=10)
    geom = models.PolygonField(null=True) # add Polygon (change to MultiPolygon?)

class Region(models.Model):
    #id = models.BigIntegerField(primary_key=True)
    country = models.CharField(max_length=255, null=True)
    admin_level = models.IntegerField(null=True)
    name = models.CharField(max_length=255, null=True)
    predicted_wealth_idx = models.DecimalField(max_digits=15, decimal_places=10) # remove later
    wealth_decile = models.IntegerField(null=True) # remove later
    geom = models.MultiPolygonField(null=True) # add MultiPolygon

class Region_Prediction(models.Model):
    #id = models.BigIntegerField(primary_key=True)
    country = models.CharField(max_length=255, null=True)
    admin_level = models.IntegerField(null=True)
    name = models.CharField(max_length=255, null=True)
    predicted_wealth_idx = models.DecimalField(max_digits=15, decimal_places=10)
    wealth_decile = models.IntegerField(null=True)
    geom = models.MultiPolygonField(null=True) # add MultiPolygon

class DHS_cluster(models.Model):
    #id = models.BigIntegerField(primary_key=True)
    #name = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    data_year = models.CharField(max_length=255, null=True)
    dhs_wealth_idx = models.DecimalField(max_digits=15, decimal_places=10)
    latitude = models.DecimalField(max_digits=15, decimal_places=10, null=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=10, null=True)
    geom = models.PointField(null=True)

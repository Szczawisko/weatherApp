from django.db import models

class Location(models.Model):
    city_name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    region = models.CharField(max_length=200,null=True,blank=True)
    longitude = models.FloatField()
    latitude = models.FloatField()


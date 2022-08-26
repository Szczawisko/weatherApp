from django.db import models

class Location(models.Model):
    city_name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    region = models.CharField(max_length=200,null=True,blank=True)
    longitude = models.FloatField()
    latitude = models.FloatField()

class Weather(models.Model):
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    date = models.DateField()
    temperature  = models.FloatField()
    pressure = models.IntegerField()
    humidity = models.IntegerField()
    wind_speed = models.FloatField()
    wind_direction = models.IntegerField()



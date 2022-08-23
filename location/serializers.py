from dataclasses import field
from pyexpat import model
from rest_framework import serializers

from .models import Location


class LocationSerializers(serializers.ModelSerializer):

    def validate_longitude(self,longitude):
        if longitude < -180 or longitude > 180:
            raise serializers.ValidationError("Longitude is in invalid range") 
        return longitude

    def validate_latitude(self,latitude):
        if latitude < -90 or latitude > 90:
            raise serializers.ValidationError("Latitude is in invalid range") 
        return latitude

    class Meta:
        model = Location
        fields=["id","city_name","country","region","longitude","latitude"]
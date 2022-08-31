from dataclasses import field, fields
from pyexpat import model
from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import Location, Weather


class LocationSerializer(serializers.ModelSerializer):

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

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields=["location","date","temperature","pressure","humidity","wind_speed","wind_direction"]

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    class Meta:
        model = User
        fields = ["username","password"]
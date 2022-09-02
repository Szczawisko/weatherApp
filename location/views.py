from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from datetime import datetime, timedelta

#from .models import Location, Weather
from .serializers import LocationSerializer, WeatherSerializer
from .menager import LocationMenager, WeatherMenager
from user.permission import IsAdminUserOrReadOnly

class LocationListApiView(APIView):

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUserOrReadOnly]

    def get(self,request,*args, **kwargs):
        locations = LocationMenager.get_locations()
        serializer = LocationSerializer(locations,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args, **kwargs):
        data = {
            'city_name':request.data.get('city_name'),
            'country':request.data.get('country'),
            'region':request.data.get('region'),
            'longitude':request.data.get('longitude'),
            'latitude':request.data.get('latitude'),
        }
        serializer = LocationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class WeatherListApiView(APIView):

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,id,*args, **kwargs):
        location = LocationMenager.get_location(id)
        if not location:
            return Response({"res": "Object with entrie id does not exist"}, status=status.HTTP_404_NOT_FOUND)

        date = request.query_params.get('date')
      
        if not date:
            date = (datetime.now().date() + timedelta(days=1)).isoformat()
        else:
            try:
                if datetime.fromisoformat(date).date() > datetime.now().date() + timedelta(days=5):
                    return Response({"res":"the date can be 5 days ahead"},status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({"res":"date must be in ISO format"},status=status.HTTP_400_BAD_REQUEST)

        weather = WeatherMenager.get_weather_from_db(location,date)

        if not weather:
            weather = WeatherMenager.get_weather_from_api(location,date)
            serializer = WeatherSerializer(data=weather)
            if not serializer.is_valid():
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
        else:
            serializer = WeatherSerializer(weather)

        return Response(serializer.data,status=status.HTTP_200_OK)




    

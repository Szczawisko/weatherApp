import requests
from datetime import datetime

from .models import Location, Weather
import credensial


class LocationMenager():
    @staticmethod
    def get_locations():
        return Location.objects.all()

    @staticmethod
    def get_location(id):
        try:
            return Location.objects.get(id=id)
        except Location.DoesNotExist:
            return None

class WeatherMenager():
    @staticmethod
    def is_publish_date_actual(weather):
        difference = datetime.now() - weather.pub_date.replace(tzinfo=None)
        if divmod(difference.total_seconds(),86400)[0] >=1:
            return False

        return True


    @staticmethod
    def get_weather_from_db(location,date):
        try:
            weather = Weather.objects.get(location=location,date=date)
            if WeatherMenager.is_publish_date_actual(weather):
                return weather

            weather.delete()
            return None 

        except Weather.DoesNotExist:
            return None

    @staticmethod
    def get_weather_from_api(location,date):
        url = f'http://api.openweathermap.org/data/2.5/forecast?lat={location.latitude}&lon={location.longitude}&units=metric&appid={credensial.open_weather_api}'
        request = requests.get(url)
        json = request.json()

        try:
            date = datetime.fromisoformat(date).date()
        except ValueError:
            raise ValueError("date is not in ISO format")

        date_to_find = datetime(date.year,date.month,date.day,12)
        date_now = datetime.fromisoformat(json['list'][0]['dt_txt'])
        difference = date_to_find-date_now
        index = int(divmod(difference.total_seconds(),3600)[0]/3)

        if index>=40:
            index = 39 
        elif index < 0:
            index = 0

        weather = json['list'][index]

        data = {
            "location": location.id,
            "date": date.isoformat(),
            "temperature": weather['main']['temp'],
            "pressure": weather['main']['pressure'],
            "humidity": weather['main']['humidity'],
            "wind_speed": weather['wind']['speed'],
            "wind_direction": weather['wind']['deg'],
        }

        return data
from django.urls import path

from . import views

urlpatterns = [
    path('',views.LocationListApiView.as_view()),
    path('/<int:id>/forecast',views.WeatherListApiView.as_view()),
    path('/user',views.UserRegister.as_view()),
]

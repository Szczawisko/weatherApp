from django.urls import path

from . import views

urlpatterns = [
    path('',views.UserListApiView.as_view()),
    path('/<int:id>/permissions',views.UserPermissions.as_view()),
    path('/login',views.UserLogin.as_view())
]

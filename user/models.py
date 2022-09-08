from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    TYPE_USER_CHOICE = (
        ('User','User'),
        ('Coordinator','Coordinator')
    )
    type_user = models.CharField(max_length=12,choices=TYPE_USER_CHOICE,default='User')


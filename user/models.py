from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    TYPE_USER_CHOICE = (
        ('U','User'),
        ('C','Coordinator')
    )
    type_user = models.CharField(max_length=1,choices=TYPE_USER_CHOICE,default='U')


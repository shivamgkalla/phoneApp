from django.db import models

 #Create your models here.
class RegisteredUser(models.Model):
    username = models.CharField(max_length=200, default="", blank=False)
    phone_no = models.PositiveIntegerField(unique=True, blank=False)
    email = models.EmailField(max_length=100, blank=True, default="")
    password = models.CharField(max_length=200, blank=False)
    spam = models.PositiveIntegerField(default=0)

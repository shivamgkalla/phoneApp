from django.db import models
from django.core.validators import MaxValueValidator

#class GlobalUser(models.Model):
#    username = models.CharField(max_length=200, default="", blank=False)
#    phone_no = models.PositiveIntegerField(unique=True, blank=False)
#    email = models.EmailField(max_length=100, blank=True, default="")
#    password = models.CharField(max_length=200, blank=False)
#    spam = models.PositiveIntegerField(default=0)

# Model for Registering the user

class RegisteredUser(models.Model):
    username = models.CharField(max_length=200, default="", blank=False)
    phone_no = models.PositiveIntegerField(validators=[MaxValueValidator(99999999)], unique=True, blank=False)
    email = models.EmailField(max_length=100, blank=True, default="")
    password = models.CharField(max_length=200, blank=False)
    spam = models.PositiveIntegerField(default=0)

# Model for Contacts of the Registered User

class Contacts(models.Model):
    username = models.CharField(max_length=200, default="", blank=False)
    phone_no = models.PositiveIntegerField(validators=[MaxValueValidator(99999999)], blank=False)
    user = models.ForeignKey(to=RegisteredUser, on_delete=models.CASCADE)
    spam = models.PositiveIntegerField(default=0)

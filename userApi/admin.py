from django.contrib import admin
from .models import RegisteredUser, Contacts

# Register your models here.

admin.site.register(RegisteredUser)
admin.site.register(Contacts)
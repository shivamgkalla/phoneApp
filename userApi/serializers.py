from rest_framework import serializers
from .models import  Contacts
from django.contrib.auth.models import User
from .models import RegisteredUser

# Serializer for Registered User

class RegisteredUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredUser
        fields = "__all__"

#class RegisteredUserSerializer(serializers.ModelSerializer):
#
#    class Meta:
#        model = User
#        fields = ('name', 'phone_number', 'email', 'password')
#
#        extra_kwargs = {
#            'name': { 'required': True, "allow_blank": False },
#            'phone_number': { 'required': True, "allow_blank": False },
#            'email': { 'required': False, "allow_blank": True },
#            'password': { 'required': True, "allow_blank": False, "min_length": 8 },
#        }

# Serializer for User Contacts

class ContactsSerializer:
    class Meta:
        model = Contacts
        fields = "__all__"


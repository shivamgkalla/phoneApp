from rest_framework import serializers
from userApi.models import RegisteredUser, Contacts

# Serializer for Registered User


class RegisteredUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredUser
        fields = ('username', 'phone_no', 'spam', 'email','id')

class RegisteredUserSerializerView(serializers.ModelSerializer):
    class Meta:
        model = RegisteredUser
        fields = ('username', 'phone_no', 'spam')

class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ('username', 'phone_no', 'spam','user_id')
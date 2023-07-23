from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import RegisteredUserSerializer
from rest_framework.response import Response
from .models import RegisteredUser, Contacts
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.exceptions import AuthenticationFailed
from searchApi.filters import SearchPhoneFilter
import jwt
import datetime
from userApi.auth import AuthMiddleware
from rest_framework.decorators import api_view, authentication_classes

# Create your views here.


@api_view(['POST'])
def register_user(request):
    data = request.data

    input_payload = RegisteredUserSerializer(data=data)

    if input_payload.is_valid():

        if not RegisteredUser.objects.filter(phone_no=data['phone_no']).exists():
            input_payload = RegisteredUser.objects.create(
                username=data['username'],
                phone_no=data['phone_no'],
                email=data['email'],
                password=make_password(data['password']),
            )
            return Response({'message': 'User registered successfully with phone number ' + data['phone_no']}, status=status.HTTP_201_CREATED)

        else:
            return Response({'error': 'User already exists. Please register with a different phone number'}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(input_payload.errors)


@api_view(['POST'])
def login_user(request):
    phone_no = request.data['phone_no']
    password = request.data['password']

    data = {"phone_no": phone_no}
    filterset = SearchPhoneFilter(data, queryset=RegisteredUser.objects.all())
    serializer = RegisteredUserSerializer(filterset.qs, many=True)

    if len(serializer.data) == 0:
        raise AuthenticationFailed("Invalid Credentials. User not found")

    if not check_password(password, serializer.data[0]['password']):
        raise AuthenticationFailed("Invalid Credentials. Incorrect Pasaword")

    payload = {
        'phone_no': phone_no,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    }

    jwtToken = jwt.encode(payload, 'secret', algorithm='HS256')

    return Response({'message': 'Logged in successfully', 'jwtToken': jwtToken}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([AuthMiddleware])
def mark_spam(request):
    phone_no = request.data['phone_no']
    allUsers = RegisteredUser.objects.filter(phone_no=phone_no)

    allUsers2 = Contacts.objects.filter(phone_no=phone_no)

    if len(allUsers) == 0 & len(allUsers2) == 0:
        raise AuthenticationFailed(
            "Sorry. No user with the given phone number found")
    try:
        for user in allUsers:
            user.spam += 1
            user.save()

        for user2 in allUsers2:
            user2.spam += 1
            user2.save()
    except:
        raise AuthenticationFailed("No user with the given phone number found")

    return Response({'message': 'Phone number marked as spam successfully'}, status=status.HTTP_200_OK)

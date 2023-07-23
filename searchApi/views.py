from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes
from .serializers import RegisteredUserSerializer, ContactsSerializer, RegisteredUserSerializerView
from rest_framework.response import Response
from userApi.models import RegisteredUser, Contacts
from rest_framework import status
from .filters import SearchUsernameFilter, SearchPhoneFilter
from rest_framework.permissions import IsAuthenticated
from userApi.auth import AuthMiddleware

# API to search Contacts based on Username

@api_view(['GET'])
@authentication_classes([AuthMiddleware])
def search_by_username(request, pk):
    print('Inside Search By Username Handler....')
    logged_in_user = request.data['logged_in_phone_no']
    if pk == "":
        return Response({'error': 'User name cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

    else:

        # database query to get all registered users which contain or start with incoming name
        data = {"username": pk}
        filterset = SearchUsernameFilter(data, queryset=RegisteredUser.objects.all())
        serializer = RegisteredUserSerializer(filterset.qs, many=True)
        count = filterset.qs.count()

        # Database query to check looged_in_user is in which registered users contacts
        filterset = SearchPhoneFilter({"phone_no": logged_in_user}, queryset=Contacts.objects.all())
        serializer2 = ContactsSerializer(filterset.qs, many=True)
        
        #logic to only render email in response when the looged_in_user is in registered users contacts
        for regUser in serializer.data:
            flag = False 
            for user in serializer2.data:
              if regUser['id'] == user['user_id']:
                flag = True 
                break
            if flag == False: 
             del regUser['email']
             break
     
        # database query to get users with incoming name from Personal Contacts
        filterset = SearchUsernameFilter(data, queryset=Contacts.objects.all())
        serializer2 = ContactsSerializer(filterset.qs, many=True)
        count2 = filterset.qs.count()

        totalCount = count + count2

        if totalCount == 0:
            return Response({'message': 'Details with given username does not exists'}, status=status.HTTP_204_NO_CONTENT)
        return Response({
            "count": totalCount,
            "Registered User": serializer.data,
            "Contacts": serializer2.data}, status=status.HTTP_200_OK)


# API to search Contacs by Phone Number

@api_view(['GET'])
@authentication_classes([AuthMiddleware])
def search_by_phone(request, pk):
    logged_in_user = request.data['logged_in_phone_no']
    print('Inside Search By Phone number Handler....')
    if pk == "":
        return Response({'error': 'Phone number cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

    else:
        data = {"phone_no": pk}

        # database query to get all registered users which contain or start with incoming phone number
        filterset = SearchPhoneFilter(data, queryset=RegisteredUser.objects.all())
        serializer = RegisteredUserSerializer(filterset.qs, many=True)
        count = filterset.qs.count()
        if count != 0: 
            # Database query to check looged_in_user is in which registered user's contacts
            filterset = SearchPhoneFilter({"phone_no": logged_in_user}, queryset=Contacts.objects.all())
            serializer2 = ContactsSerializer(filterset.qs, many=True)

             #logic to only render email in response when the looged_in_user is in registered users contacts
            for user in serializer2.data:
                 if user['user_id'] == serializer.data[0]['id']:
                     return Response({
                     "count": count,
                     "registered users": serializer.data}, status=status.HTTP_200_OK)
        
        # database query to get users with incoming phone number from Personal Contacts
        filterset = SearchPhoneFilter(data, queryset=RegisteredUser.objects.all())
        view_serializer = RegisteredUserSerializerView(filterset.qs, many=True)
        count = filterset.qs.count()
        if count != 0:
            return Response({
                "count": count,
                "registered users": view_serializer.data}, status=status.HTTP_200_OK)
        else:
            data = {"phone_no": pk}
            filterset = SearchPhoneFilter(
                data, queryset=Contacts.objects.all())
            serializer2 = ContactsSerializer(filterset.qs, many=True)
            count2 = filterset.qs.count()

            if count2 != 0:
                return Response({
                    "count": count2,
                    "contacts": serializer2.data}, status=status.HTTP_200_OK)

        return Response({'message': 'Details with given phone number does not exists'}, status=status.HTTP_204_NO_CONTENT)


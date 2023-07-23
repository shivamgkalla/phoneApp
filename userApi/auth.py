from rest_framework.exceptions import AuthenticationFailed
import jwt
from .serializers import RegisteredUserSerializer
from .models import RegisteredUser
from searchApi.filters import SearchPhoneFilter


class AuthMiddleware:

    def authenticate(self, request):
        print('Inside Middleware')
        token = request.META.get('HTTP_AUTHORIZATION', b'')
        if token == "":
            raise AuthenticationFailed(
                "Invalid Credentials. Token coming as empty")
        jwtToken = token.split()
        if len(jwtToken) == 0:
            raise AuthenticationFailed(
                "Invalid Credentials. Token coming as empty")

        if len(jwtToken) > 2 | len(jwtToken) < 2:
            raise AuthenticationFailed("Invalid Credentials. Token not proper")
        try:
            payload = jwt.decode(jwtToken[1], 'secret' , algorithms='HS256')
        except:
            raise AuthenticationFailed("Session expired. Please login again")

        data = {"phone_no": payload['phone_no']}
        filterset = SearchPhoneFilter(data, queryset=RegisteredUser.objects.all())
        serializer = RegisteredUserSerializer(filterset.qs, many=True)
        if len(serializer.data) == 0:
            raise AuthenticationFailed("Invalid Credentials.")
        pass

    def authenticate_header(self, request):
        return

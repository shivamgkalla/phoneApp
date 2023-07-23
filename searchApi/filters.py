from django_filters import rest_framework as filters
from userApi.models import RegisteredUser




class SearchUsernameFilter(filters.FilterSet):
    username = filters.CharFilter(field_name="username", lookup_expr="istartswith")
    username = filters.CharFilter(field_name="username", lookup_expr="icontains")
    class Meta:
        model = RegisteredUser
        fields = ['username']

class SearchPhoneFilter(filters.FilterSet):

    phone_no = filters.CharFilter(field_name="phone_no", lookup_expr="iexact")

    class Meta:
        model = RegisteredUser
        fields = ['phone_no']


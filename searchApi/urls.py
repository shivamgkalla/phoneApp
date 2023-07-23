from django.urls import path
from . import views

urlpatterns = [
    path('searchByName/<str:pk>/', views.search_by_username, name="search_by_username"),
    path('searchByPhone/<int:pk>/', views.search_by_phone, name="search_by_phone"),
]
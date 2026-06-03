from django.urls import path
from .views import api_services

urlpatterns = [
    path("api/services/", api_services, name="api_services"),
]

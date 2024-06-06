"""
URL configuration for project.

"""
from django.urls import path, include

urlpatterns = [
    path('api/', include('authentication.urls')),
]

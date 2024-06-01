"""
URL configuration for project.

"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.default, name='default'),
]

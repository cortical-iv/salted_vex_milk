"""URL patterns for clanhole app
"""
from django.urls import path

from . import views

app_name = 'characters'
urlpatterns = [
        #Page to show all of a user's characters
        path('<str:name>/', views.characters, name = 'characters'),
        ]


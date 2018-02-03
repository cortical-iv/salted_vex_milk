"""URL patterns for clanhole app
"""
from django.urls import path

from . import views

app_name = 'pvpstats'
urlpatterns = [
        #Page to show all of a user's characters
        path('<str:stat>/', views.pvpstats, name = 'pvpstats'),
        path('members/<str:name>/', views.memberpvp, name = 'memberpvp')
        ]

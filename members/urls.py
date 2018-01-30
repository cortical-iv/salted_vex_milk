"""URL patterns for clanhole app
"""
from django.urls import path

from . import views

app_name = 'members'
urlpatterns = [
        #Home page
        path('', views.members, name = 'members'),  #name needed for namespace resolution in template {% url 'members:members' %}
        ]
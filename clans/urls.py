"""URL patterns for clanhole app
"""
from django.urls import path

from . import views

app_name = 'clans'
urlpatterns = [
        #Home page
        path('', views.index, name = 'index'),
        path('about/', views.about, name = 'about'),
        ]
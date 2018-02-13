"""URL patterns for clanhole app
"""
from django.urls import path

from . import views

app_name = 'pvestats'
urlpatterns = [
        #Page to show user's pve stats
        path('<str:stat>/', views.pvestats, name = 'pvestats'),
        #Redirect to main landing page when they do not specify a stat
        path('', views.pve_redirect, name = 'pve_redirect')
        ]

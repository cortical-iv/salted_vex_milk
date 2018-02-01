#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 22:56:36 2017

@author: eric
"""
from django import forms
from .models import PvpStats

class PvpStatsForm(forms.ModelForm):
    class Meta:
        model = PvpStats
        fields =  ['member',  'number_matches', 'seconds_played', 'kd', 'favorite_weapon', 'longest_spree', 'most_kills']



#    member = models.OneToOneField(Member, on_delete = models.CASCADE)
#    updated = models.DateTimeField(auto_now=True)
#    seconds_played =  models.IntegerField()
#    kd = models.FloatField()
#    favorite_weapon = models.CharField(max_length = 20)
#    longest_spree = models.IntegerField()
#    most_kills = models.IntegerField()
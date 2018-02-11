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
        fields =  ['member',  'number_matches', 'greatness', 'seconds_played', 'kd', 'favorite_weapon',
                   'longest_spree', 'most_kills', 'number_wins', 'win_loss_ratio',
                   'longest_kill', 'suicides_pga', 'kills_pga', 'deaths_pga',
                   'trials_number_matches', 'trials_kd', 'trials_win_loss_ratio']




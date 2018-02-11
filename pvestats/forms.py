#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 22:56:36 2017

@author: eric
"""
from django import forms
from .models import PveStats

class PveStatsForm(forms.ModelForm):
    class Meta:
        model = PveStats
        fields  = ['member', 'greatness', 'number_story_missions', 'number_strikes', 'number_nightfalls', 'number_raid_clears',
                   'seconds_played', 'longest_single_life', 'average_life', 'kills_pga', 'deaths_pga', 'kd', 'longest_spree',
                   'most_precision_kills', 'precision_kills_pga', 'longest_kill', 'favorite_weapon', 'suicides_pga', 'suicides',
                   'assists_pga', 'resurrections_received_pga', 'resurrections_performed_pga', 'orbs_dropped_pga', 'orbs_gathered_pga']




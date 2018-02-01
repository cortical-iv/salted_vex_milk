#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 14:35:32 2018

@author: eric
"""

import django_tables2 as tables
from .models import PvpStats

class PvpStatsTable(tables.Table):
#    name = tables.LinkColumn('characters:characters', kwargs = {"name": tables.A('name')})
    number_matches = tables.Column(verbose_name = '#Matches', attrs= {"td": {"align":"center"} })
    kd = tables.Column(verbose_name = 'K/D')
    most_kills = tables.Column(verbose_name = 'Max Kills', attrs= {"td": {"align":"center"} })
    longest_spree = tables.Column(verbose_name = 'Max Spree', attrs= {"td": {"align":"center"} })
#    date_last_played = tables.DateTimeColumn(verbose_name = 'Last Played', format ='M d Y')
#    minutes_played = tables.Column(attrs= {"td": {"align":"center"}})
    class Meta:
        model = PvpStats
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-striped table-hover table-sm table-responsive'}  #note table-bordered makes things really slow
        fields =  ['member', 'number_matches', 'kd', 'longest_spree', 'most_kills']

class KdTable(tables.Table):
    number_matches = tables.Column(verbose_name = '#Matches', attrs= {"td": {"align":"center"} })
    kd = tables.Column(verbose_name = 'K/D')
    class Meta:
        model = PvpStats
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-striped table-hover table-sm table-responsive'}
        fields =  ['member', 'number_matches', 'kd']

 #has_played_d2 = tables.BooleanColumn(attrs= {"td": {"align":"center"} }, verbose_name = 'Played D2')


#     member = models.OneToOneField(Member, on_delete = models.CASCADE)
#    updated = models.DateTimeField(auto_now=True)
#    seconds_played =  models.IntegerField()
#    kd = models.FloatField()
#    favorite_weapon = models.CharField(max_length = 20)
#    longest_spree = models.IntegerField()
#    most_kills = models.IntegerField()
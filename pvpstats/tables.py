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
    longest_spree = tables.Column(verbose_name = 'Spree', attrs= {"td": {"align":"center"} })
    favorite_weapon = tables.Column(verbose_name = 'Favorite',  attrs= {"td": {"align":"center"} })
    seconds_played = tables.Column(verbose_name = 'Time Played', attrs= {"td": {"align":"center"} })
    longest_kill = tables.Column(verbose_name = "Kill Distance", attrs= {"td": {"align":"center"} })
    number_wins = tables.Column(verbose_name = '#Wins', attrs= {"td": {"align":"center"} })
    win_loss_ratio = tables.Column(verbose_name = 'W/L Ratio', attrs= {"td": {"align":"center"} })
    kills_per_match = tables.Column(verbose_name = 'Kills/match', attrs= {"td": {"align":"center"} })
    deaths_per_match = tables.Column(verbose_name = 'Deaths/match', attrs= {"td": {"align":"center"} })
    suicides = tables.Column(verbose_name = "Misadventures", attrs= {"td": {"align":"center"} })
    greatness = tables.Column(attrs= {"td": {"align":"center"} })
#    date_last_played = tables.DateTimeColumn(verbose_name = 'Last Played', format ='M d Y')
#    minutes_played = tables.Column(attrs= {"td": {"align":"center"}})
    class Meta:
        model = PvpStats
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-striped table-hover table-sm table-responsive text-nowrap'}  #note table-bordered makes things really slow
        fields =  ['member', 'number_matches', 'greatness', 'seconds_played', 'number_wins', 'win_loss_ratio',
                   'kills_per_match', 'deaths_per_match', 'kd', 'suicides', 'longest_spree',
                   'most_kills', 'favorite_weapon', 'longest_kill']



class MemberPvpTable(tables.Table):
    stat = tables.Column(verbose_name = 'Stat')
    value = tables.Column(verbose_name = 'Value')

    class Meta:
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-striped table-hover table-sm table-bordered table-responsive'}  #note table-bordered makes things really slow











#            pvp_stats['seconds_played'] = int(pvp_data['secondsPlayed']['basic']['value'])  #convert to days, hours, minutes
#            pvp_stats['number_matches'] = int(pvp_data['activitiesEntered']['basic']['displayValue'])
#            pvp_stats['kd'] = float(pvp_data['killsDeathsRatio']['basic']['displayValue'])
#            pvp_stats['favorite_weapon'] = pvp_data['weaponBestType']['basic']['displayValue']
#
#            pvp_stats['longest_spree'] = int(pvp_data['longestKillSpree']['basic']['value'])
#            pvp_stats['most_kills'] = int(pvp_data['bestSingleGameKills']['basic']['value'])
#            pvp_stats['number_wins'] = int(pvp_data['activitiesWon']['basic']['value'])
#            pvp_stats['win_loss_ratio'] = float(pvp_data['winLossRatio']['basic']['displayValue'])
#
#            pvp_stats['longest_kill_distance'] = float(pvp_data['longestKillDistance']['basic']['displayValue'])
#            pvp_stats['suicides'] = int(pvp_data['suicides']['basic']['value'])
#            pvp_stats['kills_per_match'] = float(pvp_data['kills']['pga']['displayValue'])
#            pvp_stats['deaths_per_matsh'] =  float(pvp_data['deaths']['pga']['displayValue'])
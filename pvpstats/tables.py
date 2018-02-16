#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 14:35:32 2018

@author: eric
"""
import logging
import itertools

import django_tables2 as tables
from .models import PvpStats
from salted_vex_milk.utils import render_seconds, FloatColumn

"""
Set up logger: for now just print everything to stdout.
"""
logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt =' %m/%d/%y %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PvpStatsTable(tables.Table):
    member = tables.LinkColumn(viewname = 'characters:characters', kwargs = {"name": tables.A('member.name')})
    number_matches = tables.Column(verbose_name = 'Matches', attrs= {"td": {"align":"center"} })
    kd = FloatColumn(verbose_name = 'K/D', attrs= {"td": {"align":"center"} })
    most_kills = tables.Column(verbose_name = 'Max Kills', attrs= {"td": {"align":"center"} })
    longest_spree = tables.Column(verbose_name = 'Spree', attrs= {"td": {"align":"center"} })
    favorite_weapon = tables.Column(verbose_name = 'Favorite',  attrs= {"td": {"align":"center"} })
    win_loss_ratio = FloatColumn(verbose_name = 'W/L', attrs= {"td": {"align":"center"} })
    kills_pga = FloatColumn(verbose_name = 'Kills', attrs= {"td": {"align":"center"} })
    deaths_pga = FloatColumn(verbose_name = 'Deaths', attrs= {"td": {"align":"center"} })
    suicides_pga = FloatColumn(verbose_name = "Suicides", attrs= {"td": {"align":"center"} })
    trials_number_matches = tables.Column(verbose_name = 'Trials Matches', attrs= {"td": {"align":"center"} })
    trials_kd = FloatColumn(verbose_name = 'Trials K/D', attrs= {"td": {"align":"center"} })
    trials_win_loss_ratio = FloatColumn(verbose_name = 'Trials W/L', attrs= {"td": {"align":"center"} })
    greatness = FloatColumn(attrs= {"td": {"align":"center"} })
    seconds_played = tables.Column(verbose_name = "Time Played", attrs= {"td": {"align":"center"} })

    def render_seconds_played(self, value):
        return render_seconds(value)

    
    class Meta:
        model = PvpStats
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-striped table-hover table-sm table-responsive text-nowrap'}  #note table-bordered makes things really slow
        fields =  ['member', 'number_matches', 'greatness', 'seconds_played', 'kills_pga',
                   'deaths_pga', 'kd', 'win_loss_ratio', 'longest_spree', 'most_kills',
                   'suicides_pga', 'favorite_weapon', 'trials_number_matches', 'trials_kd',
                   'trials_win_loss_ratio']




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
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 14:35:32 2018

@author: eric
"""

import django_tables2 as tables
from .models import PveStats
from salted_vex_milk.utils import FloatColumn

class PveStatsTable(tables.Table):
    number_activities = tables.Column(verbose_name = '#Activities', attrs= {"td": {"align":"center"} })
    activities_cleared = tables.Column(verbose_name = 'Cleared', attrs= {"td": {"align":"center"} })
    heroic_public_events = tables.Column(verbose_name = "HeroicPublic",  attrs= {"td": {"align":"center"} })
    adventures = tables.Column(attrs= {"td": {"align":"center"} })
    # patrols
    # strikes
    # nightfall
    # prestige nightfall
    # quests (story or whatever)
    seconds_played = tables.Column(verbose_name = 'Time Played', attrs= {"td": {"align":"center"} })
    longest_single_life = tables.Column(verbose_name = 'Longest Life', attrs= {"td": {"align":"center"} })
    average_life = FloatColumn(verbose_name = 'Avg Life', attrs= {"td": {"align":"center"} })

    kills_pga = tables.Column(verbose_name = 'Avg Kills', attrs= {"td": {"align":"center"} })
    deaths_pga = tables.Column(verbose_name = 'Avg Deaths', attrs= {"td": {"align":"center"} })
    kd = tables.Column(verbose_name = 'K/D',  attrs= {"td": {"align":"center"} })

    longest_spree = tables.Column(verbose_name = 'Spree', attrs= {"td": {"align":"center"} })
    most_precision_kills = tables.Column(verbose_name = 'Max Precision', attrs= {"td": {"align":"center"} })
    precision_kills_pga = tables.Column(verbose_name = 'Avg Precision', attrs= {"td": {"align":"center"} })
    longest_kill = tables.Column(verbose_name = "Max Distance", attrs= {"td": {"align":"center"} })
    favorite_weapon = tables.Column(verbose_name = 'Favorite')

    suicides_pga = tables.Column(verbose_name = 'Avg Suicides', attrs= {"td": {"align":"center"} })
    suicides = tables.Column(verbose_name = "Suicides", attrs= {"td": {"align":"center"} })
    resurrections_received_pga = tables.Column(verbose_name = 'Resurr Received', attrs= {"td": {"align":"center"} })
    resurrections_performed_pga = tables.Column(verbose_name = 'Resurr Performed', attrs= {"td": {"align":"center"} })
    orbs_dropped_pga = tables.Column(verbose_name = 'Orbs Dropped', attrs= {"td": {"align":"center"} })
    orbs_gathered_pga = tables.Column(verbose_name = 'Orbs Gathered', attrs= {"td": {"align":"center"} })

    class Meta:
        model = PveStats
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-striped table-hover table-sm table-responsive text-nowrap'}  #note table-bordered makes things really slow
        fields =  ['member', 'number_activities', 'activities_cleared', 'heroic_public_events', 'adventures',
                   'seconds_played', 'longest_single_life', 'average_life', 'kills_pga', 'deaths_pga', 'kd', 'longest_spree',
                   'most_precision_kills', 'precision_kills_pga', 'longest_kill', 'favorite_weapon', 'suicides_pga', 'suicides',
                   'resurrections_received_pga', 'resurrections_performed_pga', 'orbs_dropped_pga', 'orbs_gathered_pga']



#TO ADD TO MODEL:
# Stories
# Patrols (these include lost sectors)
# Strikes
# Nightfall
# Nightfall prestige
# Quests (?)

#


#To remove from model or table:
# Suicide number
# Activities/cleared (wtf does taht mean?)
# Max precision kills
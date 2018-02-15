#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 14:35:32 2018

@author: eric
"""

import django_tables2 as tables
from .models import PveStats
from salted_vex_milk.utils import render_seconds_to_seconds, render_seconds
from salted_vex_milk.utils import FloatColumn

class PveStatsTable(tables.Table):
    member = tables.LinkColumn(viewname = 'characters:characters', kwargs = {"name": tables.A('member.name')})
    greatness= FloatColumn(verbose_name = 'Greatness',  attrs= {"td": {"align":"center"} })
    number_story_missions = tables.Column(verbose_name = "Story Missions", attrs= {"td": {"align":"center"} })
    number_strikes = tables.Column(verbose_name = "Strikes", attrs= {"td": {"align":"center"} })
    number_nightfalls = tables.Column(verbose_name = "Nightfalls", attrs= {"td": {"align":"center"} })
    number_raid_clears = tables.Column(verbose_name = "Raid Clears", attrs= {"td": {"align":"center"} })

    seconds_played = tables.Column(verbose_name = 'Time Played', attrs= {"td": {"align":"center"} })
    longest_single_life = tables.Column(verbose_name = 'Longest Life', attrs= {"td": {"align":"center"} })
    average_life = FloatColumn(verbose_name = 'Mean Lifespan', attrs= {"td": {"align":"center"} })

    kills_pga = FloatColumn(verbose_name = 'Kills', attrs= {"td": {"align":"center"} })
    deaths_pga = FloatColumn(verbose_name = 'Deaths', attrs= {"td": {"align":"center"} })
    kd = FloatColumn(verbose_name = 'K/D',  attrs= {"td": {"align":"center"} })

    longest_spree = tables.Column(verbose_name = 'Spree', attrs= {"td": {"align":"center"} })
    most_precision_kills = tables.Column(verbose_name = 'Max Precision Kills', attrs= {"td": {"align":"center"} })
    precision_kills_pga = FloatColumn(verbose_name = 'Precision Kills', attrs= {"td": {"align":"center"} })
    longest_kill = tables.Column(verbose_name = "Max Kill Distance", attrs= {"td": {"align":"center"} })
    favorite_weapon = tables.Column(verbose_name = 'Favorite')

    assists_pga = FloatColumn(verbose_name = 'Assists', attrs= {"td": {"align":"center"} })
    suicides_pga = FloatColumn(verbose_name = 'Suicides', attrs= {"td": {"align":"center"} })
    resurrections_received_pga = FloatColumn(verbose_name = 'Resurrections Received', attrs= {"td": {"align":"center"} })
    resurrections_performed_pga = FloatColumn(verbose_name = 'Resurrections Performed', attrs= {"td": {"align":"center"} })
    orbs_dropped_pga = FloatColumn(verbose_name = 'Orbs Dropped', attrs= {"td": {"align":"center"} })
    orbs_gathered_pga = FloatColumn(verbose_name = 'Orbs Gathered', attrs= {"td": {"align":"center"} })

    class Meta:
        model = PveStats
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-striped table-hover table-sm table-responsive text-nowrap'}  #note table-bordered makes things really slow
        fields =  ['member', 'greatness', 'number_story_missions', 'number_strikes', 'number_nightfalls', 'number_raid_clears',
                   'seconds_played', 'longest_single_life', 'average_life', 'kills_pga', 'deaths_pga', 'kd', 'longest_spree',
                   'most_precision_kills', 'precision_kills_pga', 'longest_kill', 'suicides_pga', 'assists_pga', 'favorite_weapon',
                   'resurrections_received_pga', 'resurrections_performed_pga', 'orbs_dropped_pga', 'orbs_gathered_pga']

    def render_average_life(self, value):
        return render_seconds_to_seconds(value)

    def render_longest_single_life(self, value):
        return render_seconds_to_seconds(value)

    def render_seconds_played(self, value):
        return render_seconds(value)

#


#To remove from model or table:
# Suicide number
# Activities/cleared (wtf does taht mean?)
# Max precision kills
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 14:35:32 2018

@author: eric
"""

import django_tables2 as tables
from .models import Member
from salted_vex_milk.utils import minutes_to_days

class MemberTable(tables.Table):
    name = tables.LinkColumn('characters:characters', kwargs = {"name": tables.A('name')})
    date_joined = tables.DateTimeColumn(verbose_name = 'Joined', format = 'M d Y')
    date_last_played = tables.DateTimeColumn(verbose_name = 'Last Played', format ='M d Y')
    minutes_played = tables.Column(verbose_name = 'Time Played', attrs= {"td": {"align":"center"}})

    class Meta:
        model = Member
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-striped table-hover table-sm table-responsive text-nowrap'}  #note table-bordered makes things really slow
        fields =  ['name', 'date_joined', 'date_last_played', 'minutes_played']


    def render_minutes_played(self, value):
        time_logged = minutes_to_days(value)
        #logger.debug(time_logged)
        days = time_logged[0]
        hours = time_logged[1]
        minutes = time_logged[2]
        time_played = ''
        if value > 0:
            if days > 0:
                time_played += str(days) + 'd '
            if hours > 0:
                time_played += str(hours) + 'h '
            time_played += str(minutes) + 'm'
        else:
            time_played = '0'
        return time_played





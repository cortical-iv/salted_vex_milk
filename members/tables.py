#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 14:35:32 2018

@author: eric
"""

import django_tables2 as tables
from .models import Member
from salted_vex_milk.utils import render_minutes

class MemberTable(tables.Table):
    name = tables.LinkColumn(viewname = 'characters:characters', kwargs = {"name": tables.A('name')})
    date_joined = tables.DateTimeColumn(verbose_name = 'Joined', format = 'M d Y')
    date_last_played = tables.DateTimeColumn(verbose_name = 'Last Played', format ='M d Y')
    minutes_played = tables.Column(verbose_name = 'Time Played', attrs= {"td": {"align":"center"}})
    max_light = tables.Column(attrs= {"td": {"align":"center"}})

    class Meta:
        model = Member
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-striped table-hover table-sm table-responsive text-nowrap'}  #note table-bordered makes things really slow
        fields =  ['name', 'date_joined', 'minutes_played', 'max_light', 'date_last_played']


    def render_minutes_played(self, value):
        return render_minutes(value)





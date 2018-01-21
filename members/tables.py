#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 14:35:32 2018

@author: eric
"""

import django_tables2 as tables
from .models import Member

class MemberTable(tables.Table):
    has_played_d2 = tables.BooleanColumn(attrs= {"td": {"align":"center"} }, verbose_name = 'Played D2')
    date_joined = tables.DateTimeColumn(verbose_name = 'Joined')
    member_id = tables.Column(verbose_name = 'ID')
    class Meta:
        model = Member
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-striped table-hover table-sm'}
        fields =  ['name', 'date_joined', 'has_played_d2', 'member_id']

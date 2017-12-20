#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 22:56:36 2017

@author: eric
"""


from django import forms
from .models import Clan

class ClanForm(forms.ModelForm):
    class Meta:
        model = Clan
        fields = ['clan_id', 'name', 'creation_date', 'description', 'motto',\
                  'call_sign', 'num_members', 'founder']


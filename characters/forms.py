#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 22:56:36 2017

@author: eric
"""
from django import forms
from .models import Character

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields =  ['member', 'character_id', 'character_class', 'light', 'level',\
                   'race', 'gender', 'emblem_path', 'date_last_played', 'minutes_played']


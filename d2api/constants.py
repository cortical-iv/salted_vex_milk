#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 22:12:46 2017

@author: eric
"""
from django.conf import settings

GROUP_ID = '623172'  #you could set this as env variable if you want
BASE_URL = 'https://www.bungie.net/Platform/Destiny2/'
BASE_URL_GROUP = 'https://www.bungie.net/Platform/GroupV2/'

D2_KEY = settings.D2_KEY
D2_HEADERS = {"X-API-Key": D2_KEY}

# MEMBERSHIP_ENUM = {0: 'none', 1: 'xbox',  2: 'psn', 4: 'pc', -1: 'all' }  #to be used someday
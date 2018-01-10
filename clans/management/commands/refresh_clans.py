#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 20:34:57 2017

@author: eric
"""
import logging
#import json
from django.core.management.base import BaseCommand #, CommandError
import d2api.utils as api
from clans.forms import ClanForm
from clans.models import Clan
from d2api.constants import GROUP_ID, D2_HEADERS


"""
Set up logger: for now just print everything to stdout.
"""
logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt =' %m/%d/%y %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



class Command(BaseCommand):
    help = 'Refreshes Clan model'

    def handle(self, *args, **options):
        get_group_urlargs =  {'group_id': GROUP_ID}
        group = api.GetGroup(D2_HEADERS, url_arguments = get_group_urlargs)
        instance_kwargs = {'clan_id': GROUP_ID}
        try:
            api.bind_and_save(Clan, group.clan_info, ClanForm, **instance_kwargs)
        except Exception as e:
            msg = f"refresh_clans bind_and_save exception: {e}."
            logger.exception(msg)
            raise
        else:
            logger.debug("Clans successfully updated")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 20:34:57 2017

@author: eric
"""
import logging

from django.core.management.base import BaseCommand #, CommandError
import d2api.utils as api
from pvestats.forms import PveStatsForm
from pvestats.models import PveStats
from members.models import Member
from d2api.constants import D2_HEADERS


"""
Set up logger: for now just print everything to stdout.
"""
logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt =' %m/%d/%y %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Command(BaseCommand):
    help = 'Gets PvE stats for all clan members'

    def handle(self, *args, **options):
        #Add all characters to db
        logger.info("refresh_pvestats: Retrieving pve stats.")
        members = Member.objects.all().order_by('date_joined')
        for member in members:
            if member.has_played_d2:
                logger.info(f"refresh_pvestats: getting pve stats for {member.name}")
                stats_urlargs = {'membership_type': member.membership_type, 'member_id': member.member_id, 'character_id': '0'}
                modes = {'modes': '4,7,2,16,18'}
                pve_historical_stats = api.GetHistoricalStats(D2_HEADERS, url_arguments = stats_urlargs, request_parameters = modes)
                pve_data = pve_historical_stats.extract_pve_stats()
                #logger.debug(pve_data)
                instance_kwargs = {'member': pve_data['member']}
                try:
                    api.bind_and_save(PveStats, pve_data, PveStatsForm, **instance_kwargs)
                except Exception as e:
                    msg = f"refresh_pvestats in bind_and_save. Exception: {e}"
                    logger.exception(msg)
                    raise
            else:
                logger.debug(f"{member.name} has not played d2, no pvestats added.")
        logger.info("Done updating pvestats.")




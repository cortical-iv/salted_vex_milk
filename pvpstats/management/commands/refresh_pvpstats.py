#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 20:34:57 2017

@author: eric
"""
import logging

from django.core.management.base import BaseCommand #, CommandError
import d2api.utils as api
from pvpstats.forms import PvpStatsForm
from pvpstats.models import PvpStats
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
    help = 'Refreshes all Characters in database for clan'

    def handle(self, *args, **options):
        #Add all characters to db
        logger.info("refresh_pvpstats: Retreiving pvp stats.")
        members = Member.objects.all().order_by('date_joined')
        for member in members:
            if member.has_played_d2:
                logger.debug(f"Getting pvp stats for {member.name}")
                stats_urlargs = {'membership_type': member.membership_type, 'member_id': member.member_id, 'character_id': '0'}
                modes = {'modes': '5'}
                pvp_historical_stats = api.GetHistoricalStats(D2_HEADERS, url_arguments = stats_urlargs, request_parameters = modes)
                pvp_data = pvp_historical_stats.extract_pvp_stats()
                logger.debug(pvp_data)
                instance_kwargs = {'member': pvp_data['member']}
                try:
                    api.bind_and_save(PvpStats, pvp_data, PvpStatsForm, **instance_kwargs)
                except Exception as e:
                    msg = f"refresh_pvpstats in bind_and_save. Exception: {e}"
                    logger.exception(msg)
                    raise
            else:
                logger.debug(f"{member.name} has not played d2, no pvpstats added.")
        logger.info("Done updating pvpstats.")




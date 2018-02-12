#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 12:43:12 2018

@author: eric
"""
import logging

from django.core.management.base import BaseCommand #, CommandError
from django.core import management


"""
Set up logger: for now just print everything to stdout.
"""
logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt =' %m/%d/%y %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = 'Meta-management command that refreshes everything, should be the only thing that needs to be run'

    def handle(self, *args, **options):
        logger.info("svm refreshing clans")
        management.call_command('refresh_clans')

        logger.info("svm refreshing members")
        management.call_command('refresh_members')

        logger.info("svm refreshing characters")
        management.call_command('refresh_characters')

        logger.info("svm refreshing pvpstats")
        management.call_command('refresh_pvpstats')

        logger.info("svm refreshing pvestats")
        management.call_command('refresh_pvestats')
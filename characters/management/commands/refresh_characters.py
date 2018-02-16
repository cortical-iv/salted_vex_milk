#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 20:34:57 2017

@author: eric
"""
import logging

from django.core.management.base import BaseCommand #, CommandError
import d2api.utils as api
from characters.forms import CharacterForm
from characters.models import Character
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
        logger.info("refresh_characters: Retreiving character data.")
        members = Member.objects.all().order_by('date_joined')
        for member in members:
            logger.info(f"Getting character info for {member.name}")
            if member.has_played_d2:
                get_profile_urlargs = {'membership_type': member.membership_type,\
                                       'member_id': member.member_id}
                get_profile_params = {'components': '200'}
                characters_profile = api.GetProfile(D2_HEADERS, url_arguments = get_profile_urlargs, \
                                                    request_parameters = get_profile_params)
                logger.debug(f"Have gotten character profile...analyzing...time to pull: {characters_profile.request_duration}")
                member_chars, total_time, max_light, last_played  = characters_profile.extract_character_info()
                member.max_light = max_light
                member.minutes_played = total_time
                member.date_last_played = last_played
                for character in member_chars:
                    instance_kwargs = {'member': character['member'], 'character_id': character['character_id']}
                    try:
                        api.bind_and_save(Character, character, CharacterForm, **instance_kwargs)
                    except Exception as e:
                        msg = f"refresh_characters in bind_and_save. Exception: {e}"
                        logger.exception(msg)
                        raise
            else:
                logger.debug(f"{member.name} has not played d2, no characters added. Filling in light and such.")
                member.max_light = 0
                member.minutes_played = 0
                member.date_last_played = member.date_joined
            member.save()
        logger.info("Done updating characters.")




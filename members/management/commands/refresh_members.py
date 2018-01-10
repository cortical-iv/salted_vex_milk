#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 20:34:57 2017

@author: eric
"""
import requests
import logging

from django.core.management.base import BaseCommand #, CommandError
from django.core import management
import d2api.utils as api
from members.forms import MemberForm
from members.models import Member
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
    help = 'Refreshes Member model with all members of clan'

    def handle(self, *args, **options):
        with requests.Session() as session:
            session.headers.update(D2_HEADERS)
            #Check to see if clan exists. If it doesn't, add it
            try:
                Clan.objects.get(clan_id = GROUP_ID)
            except Clan.DoesNotExist:
                logger.warning("refresh_members: clan not in database. Running refresh_clans().")
                management.call_command('refresh_clans')

            #Add all members of clan to db
            logger.info("refresh_members: Retreiving group members.")
            members_urlargs = {'group_id': GROUP_ID}
            members = api.GetMembersOfGroup(D2_HEADERS, url_arguments = members_urlargs)
            #update or insert member data
            for member in members.member_list:
                name = member['name']
                membership_type = member['membership_type']
                logger.debug(f"Processing {name}.")

                #Add has_played_d2 attribute to member
                get_profile_params = {'components': '100'}
                get_profile_urlargs = {'membership_type': membership_type, 'member_id': member['member_id']}
                profile = api.GetProfile(D2_HEADERS, url_arguments = get_profile_urlargs, \
                                     request_parameters = get_profile_params)
                member['has_played_d2'] = profile.played_d2
                logger.debug(f"{name} profile processing seconds: {profile.request_duration}")
                #Validate and save member to db
                instance_kwargs = {'member_id': member['member_id'], 'membership_type': member['membership_type']}
                try:
                    api.bind_and_save(Member, member, MemberForm, **instance_kwargs)
                except Exception as e:
                    msg = f"refresh_members in bind_and_save. Exception: {e}."
                    logger.exception(msg)
                    raise
            logger.info("Done updating members.")






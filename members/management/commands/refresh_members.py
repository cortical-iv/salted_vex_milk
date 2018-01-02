#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 20:34:57 2017

@author: eric
"""
import requests
import logging
import time

from django.utils import timezone
from django import forms
from django.core.management.base import BaseCommand #, CommandError
from django.db.utils import IntegrityError
import d2api.utils as api
from members.forms import MemberForm
from members.models import Member
from d2api.constants import GROUP_ID, D2_HEADERS


"""
Set up logger_member_refresh: for now just print everything to stdout.
"""
logging.basicConfig(level = logging.INFO,
                    format = '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt =' %m/%d/%y %H:%M:%S')
logger_member_refresh = logging.getLogger(__name__)



class Command(BaseCommand):
    help = 'Refreshes member list'

    def handle(self, *args, **options):

        with requests.Session() as session:
            session.headers.update(D2_HEADERS)
            #Functionalize the following you will use it for each end poin
            members_url = api.get_members_of_group_url(GROUP_ID)
            logger_member_refresh.info(f"Retreiving group members. URL: {members_url}")
            try:
                members_data = api.destiny2_api_handler(members_url, session)
            except Exception as err:
                logger_member_refresh.exception(f"Error getting clan members for {GROUP_ID}.\nException: {err}.")
            else:
                members = api.extract_member_list(members_data)
                #update or insert member data
                for member in members:
                    time_init_process_member = time.process_time()
                    name = member['name']
                    logger_member_refresh.debug(f"Processing {name}.")
#                    #Determine if user has played d2 or not
                    time_init_profile = time.process_time()
                    profile_url = api.get_profile_url(member['member_id'], member['membership_type']) #/?components=' + components #200
                    profile_params = {'components': '200'}
                    try:
                        profile_response = api.make_request(profile_url, session, request_params = profile_params)
                        logger_member_refresh.debug(f"ThrottleSeconds: {profile_response.json()['ThrottleSeconds']}")

                        if profile_response.json()['ErrorStatus'] == 'DestinyAccountNotFound':
                            member['has_played_d2'] = False
                        else:
                            member['has_played_d2'] = True
                    except:
                        logger_member_refresh.error(f"No profile data for {name}. URL: {profile_url}")
                    elapsed_time_profile = time.process_time() - time_init_profile
                    logger_member_refresh.debug(f"Check if has played time: {elapsed_time_profile}")

                    #determine if member exists or not, and update/insert accordingly
                    time_init_exists = time.process_time()
                    try:
                        member_instance = Member.objects.get(member_id = member['member_id'],
                                                             membership_type = member['membership_type'])
                    except Member.DoesNotExist:
                        member_form_bound = MemberForm(member)
                    else:
                        logger_member_refresh.debug(f"{name} already exists: updating.")
                        member_form_bound = MemberForm(member, instance = member_instance)
                    elapsed_time_exists = time.process_time() - time_init_exists
                    logger_member_refresh.debug(f"Check if player instance exists: {elapsed_time_exists}")

                    #validate and save form
                    time_init_validate = time.process_time()
                    if member_form_bound.is_valid():
                        try:
                            member_form_bound.save()
                        except IntegrityError as err:
                            logger_member_refresh.error(f"Integrity error: {err}")
                        else:
                            logger_member_refresh.debug(f"{name} successfully saved.")
                    else:
                        logger_member_refresh.error(f"member form not valid. error: {member_form_bound.errors}.\nMember data: {member}")
                        raise forms.ValidationError(f"Member info not valid: {member_form_bound.errors}")
                    elapsed_time_validate = time.process_time() - time_init_validate
                    logger_member_refresh.debug(f"Validation time: {elapsed_time_validate}")

                    elapsed_time_process_member = time.process_time() - time_init_process_member
                    logger_member_refresh.debug(f"{name} add time: {elapsed_time_process_member}\n")
        logger_member_refresh.info("Done refreshing members")
        Member.updated = timezone.now()
        logger_member_refresh.info(f"Member.updated: {Member.updated}")
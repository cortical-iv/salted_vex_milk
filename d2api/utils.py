#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 22:14:35 2017

@author: eric
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilities for restit/d2_api app.
"""
##Imports
import requests
import logging
import json

from django import forms
from django.db.utils import IntegrityError

from .constants import BASE_URL, GROUP_ID, BASE_URL_GROUP
from clans.models import Clan
#from .forms import SubmitUser

"""
Set up logger: for now just print everything to stdout.
"""
logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt =' %m/%d/%y %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

"""
CORE CODE: the api handler
Make requests, and extract data from response
"""
class BungieError(Exception):
    """Raise when ErrorCode from Bungie is not 1"""

def make_request(url, session, request_params = None):
    try:
        if request_params:
            response = session.get(url, params = request_params)
        else:
            response = session.get(url)

        #Raise error for responses with 200 status that are errors
        if not response.ok:
            response.raise_for_status()
        else:
            logger.debug(f"make_request: URL: {url}. Elapsed: {response.elapsed}")

    except requests.exceptions.RequestException as requestErr:
        msg = f"RequestException in make_request. Error from bungie:\n -{requestErr}"
        raise BungieError(msg) from requestErr
    else:
        return response


def process_bungie_response(response):
    """Examines response from d2 if you got status_code 200, throws
    BungieError exception if bungie ErrorCode is not 1. For list of error
    codes, see:
        https://bungie-net.github.io/multi/schema_Exceptions-PlatformErrorCodes.html#schema_Exceptions-PlatformErrorCodes
    """
    response_url = response.url    #If you sent it something that can't be json'd
    response_json = response.json() #don't need jsondecodeerror b/c you used raise_for_status

    try:
        data = response_json['Response']
    except KeyError as keyError:
        error_code = response_json['ErrorCode']
        error_status = response_json['ErrorStatus']
        error_message = response_json['Message']
        msg1 = f"KeyError in 'process_bungie_response'.\nURL: {response_url}.\n"
        msg2 = f"Bungie error code {error_code}: {error_status}.\nMessage: {error_message}.\n"
        msg = msg1 + msg2
        raise BungieError(msg) from keyError
    else:
        return data



def destiny2_api_handler(url, session, request_params = None):
    if request_params:
        response = make_request(url, session, request_params)
    else:
        response = make_request(url, session)
    return process_bungie_response(response)


"""
ENDPOINT CLASSES
"""

class Endpoint:
    """
    Abstract end point class: this is never used directly.
    Specific endpoint classes inherit from this.
    """
    def __init__(self, headers, url_arguments = None, request_parameters = None):
        self.url_arguments = url_arguments
        self.url_initial = self.make_url()
        self.request_params = request_parameters
        self.headers = headers
        self.response = self.make_request()
        self.request_duration = self.response.elapsed.total_seconds()
        self.url = self.response.url
        self.data = self.get_data()

    def make_url(self):
        """Reimplement for each end point instance"""
        return

    def make_request(self):
        try:
            if self.request_params:
                response = requests.get(self.url_initial, headers = self.headers, \
                                        params = self.request_params)
            else:
                response = requests.get(self.url_initial, headers = self.headers)
            if not response.ok:
                response.raise_for_status()

        except requests.exceptions.RequestException as requestExc:
            msg = f"Endpoint.make_request() exception:\n{requestExc}"
            logger.exception(msg)
            raise
        else:
            return response

    def get_data(self):
        try:
            response_json = self.response.json()
        except json.JSONDecodeError as jsonError:
            msg1 = f"JSONDecodeError in Endpoint.get_data()."
            msg2 = "Response does not contain json-encoded data.\n"
            msg3 = f"URL: {self.url}.\nError: '{jsonError}'"
            msg = msg1 + msg2 + msg3
            logger.exception(msg)
            raise

        try:
            data = response_json['Response']
        except KeyError as keyError:
            error_code = response_json['ErrorCode']
            error_status = response_json['ErrorStatus']
            error_message = response_json['Message']
            msg1 = f"KeyError in Endpoint.get_data().\nURL: {self.url}.\n"
            msg2 = f"Error code {error_code}: {error_status}.\nMessage: {error_message}.\n"
            msg = msg1 + msg2
            logger.warning(msg)
            data = response_json
        return data


    def __repr__(self):
        return "Endpoint instance."


class GetProfile(Endpoint):
    """
    Get information about user's character(s): the required components querystring
    params specify the components to request.
      Endpoint:  https://bungie-net.github.io/multi/operation_get_Destiny2-GetProfile.html
      Component types:  https://bungie-net.github.io/multi/schema_Destiny-DestinyComponentType.html
    """
    def __init__(self, headers, url_arguments = None, request_parameters = None):
        super().__init__(headers, url_arguments, request_parameters)
        self.played_d2 = self.has_played_d2()

    def make_url(self):
        membership_type = str(self.url_arguments['membership_type'])
        member_id = str(self.url_arguments['member_id'])
        url = f"{BASE_URL}{membership_type}/Profile/{member_id}/"
        return url

    def has_played_d2(self):
        try:
            error_status = self.response.json()['ErrorStatus']
        except AttributeError:
            logger.error("GetProfile.has_played_d2(): no response data")
            raise
        else:
            if error_status == 'DestinyAccountNotFound':
                logger.debug(f"**User has not played d2**")
                return False
            else:
                return True

    def __repr__(self):
        return f"GetProfile instance.\nURL: {self.url}"


class SearchDestinyPlayer(Endpoint):
    """
    User card: minimal info like id and date joined
      https://bungie-net.github.io/multi/operation_get_Destiny2-SearchDestinyPlayer.html
    """
    def __init__(self, headers, url_arguments = None, request_parameters = None):
        super().__init__(headers, url_arguments, request_parameters)

    def make_url(self):
        membership_type = str(self.url_arguments['membership_type'])
        name = self.url_arguments['name']
        url = f"{BASE_URL}SearchDestinyPlayer/{membership_type}/{name}/"
        return url

    def __repr__(self):
        return f"GetProfile instance.\nURL: {self.url}"

class GetGroup(Endpoint):
    """
    Generic info about clan, like motto:
      https://bungie-net.github.io/multi/operation_get_GroupV2-GetGroup.html
    """
    def __init__(self, headers, url_arguments = None, request_parameters = None):
        super().__init__(headers, url_arguments, request_parameters)
        self.clan_info = self.extract_clan_info()

    def make_url(self):
        group_id = self.url_arguments['group_id']
        url = f"{BASE_URL_GROUP}{group_id}/"
        return url

    def extract_clan_info(self):
        """Extract data needed for Clan form"""
        clan_details = self.data['detail']
        clan_info = {}
        clan_info['clan_id'] = clan_details['groupId']
        clan_info['name'] = clan_details['name']
        clan_info['call_sign'] = clan_details['clanInfo']['clanCallsign']
        clan_info['creation_date'] = clan_details['creationDate']
        clan_info['description'] = clan_details['about']
        clan_info['motto'] = clan_details['motto']
        clan_info['num_members'] = clan_details['memberCount']
        clan_info['founder'] = self.data['founder']['destinyUserInfo']['displayName']
        return clan_info


    def __repr__(self):
        return f"GetGroup instance.\nURL: {self.url}"


class GetMembersOfGroup(Endpoint):
    """
    Info about each member of clan.
    https://bungie-net.github.io/multi/operation_get_GroupV2-GetMembersOfGroup.html
    """
    def __init__(self, headers, url_arguments = None, request_parameters = None):
        super().__init__(headers, url_arguments, request_parameters)
        self.member_list = self.make_clan_list()

    def make_url(self):
        group_id = self.url_arguments['group_id']
        url = f"{BASE_URL_GROUP}{group_id}/Members/?currentPage=1"
        return url

    def make_clan_list(self):
        try:
            self.data['results']
        except KeyError:
            logger.error("GetMembersOfGroup.make_clan_list(): No results in GetMembersOfGroup instance.")
            return

        clan = Clan.objects.get(clan_id = GROUP_ID)
        member_list = []
        for member in self.data['results']:
            clan_member = {}
            clan_member['clan'] = clan.id
            clan_member['membership_type'] = member['destinyUserInfo']['membershipType']
            clan_member['name'] = member['destinyUserInfo']['displayName']
            clan_member['member_id'] = member['destinyUserInfo']['membershipId']
            clan_member['date_joined']  = member['joinDate']
            member_list.append(clan_member)
        return member_list

    def print_clan_list(self):
        """Mostly for testing purposes: prints each member in clan_list."""
        try:
            self.members
        except AttributeError:
            logger.error("GetMembersOfGroup.print_clan_list(): object has no clan_members.")
            return

        name_list = [member['name'] for member in self.members]
        col_width = max(len(word) for word in name_list)
        for member in self.members:
            member_name = member['name']
            length_name = len(member_name)
            num_spaces = col_width - length_name
            member_name_padded = member_name + " "*num_spaces
            msg1 = f"{member_name_padded}\tMembership type: {member['membership_type']}"
            msg2 = f"\tID: {member['id']}\tJoined: {member['date_joined']}"
            print(msg1+msg2)

    def __repr__(self):
        return f"GetMembersOfGroup instance.\nURL: {self.url}"



"""
ABSTRACT HELPER FUNCTIONS
"""
def bind_and_save(Model, data, Form, **instance_kwargs):
    """
    Determine if model instance exists (using instance_kwargs. a dictionary of
    unique identifiers).  Bind data to form, using instance if instance exists.
    Validate and save data into Model.
    """
    try:
        model_instance = Model.objects.get(**instance_kwargs)
    except Model.DoesNotExist:
        logger.debug(f"bind_and_save: no instance in db: inserting.\n")
        form_bound = Form(data)
    else:
        logger.debug(f"{model_instance} instance already exists: updating.\n")
        form_bound = Form(data, instance = model_instance)

    #Validate and save form
    if form_bound.is_valid():
        try:
            form_bound.save()
        except IntegrityError as err:
            logger.error(f"Integrity error: {err}")
    else:
        err_msg = f"Form not valid. Error: {form_bound.errors}"
        logger.error(err_msg)
        raise forms.ValidationError(err_msg)

"""
MODEL-SPECIFIC HELPER FUNCTIONS
"""






#

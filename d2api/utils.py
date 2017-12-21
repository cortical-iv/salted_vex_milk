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
import json
import requests
import logging

from .constants import BASE_URL, GROUP_ID, BASE_URL_GROUP, D2_HEADERS
from clans.models import Clan
#from .forms import SubmitUser

"""
Set up logger: for now just print everything to stdout.
"""
logging.basicConfig(level = logging.INFO,
                    format = '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt =' %m/%d/%y %H:%M:%S')
logger = logging.getLogger(__name__)


"""
CORE CODE: the api handler
Make requests, and extract data from response
"""
class BungieError(Exception):
    """Raise when ErrorCode from Bungie is not 1"""


def make_request(url, session):
    try:
        response = session.get(url)
        if not response.ok:
            response.raise_for_status()
    except requests.exceptions.RequestException as requestException:
        raise
    else:
        return response


def process_bungie_response(response):
    """Examines response from d2 if you got status_code 200, throws
    BungieError exception if bungie ErrorCode is not 1. For list of error
    codes, see:
        https://bungie-net.github.io/multi/schema_Exceptions-PlatformErrorCodes.html#schema_Exceptions-PlatformErrorCodes
    """
    response_url = response.url    #If you oops sent it something that can't be json'd
    try:
        response_json = response.json()
    except json.JSONDecodeError as jsonError:
        msg1 = f"JSONDecodeError in process_bungie_response().\n"
        msg2 = "Response does not contain json data.\n"
        msg3 = f"URL: {response_url}.\nError: '{jsonError}'"
        msg = msg1 + msg2 + msg3
        raise BungieError(msg) from jsonError

    try:
        data = response_json['Response']
    except KeyError as keyError:
        error_code = response_json['ErrorCode']
        error_status = response_json['ErrorStatus']
        error_message = response_json['Message']
        msg1 = f"KeyError in process_bungie_response.\nURL: {response_url}.\n"
        msg2 = f"Error code {error_code}: {error_status}.\nMessage: {error_message}.\n"
        msg = msg1 + msg2
        raise BungieError(msg) from keyError
    else:
        return data


def destiny2_api_handler(url, session):
    response = make_request(url, session)
    return process_bungie_response(response)


"""
URL generators
"""
def search_destiny_player_url(user_name):
    """Get user's info card:
        https://bungie-net.github.io/multi/operation_get_Destiny2-SearchDestinyPlayer.html
      Right now it is constrained to ps4 (platform = 2)
    """
    return BASE_URL + 'SearchDestinyPlayer/2/' + user_name + '/'


def get_group_url(group_id):
    """
    Pull information about a clan
        https://bungie-net.github.io/multi/operation_get_GroupV2-GetGroup.html
    """
    return BASE_URL_GROUP + group_id + '/'


def get_members_of_group_url(group_id):
    """
    Pull all members of a clan.
        https://bungie-net.github.io/multi/operation_get_GroupV2-GetMembersOfGroup.html
    """
    return BASE_URL_GROUP + group_id + '/Members/?currentPage=1'



"""
HELPER FUNCTIONS
"""
def extract_clan_info(clan_data):
    """Returns info needed for Clan form"""
    clan_details = clan_data['detail']
    clan_info = {}
    clan_info['clan_id'] = clan_details['groupId']
    clan_info['name'] = clan_details['name']
    clan_info['call_sign'] = clan_details['clanInfo']['clanCallsign']
    clan_info['creation_date'] = clan_details['creationDate']
    clan_info['description'] = clan_details['about']
    clan_info['motto'] = clan_details['motto']
    clan_info['num_members'] = clan_details['memberCount']
    clan_info['founder'] = clan_data['founder']['destinyUserInfo']['displayName']
    return clan_info


def extract_member_list(member_data):
    """
    Using GetMembersOfGroup end point, create list of member info for clan members.
        Each elt is a dict with username. id, join date. Filters out people not on psn.
    Each elt of list is ready for MemberForm
    """
    member_data = member_data['results']
    clan = Clan.objects.get(clan_id = GROUP_ID)
    clan_members = []
    for member in member_data:
        clan_member = {}
        clan_member['membership_type'] = member['destinyUserInfo']['membershipType']
        clan_member['name'] = member['destinyUserInfo']['displayName']
        clan_member['member_id'] = member['destinyUserInfo']['membershipId']
        clan_member['date_joined']  = member['joinDate']
        clan_member['clan'] = clan.id
        logging.info(clan_member)
        clan_members.append(clan_member)
    logging.info("Done with extract_member_list")
    return clan_members





#def add_user(user_name):
#    """
#    Validate form data containing 'display_name', request their info from server,
#    and pull in via a serializer. Returns dictionary, add_user_results, with two keys:
#        'flag': 1 if successful, 0 if not, and None if that user is not a D2 player in PS4.
#        'message': message about the outcome (success, validation error, etc).
#    """
#    print("\n\n\n***Key: {}".format(D2_KEY))
#    add_user_results = {'flag': 0, 'message': ''}
#    search_url = search_destiny_player_url(user_name)
#    player_search_request = requests.get(search_url, headers = {"X-API-Key": D2_KEY})
#    player_search_response = player_search_request.json()['Response']
#    print(player_search_response)
#    if player_search_response:
#        #Create dictionary of data and bind it to the SubmitUser form.
#        user_data = {'display_name': player_search_response[0]['displayName'], \
#                     'user_id': player_search_response[0]['membershipId']}
#        submit_user_form = SubmitUser(user_data)
#        #Validate and save data
#        if submit_user_form.is_valid():
#            submit_user_form.save() #save data to database
#            add_user_results['flag'] = 1
#            add_user_results['message'] = 'Successfully added {0}'.format(user_name)
#        else:
#            msg = submit_user_form.errors
#            print(msg)
#            add_user_results['message'] = msg
#    else:
#        msg = "'{0}' is not a Destiny2 player on PS4".format(user_name)
#        add_user_results['message'] = msg
#
#
#    return add_user_results
#

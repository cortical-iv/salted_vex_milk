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
import dateutil.parser


from django import forms
from django.db.utils import IntegrityError

from .constants import BASE_URL, GROUP_ID, BASE_URL_GROUP, CLASS_ENUM, GENDER_ENUM, RACE_ENUM
from clans.models import Clan
from members.models import Member
#from .forms import SubmitUser

"""
Set up logger: for now just print everything to stdout.
"""
logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt =' %m/%d/%y %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


"""
ENDPOINT CLASSES
"""

class Endpoint:
    """
    Abstract endpoint class: this is never used directly: specific endpoint classes
    inherit from this and need to reimplement make_url, which returns None.

    Call:
        endpoint_instance = Endpoint(headers, url_arguments=None, request_parameters = None)

    Parameters:
        headers: dictionary for requests:  {"X-API-Key": <your d2 key>}
        url_arguments: dictionary of url-specific parameters. E.g., {'member_id': '4611686018437883438'}
        request_parameters: querystring for request, if needed. E.g., {'components': '200'}

    """
    def __init__(self, headers, url_arguments = None, request_parameters = None):
        self.url_arguments = url_arguments
        self.url_initial = self.make_url()
        self.request_params = request_parameters
        self.headers = headers
        logger.debug("about to make request")
        self.response = self.make_request()
        self.request_duration = self.response.elapsed.total_seconds()
        self.url = self.response.url
        logger.debug("about to get_data()")
        self.data = self.get_data()

    def make_url(self):
        """Reimplement for each end point instance"""
        return

    def make_request(self):
        try:
            logger.debug("in make_request")
            if self.request_params:
                logger.debug(f"request_params? {self.request_params}")
                logger.debug(f"url initial: {self.url_initial}")
                logger.debug(f"Headers: {self.headers}")
                response = requests.get(self.url_initial, headers = self.headers, \
                                        params = self.request_params, timeout = 2)
                logger.debug("got response")
            else:
                logger.debug("Get response now")
                response = requests.get(self.url_initial, headers = self.headers, timeout = 2)
            if not response.ok:
                response.raise_for_status()

        except requests.exceptions.RequestException as requestExc:
            msg = f"Endpoint.make_request() exception:\n{requestExc}"
            logger.exception(msg)
            raise
        else:
            logger.debug("return response")
            return response

    def get_data(self):
        try:
            response_json = self.response.json()
        except json.JSONDecodeError as jsonError:
            #Response is not json coded: probably server error
            msg1 = f"JSONDecodeError in Endpoint.get_data()."
            msg2 = "Response does not contain json-encoded data.\n"
            msg3 = f"URL: {self.url}.\nError: '{jsonError}'"
            msg = msg1 + msg2 + msg3 + msg3
            logger.exception(msg)
            raise

        try:
            data = response_json['Response']
        except KeyError as keyError:
            #Response key is not defined: return rest of response it contains details
            error_code = response_json['ErrorCode']
            error_status = response_json['ErrorStatus']
            error_message = response_json['Message']
            msg1 = f"KeyError in Endpoint.get_data().\nURL: {self.url}.\n"
            msg2 = f"Error code {error_code}: {error_status}.\nMessage: {error_message}.\n"
            msg3 = "For bungie data this usually means you got a bungie error, like the user has not played d2.\n"
            msg = msg1 + msg2 + msg3
            logger.warning(msg)
            data = response_json
        return data


    def __repr__(self):
        return "Endpoint instance."


class GetHistoricalStats(Endpoint):
    """
    Return tons of useful stats about a character (or set character_id = '0' for
    all character data lumped together).
        https://bungie-net.github.io/multi/operation_get_Destiny2-GetHistoricalStats.html
    Url argument: modes ('?modes=X,Y,Z')
        modes: activity type to return (raid: 4; PvP: 5; PvE 7)

    Example call:
        headers = {"X-API-Key": <your d2 key>}
        stats_arguments = {'membership_type': '2', 'member_id': '4611686018459314819', 'character_id': '0'}
        modes = {'modes': '5'}
        pvp_stats = GetHistoricalStats(headers, url_arguments = stats_arguments, request_parameters = modes)
    """
    def __init__(self, headers, url_arguments = None, request_parameters = None):
        super().__init__(headers, url_arguments, request_parameters)


    def make_url(self):
        membership_type = str(self.url_arguments['membership_type'])
        member_id = str(self.url_arguments['member_id'])
        character_id = str(self.url_arguments['character_id'])
        url = f"{BASE_URL}{membership_type}/Account/{member_id}/Character/{character_id}/Stats/"
        return url

    def extract_pve_stats(self):
        member = Member.objects.get(member_id = self.url_arguments['member_id']) #foreign key
        pve_stats ={}
        pve_stats['member'] = member.id
        try:
            pve_data = self.data['allPvE']['allTime']
        except KeyError as e:
            logger.info(f"{member.name} GetHistoricalStats.extract_pve_stats(): no PvE stats. KeyError {e}")
            pve_stats['number_story_missions'] = 0
            pve_stats['number_strikes'] = 0
            pve_stats['number_nightfalls'] = 0
            pve_stats['number_raid_clears'] = 0

            pve_stats['seconds_played'] = 0
            pve_stats['longest_single_life'] = 0
            pve_stats['average_life'] = 0

            pve_stats['kills_pga'] = 0.0
            pve_stats['deaths_pga'] =  0.0
            pve_stats['kd'] = 0.0
            pve_stats['longest_spree'] = 0
            pve_stats['most_precision_kills'] = 0
            pve_stats['precision_kills_pga'] = 0.0
            pve_stats['longest_kill'] = 0.0
            pve_stats['favorite_weapon'] = '-'

            pve_stats['assists_pga'] = 0.0
            pve_stats['suicides_pga'] = 0.0
            pve_stats['suicides'] = 0
            pve_stats['resurrections_received_pga'] = 0.0
            pve_stats['resurrections_performed_pga'] = 0.0
            pve_stats['orbs_gathered_pga'] = 0.0
            pve_stats['orbs_dropped_pga'] = 0.0

            pve_stats['greatness'] = 0.0

        else:
            pve_stats['seconds_played'] = int(pve_data['secondsPlayed']['basic']['value'])
            pve_stats['longest_single_life'] = int(pve_data['longestSingleLife']['basic']['value'])
            pve_stats['average_life'] = int(pve_data['averageLifespan']['basic']['value'])

            pve_stats['kills_pga'] = pve_data['kills']['pga']['value']
            pve_stats['deaths_pga'] =  pve_data['deaths']['pga']['value']
            pve_stats['kd'] = pve_data['killsDeathsRatio']['basic']['value']
            pve_stats['longest_spree'] = int(pve_data['longestKillSpree']['basic']['value'])
            pve_stats['most_precision_kills'] = int(pve_data['mostPrecisionKills']['basic']['value'])
            pve_stats['precision_kills_pga'] = pve_data['precisionKills']['pga']['value']
            pve_stats['longest_kill'] = pve_data['longestKillDistance']['basic']['value']
            pve_stats['favorite_weapon'] = pve_data['weaponBestType']['basic']['displayValue']

            pve_stats['assists_pga'] = pve_data['assists']['pga']['value']
            logger.debug(f"pga assists: {pve_stats['assists_pga']}")
            pve_stats['suicides_pga'] = pve_data['suicides']['pga']['value']
            pve_stats['suicides'] = int(pve_data['suicides']['basic']['displayValue'])
            pve_stats['resurrections_received_pga'] = pve_data['resurrectionsReceived']['pga']['value']
            pve_stats['resurrections_performed_pga'] = pve_data['resurrectionsPerformed']['pga']['value']
            pve_stats['orbs_gathered_pga'] = pve_data['orbsGathered']['pga']['value']
            pve_stats['orbs_dropped_pga'] = pve_data['orbsDropped']['pga']['value']

            #Story missions
            try:
                story_data = self.data['story']['allTime']
            except KeyError as e:
                logger.debug(f"{member.name} GetHistoricalStats.extract_pve_stats(): no story mission data. KeyError {e}")
                pve_stats['number_story_missions'] = 0
            else:
                logger.info('getting story missions')
                pve_stats['number_story_missions'] = story_data['activitiesCleared']['basic']['value']

            #Strikes
            try:
                strike_data = self.data['allStrikes']['allTime']
            except KeyError as e:
                logger.debug(f"{member.name} GetHistoricalStats.extract_pve_stats(): no strikes. KeyError {e}")
                pve_stats['number_strikes'] = 0
            else:
                pve_stats['number_strikes'] = strike_data['activitiesCleared']['basic']['value']

            #Nightfall
            try:
                nightfall_data = self.data['nightfall']['allTime']
            except KeyError as e:
                logger.debug(f"{member.name} GetHistoricalStats.extract_pve_stats(): no nightfalls. KeyError {e}")
                pve_stats['number_nightfalls'] = 0
            else:
                pve_stats['number_nightfalls'] = nightfall_data['activitiesCleared']['basic']['value']

            #Raid clears
            try:
                raid_data =  self.data['raid']['allTime']
            except KeyError as e:
                logger.debug(f"{member.name} GetHistoricalStats.extract_pve_stats(): no raid data. KeyError {e}")
                pve_stats['number_raid_clears'] = 0
            else:
                pve_stats['number_raid_clears'] = raid_data['activitiesCleared']['basic']['value']

            pve_stats['greatness'] = self.extract_pve_greatness(pve_stats)
            logger.info(f"pve stats greatness: {pve_stats['greatness']}")
        return pve_stats


    def extract_pvp_stats(self):
        member = Member.objects.get(member_id = self.url_arguments['member_id']) #foreign key
        pvp_stats ={}
        pvp_stats['member'] = member.id
        try:
            pvp_data = self.data['allPvP']['allTime']
        except KeyError as e:
            logger.info(f"{member.name} GetHistoricalStats.extract_pvp_stats(): no PvP stats. KeyError {e}")
            pvp_stats['number_matches'] = 0
            pvp_stats['seconds_played'] = int(0)
            pvp_stats['kd'] = 0.0
            pvp_stats['favorite_weapon'] = '-'
            pvp_stats['longest_spree'] =  0
            pvp_stats['most_kills'] = 0
            pvp_stats['number_wins'] = int(0)
            pvp_stats['win_loss_ratio'] = 0.0
            pvp_stats['longest_kill'] = 0.0
            pvp_stats['suicides_pga'] = int(0)
            pvp_stats['kills_pga'] = 0.0
            pvp_stats['deaths_pga'] =   0.0
            pvp_stats['trials_number_matches'] = 0
            pvp_stats['trials_kd'] = 0.0
            pvp_stats['trials_win_loss_ratio'] = 0.0
            pvp_stats['greatness'] = 0.0
        else:
            pvp_stats['seconds_played'] = int(pvp_data['secondsPlayed']['basic']['value'])  #convert to days, hours, minutes
            pvp_stats['number_matches'] = int(pvp_data['activitiesEntered']['basic']['displayValue'])
            pvp_stats['kd'] = pvp_data['killsDeathsRatio']['basic']['value']
            pvp_stats['favorite_weapon'] = pvp_data['weaponBestType']['basic']['displayValue']
            pvp_stats['longest_spree'] = int(pvp_data['longestKillSpree']['basic']['value'])
            pvp_stats['most_kills'] = int(pvp_data['bestSingleGameKills']['basic']['value'])
            pvp_stats['number_wins'] = int(pvp_data['activitiesWon']['basic']['value'])
            try:
                pvp_stats['win_loss_ratio'] = float(pvp_data['winLossRatio']['basic']['displayValue'])
            except ValueError as e:  #no losses
                pvp_stats['win_loss_ratio'] = float(pvp_stats['number_wins'])
            pvp_stats['longest_kill'] = pvp_data['longestKillDistance']['basic']['value']
            pvp_stats['suicides_pga'] = pvp_data['suicides']['pga']['value']
            logger.debug(pvp_stats['suicides_pga'] )
            pvp_stats['kills_pga'] = pvp_data['kills']['pga']['value']
            pvp_stats['deaths_pga'] =  pvp_data['deaths']['pga']['value']
            #Trials data
            try:
                trials_data = self.data['trialsofthenine']['allTime']
            except KeyError as e:
                logger.debug(f"{member.name} GetHistoricalStats.extract_pvp_stats has not done trials. KeyError {e}.")
                pvp_stats['trials_number_matches'] = 0
                pvp_stats['trials_kd'] = 0.0
                pvp_stats['trials_win_loss_ratio'] = 0.0
            else:
                twins = trials_data['activitiesWon']['basic']['value']
                pvp_stats['trials_number_matches'] = int(trials_data['activitiesEntered']['basic']['displayValue'])
                pvp_stats['trials_kd'] = trials_data['killsDeathsRatio']['basic']['value']
                try:
                    pvp_stats['trials_win_loss_ratio'] = float(trials_data['winLossRatio']['basic']['displayValue'])
                except ValueError as e:
                    logger.debug(f"ValueError for trials w/l ratio with error e: {e}")
                    pvp_stats['trials_win_loss_ratio'] = float(twins)

            pvp_stats['greatness'] = self.extract_pvp_greatness(pvp_stats)
        return pvp_stats

    def extract_pvp_greatness(self, pvp_stats):
        """ Calculate greatness factor (TM) for pvp"""
        #General PVP component
        if pvp_stats['number_matches'] < 20:
            experience_factor = 0.05
        elif pvp_stats['number_matches'] < 50:
            experience_factor = 0.8
        else:
            experience_factor = 1.0
        try:
            weighted_skill = 0.4*pvp_stats['kd']+ 0.2*pvp_stats['win_loss_ratio'] +\
                        0.1*pvp_stats['longest_spree']/10 + 0.1*pvp_stats['most_kills']/20
        except KeyError as e:
            logger.debug(f"KeyError in GetHistoricStats.extract_pvp_greatness(): {e}")
            raise
        #Trials component
        if pvp_stats['trials_number_matches'] < 10:
            trials_experience_factor = 0.05
        elif pvp_stats['trials_number_matches'] < 25:
            trials_experience_factor = 0.8
        else:
            trials_experience_factor = 1.0
        weighted_trials_skill = .1*pvp_stats['trials_kd']/0.5 + 0.1*pvp_stats['trials_win_loss_ratio']/0.4

        greatness = experience_factor*weighted_skill + trials_experience_factor*weighted_trials_skill
        return greatness

    def extract_pve_greatness(self, pve_stats):
        """ Calculate greatness factor (TM) for pve"""
        logger.debug(pve_stats)

        #General component
        num_basics = pve_stats['number_story_missions'] + pve_stats['number_strikes']
        if num_basics < 50:
            experience_factor_basic = 0.05
        elif num_basics < 200:
            experience_factor_basic = 0.8
        else:
            experience_factor_basic = 1.0
        try:
            basic_skill = 0.15*(max([pve_stats['longest_spree']/300, 1.1])) +\
                          0.15*(max([pve_stats['precision_kills_pga']/25, 1.1])) +\
                          0.2*(max([pve_stats['kd']/35, 1.1])) +\
                          0.15*(max(pve_stats['assists_pga']/30, 1.1)) +\
                          0.1*pve_stats['resurrections_performed_pga']/1.2 +\
                          0.1*pve_stats['orbs_dropped_pga']/7 +\
                          -0.1*pve_stats['suicides_pga']/10


        except KeyError as e:
            logger.debug(f"KeyError in GetHistoricStats.extract_pve_greatness(): {e}")
            raise
        else:
            basic_contribution = experience_factor_basic * basic_skill

        #Raid component
        num_raid_clears = pve_stats['number_raid_clears']
        if num_raid_clears == 0:
            raid_contribution = 0
        elif num_raid_clears == 1 :
            raid_contribution = 0.05
        elif num_raid_clears < 5:
            raid_contribution = 0.1
        else:
            raid_contribution = 0.15

        #Nightfall
        num_nightfalls = pve_stats['number_nightfalls']
        if num_nightfalls == 0:
            nightfall_contribution = 0
        elif num_nightfalls < 10:
            nightfall_contribution =  0.05
        else:
            nightfall_contribution = 0.1


        #Nightfall component
        greatness = basic_contribution + raid_contribution + nightfall_contribution
        logger.debug(f"Greatness: {greatness}")
        return greatness

class SearchDestinyPlayer(Endpoint):
    """
    User card: minimal info like id and date joined. This is where you can get id from name.
      https://bungie-net.github.io/multi/operation_get_Destiny2-SearchDestinyPlayer.html

    Example call:
        headers = {"X-API-Key": <your d2 key>}
        search_arguments = {'membership_type': '2', 'name: 'cortical_iv'}
        my_profile = GetProfile(headers, url_arguments = search_arguments)
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


class GetProfile(Endpoint):
    """
    Get information about user's character(s): the required 'components' querystring
    request_parameters specifies the components to request.
      Endpoint:  https://bungie-net.github.io/multi/operation_get_Destiny2-GetProfile.html
      Component types:  https://bungie-net.github.io/multi/schema_Destiny-DestinyComponentType.html

    Example call:
        headers = {"X-API-Key": <your d2 key>}
        profile_arguments = {'membership_type': '2', 'member_id': '4611686018459314819'}
        components = {'components': '200'}
        my_profile = GetProfile(headers, url_arguments = profile_arguments, request_parameters = components)
    """
    def __init__(self, headers, url_arguments = None, request_parameters = None):
        super().__init__(headers, url_arguments, request_parameters)

    def make_url(self):
        membership_type = str(self.url_arguments['membership_type'])
        member_id = str(self.url_arguments['member_id'])
        url = f"{BASE_URL}{membership_type}/Profile/{member_id}/"
        logger.debug(f"Making url in GetProfile: {url}")
        return url

    def has_played_d2(self):
        try:
            error_status = self.response.json()['ErrorStatus']
        except AttributeError:
            logger.error("Error in GetProfile.has_played_d2().")
            raise
        else:
            if error_status == 'DestinyAccountNotFound':
                logger.debug(f"**User has not played d2**")
                return False
            else:
                return True

    def extract_character_info(self):
        """For compontents==200 (characters), will extract stuff for Character model:
            """
        if self.request_params['components'] is not '200':
            msg = ('GetProfile.extract_character_info() only works with character component (200)')
            logger.error(msg)
            raise TypeError(msg)
        elif not self.has_played_d2():
            logger.debug('Member has not played d2, so no characters.')
            return None
        else:
            member = Member.objects.get(member_id = self.url_arguments['member_id']) #foreign key
            user_characters = self.data['characters']['data']
            #print(user_characters)
            num_chars = len(user_characters)
            logger.debug(f"Extracting info for {num_chars} characters.")
            character_ids = list(user_characters.keys())
            character_list = []
            character_times = []
            character_lights = []
            character_last_played = []
            for character_id in character_ids:
                data = user_characters[character_id]
                character_info = {}
                character_info['member'] = member.id
                character_info['character_id'] = character_id
                character_info['race'] = RACE_ENUM[data['raceType']]
                character_info['gender'] = GENDER_ENUM[data['genderType']]
                character_info['character_class'] = CLASS_ENUM[data['classType']]
                character_info['light'] = data['light']
                character_info['level'] = data['levelProgression']['level']
                character_info['emblem_path'] = data['emblemPath']
                character_info['date_last_played'] = dateutil.parser.parse(data['dateLastPlayed'])
                character_info['minutes_played'] = data['minutesPlayedTotal']
                character_list.append(character_info)
                character_times.append(int(data['minutesPlayedTotal']))
                character_lights.append(int(data['light']))
                character_last_played.append(character_info['date_last_played'])
                logger.debug(f"character_info: {character_info}")
            total_time = sum(character_times)
            max_light = max(character_lights)
            date_last_played = max(character_last_played)
            return (character_list, total_time, max_light, date_last_played)



class GetGroup(Endpoint):
    """
    Generic info about clan, like motto:
      https://bungie-net.github.io/multi/operation_get_GroupV2-GetGroup.html

    Example call:
        headers = {"X-API-Key": <your d2 key>}
        group_arguments = {'group_id': '623172'}
        my_profile = GetProfile(headers, url_arguments = group_arguments)
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
        clan_info['creation_date'] = dateutil.parser.parse(clan_details['creationDate'])
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

    Example call:
        headers = {"X-API-Key": <your d2 key>}
        members_arguments = {'group_id': '623172'}
        my_profile = GetProfile(headers, url_arguments = members_arguments)
    """
    def __init__(self, headers, url_arguments = None, request_parameters = None):
        super().__init__(headers, url_arguments, request_parameters)
        self.member_list = self.extract_clan_list()

    def make_url(self):
        group_id = self.url_arguments['group_id']
        url = f"{BASE_URL_GROUP}{group_id}/Members/?currentPage=1"
        return url

    def extract_clan_list(self):
        """
        Makes list of dictionaries, one for each member: this is for insertion
        of user data into a form.
        """
        try:
            self.data['results']
        except KeyError:
            logger.error("GetMembersOfGroup.extract_clan_list(): No results in GetMembersOfGroup instance.")
            return

        clan = Clan.objects.get(clan_id = GROUP_ID)
        member_list = []
        for member in self.data['results']:
            clan_member = {}
            clan_member['clan'] = clan.id
            clan_member['membership_type'] = member['destinyUserInfo']['membershipType']
            clan_member['name'] = member['destinyUserInfo']['displayName']
            clan_member['member_id'] = member['destinyUserInfo']['membershipId']
            clan_member['date_joined']  = dateutil.parser.parse(member['joinDate'])
            member_list.append(clan_member)
        return member_list

    def print_clan_list(self):
        """Useful for debugging"""
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
HELPER FUNCTIONS
"""
def bind_and_save(Model, data, Form, **instance_kwargs):
    """
    Bind 'data' to django 'Form' corresponding to 'Model' class.
    Then validate, and save. If model instance (uniquely specified
    by '**instance_kwargs' dictionary) exists, update row; otherwise create row.
    E.g., **instance_kwargs could be {clan_id: '12323'}
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







#

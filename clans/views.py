from django.shortcuts import render

import requests
import logging

from django import forms
import d2api.utils as api
from .forms import ClanForm
from .models import Clan
from d2api.constants import GROUP_ID, D2_HEADERS


"""
Set up logger: for now just print everything to stdout.
"""
logging.basicConfig(level = logging.INFO,
                    format = '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt =' %m/%d/%y %H:%M:%S')
logger = logging.getLogger(__name__)



# Create your views here.
def index(request):
    """Home page for salted vex milk"""
    if request.method == 'POST':
        with requests.Session() as session:
            session.headers.update(D2_HEADERS)

            #Functionalize the following you will use it for each end point
            group_url = api.get_group_url(GROUP_ID)
            logging.info(f"Retreiving info about clan. URL: {group_url}")
            try:
                group_data = api.destiny2_api_handler(group_url, session)
            except Exception as err:
                logging.exception(f"Error getting clan data for {GROUP_ID}.\nException: {err}.")
            else:
                clan_info = api.extract_clan_info(group_data)
                #Someone suggested pushing the following into the Form instead of the view
                try:
                    clan_instance = Clan.objects.get(clan_id = clan_info['clan_id'])
                except Clan.DoesNotExist:
                    logging.debug("Adding clan to db.")
                    clan_form_bound = ClanForm(clan_info)
                else:
                    logging.debug("Clan already exists: updating.")
                    clan_form_bound = ClanForm(clan_info, instance = clan_instance)


                if clan_form_bound.is_valid():
                    clan_form_bound.save()
                    logging.debug("Clan successfully saved.")
                else:
                    logging.error(f"clan form not valid. error: {clan_form_bound.errors}")
                    raise forms.ValidationError(f"Clan info not valid: {clan_form_bound.errors}")

    else:
        logging.debug("GET request in view.index: just display data.")

    #need try/except in case object doesn't exist yet
    try:
        clan_instance = Clan.objects.get(clan_id = GROUP_ID)
        context = {'clan': clan_instance}
    except:
        context = {}
    return render(request, 'clans/index.html', context) # 'index.html', {'update_clan_form': update_clan_form})


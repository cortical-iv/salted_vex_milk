import requests
import logging
from django.shortcuts import render

from django import forms
import d2api.utils as api
from .forms import MemberForm
from .models import Member
from clans.models import Clan
from d2api.constants import GROUP_ID, D2_HEADERS


"""
Set up logger: for now just print everything to stdout.
"""
logging.basicConfig(level = logging.INFO,
                    format = '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt =' %m/%d/%y %H:%M:%S')
logger = logging.getLogger(__name__)





# Create your views here.
def members(request):
    """Home page for salted vex milk"""
    if request.method == 'POST':
        with requests.Session() as session:
            session.headers.update(D2_HEADERS)
            #Functionalize the following you will use it for each end poin
            members_url = api.get_members_of_group_url(GROUP_ID)
            logging.info(f"Retreiving group members. URL: {members_url}")
            try:
                members_data = api.destiny2_api_handler(members_url, session)
            except Exception as err:
                logging.exception(f"Error getting clan members for {GROUP_ID}.\nException: {err}.")
            else:
                members = api.extract_member_list(members_data)
                logging.info("members list extracted")
                #insert each member into database
                for member in members:
                    logging.info(f"deep in views member: {member}")
                    name = member['name']
                    try:
                        member_instance = Member.objects.get(member_id = member['member_id'],
                                                             membership_type = member['membership_type'])
                    except Member.DoesNotExist:
                        logging.info(f"Adding {name} to db.")
                        member_form_bound = MemberForm(member)
                    else:
                        logging.info(f"{name} already exists: updating.")
                        member_form_bound = MemberForm(member, instance = member_instance)


                    if member_form_bound.is_valid():
                        member_form_bound.save()
                        logging.info(f"{name} successfully saved.")
                    else:
                        logging.error(f"member form not valid. error: {member_form_bound.errors}.\nMember data: {member}")
                        logging.info(f"Member bound form: {member_form_bound}")
                        raise forms.ValidationError(f"Member info not valid: {member_form_bound.errors}")


    else:
        logging.info("GET request in members/members.html: just display data.")


    all_members = Member.objects.all()
    context = {'members': all_members}
    return render(request, 'members/members.html', context) # 'index.html', {'update_clan_form': update_clan_form})
import logging

from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import Member
from .tables import MemberTable
from clans.models import Clan
from d2api.constants import GROUP_ID
from django.conf import settings

"""
Set up logger: for now just print everything to stdout.
"""
logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt =' %m/%d/%y %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Create your views here.
def members(request):
    """Page showing member information"""
    logger.debug(f"DEBUG: {settings.DEBUG}")
    all_members = Member.objects.all().order_by('date_joined')
    latest_update = all_members.latest('updated').updated
    member_table = MemberTable(all_members)
    RequestConfig(request, paginate={'per_page':10}).configure(member_table)
    logger.debug(f"Rendering members page in members.views w/refresh datetime: {latest_update}")
    clan = Clan.objects.get(clan_id = GROUP_ID)
    context = {'member_table': member_table, 'updated': latest_update, 'clan': clan}
    return render(request, 'members/members.html', context)


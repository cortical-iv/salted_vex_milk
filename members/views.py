import logging

from django.shortcuts import render, get_object_or_404
from django.http import Http404

from django_tables2 import RequestConfig

from .models import Member
from .tables import MemberTable
from clans.models import Clan
from d2api.constants import GROUP_ID


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
    
    all_members = Member.objects.all().order_by('-date_last_played')
    logger.debug(f"All_members: {all_members}")
    if not all_members:
        raise Http404("No members in database yet.")
    try:
        latest_update = all_members.latest('updated').updated
    except:
        latest_update = None
    member_table = MemberTable(all_members)
    RequestConfig(request, paginate={'per_page':10}).configure(member_table)
    logger.debug(f"Rendering members page in members.views w/refresh datetime: {latest_update}")
    clan = get_object_or_404(Clan, clan_id = GROUP_ID)
    context = {'member_table': member_table, 'updated': latest_update, 'clan': clan}
    return render(request, 'members/members.html', context)


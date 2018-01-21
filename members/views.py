import logging

from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import Member
from .tables import MemberTable



"""
Set up logger: for now just print everything to stdout.
"""
logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt =' %m/%d/%y %H:%M:%S')
logger_memberview = logging.getLogger(__name__)
logger_memberview.setLevel(logging.DEBUG)

# Create your views here.
def members(request):
    """Page showing member information"""
    all_members = Member.objects.all().order_by('date_joined')
    latest_update = all_members.latest('updated').updated
    member_table = MemberTable(all_members)
    RequestConfig(request, paginate={'per_page':100}).configure(member_table)
    logger_memberview.debug(f"Rendering members page in members.views w/refresh datetime: {latest_update}")

    context = {'member_table': member_table, 'updated': latest_update}
    return render(request, 'members/members.html', context)

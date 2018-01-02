import logging

from django.shortcuts import render
from .models import Member



"""
Set up logger: for now just print everything to stdout.
"""
logging.basicConfig(level = logging.DEBUG,  #DEBUG, INFO
                    format = '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt =' %m/%d/%y %H:%M:%S')
logger_memberview = logging.getLogger(__name__)


# Create your views here.
def members(request):
    """Page showing member information"""
    all_members = Member.objects.all().order_by('date_joined')
    updated = all_members.last().updated
    logger_memberview.debug(f"Rendering members page with refresh datetime: {updated}")

    context = {'members': all_members, 'updated': updated}
    return render(request, 'members/members.html', context)
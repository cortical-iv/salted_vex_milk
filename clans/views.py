from django.shortcuts import render

import logging


from .models import Clan
from d2api.constants import GROUP_ID

"""
Set up logger: for now just print everything to stdout.
"""
logging.basicConfig(level = logging.INFO,
                    format = '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt =' %m/%d/%y %H:%M:%S')
logger_clanview = logging.getLogger(__name__)
logger_clanview.setLevel(logging.INFO)


# Create your views here.
def index(request):
    """Home page for salted vex milk"""
    logger_clanview.debug("Rendering home page in clans.views")
    try:
        clan_instance = Clan.objects.get(clan_id = GROUP_ID)
        context = {'clan': clan_instance}
    except:
        context = {}
    return render(request, 'clans/index.html', context) # 'index.html', {'update_clan_form': update_clan_form})


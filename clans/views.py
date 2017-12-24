from django.shortcuts import render

import logging


from django.core import management
from .models import Clan
from d2api.constants import GROUP_ID

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
        logging.info("Pulling clan data, about to call refresh_clans")
        management.call_command('refresh_clans')
    else:
        logging.debug("GET request in view.index: just display data.")

    try:
        clan_instance = Clan.objects.get(clan_id = GROUP_ID)
        context = {'clan': clan_instance}
    except:
        context = {}
    return render(request, 'clans/index.html', context) # 'index.html', {'update_clan_form': update_clan_form})


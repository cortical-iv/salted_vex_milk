from django.shortcuts import render
import logging

from members.models import Member
from .models import Character
from salted_vex_milk.utils import render_minutes


"""
Set up logger: for now just print everything to stdout.
"""
logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt =' %m/%d/%y %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create your views here.
def characters(request, name='cortical_iv'):
    """Page showing member information"""
    member = Member.objects.get(name=name)
    characters = Character.objects.filter(member=member.id)
    logger.debug(f"Checking member {name} and joined {member.date_joined}. They have {len(characters)} characters.")
    if member.has_played_d2:
        updated = characters.first().updated
    else:
        updated = None

    context = {'member': member, 'characters': characters, 'updated': updated}
    return render(request, 'characters/characters.html', context)




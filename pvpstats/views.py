from django.shortcuts import render
import logging
from django_tables2 import RequestConfig

#from members.models import Member
from .models import PvpStats
import pvpstats.tables as stats_tables
#from .tables import PvpStatsTable


"""
Set up logger: for now just print everything to stdout.
"""
logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt =' %m/%d/%y %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create your views here.
def pvpstats(request, stat = 'kd'):
    """Page showing member information"""
    all_stats = PvpStats.objects.all()
    latest_update = all_stats.latest('updated').updated

    if stat is 'kd':
        pvpstats_table = stats_tables.KdTable(all_stats)
    else:
        pvpstats_table = stats_tables.PvpStatsTable(all_stats)
    #pvpstats_table.Meta.fields = stat
    RequestConfig(request, paginate={'per_page':25}).configure(pvpstats_table)

    context = {'pvpstats_table': pvpstats_table, 'updated': latest_update}
    return render(request, 'pvpstats/pvpstats.html', context)




#def members(request):
#    """Page showing member information"""
#    all_stats = Member.objects.all().order_by('date_joined')
#    latest_update = all_members.latest('updated').updated
#    pvpstats_ta = MemberTable(all_members)
#    RequestConfig(request, paginate={'per_page':25}).configure(member_table)
#    logger_memberview.debug(f"Rendering members page in members.views w/refresh datetime: {latest_update}")
#
#    context = {'member_table': member_table, 'updated': latest_update}
#    return render(request, 'members/members.html', context)


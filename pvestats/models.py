from django.db import models
from members.models import Member

# Create your models here.
class PveStats(models.Model):
    """
    PvE stats for clan members. Each row has MEMBER as a reference field. This is
    the real point of it all!
    """
    member = models.OneToOneField(Member, on_delete = models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    greatness = models.FloatField(null = True)
    number_strikes = models.IntegerField(null=True)
    number_story_missions = models.IntegerField(null=True)
    number_nightfalls = models.IntegerField(null=True)
    number_prestige_nightfalls = models.IntegerField(null=True)
    number_raid_clears = models.IntegerField(null=True)


    seconds_played =  models.IntegerField(null=True)
    longest_single_life = models.IntegerField(null=True)
    average_life = models.IntegerField(null=True)

    kills_pga = models.FloatField(null=True)
    deaths_pga = models.FloatField(null=True)
    kd = models.FloatField(null=True)
    longest_spree = models.IntegerField(null=True)

    most_precision_kills = models.IntegerField(null=True)
    precision_kills_pga = models.FloatField(null=True)
    longest_kill = models.FloatField(null=True)
    favorite_weapon = models.CharField(max_length = 20, null=True)

    assists_pga = models.FloatField(null=True)
    suicides_pga = models.FloatField(null=True)
    suicides = models.IntegerField(null=True)
    resurrections_received_pga = models.FloatField(null=True)
    resurrections_performed_pga = models.FloatField(null=True)
    orbs_dropped_pga = models.FloatField(null=True)
    orbs_gathered_pga = models.FloatField(null=True)

#    greatness = models.FloatField(null=True)



    class Meta:
        verbose_name_plural = "PvE Stats"

    def __str__(self):
        return f"{self.member.name} PvE Stats"

    def __repr__(self):
        return f"{self.member.name} PvE Stats"



#        pve_stats['number_activities'] = int(pve_data['activitiesEntered']['basic']['displayValue'])
#        pve_stats['activities_cleared'] = int(pve_data['activitiesCleared']['basic']['displayValue'])
#        pve_stats['heroic_public_events'] = int(pve_data['heroicPublicEventsCompleted']['basic']['displayValue'])
#        pve_stats['adventures'] = int(pve_data['adventuresCompleted']['basic']['displayValue'])
#
#        pve_stats['seconds_played'] = int(pve_data['secondsPlayed']['basic']['value'])  #convert to days, hours, minutes
#        pve_stats['longest_single_life'] = int(pve_data['longestSingleLife']['basic']['value'])
#        pve_stats['average_life'] = pve_data['averageLifespan']['basic']['value']
#
#        pve_stats['kills_pga'] = float(pve_data['kills']['pga']['displayValue'])
#        pve_stats['deaths_pga'] =  float(pve_data['deaths']['pga']['displayValue'])
#        pve_stats['kd'] = float(pve_data['killsDeathsRatio']['basic']['displayValue'])
#        pve_stats['longest_spree'] = int(pve_data['longestKillSpree']['basic']['value'])

#        pve_stats['most_precision_kills'] = int(pve_data['mostPrecisionKills']['basic']['value'])
#        pve_stats['precision_kills_pga'] = float(pve_data['precisionKills']['pga']['displayValue'])
#        pve_stats['longest_kill'] = float(pve_data['longestKillDistance']['basic']['displayValue'])
#        pve_stats['favorite_weapon'] = pve_data['weaponBestType']['basic']['displayValue']
#
#
#        pve_stats['suicides_pga'] = float(pve_data['suicides']['pga']['displayValue'])
#        pve_stats['suicides'] = int(pve_data['suicides']['basic']['displayValue'])
#        pve_stats['resurrections_received_pga'] = float(pve_data['resurrectionsReceived']['pga']['displayValue'])
#        pve_stats['resurrections_performed_pga'] = float(pve_data['resurrectionsPerformed']['pga']['displayValue'])
#        pve_stats['orbs_gathered_pga'] = float(pve_data['orbsGathered']['pga']['displayValue'])
#        pve_stats['orbs_dropped_pga'] = float(pve_data['orbsDropped']['pga']['displayValue'])
#


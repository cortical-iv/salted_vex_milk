from django.db import models
from clans.models import Clan

# Create your models here.
class Member(models.Model):
    """Data about individual clan members, like join date, member_id, and name.
    Each member has clan_id as a foreign key. Doesn't include game stats."""
    clan = models.ForeignKey(Clan, on_delete = models.CASCADE)
    member_id = models.CharField(unique=True, max_length = 20)
    name = models.CharField(blank=False, null=False, max_length = 16)
    date_joined = models.DateTimeField()
    membership_type = models.IntegerField()
    has_played_d2 = models.BooleanField(default = False)
    updated = models.DateTimeField(auto_now=True)
    max_light = models.IntegerField(blank=True, null=True)
    minutes_played = models.IntegerField(blank=True, null=True)
    date_last_played = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('member_id', 'membership_type') #need both to uniquely identify players

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

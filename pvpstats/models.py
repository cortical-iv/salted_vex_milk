from django.db import models
from members.models import Member

# Create your models here.
class PvpStats(models.Model):
    """
    PvP stats for clan member. Each row has MEMBER as a foreign key. This is
    the real point of it all!
    """
    member = models.OneToOneField(Member, on_delete = models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    number_matches = models.IntegerField()
    seconds_played =  models.IntegerField()
    kd = models.FloatField()
    favorite_weapon = models.CharField(max_length = 20)
    longest_spree = models.IntegerField()
    most_kills = models.IntegerField()

    class Meta:
        verbose_name_plural = "PvP Stats"

    def __str__(self):
        return f"{self.member.name} PvP Stats"

    def __repr__(self):
        return f"{self.member.name} PvP Stats"




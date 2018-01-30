from django.db import models
from members.models import Member

# Create your models here.
class Character(models.Model):
    """Data about individual character, like id, [light/power] level, and
    date last played. Doesn't include game stats. Each character has a
    MEMBER as a foreign key. Doesn't include game stats."""
    member = models.ForeignKey(Member, on_delete = models.CASCADE)
    character_id = models.CharField(unique=True, max_length = 20)
    character_class = models.CharField(blank=False, null=False, max_length = 16)
    light = models.IntegerField()
    level = models.IntegerField()
    race = models.CharField(max_length = 16)
    gender = models.CharField(max_length = 6)
    emblem_path = models.CharField(max_length = 200)
    date_last_played = models.DateTimeField()
    minutes_played = models.IntegerField()
    updated = models.DateTimeField(auto_now=True)



    class Meta:
        unique_together = ('member', 'character_id') #need both to uniquely identify players

    def __str__(self):
        return f"{self.member.name} character {self.character_id}"

    def __repr__(self):
        return f"{self.member.name} character {self.character_id}"


from django.db import models
#from d2api.constants import GROUP_ID, D2_HEADERS, BASE_URL, BASE_URL_GROUP


# Create your models here.
class Clan(models.Model):
    """Generic information about the clan, like date created and number of members.
    Also includes date this information was pulled."""
    clan_id = models.IntegerField(unique=True, blank=False, null=False)
    name = models.CharField(unique=True, blank=False, null=False, max_length = 200)
    call_sign = models.CharField(max_length = 10, null=True)
    creation_date = models.CharField(max_length = 100) #DateTimeField()
    description = models.TextField()
    motto = models.CharField(max_length = 200)
    num_members = models.IntegerField()
    founder = models.CharField(max_length = 16)
    updated = models.DateTimeField(auto_now = True)

    class Meta:
        unique_together = ('name', 'clan_id')

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
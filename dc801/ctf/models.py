from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class CTF_Game(models.Model):
    name        = models.CharField(max_length=254)
    start_time  = models.DateTimeField('Date Game Starts')
    end_time    = models.DateTimeField('Date Game Ends')
    description = models.CharField(max_length=254)


class Flag(models.Model):

    flag    = models.CharField(max_length=254)
    notes   = models.CharField(max_length=254)
    game_id = models.IntegerField(default=0)

    def __unicode__(self):
        return self.flag
    
class Capture(models.Model):
    flag            = models.ForeignKey(Flag)
    capture_date    = models.DateTimeField('Date flags was captured')
    user            = models.ForeignKey(User)


# Create your models here.

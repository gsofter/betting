from django.db import models
from django.urls import reverse
# Create your models here.

class ATPPlayer(models.Model):
    rank   = models.IntegerField()
    max_rank = models.IntegerField(null=True)   #0 : CH -1: NCH
    name    = models.CharField(max_length=50)    
    age = models.IntegerField(null=True)
    country = models.CharField(max_length=50)
    pts = models.IntegerField(null=True)
    inc_pts = models.IntegerField(null=True)
    dec_pts = models.IntegerField(null=True)
    cur_tournament = models.CharField(max_length=50, null=True)
    prev_tournament = models.CharField(max_length=50, null=True)
    next_pts = models.IntegerField(null=True)
    max_pts = models.IntegerField(null=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("player:player_edit", kwargs={'pk': self.pk})

class WTAPlayer(models.Model):
    rank   = models.IntegerField()
    max_rank = models.IntegerField(null=True)   #0 : CH -1: NCH
    name    = models.CharField(max_length=50)    
    age = models.IntegerField(null=True)
    country = models.CharField(max_length=50)
    pts = models.IntegerField(null=True)
    inc_pts = models.IntegerField(null=True)
    dec_pts = models.IntegerField(null=True)
    cur_tournament = models.CharField(max_length=50, null=True)
    prev_tournament = models.CharField(max_length=50, null=True)
    next_pts = models.IntegerField(null=True)
    max_pts = models.IntegerField(null=True)

    def __str__(self):
        return self.name

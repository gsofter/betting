from django.db import models

# Create your models here.

class ATPTournament(models.Model):
    round = models.CharField(max_length=50, null=True)
    date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length = 50, null = True)
    location = models.CharField(max_length = 50, null = True)
    series = models.CharField(max_length = 50, null = True)
    surface = models.CharField(max_length = 50, null = True)
    price = models.CharField(max_length = 50, null=True)
    nicknames = models.CharField(max_length = 50, null=True)
    year = models.IntegerField(null=True, default=0)
    def __str__(self):
        return self.name + ' ' + self.location

class WTATournament(models.Model):
    round = models.CharField(max_length=50, null=True)
    date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length = 50, null = True)
    location = models.CharField(max_length = 50, null = True)
    series = models.CharField(max_length = 50, null = True)
    surface = models.CharField(max_length = 50, null = True)
    price = models.CharField(max_length = 50, null=True)
    nicknames = models.CharField(max_length = 50, null=True)
    year = models.IntegerField(null=True, default=0)
    def __str__(self):
        return self.name + ' ' + self.location
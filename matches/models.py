from django.db import models
from django.utils import timezone

# Create your models here.
class ATPMatch(models.Model):
    #general match data
    date = models.DateTimeField(blank=True, null=True)  #Match Date
    round = models.CharField(max_length=20, null=True)  #Match rounds
    tournament = models.CharField(max_length=50, null=True) #Tournament name
    location = models.CharField(max_length=50, null=True) #Location name
    court = models.CharField(max_length=50, null=True)
    surface = models.CharField(max_length=50, null=True)
    winner = models.CharField(max_length = 50, null=True) ## of games in the match
    loser = models.CharField(max_length = 50, null=True) ## of games in the match
    home_r1 = models.IntegerField( null=True) #Number of games won in the match by Home player
    away_r1 = models.IntegerField( null=True) #Number of games won in the match by Away player
    home_r2 = models.IntegerField( null=True) #Number of games won in the match by Home player
    away_r2 = models.IntegerField( null=True) #Number of games won in the match by Away player
    home_r3 = models.IntegerField( null=True) #Number of games won in the match by Home player
    away_r3 = models.IntegerField( null=True) #Number of games won in the match by Away player
    home_r4 = models.IntegerField( null=True) #Number of games won in the match by Home player
    away_r4 = models.IntegerField( null=True) #Number of games won in the match by Away player
    home_r5 = models.IntegerField( null=True) #Number of games won in the match by Home player
    away_r5 = models.IntegerField( null=True) #Number of games won in the match by Away player
    home_winsets = models.IntegerField( null=True) #Number of sets won by Home player
    away_winsets = models.IntegerField( null=True) #Number of sets won by Away player
    totalsets = models.IntegerField(null=True) # wsets + lsets
    totalgames = models.IntegerField(null=True) # w1 + l1 + w2 + l2 + w3 + l3 + w4 + l4 + w5 + l5
    bestof = models.IntegerField(null=True)    # 3 , 5
    comment = models.CharField(max_length=50, null=True) #Number of sets won by Away player
    status = models.CharField(max_length = 50, null=True)
    
    #home, away player
    home = models.CharField(max_length=50, null=True)
    away = models.CharField(max_length=50, null=True)
    
    #Home player match performance data
    home_aces = models.CharField(max_length=50, null=True) #Home player Aces
    home_doublefault = models.CharField(max_length=50, null=True) #Home player Double Fault
    home_ser1 = models.IntegerField(null=True)    #Home player 1st Serve points Won
    home_ser2 = models.IntegerField(null=True)    #Home player 2nd Serve points Won
    home_ser = models.IntegerField(null=True)    #Home player Serve games won
    home_rec = models.IntegerField(null=True)   #Home player recevier points won
    home_total = models.IntegerField(null=True) #Home player total game points
    
    #Away player match performance data
    away_aces = models.CharField(max_length=50, null=True)    #Away player Aces
    away_doublefault = models.CharField(max_length=50, null=True) # Away player Double Default
    away_ser1 = models.IntegerField(null=True)  #Away player 1St Serve Points won
    away_ser2 = models.IntegerField(null=True)  #Away player 2nd Server Points won
    away_ser = models.IntegerField(null=True)  #Away player Serve won games
    away_rec = models.IntegerField(null=True)   #Away player receiver points won
    away_total = models.IntegerField(null=True) #Away player total points won

    #odds data
    home_b365 = models.FloatField(blank=True, null=True)     # bet365 Home player odds
    away_b365 = models.FloatField( blank=True, null=True)    # bet365 Away player odds
    home_ps = models.FloatField( blank=True, null=True)     # Pinnacles Sports odds of match Home player
    away_ps = models.FloatField( blank=True, null=True)     # Pinnacles Sports odds of match Away player
    home_winamax = models.FloatField( blank=True, null=True)    # Winamax Sports odds of match Home player
    away_winamax = models.FloatField( blank=True, null=True)    # Winamax Sports odds of match Away player
    
    home_unibet = models.FloatField( blank=True, null=True)    # Unibet  Sports odds of match Home player
    away_unibet = models.FloatField( blank=True, null=True)    # Unibet  Sports odds of match Away player
    home_betclic = models.FloatField( blank=True, null=True)    # Betclic.fr  Sports odds of match Home player
    away_betclic = models.FloatField( blank=True, null=True)    # Betclic.fr  Sports odds of match Away player
    
    home_max = models.FloatField( blank=True, null=True)    # Sports odds of average odds of match Home player
    away_max = models.FloatField( blank=True, null=True)    # Sports odds of average odds of match Away player
    home_avg = models.FloatField( blank=True, null=True)    # Sports odds of average odds of match Home player
    away_avg = models.FloatField( blank=True, null=True)    # Sports odds of average odds of match Away player
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.home + " vs " + self.away

class WTAMatch(models.Model):
    #general match data
    date = models.DateTimeField(blank=True, null=True)  #Match Date
    round = models.CharField(max_length=50, null=True)  #Match rounds
    tournament = models.CharField(max_length=50, null=True) #Tournament name
    location = models.CharField(max_length=50, null=True) #Location name
    court = models.CharField(max_length=50, null=True)
    surface = models.CharField(max_length=50, null=True)
    winner = models.CharField(max_length = 50, null=True) ## of games in the match
    loser = models.CharField(max_length = 50, null=True) ## of games in the match
    home_r1 = models.IntegerField( null=True) #Number of games won in the match by Home player
    away_r1 = models.IntegerField( null=True) #Number of games won in the match by Away player
    home_r2 = models.IntegerField( null=True) #Number of games won in the match by Home player
    away_r2 = models.IntegerField( null=True) #Number of games won in the match by Away player
    home_r3 = models.IntegerField( null=True) #Number of games won in the match by Home player
    away_r3 = models.IntegerField( null=True) #Number of games won in the match by Away player
    home_r4 = models.IntegerField( null=True) #Number of games won in the match by Home player
    away_r4 = models.IntegerField( null=True) #Number of games won in the match by Away player
    home_r5 = models.IntegerField( null=True) #Number of games won in the match by Home player
    away_r5 = models.IntegerField( null=True) #Number of games won in the match by Away player
    home_winsets = models.IntegerField( null=True) #Number of sets won by Home player
    away_winsets = models.IntegerField( null=True) #Number of sets won by Away player
    totalsets = models.IntegerField(null=True) # wsets + lsets
    totalgames = models.IntegerField(null=True) # w1 + l1 + w2 + l2 + w3 + l3 + w4 + l4 + w5 + l5
    bestof = models.IntegerField(null=True)    # 3 , 5
    comment = models.CharField(max_length=50, null=True) #Number of sets won by Away player
    status = models.CharField(max_length = 50, null=True)
    
    #home, away player
    home = models.CharField(max_length=50, null=True)
    away = models.CharField(max_length=50, null=True)
    
    #Home player match performance data
    home_aces = models.CharField(max_length=50, null=True) #Home player Aces
    home_doublefault = models.CharField(max_length=50, null=True) #Home player Double Fault
    home_ser1 = models.IntegerField(null=True)    #Home player 1st Serve points Won
    home_ser2 = models.IntegerField(null=True)    #Home player 2nd Serve points Won
    homs_ser = models.IntegerField(null=True)    #Home player Serve games won
    home_rec = models.IntegerField(null=True)   #Home player recevier points won
    home_total = models.IntegerField(null=True) #Home player total game points
    
    #Away player match performance data
    away_aces = models.CharField(max_length=50, null=True)    #Away player Aces
    away_doublefault = models.CharField(max_length=50, null=True) # Away player Double Default
    away_ser1 = models.IntegerField(null=True)  #Away player 1St Serve Points won
    away_ser2 = models.IntegerField(null=True)  #Away player 2nd Server Points won
    away_ser = models.IntegerField(null=True)  #Away player Serve won games
    away_rec = models.IntegerField(null=True)   #Away player receiver points won
    away_total = models.IntegerField(null=True) #Away player total points won

    #odds data
    home_b365 = models.FloatField(blank=True, null=True)     # bet365 Home player odds
    away_b365 = models.FloatField( blank=True, null=True)    # bet365 Away player odds
    home_ps = models.FloatField( blank=True, null=True)     # Pinnacles Sports odds of match Home player
    away_ps = models.FloatField( blank=True, null=True)     # Pinnacles Sports odds of match Away player
    home_winamax = models.FloatField( blank=True, null=True)    # Winamax Sports odds of match Home player
    away_winamax = models.FloatField( blank=True, null=True)    # Winamax Sports odds of match Away player
    home_unibet = models.FloatField( blank=True, null=True)    # Unibet  Sports odds of match Home player
    away_unibet = models.FloatField( blank=True, null=True)    # Unibet  Sports odds of match Away player
    home_betclic = models.FloatField( blank=True, null=True)    # Betclic.fr  Sports odds of match Home player
    away_betclic = models.FloatField( blank=True, null=True)    # Betclic.fr  Sports odds of match Away player
    
    home_max = models.FloatField( blank=True, null=True)    # Sports odds of average odds of match Home player
    away_max = models.FloatField( blank=True, null=True)    # Sports odds of average odds of match Away player
    created_at = models.DateTimeField(auto_now_add=True)
    home_avg = models.FloatField( blank=True, null=True)    # Sports odds of average odds of match Home player
    away_avg = models.FloatField( blank=True, null=True)    # Sports odds of average odds of match Away player
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.home + " vs " + self.away
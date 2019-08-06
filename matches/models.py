from django.db import models
# Create your models here.
class Match(models.Model):
    atp         = models.IntegerField()
    location    = models.CharField(max_length=50)
    tournament  = models.CharField(max_length=50)
    date        = models.DateTimeField(blank=True, null=True)
    series = models.CharField(max_length=50, blank=True, null=True)
    court = models.CharField(max_length=50, blank=True, null=True)
    surface = models.CharField(max_length=50, blank=True, null=True)
    round = models.CharField(max_length=50, blank=True, null=True)
    bestof = models.IntegerField(blank=True, null=True)
    winner = models.CharField(max_length=50, blank=True, null=True)
    loser = models.CharField(max_length=50, blank=True, null=True)
    wrank = models.IntegerField(blank=True, null=True)
    lrank = models.IntegerField(blank=True, null=True)
    wpts = models.IntegerField(blank=True, null=True)
    lpts = models.IntegerField(blank=True, null=True)
    w1 = models.IntegerField(blank=True, null=True)
    l1 = models.IntegerField(blank=True, null=True)
    w2 = models.IntegerField(blank=True, null=True)
    l2 = models.IntegerField(blank=True, null=True)
    w3 = models.IntegerField(blank=True, null=True)
    l3 = models.IntegerField(blank=True, null=True)
    w4 = models.IntegerField(blank=True, null=True)
    l4 = models.IntegerField(blank=True, null=True)
    w5 = models.IntegerField(blank=True, null=True)
    l5 = models.IntegerField(blank=True, null=True)
    wsets = models.IntegerField(blank=True, null=True)
    lsets = models.IntegerField(blank=True, null=True)
    comment = models.CharField(max_length=50, blank=True, null=True)
    b365w = models.FloatField(blank=True, null=True)
    b356l = models.FloatField( blank=True, null=True)
    psw = models.FloatField( blank=True, null=True)
    psl = models.FloatField( blank=True, null=True)
    maxw = models.FloatField( blank=True, null=True)
    maxl = models.FloatField( blank=True, null=True)
    avgw = models.FloatField( blank=True, null=True)
    avgl = models.FloatField( blank=True, null=True)

    def __str__(self):
        return self.winner + " vs " + self.loser

class ATPMatch(models.Model):
    #general match data
    date = models.DateTimeField(blank=True, null=True)  #Match Date
    round = models.CharField(max_length=20, null=True)  #Match rounds
    tournament = models.CharField(max_length=50, null=True) #Tournament name
    location = models.CharField(max_length=50, null=True) #Location name
    winner = models.CharField(max_length = 20, null=True) ## of games in the match
    loser = models.CharField(max_length = 20, null=True) ## of games in the match
    w1 = models.IntegerField( null=True) #Number of games won in the match by winner
    l1 = models.IntegerField( null=True) #Number of games won in the match by loser
    w2 = models.IntegerField( null=True) #Number of games won in the match by winner
    l2 = models.IntegerField( null=True) #Number of games won in the match by loser
    w3 = models.IntegerField( null=True) #Number of games won in the match by winner
    l3 = models.IntegerField( null=True) #Number of games won in the match by loser
    w4 = models.IntegerField( null=True) #Number of games won in the match by winner
    l4 = models.IntegerField( null=True) #Number of games won in the match by loser
    w5 = models.IntegerField( null=True) #Number of games won in the match by winner
    l5 = models.IntegerField( null=True) #Number of games won in the match by loser
    wsets = models.IntegerField( null=True) #Number of sets won by winner
    lsets = models.IntegerField( null=True) #Number of sets won by loser
    totalsets = models.IntegerField(null=True) # wsets + lsets
    totalgames = models.IntegerField(null=True) # w1 + l1 + w2 + l2 + w3 + l3 + w4 + l4 + w5 + l5
    bestof = models.IntegerField(null=True)    # 3 , 5
    comment = models.CharField(max_length=50, null=True) #Number of sets won by loser
    status = models.CharField(max_length = 50, null=True)
    
    #home, away player
    home = models.CharField(max_length=50, null=True)
    away = models.CharField(max_length=50, null=True)
    
    #winner match performance data
    waces = models.CharField(max_length=50, null=True) #Winner Aces
    wdfault = models.CharField(max_length=50, null=True) #Winner Double Fault
    wser1 = models.IntegerField(null=True)    #Winner 1st Serve points Won
    wser2 = models.IntegerField(null=True)    #Winner 2nd Serve points Won
    wser = models.IntegerField(null=True)    #Winner Serve games won
    wrec = models.IntegerField(null=True)   #Winner recevier points won
    wtotal = models.IntegerField(null=True) #Winner total game points
    
    #loser match performance data
    laces = models.CharField(max_length=50, null=True)    #Loser Aces
    ldfault = models.CharField(max_length=50, null=True) # Loser Double Default
    lser1 = models.IntegerField(null=True)  #Loser 1St Serve Points won
    lser2 = models.IntegerField(null=True)  #Loser 2nd Server Points won
    lser = models.IntegerField(null=True)  #Loser Serve won games
    lrec = models.IntegerField(null=True)   #Loser receiver points won
    ltotal = models.IntegerField(null=True) #Loser total points won

    #odds data
    b365w = models.FloatField(blank=True, null=True)     # bet365 winner odds
    b356l = models.FloatField( blank=True, null=True)    # bet365 loser odds
    psw = models.FloatField( blank=True, null=True)     # Pinnacles Sports odds of match winner
    psl = models.FloatField( blank=True, null=True)     # Pinnacles Sports odds of match loser
    maxw = models.FloatField( blank=True, null=True)    # Winamax Sports odds of match winner
    maxl = models.FloatField( blank=True, null=True)    # Winamax Sports odds of match loser
    
    ubw = models.FloatField( blank=True, null=True)    # Unibet  Sports odds of match winner
    ubl = models.FloatField( blank=True, null=True)    # Unibet  Sports odds of match loser
    bcw = models.FloatField( blank=True, null=True)    # Betclic.fr  Sports odds of match winner
    bcl = models.FloatField( blank=True, null=True)    # Betclic.fr  Sports odds of match loser
    avgw = models.FloatField( blank=True, null=True)    # Sports odds of average odds of match winner
    avgl = models.FloatField( blank=True, null=True)    # Sports odds of average odds of match loser
    
    def __str__(self):
        return self.home + " vs " + self.away


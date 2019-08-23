# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from players.models import ATPPlayer, WTAPlayer
from matches.models import ATPMatch, WTAMatch
from tournaments.models import ATPTournament, WTATournament

class AtpPlayerItem(DjangoItem):
    django_model = ATPPlayer

class WtaPlayerItem(DjangoItem):
    django_model = WTAPlayer

class AtpMatchItem(DjangoItem):
    django_model = ATPMatch

class WtaMatchItem(DjangoItem):
    django_model = WTAMatch

class AtpTournamentItem(DjangoItem):
    django_model = ATPTournament

class WtaTournamentItem(DjangoItem):
    django_model = WTATournament

class AtpPerformItem(scrapy.Item):
    home = scrapy.Field()
    away = scrapy.Field()
    date = scrapy.Field()
    home_aces = scrapy.Field()
    home_doublefault = scrapy.Field()
    home_total = scrapy.Field()
    home_ser = scrapy.Field()
    home_ser1 = scrapy.Field()
    home_ser2 = scrapy.Field()
    home_rec = scrapy.Field()
    away_aces = scrapy.Field()
    away_doublefault = scrapy.Field()
    away_total = scrapy.Field()
    away_ser = scrapy.Field()
    away_ser1 = scrapy.Field()
    away_ser2 = scrapy.Field()
    away_rec = scrapy.Field()

class WtaPerformItem(scrapy.Item):
    home = scrapy.Field()
    away = scrapy.Field()
    date = scrapy.Field()
    home_aces = scrapy.Field()
    home_doublefault = scrapy.Field()
    home_total = scrapy.Field()
    home_ser = scrapy.Field()
    home_ser1 = scrapy.Field()
    home_ser2 = scrapy.Field()
    home_rec = scrapy.Field()
    away_aces = scrapy.Field()
    away_doublefault = scrapy.Field()
    away_total = scrapy.Field()
    away_ser = scrapy.Field()
    away_ser1 = scrapy.Field()
    away_ser2 = scrapy.Field()
    away_rec = scrapy.Field()
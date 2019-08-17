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
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from players.models import ATPPlayer
from matches.models import ATPMatch

class AtpPlayerItem(DjangoItem):
    django_model = ATPPlayer

class AtpMatchItem(DjangoItem):
    django_model = ATPMatch

from django.contrib import admin
from .models import ATPMatch, WTAMatch
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(ATPMatch)
@admin.register(WTAMatch)
class ViewAdmin(ImportExportModelAdmin):
    list_display = ('date', 'winner', 'loser', 'tournament', 'home', 'away', 'home_winsets','away_winsets', 'home_b365', 'away_b365', 'home_ps', 'away_ps', 'home_winamax', 'away_winamax', 'home_unibet', 'away_unibet', 'home_betclic', 'away_betclic', 'home_max', 'away_max', 'home_avg', 'away_avg')
    search_fields = ('date', 'home', 'away', 'home_max', 'away_max')
    exclude=('id', )
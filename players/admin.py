from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import ATPPlayer
from .models import WTAPlayer

@admin.register(ATPPlayer)
@admin.register(WTAPlayer)
class ViewAdmin(ImportExportModelAdmin):
    list_display = ('rank', 'name', 'nicknames')
    search_fields = ['name']
    list_editable = ['nicknames']
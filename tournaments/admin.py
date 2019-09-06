from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import ATPTournament
from .models import WTATournament
# Register your models here.
@admin.register(ATPTournament)
@admin.register(WTATournament)
class ViewAdmin(ImportExportModelAdmin):
    list_display = ('name', 'year', 'nicknames')
    search_fields = ['name', 'year']
    list_editable = ['nicknames']
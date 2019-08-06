from django.contrib import admin
from .models import Match
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(Match)
class ViewAdmin(ImportExportModelAdmin):
    exclude=('id', )
from django.contrib import admin
from .models import ATPMatch, WTAMatch
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(ATPMatch)
@admin.register(WTAMatch)
class ViewAdmin(ImportExportModelAdmin):
    exclude=('id', )
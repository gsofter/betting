from django.contrib import admin

from .models import ATPTournament
from .models import WTATournament
# Register your models here.
admin.site.register(ATPTournament)
admin.site.register(WTATournament)
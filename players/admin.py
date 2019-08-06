from django.contrib import admin

from .models import ATPPlayer
from .models import WTAPlayer
# Register your models here.
admin.site.register(ATPPlayer)
admin.site.register(WTAPlayer)
from django.contrib import admin
from .models import DamageType, DamageStatus, General
from .models import Damage, LocationDetails

admin.site.register(DamageType)
admin.site.register(DamageStatus)
admin.site.register(Damage)
admin.site.register(General)
admin.site.register(LocationDetails)

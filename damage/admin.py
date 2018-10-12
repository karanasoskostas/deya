from django.contrib import admin
from .models import DamageType, DamageStatus, General, ContactDetails,\
    Damage, LocationDetails, DamageHistoryStatus, ContactManagement

admin.site.register(DamageType)
admin.site.register(DamageStatus)
admin.site.register(Damage)
admin.site.register(General)
admin.site.register(LocationDetails)
admin.site.register(ContactDetails)
admin.site.register(DamageHistoryStatus)
admin.site.register(ContactManagement)
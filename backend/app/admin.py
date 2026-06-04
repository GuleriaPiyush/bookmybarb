from django.contrib import admin
from .models import Service, Slot, Booking,ShopSetting

# Register your models here.

admin.site.register(Slot)
admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(ShopSetting)
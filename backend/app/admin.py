from django.contrib import admin
from .models import Service, Slot, Booking,ShopSetting,TemplateSlot,ScheduleTemplate

# Register your models here.

admin.site.register(Slot)
admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(ShopSetting)
admin.site.register(ScheduleTemplate)
admin.site.register(TemplateSlot)
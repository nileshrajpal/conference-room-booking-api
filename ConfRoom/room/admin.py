from django.contrib import admin
from .models import User, Room, Slot


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc')


class SlotAdmin(admin.ModelAdmin):
    list_display = ('room', 'start_time', 'end_time', 'is_available', 'booked_by')


admin.site.register(Room, RoomAdmin)
admin.site.register(Slot, SlotAdmin)

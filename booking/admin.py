

# Register your models here.

from django.contrib import admin
from .models import Room, Booking

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['room', 'user', 'date', 'time', 'status']
    list_filter = ['status', 'date']
    search_fields = ['room__name', 'user__username']

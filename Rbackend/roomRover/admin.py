from django.contrib import admin

# Register your models here.
from .models import Room

class RoomAdmin(admin.ModelAdmin):
    list_display = ('property_name', 'city', 'state', 'user')
    list_filter = ('city', 'state', 'parking_available', 'bachelors_allowed')
    search_fields = ('property_name', 'city', 'state', 'user__username')

admin.site.register(Room, RoomAdmin)

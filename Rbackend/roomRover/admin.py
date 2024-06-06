from django.contrib import admin
from .models import Room, RoomImage

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1  # Number of extra forms to display

class RoomAdmin(admin.ModelAdmin):
    list_display = ('property_name', 'city', 'state', 'user')
    list_filter = ('city', 'state', 'parking_available', 'bachelors_allowed')
    search_fields = ('property_name', 'city', 'state', 'user__username')
    inlines = [RoomImageInline]  # Add the inline class here

admin.site.register(Room, RoomAdmin)
admin.site.register(RoomImage)  # Register the RoomImage model

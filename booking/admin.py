from django.contrib import admin
from .models import Room, RoomType, Booking

admin.site.register(RoomType)
admin.site.register(Booking)
admin.site.register(Room)

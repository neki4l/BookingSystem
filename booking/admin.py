from django.contrib import admin
from .models import Room, RoomType, Booking, Review, Service, BookingService

admin.site.register(RoomType)
admin.site.register(Booking)
admin.site.register(Room)
admin.site.register(Review)
admin.site.register(BookingService)
admin.site.register(Service)

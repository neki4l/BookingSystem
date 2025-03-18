from django.db import models
from django.contrib.auth.models import User

#TODO: Сделать фото у номера, а не типа, сделать отмену бронирования

class RoomType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='room_types/')

    def __str__(self):
        return self.name

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    floor_number = models.IntegerField(default=1)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room_type.name} - {self.room_number}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Только при новом бронировании
            if not self.room.is_available:
                raise ValueError("Этот номер уже забронирован!")
            self.room.is_available = False
            self.room.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.room.is_available = True
        self.room.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.room}"
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class RoomType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")
    capacity = models.PositiveIntegerField(verbose_name="Вместимость")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Тип номера"
        verbose_name_plural = "Типы номеров"

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True, verbose_name="Номер комнаты")
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, verbose_name="Тип комнаты")
    floor_number = models.IntegerField(default=1, verbose_name="Этаж")
    image = models.ImageField(upload_to='room_types/', default='room_types/default.jpg', verbose_name="Фото комнаты")
    is_available = models.BooleanField(default=True, verbose_name="Доступность")

    def __str__(self):
        return f"{self.room_type.name} - {self.room_number}"
    
    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Комната")
    total_price = models.IntegerField(default=0, verbose_name="Общая стоимость")
    check_in = models.DateField(verbose_name="Заезд")
    check_out = models.DateField(verbose_name="Выезд")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def save(self, *args, **kwargs):
        if not self.pk:
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
    
    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Рейтинг"
    )
    comment = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Отзыв от {self.user.username}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
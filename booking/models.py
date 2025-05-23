from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

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
    is_cancelled = models.BooleanField(default=False, verbose_name='Отменено')
    check_in = models.DateField(verbose_name="Заезд")
    check_out = models.DateField(verbose_name="Выезд")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата Обновления")
    
    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.room.is_available:
                raise ValueError("Этот номер уже забронирован!")
            self.room.is_available = False
            self.room.save()
        super().save(*args, **kwargs)
        
    def check_dates(self):
        if self.check_out < timezone.now().date():
            self.room.is_available = True
            self.room.save()

    def delete(self, *args, **kwargs):
        self.room.is_available = True
        self.room.save()
        super().delete(*args, **kwargs)
        
    def calculate_total_price(self):
        room_price = max(1, (self.check_out - self.check_in).days) * self.room.room_type.price
        
        services_price = sum(
            service.service.price * service.quantity
            for service in self.services.all()
        )
        self.total_price = room_price + services_price
        self.save()
    
    def cancel(self):
        self.is_cancelled = True
        self.room.is_available = True
        self.room.save()
        self.save()
    
    def clean(self):
        if self.check_in > self.check_out:
            raise ValidationError("Дата выезда должна быть больше или ровна дате заезда!")

        
    def __str__(self):
        return f"{self.user.username} - {self.room}"
    
    
class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название услуги")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")
    description = models.TextField(verbose_name="Описание", blank=True)

    def __str__(self):
            return f"{self.name} ({self.price} руб)"

    class Meta:
            verbose_name = "Дополнительная услуга"
            verbose_name_plural = "Дополнительные услуги"
            
            
class BookingService(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="services")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
            return f"{self.service.name} x {self.quantity}"

    class Meta:
            verbose_name = "Услуга в бронировании"
            verbose_name_plural = "Услуги в бронировании"
    
    
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
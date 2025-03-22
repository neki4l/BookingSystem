# Generated by Django 5.1.7 on 2025-03-22 10:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_alter_booking_options_alter_room_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название услуги')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Цена')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Дополнительная услуга',
                'verbose_name_plural': 'Дополнительные услуги',
            },
        ),
        migrations.CreateModel(
            name='BookingService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='booking.booking')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.service')),
            ],
            options={
                'verbose_name': 'Услуга в бронировании',
                'verbose_name_plural': 'Услуги в бронировании',
            },
        ),
    ]

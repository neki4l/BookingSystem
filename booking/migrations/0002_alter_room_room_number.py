# Generated by Django 5.1.7 on 2025-03-18 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_number',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]

# Generated by Django 5.1.7 on 2025-04-14 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('holidays', '0005_booking_payed'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='description',
            field=models.CharField(default='hello', max_length=500),
            preserve_default=False,
        ),
    ]

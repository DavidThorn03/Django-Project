# Generated by Django 5.1.7 on 2025-04-08 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('holidays', '0003_alter_booking_approved_alter_booking_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='check_in',
            field=models.DateField(verbose_name='check in date'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='check_out',
            field=models.DateField(verbose_name='check out date'),
        ),
    ]

# Generated by Django 5.1.3 on 2024-12-08 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0004_remove_parkingspace_daily_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rentalrecord',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='rentalrecord',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='rentalrecord',
            name='start_date',
        ),
    ]

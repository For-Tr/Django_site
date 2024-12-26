import datetime
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

class ParkingSpace(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    availability = models.BooleanField(default=True)
    hourly_price = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return f"Space {self.id} at {self.location}"

class RentalRecord(models.Model):
    parking_space = models.ForeignKey('ParkingSpace', related_name='rentals', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    provider = models.ForeignKey(User, related_name='provided_rentals', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Rental from {self.start_date} to {self.end_date} for Space {self.parking_space.location}"


class Order(models.Model):

    def get_orders_for_user(user_identifier):
        orders = Order.objects.filter(user_identifier=user_identifier).order_by('-created_at')
        return orders
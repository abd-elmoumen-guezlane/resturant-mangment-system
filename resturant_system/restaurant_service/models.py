
from django.db import models

class RestaurantInfo(models.Model):
    name = models.CharField(max_length=150, default="My Restaurant")
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    opening_time = models.CharField(max_length=50, default="09:00")
    closing_time = models.CharField(max_length=50, default="23:00")

    def __str__(self):
        return self.name

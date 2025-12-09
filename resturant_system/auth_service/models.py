
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('CLIENT', 'Client'),
        ('DELIVERY', 'Delivery Worker'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CLIENT')

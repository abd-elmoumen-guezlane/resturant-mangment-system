from django.db import models
from django.conf import settings
from orders.models import Order

# ============================================
# Profil du livreur (compte)
# ============================================
class DeliveryProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    phone = models.CharField(max_length=20)
    vehicle_type = models.CharField(
        max_length=50,
        help_text="Moto, voiture, vélo..."
    )
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Livreur : {self.user.username}"


# ============================================
# Livraison (Delivery)
# ============================================
class Delivery(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('on_the_way', 'En route'),
        ('delivered', 'Livrée'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    delivery_person = models.ForeignKey(
        DeliveryProfile, on_delete=models.SET_NULL, null=True
    )
    address = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery #{self.id} - Order #{self.order.id}"

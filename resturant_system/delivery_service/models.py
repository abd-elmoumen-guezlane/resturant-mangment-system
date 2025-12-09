
from django.db import models

class DeliveryAssignment(models.Model):
    order_id = models.IntegerField()     # reference of order in order_service
    delivery_worker_id = models.IntegerField()   # user_id from auth_service

    assigned_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    STATUS_CHOICES = (
        ('ASSIGNED', 'Assigned'),
        ('DELIVERING', 'Delivering'),
        ('COMPLETED', 'Delivered'),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ASSIGNED')

    def __str__(self):
        return f"Delivery for order {self.order_id}"

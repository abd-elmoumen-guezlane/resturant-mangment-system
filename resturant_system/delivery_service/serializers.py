# delivery_service/serializers.py

from rest_framework import serializers
from .models import DeliveryAssignment

class DeliveryAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAssignment
        fields = [
            "id",
            "order_id",
            "delivery_worker_id",
            "assigned_at",
            "delivered_at",
            "status",
        ]

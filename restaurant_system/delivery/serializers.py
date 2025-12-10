from rest_framework import serializers
from .models import DeliveryProfile, Delivery
from orders.serializers import OrderSerializer
from orders.models import Order


# DeliveryProfile Serializer
class DeliveryProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryProfile
        fields = ['id', 'user', 'phone', 'vehicle_type', 'is_available']
        read_only_fields = ['id']

# Delivery Serializer
class DeliverySerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    delivery_person = DeliveryProfileSerializer(read_only=True)

    # Champs pour POST / PUT
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
        source='order',
        write_only=True
    )
    delivery_person_id = serializers.PrimaryKeyRelatedField(
        queryset=DeliveryProfile.objects.all(),
        source='delivery_person',
        write_only=True
    )

    class Meta:
        model = Delivery
        fields = ['id', 'order', 'order_id', 'delivery_person', 'delivery_person_id', 'address', 'status', 'created_at']
        read_only_fields = ['id', 'order', 'delivery_person', 'created_at']

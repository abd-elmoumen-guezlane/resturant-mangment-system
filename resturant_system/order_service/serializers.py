
from rest_framework import serializers
from .models import GuestInfo, Order, OrderItem

class GuestInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestInfo
        fields = ["fullname", "phone", "address"]

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "menu_item_id",
            "quantity",
            "price",
        ]
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    guest = GuestInfoSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_id",
            "guest",
            "created_at",
            "status",
            "total_price",
            "items"
        ]

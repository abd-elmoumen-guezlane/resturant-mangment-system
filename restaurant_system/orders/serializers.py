from rest_framework import serializers
from .models import Order, OrderItem
from menu.serializers import MenuItemSerializer
from menu.models import MenuItem 

# OrderItem Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(),
        source='menu_item',
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menu_item', 'menu_item_id', 'quantity', 'price']
        read_only_fields = ['id', 'price', 'menu_item']

# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'customer_email', 'customer_phone', 'status', 'total_price', 'created_at', 'updated_at', 'items']
        read_only_fields = ['id', 'total_price', 'created_at', 'updated_at']

from rest_framework import serializers
from .models import Order, OrderItem
from menu.serializers import MenuItemSerializer  # si vous voulez inclure les infos du menu

# Serializer pour les détails de la commande
class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)  # pour afficher les détails du plat

    class Meta:
        model = OrderItem
        fields = '__all__'

# Serializer pour la commande principale
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)  # inclut les OrderItems associés

    class Meta:
        model = Order
        fields = '__all__'

from rest_framework import serializers
from .models import DeliveryProfile, Delivery
from orders.serializers import OrderSerializer  # si tu veux inclure les infos de la commande

# Serializer pour le profil du livreur
class DeliveryProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryProfile
        fields = ['id', 'user', 'phone', 'vehicle_type', 'is_available']
        read_only_fields = ['id']

# Serializer pour la livraison
class DeliverySerializer(serializers.ModelSerializer):
    # Affiche les détails de la commande via nested serializer
    order = OrderSerializer(read_only=True)  
    delivery_person = DeliveryProfileSerializer(read_only=True)  # détail du livreur
    delivery_person_id = serializers.PrimaryKeyRelatedField(
        queryset=DeliveryProfile.objects.all(),
        source='delivery_person',
        write_only=True
    )

    class Meta:
        model = Delivery
        fields = [
            'id', 'order', 'delivery_person', 'delivery_person_id', 
            'address', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'order', 'delivery_person']


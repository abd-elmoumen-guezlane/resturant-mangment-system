from rest_framework import viewsets, permissions
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

# ============================
# ViewSet pour Order
# ============================
class OrderViewSet(viewsets.ModelViewSet):
    """
    CRUD complet pour les commandes principales
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]  # ou IsAuthenticated si nécessaire

# ============================
# ViewSet pour OrderItem
# ============================
class OrderItemViewSet(viewsets.ModelViewSet):
    """
    CRUD pour les détails de commande
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.AllowAny]  # ou IsAuthenticated

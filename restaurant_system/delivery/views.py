from rest_framework import viewsets, permissions
from .models import DeliveryProfile, Delivery
from .serializers import DeliveryProfileSerializer, DeliverySerializer

# ==============================
# ViewSet pour DeliveryProfile
# ==============================
class DeliveryProfileViewSet(viewsets.ModelViewSet):
    """
    CRUD complet pour les profils des livreurs
    """
    queryset = DeliveryProfile.objects.all()
    serializer_class = DeliveryProfileSerializer
    permission_classes = [permissions.IsAdminUser]  # seuls les admins peuvent gérer les livreurs

# ==============================
# ViewSet pour Delivery
# ==============================
class DeliveryViewSet(viewsets.ModelViewSet):
    """
    CRUD pour les livraisons
    """
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

    def get_permissions(self):
        """
        Admin: peut tout faire
        Livreur: peut voir/modifier uniquement ses livraisons
        """
        user = self.request.user
        if user.is_staff:  # Admin
            return [permissions.IsAdminUser()]
        else:
            return [permissions.IsAuthenticated()]  # Livreurs connectés

    def get_queryset(self):
        """
        Les livreurs ne voient que leurs livraisons
        """
        user = self.request.user
        if user.is_staff:
            return Delivery.objects.all()
        else:
            try:
                profile = DeliveryProfile.objects.get(user=user)
                return Delivery.objects.filter(delivery_person=profile)
            except DeliveryProfile.DoesNotExist:
                return Delivery.objects.none()
